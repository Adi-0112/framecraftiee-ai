import json
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="FrameCraft AI | Storyboard Pipeline",
    page_icon="🎬",
    layout="wide"
)

# Custom Styling for Creative Tool Aesthetic
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        background-color: #6366f1;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        border: none;
        width: 100%;
    }
    .shot-card {
        background: #1e222d;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #6366f1;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar: Configuration
with st.sidebar:
    st.title("🎬 FrameCraft AI")
    st.caption("AI Storyboard & Shot Pipeline for Creative Teams")
    
    api_key = st.text_input("Enter Gemini API Key", type="password", help="Get a free key from Google AI Studio")
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            api_key = ""
    st.markdown("---")
    aspect_ratio = st.selectbox("Aspect Ratio", ["16:9 (Cinematic)", "2.39:1 (Anamorphic)", "9:16 (Vertical/Reels)", "4:3 (Classic)"])
    visual_tone = st.selectbox("Cinematic Tone", [
        "Neo-Noir & Moody (Fincher Style)",
        "Warm & Saturated (Wong Kar-wai)",
        "Desaturated & Gritty (Villeneuve Style)",
        "Vibrant High-Key Commercial",
        "Cyberpunk Neon Glow"
    ])

st.subheader("Turn Scripts into Production-Ready Shot Lists & Image Prompts")
st.write("Designed for filmmakers, agencies, and AI video editors running node-based workflows.")

script_text = st.text_area(
    "Scene Description / Script Fragment:",
    placeholder="E.g., A cyber-detective steps into a rain-slicked alley in downtown Tokyo. A flickering neon sign reflects off his trench coat as he notices a dropped memory chip.",
    height=120
)

col_gen, col_empty = st.columns([1, 3])
with col_gen:
    generate_btn = st.button("Generate Storyboard Shots 🚀")

def generate_shotlist(script, tone, ratio, key):
    client = genai.Client(api_key=key)
    
    prompt = f"""
    You are an expert film director and cinematographer. Break down this scene into exactly 3 consecutive cinematic shots:
    1. Establishing / Wide Shot
    2. Medium Action Shot
    3. Close-up / Focal Detail Shot

    Scene: {script}
    Visual Tone: {tone}
    Aspect Ratio: {ratio}

    Return ONLY a valid JSON array of 3 objects with these exact keys:
    - "shot_type": (e.g., Wide Shot, Medium Shot, Extreme Close-up)
    - "camera_movement": (e.g., Slow Dolly In, Static Low-Angle, Pan Right)
    - "lens_choice": (e.g., 24mm Wide Anamorphic, 50mm Prime, 85mm Macro f/1.4)
    - "lighting": (description of light, shadow, color contrast)
    - "visual_prompt": (A production-grade prompt for Midjourney, Flux, or HexCoded Creative Studio with camera/lighting tokens)
    - "action_description": (Brief 1-line narrative description of the action)
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    return json.loads(response.text)

if generate_btn:
    if not api_key:
        st.error("Please provide a Gemini API Key in the sidebar.")
    elif not script_text.strip():
        st.warning("Please enter a scene description first.")
    else:
        with st.spinner("Breaking down shots & engineering creative prompts..."):
            try:
                shots = generate_shotlist(script_text, visual_tone, aspect_ratio, api_key)
                
                st.success("Storyboard breakdown complete! Ready for generation nodes.")
                
                cols = st.columns(3)
                for i, shot in enumerate(shots):
                    with cols[i]:
                        st.markdown(f"### Shot {i+1}: {shot['shot_type']}")
                        st.markdown(f"**Action:** {shot['action_description']}")
                        st.markdown(f"🎥 **Camera:** {shot['camera_movement']}")
                        st.markdown(f"🔍 **Lens:** {shot['lens_choice']}")
                        st.markdown(f"💡 **Lighting:** {shot['lighting']}")
                        
                        st.text_area(
                            f"Node Prompt (Shot {i+1})",
                            value=shot['visual_prompt'],
                            height=120,
                            key=f"prompt_{i}"
                        )
            except Exception as e:
                st.error(f"Error generating shots: {e}")