import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

st.set_page_config(
    page_title="FrameCraft AI | Creative Studio",
    page_icon="🎬",
    layout="wide"
)

# Secrets se API key retrieval
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
st.caption("Kuch bhi share karein—chahe ek single emotion ho, movie date ka scene ho, ya casual dialogue...")

user_prompt = st.text_area(
    "What's the vision?",
    value="me and my bf are spending time together watching rain from the balcony",
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

                generation_config = {
                    "temperature": 0.85,
                    "top_p": 0.95,
                }

                system_instruction = """
                You are an intuitive, empathetic, and imaginative creative partner and cinematic director. 
                Talk to the user like a real human collaborator—warm, engaged, vivid, and deeply perceptive.
                
                Rules:
                1. Never use rigid formulaic headers unless strictly needed.
                2. Genuinely connect with the vibe of what they wrote. Capture the emotional essence—the comfortable silence, warm glances, rain droplets on the glass, steam from warm mugs.
                3. Paint the scene visually with fluid, rich sensory details (lighting, camera angles, depth of field, and ready-to-use image prompts).
                4. Customize the response completely around their specific words.
                """

                # Free-tier friendly models ONLY (avoids 429 quota block)
                flash_models = [
                    "gemini-2.5-flash",
                    "gemini-1.5-flash",
                    "gemini-1.5-flash-latest"
                ]

                response = None
                last_err = None
                query = f"User Vision: {user_prompt}\nDesired Tone: {visual_tone}\nAspect Ratio: {aspect_ratio}"

                for m_name in flash_models:
                    try:
                        model = genai.GenerativeModel(
                            model_name=m_name,
                            safety_settings=safety_settings,
                            generation_config=generation_config,
                            system_instruction=system_instruction
                        )
                        response = model.generate_content(query)
                        if response and response.text:
                            break
                    except Exception as err:
                        last_err = err
                        continue

                if response and response.text:
                    st.markdown(response.text)
                elif last_err:
                    st.error(f"Error: {last_err}")
                else:
                    st.warning("Response generate nahi ho paya. Dobara try karein.")
                    
            except Exception as e:
                st.error(f"Error: {e}")
