import json
import os
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from backend.config import settings

class ClinicalChain:
    def __init__(self):
        # We enforce using a Real LLM (Gemini)
        api_key = settings.GOOGLE_API_KEY
        if not api_key:
            print("WARNING: GOOGLE_API_KEY not found. Medical Agent will fail.")
        
        self.llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            temperature=0,
            google_api_key=api_key
        )
        
        # Load Prompts
        with open("backend/prompts/entity_extraction.txt", "r") as f:
            self.entity_prompt = PromptTemplate.from_template(f.read())
        
        with open("backend/prompts/explanation.txt", "r") as f:
            self.explain_prompt = PromptTemplate.from_template(f.read())

    def extract_entities(self, text: str):
        """
        Uses LLM to extract LabEntity objects and diagnosis from text.
        Returns a dict with 'entities' and 'diagnosis' keys.
        """
        chain = self.entity_prompt | self.llm | JsonOutputParser()
        try:
            result = chain.invoke({"text": text})
            # Ensure proper structure
            if isinstance(result, dict) and "entities" in result and "diagnosis" in result:
                return result
            # Fallback for old format (list of entities)
            elif isinstance(result, list):
                return {"entities": result, "diagnosis": []}
            # Single entity dict
            elif isinstance(result, dict):
                return {"entities": [result], "diagnosis": []}
            else:
                return {"entities": [], "diagnosis": []}
        except Exception as e:
            print(f"Entity Extraction Warning: {e}")
            return {"entities": [], "diagnosis": []}

    def generate_explanation(self, entities):
        """
        Uses LLM to explain results and suggest medications.
        """
        chain = self.explain_prompt | self.llm | JsonOutputParser()
        try:
            response = chain.invoke({"entities": json.dumps(entities)})
            return response
        except Exception as e:
            print(f"Explanation Error: {e}")
            return {
                "explanation": "Could not generate detailed explanation due to an error.",
                "medication_suggestions": [],
                "follow_up_suggestions": []
            }

    def chat(self, chat_history: list, user_input: str, context: str):
        """
        Conversational chat with the report context.
        """
        system_msg = f"""You are a helpful medical assistant. 
        Context from Patient's Lab Report:
        {context}
        
        Answer the user's question based on this report. Be helpful, empathetic, but clear that you are an AI. 
        IMPORTANT: DO NOT use introductory phrases like "Hello", "I'm an AI assistant", or "As a medical assistant" if the conversation has already started. Just answer the question directly and naturally."""
        
        messages = [("system", system_msg)]
        for msg in chat_history:
            role = "human" if msg['role'] == 'user' else "ai"
            messages.append((role, msg['content']))
        
        messages.append(("human", user_input))
        
        response = self.llm.invoke(messages)
        return response.content

    def run_analysis(self, text: str):
        # 1. Extraction
        extraction_result = self.extract_entities(text)
        entities = extraction_result.get("entities", [])
        diagnosis = extraction_result.get("diagnosis", [])
        
        if not entities and not diagnosis:
            return {
                "entities": [],
                "diagnosis": [],
                "summary": "No measurable data found.",
                "explanation": "The AI could not identify standard lab tests or diagnosis in this document.",
                "medication_suggestions": [],
                "follow_up_suggestions": [],
                "disclaimer": ""
            }

        # 2. Explanation & Medications
        explanation_data = self.generate_explanation(entities)
        
        # Create summary
        summary_parts = []
        if entities:
            summary_parts.append(f"{len(entities)} lab test(s)")
        if diagnosis:
            summary_parts.append(f"{len(diagnosis)} diagnosis/condition(s)")
        summary = f"Analyzed {', '.join(summary_parts)}." if summary_parts else "Analysis complete."
        
        return {
            "entities": entities,
            "diagnosis": diagnosis,
            "summary": summary,
            "explanation": explanation_data.get("explanation", ""),
            "medication_suggestions": explanation_data.get("medication_suggestions", []),
            "follow_up_suggestions": explanation_data.get("follow_up_suggestions", ["Consult a doctor."]),
            "disclaimer": "DISCLAIMER: AI-generated suggestions. Consult a physician before taking any medication."
        }
