# AI Professional Coach

A simple Streamlit-based chat application that provides a clean interface for chatting with a professional coaching assistant. The coach focuses on career change and helps the 'client' explore their current situation, generate ideas for next steps and design an actionable plan to progress. At the end of the conversation a summary of the discussion is produced.

## Setup

### 1. Install Dependencies

This project uses `uv` for dependency management:

```bash
uv sync
```

### 2. Configure OpenAI API Key

1. Get your OpenAI API key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```
