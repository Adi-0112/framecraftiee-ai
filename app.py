import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

st.set_page_config(
    page_title="FrameCraft AI | Creative Studio",
    page_icon="🎬",
    layout="wide"
)

# Sidebar setup
with st.sidebar:
    st.title("🎬 FrameCraft AI")
    st.caption("AI Creative Partner & Shot Breakdown Engine")
    
    # API key handling with automatic secrets fallback
    api_key = st.text_input("Enter Gemini API Key", type="password")
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            api_key = ""
            
    st.markdown("---")
    aspect_ratio = st.selectbox(
        "Aspect Ratio",
        ["16:9 (Cinematic)", "2.39:1 (Anamorphic)", "9:16 (Vertical)", "4:3 (Classic)"]
    )
    visual_tone = st.selectbox(
        "Visual Tone",
        ["Moody & Cinematic", "Warm & Romantic", "Vibrant Commercial", "Cyberpunk Neon", "Documentary Realism"]
    )

# Main UI
st.subheader("Transform Any Idea, Scene, or Conversation Into Cinema")
st.caption("Enter a scene, a dialogue beat, or any creative scenario.")

user_prompt = st.text_area(
    "Your Creative Concept / Scene:",
    placeholder="E.g., Me and my partner having a cozy candlelight date under city rain...",
    height=130
)

if st.button("Generate Breakdown 🚀"):
    if not api_key:
        st.error("Please provide a Gemini API Key in the sidebar or via secrets.")
    elif not user_prompt.strip():
        st.warning("Please type an idea or scene description first.")
    else:
        with st.spinner("Directing scene with creative depth..."):
            try:
                genai.configure(api_key=api_key)
                
                # Unblock creative, romantic, and casual scenes
                safety_settings = {
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
                
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    safety_settings=safety_settings,
                    system_instruction="""
                    You are an intuitive, empathetic, and seasoned film director and creative collaborator.
                    You do not talk like a cold, rigid algorithm. You communicate with genuine warmth, vivid imagery, and sharp cinematic insight.
                    
                    When given any input (creative story, romance, dramatic action, or casual concept):
                    1. Acknowledge and validate the core emotion/vibe warmly in 1-2 lines.
                    2. Provide a cohesive 3-shot sequence (Establishing Wide, Medium Connection, Close-up Detail).
                    3. For each shot, clearly outline:
                       - Shot Type & Camera Movement
                       - Lens Choice & Depth of Field
                       - Lighting & Atmosphere
                       - Ready-to-use Image/Video Generation Prompt (for Flux/Midjourney)
                    Format clearly with bold headers and readable bullet points.
                    """
                )
                
                query = f"Concept: {user_prompt}\nDesired Tone: {visual_tone}\nTarget Aspect Ratio: {aspect_ratio}"
                response = model.generate_content(query)
                
                if response.text:
                    st.markdown(response.text)
                else:
                    st.warning("The model returned an empty response. Please try tweaking your prompt slightly.")
                    
            except Exception as e:
                st.error(f"Error generating response: {e}")
