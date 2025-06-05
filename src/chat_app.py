from datetime import datetime
from typing import List, Tuple

import streamlit as st
from streamlit_extras.bottom_container import bottom

from src.openai_client import get_openai_client


def initialize_session_state():
    """Initialize session state variables for chat history"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "message_counter" not in st.session_state:
        st.session_state.message_counter = 0


def add_message(role: str, content: str):
    """Add a new message to the chat history"""
    st.session_state.messages.append(
        {
            "id": st.session_state.message_counter,
            "role": role,
            "content": content,
            "timestamp": datetime.now().strftime("%H:%M"),
        }
    )
    st.session_state.message_counter += 1


def display_messages():
    """Display all messages in the chat"""
    if not st.session_state.messages:
        st.info("👋 Start a conversation by typing a message below!")
        return

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            # Optional: show timestamp in smaller text
            st.caption(f"Sent at {message['timestamp']}")


def generate_assistant_response(user_message: str, chat_history: List[Tuple[str, str]]) -> str:
    """Generate an assistant response using OpenAI ChatGPT"""
    try:
        # Get OpenAI client
        openai_client = get_openai_client()

        # Use chat history if available, otherwise empty list
        messages = [(m["role"], m["content"]) for m in chat_history]
        messages += [("user", user_message)]

        # Get response from OpenAI
        response = openai_client.get_response_for_chat(messages)

        return response

    except Exception as e:
        # Fallback to simple response if OpenAI fails
        error_msg = str(e)
        if "api key" in error_msg.lower() or "OPENAI_API_KEY" in error_msg:
            return "⚠️ OpenAI API key not configured. Please set your OPENAI_API_KEY environment variable."
        else:
            return f"⚠️ Sorry, I encountered an error: {error_msg}. Please try again."


def main():
    """Main function to run the Streamlit chat app"""
    # Page configuration
    st.set_page_config(
        page_title="AI Coach Chat", page_icon="💬", layout="wide", initial_sidebar_state="collapsed"
    )

    # Initialize session state
    initialize_session_state()

    # App header
    st.title("💬 AI Coach Chat")
    st.markdown("Welcome to your personal AI chat assistant!")

    # Create a container for chat messages that takes up most of the space
    chat_container = st.container()

    with chat_container:
        # Display existing messages
        display_messages()

    # Use bottom container for input - this stays at the bottom
    with bottom():
        st.markdown("---")
        with st.form(key="chat_form", clear_on_submit=True):
            col1, col2 = st.columns([6, 1])

            with col1:
                user_input = st.text_input(
                    "Type your message here...",
                    placeholder="Ask me anything!",
                    key="user_input",
                    label_visibility="collapsed",
                )

            with col2:
                send_button = st.form_submit_button("Send", use_container_width=True)

        # Handle message submission
        if send_button and user_input.strip():
            # Add user message
            add_message("user", user_input)

            # Generate and add assistant response with chat history
            assistant_response = generate_assistant_response(
                user_input, st.session_state.messages[:-1]
            )
            add_message("assistant", assistant_response)
            # Rerun to update the display
            st.rerun()

    # Sidebar with chat controls
    with st.sidebar:
        st.header("Chat Controls")

        if st.button("Clear Chat History", type="secondary"):
            st.session_state.messages = []
            st.session_state.message_counter = 0
            st.rerun()

        st.markdown("---")
        st.markdown(f"**Total messages:** {len(st.session_state.messages)}")

        if st.session_state.messages:
            st.markdown(f"**Last message:** {st.session_state.messages[-1]['timestamp']}")


if __name__ == "__main__":
    main()
