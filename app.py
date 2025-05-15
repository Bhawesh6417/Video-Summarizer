import streamlit as st 
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file, get_file
import google.generativeai as genai

import time
from pathlib import Path
import tempfile
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Page configuration
st.set_page_config(
    page_title="Multimodal AI Agent - Video Summarizer",
    page_icon="🎥",
    layout="wide"
)

st.title("Phidata Video AI Summarizer Agent 🎥🎤🖬 - Not More than 200 MB")
st.header("Powered by Gemini 2.0 Flash Exp")

# Theme switcher
theme = st.radio("Choose Theme", ["Light", "Dark"])
if theme == "Dark":
    st.markdown("""
    <style>
    body {background-color: #0e1117; color: white;}
    </style>
    """, unsafe_allow_html=True)

# Output language selection
lang = st.selectbox("Output Language", ["English", "Spanish", "French", "German"])

# Summary format
summary_mode = st.radio("Choose summary format:", ["Detailed", "Bullet Points"])

# Enable/disable web search
web_search = st.checkbox("Allow external web search for more accurate answers", value=True)

# Initialize agent
@st.cache_resource
def initialize_agent():
    tools = [DuckDuckGo()] if web_search else []
    return Agent(
        name="Video AI Summarizer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=tools,
        markdown=True,
    )

multimodal_Agent = initialize_agent()

# File uploader
video_file = st.file_uploader(
    "Upload a video file", type=['mp4', 'mov', 'avi'], help="Upload a video for AI analysis"
)

if video_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
        total_bytes = video_file.size
        chunk_size = 1024 * 1024
        uploaded = 0
        progress_bar = st.progress(0)
        while True:
            chunk = video_file.read(chunk_size)
            if not chunk:
                break
            temp_video.write(chunk)
            uploaded += len(chunk)
            progress_bar.progress(min(uploaded / total_bytes, 1.0))
        video_path = temp_video.name

    st.video(video_path, format="video/mp4", start_time=0)

    user_query = st.text_area(
        "What insights are you seeking from the video?",
        placeholder="Ask anything about the video content.",
        help="Provide specific questions or insights you want from the video."
    )

    if st.button("🔍 Analyze Video", key="analyze_video_button"):
        if not user_query:
            st.warning("Please enter a question or insight to analyze the video.")
        else:
            try:
                with st.spinner("Processing video and gathering insights..."):
                    processed_video = upload_file(video_path)
                    while processed_video.state.name == "PROCESSING":
                        time.sleep(1)
                        processed_video = get_file(processed_video.name)

                    # Prompt for analysis
                    analysis_prompt = f"""
                    Analyze the uploaded video and provide a summary in {summary_mode} format.
                    Respond to this user query: {user_query}
                    Also translate the final response to {lang}.
                    """

                    response = multimodal_Agent.run(analysis_prompt, videos=[processed_video])

                    transcript_prompt = "Generate a full transcript of the video."
                    transcript_response = multimodal_Agent.run(transcript_prompt, videos=[processed_video])

                    timestamp_prompt = "Identify key moments in the video with approximate timestamps."
                    highlights_response = multimodal_Agent.run(timestamp_prompt, videos=[processed_video])

                # Display with tabs
                tab1, tab2, tab3 = st.tabs(["📝 Summary", "🕓 Key Moments", "📜 Transcript"])
                with tab1:
                    st.markdown(response.content)
                with tab2:
                    st.markdown(highlights_response.content)
                with tab3:
                    st.markdown(transcript_response.content)

                # Download option
                st.download_button("📄 Download Summary", response.content, file_name="summary.txt")

            except Exception as error:
                st.error(f"An error occurred during analysis: {error}")
            finally:
                Path(video_path).unlink(missing_ok=True)
else:
    st.info("Upload a video file to begin analysis.")

# Customize text area height
st.markdown(
    """
    <style>
    .stTextArea textarea {
        height: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)