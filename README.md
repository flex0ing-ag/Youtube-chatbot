# YouTube Learning AI Assistant

A full-stack AI app for chatting with YouTube videos using transcripts, LLM-powered Q&A, and text-to-speech playback.

This project combines:
- FastAPI backend for transcript extraction and AI chat logic
- Streamlit frontend for user interaction
- Google Gemini via LangChain
- YouTube transcript fetching via `youtube-transcript-api`
- Docker Compose for simple local deployment

## Demo

<img width="1920" height="1080" alt="Screenshot" src="https://github.com/user-attachments/assets/9e9a62a1-a14f-4f16-8936-338a3a94bc70" />

## Features

- Extract transcript text from a YouTube video
- Ask AI questions about the video content
- Convert transcript to audio using `gTTS`
- Local Docker-based deployment
- Easy setup for development and demos

## Tech Stack

- Backend: FastAPI
- Frontend: Streamlit
- AI: LangChain + Google Gemini
- Transcript: `youtube-transcript-api`
- Deployment: Docker + Docker Compose

## Project Structure

```text
Youtube-chatbot/
├── Backend/                # API logic and LLM service
│   ├── llm_service.py
│   ├── main.py
│   ├── models.py
│   └── utils.py
├── Frontend/               # Streamlit UI
│   └── app.py
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yaml
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── .env                    # local secret file (not committed)
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/flex0ing-ag/Youtube-chatbot.git
cd Youtube-chatbot
```

### 2. Create your environment file

Copy the example file and add your personal Gemini key:

```bash
cp .env.example .env
```

Then edit `.env` and set:

```env
GEMINI_API_KEY=your_key_here
BACKEND_URL=http://backend:8000
```

### 3. Quick deploy with published Docker images

You can pull and run the images directly from Docker Hub:

- Frontend: https://hub.docker.com/r/anshikagpt27/youtube-chatbot-frontend
- Backend: https://hub.docker.com/r/anshikagpt27/youtube-chatbot-backend

```bash
docker pull anshikagpt27/youtube-chatbot-backend
docker pull anshikagpt27/youtube-chatbot-frontend
```

Run them with:

```bash
docker run -d --name youtube-chatbot-backend -p 8000:8000 --env-file .env anshikagpt27/youtube-chatbot-backend
docker run -d --name youtube-chatbot-frontend -p 8501:8501 -e BACKEND_URL=http://host.docker.internal:8000 anshikagpt27/youtube-chatbot-frontend
```

Then open:
- Frontend: http://localhost:8501
- Backend: http://localhost:8000

### 4. Start the app with local Docker Compose

```bash
docker compose up --build
```

### 5. Run locally without Docker

Backend:

```bash
cd Youtube-chatbot
python -m uvicorn Backend.main:app --host 0.0.0.0 --port 8000
```

Frontend:

```bash
cd Youtube-chatbot/Frontend
streamlit run app.py
```

## Environment Variables

| Variable | Required | Description |
|---|---:|---|
| `GEMINI_API_KEY` | Yes | Your Google Gemini API key |
| `BACKEND_URL` | Optional for local runs | Backend service URL for the frontend |

## Deployment Notes

This app is structured for simple container-based deployment. For production, you should:

- keep secrets in a real secret manager or deployment environment variables
- use a reverse proxy like NGINX or Cloud Run / Railway / Render / Fly.io
- enable HTTPS and proper domain routing
- add health checks and monitoring
- set `GEMINI_API_KEY` in the deployment environment, not in the repo

## License

This project is for educational and personal use.

## Contributing

Pull requests are welcome. If you want to improve the frontend, backend logic, or deployment setup, feel free to open a PR.

