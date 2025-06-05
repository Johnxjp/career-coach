# AI Coach Chat Application

A simple Streamlit-based chat application that provides a clean interface for chatting with an AI assistant.

## Features

- Clean, modern chat interface
- Real-time message display
- Message timestamps
- Chat history management
- Responsive design
- Sidebar with chat controls

## Running the Application

### Option 1: Direct Streamlit Run
```bash
streamlit run src/chat_app.py
```

### Option 2: Using the Runner Script
```bash
python run_chat.py
```

### Option 3: Module Execution
```bash
streamlit run src/chat_app.py
```

## Dependencies

This project uses `uv` for dependency management. The main dependencies are:
- `streamlit>=1.45.1`

To add new dependencies:
```bash
uv add package-name
```

## Project Structure

```
ai-coach/
├── src/
│   ├── __init__.py
│   └── chat_app.py          # Main chat application
├── run_chat.py              # Entry point script
├── pyproject.toml           # Project configuration
└── README.md               # This file
```

## Usage

1. Start the application using one of the methods above
2. Open your browser to the provided URL (usually http://localhost:8501)
3. Type messages in the input box at the bottom
4. Click "Send" or press Enter to send messages
5. Use the sidebar to clear chat history or view message statistics

## Customization

The assistant responses are currently simple rule-based responses. You can easily integrate with AI services like OpenAI, Anthropic, or other LLM providers by modifying the `generate_assistant_response` function in `src/chat_app.py`.