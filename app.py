import streamlit as st
import google.generativeai as genai
from google.generativeai import upload_file, get_file  # type: ignore
from dotenv import load_dotenv
import tempfile
import os
import time
from pathlib import Path

# Load API key
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)  # type: ignore

# Define available languages
LANGUAGE_CODES = {
    "English": "en", "Spanish": "es", "French": "fr", "German": "de",
    "Hindi": "hi", "Bengali": "bn", "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja", "Korean": "ko", "Arabic": "ar", "Portuguese": "pt",
    "Russian": "ru", "Italian": "it", "Dutch": "nl", "Turkish": "tr",
    "Tamil": "ta", "Telugu": "te", "Gujarati": "gu", "Urdu": "ur",
    "Punjabi": "pa", "Swahili": "sw", "Thai": "th", "Vietnamese": "vi",
    "Polish": "pl", "Greek": "el", "Hebrew": "he", "Indonesian": "id",
    "Filipino": "tl", "Malay": "ms", "Ukrainian": "uk", "Romanian": "ro",
    "Czech": "cs", "Hungarian": "hu", "Slovak": "sk", "Norwegian": "no",
    "Swedish": "sv", "Finnish": "fi", "Danish": "da"
}

# Page config
st.set_page_config(page_title="Gemini Video Analyzer", page_icon="🎥", layout="wide")
st.title("🎥 Gemini Video Analyzer (<=200MB)")
st.header("Powered by Google Gemini")

# Language selection
lang_name = st.selectbox("Choose output language", list(LANGUAGE_CODES.keys()))

# Summary format
summary_mode = st.radio("Summary format:", ["Detailed", "Bullet Points"])

# Upload video
video_file = st.file_uploader("Upload a video (MP4/MOV/AVI)", type=["mp4", "mov", "avi"])

if video_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
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

    st.video(video_path)

    if st.button("🔍 Analyze Video"):
        try:
            with st.spinner("Uploading video and generating analysis..."):
                uploaded_video = upload_file(video_path)
                while uploaded_video.state.name == "PROCESSING":
                    time.sleep(1)
                    uploaded_video = get_file(uploaded_video.name)

                model = genai.GenerativeModel("gemini-2.0-flash-exp")  # type: ignore

                # Prompt for video analysis
                analysis_prompt = f"""
                Perform a comprehensive analysis of the uploaded video.
                Describe the events, people, context, and flow of the video in an informative and structured way.
                Respond fully in {lang_name}.
                """
                analysis_response = model.generate_content([analysis_prompt, uploaded_video])
                analysis_text = analysis_response.text

                # Transcript in selected language
                transcript_translated_prompt = f"Generate a full transcript of the video in {lang_name}."
                transcript_translated_response = model.generate_content(
                    [transcript_translated_prompt, uploaded_video]
                )
                transcript_translated_text = transcript_translated_response.text

                # Transcript in original language
                transcript_original_prompt = "Generate a full transcript of the video in its original language."
                transcript_original_response = model.generate_content(
                    [transcript_original_prompt, uploaded_video]
                )
                transcript_original_text = transcript_original_response.text

                # Key moments
                highlights_prompt = f"Identify key moments in the video with approximate timestamps in {lang_name}."
                highlights_response = model.generate_content([highlights_prompt, uploaded_video])
                highlights_text = highlights_response.text

            # Display results
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Video Analysis",
                "🕓 Key Moments",
                f"🌐 Transcript ({lang_name})",
                "📜 Transcript (Original)"
            ])
            with tab1:
                st.markdown(analysis_text)
            with tab2:
                st.markdown(highlights_text)
            with tab3:
                st.markdown(transcript_translated_text)
            with tab4:
                st.markdown(transcript_original_text)

            # Download
            st.download_button("📄 Download Analysis", analysis_text, file_name=f"video_analysis_{lang_name}.txt")

        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            Path(video_path).unlink(missing_ok=True)
else:
    st.info("Upload a video to get started.")
