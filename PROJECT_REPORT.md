# YouTube Learning AI Assistant – Project Report

## 1. What this project does

This project is a full-stack web application that lets a user:

- paste a YouTube video link
- fetch the video transcript
- ask questions about the transcript
- get AI-powered answers based on the video content
- listen to the transcript as audio

In simple terms, it behaves like a personal AI study assistant for YouTube videos.

Example: a user gives the app a video about Python, asks “What are the advantages of lists in Python?”, and the app reads the transcript, sends it to Gemini, and returns an answer based only on the video’s content.

---

## 2. Why this project exists

Most YouTube videos contain useful information, but often:

- transcripts are not visible to the user
- videos are long and hard to search
- users want quick answers without watching the entire video
- it is hard to ask questions about a video and get precise answers

This app solves that by combining:

- a transcript extraction system
- an AI model that understands the transcript
- a simple interface that users can interact with

This makes it useful for:

- students learning from tutorials
- researchers summarizing content
- people reviewing long videos quickly
- anyone wanting a faster way to ask questions about a recorded lecture or tutorial

---

## 3. High-level architecture

The project has 3 main layers:

### 3.1 Frontend layer
This is the user interface.

- It is built with Streamlit.
- It allows a user to paste a YouTube URL.
- It shows the transcript.
- It sends questions to the backend.
- It can generate speech from the transcript.

This layer is designed for simplicity. A common user does not need to write any code to use it.

### 3.2 Backend layer
This is the API server.

- It is built with FastAPI.
- It receives requests from the frontend.
- It extracts the YouTube video ID.
- It fetches transcript data.
- It sends the transcript and user question to the AI model.
- It returns answers to the frontend.

The backend is the “brain” of the app because it connects the user, the transcript API, and the AI model.

### 3.3 AI layer
This is where the real intelligence happens.

- It uses Google Gemini through LangChain.
- The AI reads the transcript and answers the user’s question using that transcript as context.

This means answers are based on the video, not random web knowledge.

---

## 4. Project structure and what each file does

Below is a complete explanation of every important file in the project.

### 4.1 README.md
Purpose:
- explains the project
- tells users how to install and run it
- shows the setup steps
- documents the project structure

Why it matters:
- new developers can understand the project quickly
- other users can know how to run the app without reading the code first

What is in it:
- project overview
- features list
- technologies used
- local setup steps
- Docker instructions
- deployment notes

---

### 4.2 requirements.txt
Purpose:
- lists all Python dependencies required by the project

Why it matters:
- this file allows installation with one command
- every Python library used by the backend/frontend is listed here

Example libraries include:

- FastAPI: API framework for backend
- Uvicorn: server runner for FastAPI
- Streamlit: frontend web app framework
- python-dotenv: loads environment variables
- langchain-google-genai: Google Gemini integration
- youtube-transcript-api: fetch YouTube transcript text
- gTTS: text-to-speech conversion

Without this file, the project would be much harder to install and run consistently.

---

### 4.3 .env.example
Purpose:
- shows the environment variables required by the project
- acts as a template for real secrets

Why it matters:
- secrets like API keys should not be committed to GitHub
- this file makes setup safe and easy

Typical variables:

- GEMINI_API_KEY: required to access the Gemini model
- BACKEND_URL: optional for frontend to know where the backend API is running

This file keeps configuration organized and secure.

---

### 4.4 .gitignore
Purpose:
- prevents sensitive or unnecessary files from being uploaded to GitHub

Why it matters:
- .env files should never be pushed
- cache folders, virtual environments, and editor settings should be ignored

It usually includes:

- .env
- __pycache__
- .venv
- .idea
- .vscode
- logs and generated files

This is important for security and cleanliness.

---

### 4.5 Backend/ main.py
Purpose:
- defines the API endpoints for the backend

Why it matters:
- the frontend talks to this server
- this file exposes actions like fetching a transcript or asking a question

Main features:

#### app = FastAPI()
This creates the backend application itself.

#### /health
Returns a simple status message to show the API is running.

This is useful for testing if the server is alive.

#### /generate_videoid
This endpoint accepts a YouTube URL and extracts the video ID.

Why needed:
- a YouTube URL is not the same as a video ID
- transcript APIs usually work with video ID, not full URL

#### /generate_transcript
This endpoint receives a video ID and asks the service layer to fetch the transcript.

Why needed:
- the frontend does not talk directly to YouTube transcript APIs
- the backend centralizes logic and error handling

#### /chat
This is the most important endpoint.

It receives:
- the video URL
- the user question

Then it:
- extracts the video ID
- fetches the transcript
- sends transcript + question to Gemini
- returns the AI response

The app uses Pydantic models to validate incoming JSON data.

---

### 4.6 Backend/ llm_service.py
Purpose:
- handles AI and transcript logic

Why it matters:
- this is the main “working engine” of the project
- it connects the app to Google Gemini and YouTube transcript extraction

Important parts:

#### load_dotenv
This loads environment variables from local .env files.

Why needed:
- the API key for Gemini is kept securely outside the code

#### LLMService.__init__
This constructor creates the AI model object.

It sets:
- model: gemini-1.5-flash
- temperature: 0.7

Why these values matter:
- temperature controls creativity; a lower value gives more stable answers
- the model is chosen for speed and cost efficiency

#### PromptTemplate
This defines the instruction sent to the AI.

It tells Gemini:
- you are a helpful AI tutor
- use only the transcript to answer
- answer the user’s question

This helps keep the AI grounded in the video content instead of making up answers.

#### get_transcript(video_id)
This function fetches the transcript for the video.

It uses the YouTube Transcript API library.

The code handles two API styles:
- older version style
- newer version style

This is important because the library API may change across versions.

Then it converts transcript entries into plain text by collecting each item’s text.

This results in a clean transcript string ready for the AI model.

#### chat_with_transcript(url, query)
This is the main Q&A function.

Process:
1. extract video ID from URL
2. fetch transcript
3. construct a prompt using the transcript and user question
4. run the model
5. return AI answer

This is the key logic that allows the app to answer questions based on the video content.

---

### 4.7 Backend/ models.py
Purpose:
- defines the request and response data structures

Why it matters:
- FastAPI uses these models to validate input and output
- this makes the API more reliable and easier to understand

Models defined:

- YouTubeURL: expects a JSON object like {"url": "..."}
- YouTubeID: expects {"id": "abc123"}
- TranscriptResponse: returns {"transcript": "..."}
- ChatRequest: expects {"url": "...", "query": "..."}
- ChatResponse: returns {"query": "...", "response": "..."}

This is a good example of clean API design.

---

### 4.8 Backend/ utils.py
Purpose:
- contains the logic to extract a YouTube video ID from a URL

Why it matters:
- the app may receive multiple types of YouTube URLs:
  - standard watch URLs
  - short links
  - URL variants with extra parameters

This file uses regular expressions to find the video ID in the URL.

Example:
- https://www.youtube.com/watch?v=dQw4w9WgXcQ
- https://youtu.be/dQw4w9WgXcQ

The function detects the ID and returns it.

---

### 4.9 Frontend/ app.py
Purpose:
- builds the Streamlit user interface

Why it matters:
- this is the part users actually see and interact with

Main sections:

#### App styling
The page uses custom HTML/CSS to make the interface look modern and friendly.

#### Session state
This stores:
- transcript
- chat history
- current video URL

Session state is important because the app must remember what the user has done while the page stays open.

#### Sidebar
The sidebar shows:
- chat history
- transcript preview
- clear conversation button

This improves usability.

#### Fetch Transcript button
When the user enters a YouTube URL and clicks the button, the frontend does this:

1. sends the URL to /generate_videoid
2. receives the video ID
3. sends the ID to /generate_transcript
4. saves the transcript in session state

#### Chat input
Once a transcript is loaded, the user can ask questions in the chat area.

The frontend sends:
- the saved URL
- the user question

to the backend /chat route, which returns the AI answer.

#### Audio conversion
The app uses gTTS to convert the transcript text into an MP3 file and plays it in the browser.

This adds an audio learning feature and makes the app feel more like a study tool.

---

### 4.10 Dockerfile.backend
Purpose:
- builds the backend into a Docker container

Why it matters:
- makes deployment consistent across machines
- allows the app to run in the same environment everywhere

Typical steps:
- choose Python image
- install requirements
- copy backend files into the container
- start the app with Uvicorn

This file is important for deploying the backend as a service.

---

### 4.11 Dockerfile.frontend
Purpose:
- builds the Streamlit frontend into a Docker container

Why it matters:
- the user interface can run in a standardized environment
- deployment becomes easier and more scalable

---

### 4.12 docker-compose.yaml
Purpose:
- runs multiple services together in one setup

Why it matters:
- the backend and frontend can be started together with a single command
- it reduces complexity during local development and testing

This file connects the app services and manages environment configuration.

---

## 5. How the app works end-to-end

Here is the full lifecycle of a user request:

### Step 1: User enters a YouTube URL
The user types something like:

https://www.youtube.com/watch?v=abc123xyz

### Step 2: Frontend validates and extracts ID
The Streamlit app sends the URL to the backend /generate_videoid endpoint.

The backend calls the utility function:

extract_youtube_video_id(url)

This returns only the video ID.

### Step 3: Backend fetches the transcript
The backend calls LLMService.get_transcript(video_id).

The transcript API downloads the video transcript and converts it to plain text.

### Step 4: Transcript is shown in the UI
The frontend stores the transcript in session state and displays it in the app.

### Step 5: User asks a question
Example:

“What is the main point of this video?”

### Step 6: Backend sends transcript + question to Gemini
The backend uses LangChain PromptTemplate and ChatGoogleGenerativeAI.

The prompt is built like this:

- “You are a helpful AI tutor.”
- “Use the transcript to answer.”
- “Here is the transcript.”
- “Here is the question.”

### Step 7: AI answers using the transcript
Gemini reads the transcript and responds with a grounded answer.

This is much more useful than general internet-based answers because it is tied to the video content.

### Step 8: Frontend displays answer and supports audio
The frontend renders the answer in chat and can also convert the transcript to sound using gTTS.

---

## 6. Why these technologies are used

### FastAPI
Used for the backend API because it is:
- fast
- modern
- easy to build with Python
- good for REST APIs
- compatible with Pydantic validation

### Streamlit
Used for the frontend because it is:
- easy to build simple AI apps quickly
- designed for prototyping and data apps
- user-friendly for non-web developers

### LangChain + Google Gemini
Used because they provide:
- an LLM-powered question-answering workflow
- easy integration with prompt templates
- strong natural language understanding

### youtube-transcript-api
Used because it extracts transcript text from YouTube videos without manually scraping the site.

### gTTS
Used because it converts transcript text into downloadable or playable audio.

### python-dotenv
Used so the app can read secrets from a .env file without hardcoding them in code.

### Docker + Docker Compose
Used because they make deployment simple and consistent.

---

## 7. Why the project is structured this way

The project splits responsibilities into separate folders:

- Backend: logic and API
- Frontend: user interface
- Docker files: deployment
- .env files: configuration secrets

This separation is important because it keeps the code organized.

A common project principle is:

- UI should not contain business logic
- API logic should be separated from frontend logic
- AI and transcript handling should be centralized
- secrets should not be stored in the repository

This app follows that pattern well.

---

## 8. What the app is good at

This project is especially good for:

- learning from video tutorials
- summary-based Q&A over long content
- fast knowledge retrieval without full video watching
- demoing AI-powered document reasoning in a simple interface

It is not a full production system for heavy enterprise use without additional work such as:

- better auth and user accounts
- secure API key management
- better error logging
- rate limiting
- video caching
- larger-scale deployment architecture

---

## 9. Security and best practices

This project intentionally keeps some things simple, but there are important points to remember:

- do not commit your real .env file
- never expose API keys in public code
- use environment variables in deployment platforms
- keep backend and frontend separated
- validate user inputs

The project already follows some of this through .gitignore and env configuration.

---

## 10. How to run the project

### Local backend
```bash
cd Youtube-chatbot
python -m uvicorn Backend.main:app --host 0.0.0.0 --port 8000
```

### Local frontend
```bash
cd Youtube-chatbot/Frontend
streamlit run app.py
```

### With Docker Compose
```bash
cd Youtube-chatbot
docker compose up --build
```

---

## 11. Simple explanation for a non-technical user

If you are not a programmer, the easiest way to think about this project is:

- the app is a smart assistant for YouTube videos
- it reads the text of a video automatically
- it lets you ask questions about the video
- it answers using the transcript and an AI model
- the frontend is what you see, the backend works behind the scenes, and the AI is what understands the content

So instead of watching a long video from start to finish, you can ask direct questions like:

- “What are the key ideas?”
- “Can you explain this part more simply?”
- “What are the drawbacks mentioned?”
- “Summarize the main points.”

This makes the app useful for study, learning, and quick review.

---

## 12. Final summary

This project is a lightweight AI-powered YouTube learning assistant.

It combines:

- YouTube transcript extraction
- a Python API backend
- a simple Streamlit frontend
- Google Gemini for answers
- Docker for easy deployment

The code is organized in a clean way so the responsibilities are separated:

- frontend handles user interface
- backend handles logic and API requests
- service layer handles transcript + AI processing
- utilities handle reusable helper logic
- environment files keep secrets safe

This is a good example of a practical AI application built with Python, modern web frameworks, and cloud-friendly deployment tools.

---

## 13. Optional conversion to Word document

This file is written in Markdown so it is easy to read in GitHub and also easy to convert to a .docx file using tools like Pandoc.

Example command:

```bash
pandoc PROJECT_REPORT.md -o PROJECT_REPORT.docx
```

If a .docx version is needed later, this Markdown file can be turned into a Word document with a single conversion step.
