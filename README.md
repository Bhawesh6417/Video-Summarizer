🎥 Phidata Video AI Summarizer Agent

This Streamlit-based application leverages Google's Gemini 2.0 Flash Exp and Phidata's AI Agent capabilities to provide detailed, multimodal video summarization with optional web-enhanced insights.

🚀 Features

Upload video files up to 200MB (.mp4, .mov, .avi)

Multimodal video analysis using Gemini 2.0

Transcript generation and key moment detection

Web search integration using DuckDuckGo (optional)

Multiple summary formats: Detailed or Bullet Points

Language support: English, Spanish, French, German

Themed UI: Light/Dark toggle

Tabbed display for Summary, Key Moments, and Transcript

Downloadable summary output

🧠 Tech Stack

Streamlit

Phi Agent Framework

Google Generative AI

Gemini 2.0 Flash Exp

DuckDuckGo Tool

Python

📦 Setup Instructions

Clone the repository:

https://github.com/yourusername/video-ai-summarizer.git
cd video-ai-summarizer

Install dependencies:

pip install -r requirements.txt

Set up .env file:

GOOGLE_API_KEY=your_google_api_key

Run the app:

streamlit run app.py

📁 Project Structure

video-ai-summarizer/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env                    # API key (not tracked)
└── README.md               # This file

📝 Example Use Cases

Generate meeting summaries from recorded video

Extract educational content highlights

Provide multilingual summaries for accessibility

Retrieve detailed responses to video queries

⚠️ Notes

Maximum video file size: 200MB

Requires a valid Google Generative AI API Key

📊 Sample Output

https://github.com/user-attachments/assets/7ecf9522-f3d5-43d6-b427-0884028ab60f

![image](https://github.com/user-attachments/assets/7557de01-746c-4dde-946a-3611ffffd633)

![image](https://github.com/user-attachments/assets/af0a7123-0928-4d03-8e84-ff0f1bb2576c)

![image](https://github.com/user-attachments/assets/fb86dfd2-1aab-41b1-891f-d45110f46219)



