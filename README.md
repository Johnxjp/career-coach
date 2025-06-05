# AI Coach Chat Application

A simple Streamlit-based chat application that provides a clean interface for chatting with an AI assistant powered by OpenAI's ChatGPT.

## Features

- Clean, modern chat interface
- Real-time message display with timestamps
- Chat history management with full conversation context
- Integration with OpenAI ChatGPT (gpt-4o-mini by default)
- Configurable AI model settings
- Responsive design with bottom-anchored input
- Sidebar with chat controls and statistics

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

### 3. Run the Application

Choose one of these methods:

#### Option 1: Direct Streamlit Run
```bash
streamlit run src/chat_app.py
```

#### Option 2: Using the Entry Point
```bash
python main.py
```

## Dependencies

The main dependencies are:
- `streamlit>=1.45.1` - Web app framework
- `streamlit-extras>=0.7.1` - Additional Streamlit components
- `openai>=1.84.0` - OpenAI API client

To add new dependencies:
```bash
uv add package-name
```

## Project Structure

```
ai-coach/
├── src/
│   ├── __init__.py
│   ├── chat_app.py          # Main Streamlit chat application
│   └── openai_client.py     # OpenAI API integration
├── main.py                  # Entry point script
├── pyproject.toml           # Project configuration and dependencies
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore patterns
└── README.md               # This file
```

## Configuration

### Environment Variables

The application uses environment variables for configuration:

- `OPENAI_API_KEY` (required): Your OpenAI API key
- `OPENAI_MODEL` (optional): Model to use (default: `gpt-4o-mini`)
- `OPENAI_MAX_TOKENS` (optional): Maximum response length (default: 1000)
- `OPENAI_TEMPERATURE` (optional): Response creativity (default: 0.7)

Available models include:
- `gpt-4o-mini` (default, cost-effective)
- `gpt-4o` (latest GPT-4 model)
- `gpt-4-turbo`
- `gpt-3.5-turbo`

## Usage

1. Start the application using one of the methods above
2. Open your browser to the provided URL (usually http://localhost:8501)
3. Type messages in the input box at the bottom
4. Click "Send" or press Enter to send messages
5. The AI assistant will respond using OpenAI's ChatGPT
6. Use the sidebar to clear chat history or view message statistics

## Features in Detail

### Chat Interface
- Messages are displayed in chronological order
- Input box is anchored to the bottom of the screen
- Timestamps are shown for each message
- Auto-scroll to newest messages

### AI Integration
- Full conversation context is sent to OpenAI
- Error handling for API failures and missing keys
- Configurable model and parameters
- Fallback error messages for troubleshooting

### Session Management
- Chat history persists during the session
- Message counter for unique IDs
- Clear chat functionality
- Message statistics in sidebar

## Troubleshooting

### "OpenAI API key not configured" Error
- Make sure you've set up your `.env` file with a valid `OPENAI_API_KEY`
- Restart the Streamlit application after adding the API key

### API Errors
- Check your OpenAI account has available credits
- Verify your API key is valid and active
- Check the OpenAI status page for service issues

## Customization

The application is designed to be easily extensible:

- Modify `generate_assistant_response()` to change AI behavior
- Adjust the system message in `openai_client.py` to customize the assistant's personality
- Add new configuration options in the `OpenAIConfig` class
- Extend the UI with additional Streamlit components