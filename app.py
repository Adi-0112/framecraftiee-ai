import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

st.set_page_config(
    page_title="FrameCraft AI | Creative Studio",
    page_icon="🎬",
    layout="wide"
)

# Fetch API key
api_key = ""
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = ""

with st.sidebar:
    st.title("🎬 FrameCraft AI")
    st.caption("AI Co-Creator & Visual Director")
    
    if not api_key:
        api_key = st.text_input("Enter Gemini API Key", type="password")
    else:
        st.success("API Connected ⚡")
            
    st.markdown("---")
    aspect_ratio = st.selectbox(
        "Aspect Ratio",
        ["16:9 (Cinematic)", "2.39:1 (Anamorphic)", "9:16 (Vertical)", "4:3 (Classic)"]
    )
    visual_tone = st.selectbox(
        "Visual Tone",
        ["Natural & Organic", "Warm & Romantic", "Moody & Atmospheric", "High Energy & Vibrant", "Raw & Minimal"]
    )

st.subheader("Transform Any Feeling, Idea, or Story Into Cinema")
st.caption("Kuch bhi share karein—chahe ek single emotion ho, movie date ka scene ho, ya dialogue...")

user_prompt = st.text_area(
    "What's the vision?",
    placeholder="E.g., I'm going for a cozy movie date with my partner, create a cinematic moment for us...",
    height=120
)

if st.button("Bring Scene to Life ✨"):
    if not api_key:
        st.error("API Key nahi mili. Kripya Streamlit Secrets me add karein.")
    elif not user_prompt.strip():
        st.warning("Pehle koi idea ya scene toh likhiye!")
    else:
        with st.spinner("Visualizing the moment..."):
            try:
                genai.configure(api_key=api_key)
                
                safety_settings = {
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }

                # Human-like natural creativity ke liye config
                generation_config = {
                    "temperature": 0.85,  # Isse responses dynamic, creative aur natural banenge
                    "top_p": 0.95,
                }
                
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    safety_settings=safety_settings,
                    generation_config=generation_config,
                    system_instruction="""
                    You are an intuitive, empathetic, and imaginative creative partner and cinematic director. 
                    Talk to the user like a real human collaborator—warm, engaged, vivid, and deeply perceptive.
                    
                    Rules for your response:
                    1. Never use cookie-cutter formulas or repetitive boilerplate phrasing.
                    2. First, genuinely connect with the vibe of what they wrote. If it's a cozy movie date, talk about the little unspoken things—the glow of the screen reflecting in their eyes, the shared blanket, the comfortable silence, the laugh during a dialogue.
                    3. Paint the scene visually. Break down how this specific moment unfolds cinematically, but describe it fluidly with vivid sensory details (lighting, angles, atmosphere, and ready-to-use visual generation prompts).
                    4. Always customize your response completely around the nuance of their specific words, giving every prompt its own distinct personality and heart.
                    """
                )
                
                query = f"User Vision: {user_prompt}\nDesired Tone: {visual_tone}\nAspect Ratio: {aspect_ratio}"
                response = model.generate_content(query)
                
                if response.text:
                    st.markdown(response.text)
                else:
                    st.warning("Response generate nahi ho paya. Dobara try karein.")
                    
            except Exception as e:
                st.error(f"Error: {e}")
