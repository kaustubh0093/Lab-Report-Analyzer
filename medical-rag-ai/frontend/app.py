import streamlit as st
import requests
from PIL import Image
import json
import os

# Setup Page Config
st.set_page_config(
    page_title="Medical RAG AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        margin-bottom: 15px;
        transition: transform 0.2s;
        color: #212529; /* Explicit dark text for white background */
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.12);
    }
    .metric-card h4 {
        margin-top: 0;
        color: #495057;
        font-size: 1rem;
        font-weight: 600;
    }
    .metric-card p {
        margin-bottom: 5px;
        color: #6c757d;
    }
    .metric-value {
        font-size: 1.6em;
        font-weight: 800;
        color: #007bff;
        margin: 10px 0;
    }
    .metric-unit {
        font-size: 0.6em;
        color: #adb5bd;
        font-weight: normal;
    }
    .flag-high {
        color: #dc3545;
        font-weight: bold;
    }
    .flag-low {
        color: #ffc107;
        font-weight: bold;
    }
    .flag-normal {
        color: #28a745;
        font-weight: bold;
    }
    h1, h2, h3 {
        color: #343a40;
    }
    .disclaimer {
        padding: 15px;
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        color: #856404;
        font-size: 0.9em;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

API_URL = os.getenv("API_URL", "http://localhost:8000/api")

def main():
    # Session State Initialization
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "report_context" not in st.session_state:
        st.session_state.report_context = ""

    # Sidebar
    with st.sidebar:
        st.title("🩺 Medical AI")
        st.markdown("---")
        st.info("**System Status**: Online 🟢")
        st.markdown("### Features")
        st.markdown("- 📄 OCR for Scanned Reports")
        st.markdown("- 🧬 Clinical Entity Extraction")
        st.markdown("- 💊 Medication Suggestions")
        st.markdown("- 💬 Chat with your Report")
        st.markdown("---")
        st.warning("⚠️ **Disclaimer**: NOT A DOCTOR. Educational use only.")
        
        if st.button("Start New Analysis"):
            st.session_state.analysis_results = None
            st.session_state.chat_history = []
            st.session_state.report_context = ""
            st.rerun()

    # Main Content
    st.title("🧠 AI Medical Report Analyzer")
    st.markdown("### Interpret lab reports & Chat with AI Doctor")

    # File Upload
    uploaded_file = st.file_uploader("Upload Lab Report (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])

    if uploaded_file:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if uploaded_file.type.startswith('image'):
                st.image(uploaded_file, caption="Uploaded Report", use_container_width=True)
            else:
                st.success("PDF Uploaded")
            
            if st.button("🔍 Analyze Report"):
                with st.spinner("Processing with OCR & AI Agent..."):
                    # 1. Upload & Extract
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        response = requests.post(f"{API_URL}/upload-report", files=files)
                        
                        if response.status_code == 200:
                            data = response.json()
                            extracted_text = data.get("text", "")
                            
                            if not extracted_text:
                                st.error("No text extracted. Try a clearer image.")
                            else:
                                # 2. Analyze
                                analyze_payload = {"text": extracted_text}
                                analysis_res = requests.post(f"{API_URL}/analyze", json=analyze_payload)
                                
                                if analysis_res.status_code == 200:
                                    results = analysis_res.json()
                                    # Store in Session State
                                    st.session_state.analysis_results = results
                                    # Construct context for chat specific to this report
                                    st.session_state.report_context = f"Summary: {results['summary']}\nExplanation: {results['explanation']}\nFindings: " + ", ".join([f"{e['test_name']}: {e['value']}" for e in results['entities']])
                                    st.success("Analysis Complete!")
                                else:
                                    st.error(f"Analysis Failed: {analysis_res.text}")
                        else:
                            st.error(f"Upload Failed: {response.text}")
                    except Exception as e:
                        st.error(f"Connection Error: {e}. Is the backend running?")
    
    # Display Results if available
    if st.session_state.analysis_results:
        display_results(st.session_state.analysis_results)
        display_chat_interface()

def display_results(data):
    st.markdown("---")
    st.header("📋 Analysis Results")
    
    # Summary
    st.markdown(f"**Summary**: {data['summary']}")
    
    # Entities Table
    st.subheader("🧬 Extracted Vitals & Labs")
    
    # Custom Grid for beautiful display
    if data['entities']:
        cols = st.columns(3)
        for idx, entity in enumerate(data['entities']):
            col = cols[idx % 3]
            flag_class = "flag-normal"
            if "Low" in str(entity.get('flag', '')): flag_class = "flag-low"
            if "High" in str(entity.get('flag', '')): flag_class = "flag-high"
            
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{entity['test_name']}</h4>
                    <p class="metric-value">{entity['value']} <span class="metric-unit">{entity['unit']}</span></p>
                    <p><strong>Range:</strong> {entity.get('reference_range', 'N/A')}</p>
                    <p class="{flag_class}">Status: {entity.get('flag', 'Unknown')}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No specific entities detected.")
            
    # Explanation
    st.markdown("---")
    st.subheader("💡 Clinical Explanation")
    st.info(data['explanation'])
    
    # Medications
    st.subheader("💊 Suggested Medications & Treatments")
    if data.get('medication_suggestions'):
        for item in data['medication_suggestions']:
            st.markdown(f"- {item}")
    else:
        st.markdown("_No specific medication suggestions available (Result might be normal)._")

    # Follow-up
    st.subheader("🔎 Suggested Follow-ups")
    for item in data['follow_up_suggestions']:
        st.markdown(f"- {item}")
        
    # Disclaimer
    st.markdown(f"""
    <div class="disclaimer">
        <strong>SAFETY NOTICE:</strong> {data['disclaimer']}
    </div>
    """, unsafe_allow_html=True)

def display_chat_interface():
    st.markdown("---")
    st.header("💬 Chat with AI Doctor")
    
    # Display history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    if prompt := st.chat_input("Ask a follow-up question about your report..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Get AI response
        with st.chat_message("assistant"):
            try:
                payload = {
                    "context": st.session_state.report_context,
                    "history": st.session_state.chat_history,
                    "message": prompt
                }
                response = requests.post(f"{API_URL}/chat", json=payload)
                if response.status_code == 200:
                    ai_msg = response.json()["response"]
                    st.markdown(ai_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_msg})
                else:
                    st.error("Failed to get response.")
            except Exception as e:
                st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
