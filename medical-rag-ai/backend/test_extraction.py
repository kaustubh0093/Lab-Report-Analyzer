import json
from backend.rag.clinical_chain import ClinicalChain

def test_extraction():
    agent = ClinicalChain()
    
    # Sample text with implicit status
    text = "Patient Hemoglobin is 12.20 g/dL. Reference range is 13.00 - 17.00 g/dL."
    
    print(f"Testing extraction for: {text}")
    entities = agent.extract_entities(text)
    
    print("\nExtracted Entities:")
    print(json.dumps(entities, indent=2))
    
    # Check if 'flag' is 'Low'
    for entity in entities:
        if entity['test_name'].lower() == 'hemoglobin':
            flag = entity.get('flag', 'Unknown')
            print(f"\nHemoglobin Flag: {flag}")
            if flag == 'Low':
                print("✅ Pass: Flag correctly inferred as 'Low'")
            else:
                print(f"❌ Fail: Expected 'Low', got '{flag}'")

if __name__ == "__main__":
    test_extraction()
