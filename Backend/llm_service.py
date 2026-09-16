import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from youtube_transcript_api import YouTubeTranscriptApi

from .utils import extract_youtube_video_id

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
load_dotenv(Path.cwd() / ".env")


class LLMService:
    """
    Handles LLM-based responses and transcript extraction.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        llm_kwargs = {"model": "gemini-1.5-flash", "temperature": 0.7}
        if api_key:
            llm_kwargs["google_api_key"] = api_key
        self.llm = ChatGoogleGenerativeAI(**llm_kwargs)
        self.parser = StrOutputParser()
        self.prompt = PromptTemplate(
            input_variables=["query", "transcript"],
            template="""
            You are a helpful AI tutor. Use the video transcript to answer the student's question.

            Transcript: {transcript}

            Question: {query}

            Answer:
            """
        )

    def get_transcript(self, video_id: str) -> str:
        """
        Fetch YouTube transcript by video ID.
        """
        transcript_api = YouTubeTranscriptApi()
        if hasattr(transcript_api, "fetch"):
            transcript = transcript_api.fetch(video_id)
        else:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)

        def extract_text(item):
            if isinstance(item, dict):
                return item.get("text", "")
            if hasattr(item, "text"):
                return item.text
            return str(item)

        return " ".join(extract_text(item) for item in transcript)

    def chat_with_transcript(self, url: str, query: str) -> str:
        """
        Handle AI Q&A over the YouTube transcript.
        """
        video_id = extract_youtube_video_id(url)
        if not video_id:
            return "Invalid YouTube URL."

        try:
            transcript = self.get_transcript(video_id)
        except Exception as e:
            return f"Transcript not available: {str(e)}"

        chain = self.prompt | self.llm | self.parser
        return chain.invoke({"query": query, "transcript": transcript}).strip()
