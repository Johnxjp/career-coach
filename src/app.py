from datetime import datetime
import os
from typing import List, Tuple

import streamlit as st
from streamlit_extras.bottom_container import bottom

from src.openai_client import OpenAIClient, get_openai_client
from src.prompts import client_message, intro_message, generate_summary_message


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


def initialize_session_state():
    """Initialize session state variables for chat history"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.message_counter = 0
        add_message("assistant", intro_message)
    if "is_active" not in st.session_state:
        st.session_state.is_active = True


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


def generate_assistant_response(
    client: OpenAIClient, user_message: str, chat_history: List[Tuple[str, str]]
) -> str:
    """Generate an assistant response using OpenAI ChatGPT"""
    try:
        # Use chat history if available, otherwise empty list
        messages = [(m["role"], m["content"]) for m in chat_history]
        messages += [("user", client_message.format(client_message=user_message))]

        # Get response from OpenAI
        response = client.get_response_for_chat(messages)
        # response = "good news"

        return response

    except Exception as e:
        # Fallback to simple response if OpenAI fails
        error_msg = str(e)
        if "api key" in error_msg.lower() or "OPENAI_API_KEY" in error_msg:
            return "⚠️ OpenAI API key not configured. Please set your OPENAI_API_KEY environment variable."
        else:
            return f"⚠️ Sorry, I encountered an error: {error_msg}. Please try again."


def generate_summary_file(client: OpenAIClient, chat_history: List[dict]) -> str:
    """
    Generate a summary file from the chat messages.
    The content format is markdown. The content should be between <text> and </text> tags.
    The prompt has been designed to start with <text> so that the model is prompted to immediately start writing the summary.
    """
    try:
        messages = [(m["role"], m["content"]) for m in chat_history]
        messages += [("user", generate_summary_message)]
        response = client.get_response_for_chat(messages)
        summary = response.strip()
        if "<text>" in summary:
            summary = summary.split("<text>")[1]
        if "</text>" in summary:
            summary = summary.split("</text>")[0]

        summary = summary.strip()

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"career_coaching_summary_{timestamp}.md"

        # Create summaries directory if it doesn't exist
        os.makedirs("summaries", exist_ok=True)
        filepath = os.path.join("summaries", filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(summary)

        return filepath

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
        page_title="AI Coach Chat", page_icon="💬", layout="wide", initial_sidebar_state="expanded"
    )
    openai_client = get_openai_client()

    # Initialize session state
    initialize_session_state()

    # App header
    st.title("💬 AI Career Coach")

    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("A personal coach to help you figure out your career path and next steps!")
    with col2:
        end_conversation = st.button(
            "Finish Conversation",
            use_container_width=True,
        )

    # Create a container for chat messages that takes up most of the space
    chat_container = st.container()

    with chat_container:
        # Display existing messages
        display_messages()

    # Use bottom container for input - this stays at the bottom
    if st.session_state.is_active:
        with bottom():
            with st.form(key="chat_form", clear_on_submit=True):
                col1, col2 = st.columns([6, 1])

                with col1:
                    user_input = st.text_area(
                        "Type your message here...",
                        placeholder="Ask me anything!",
                        height=68,
                        key="user_input",
                        label_visibility="collapsed",
                    )

                with col2:
                    send_button = st.form_submit_button("Send", use_container_width=True)

        # Handle message submission
        if send_button and user_input.strip():
            # Add user message
            add_message("user", user_input)
            with st.chat_message("user"):
                st.write(user_input)

            # Generate and add assistant response with chat history
            assistant_response = generate_assistant_response(
                openai_client, user_input, st.session_state.messages[:-1]
            )
            add_message("assistant", assistant_response)
            # Rerun to update the display
            st.rerun()

        if end_conversation:
            # Generate summary file
            st.session_state.is_active = False
            st.success("Conversation ended. You can start a new one by refreshing!")
            if len(st.session_state.messages) > 2:  # Only show if there's actual conversation
                with st.spinner("Generating summary..."):
                    summary_file = generate_summary_file(openai_client, st.session_state.messages)

                    if summary_file:
                        st.success("Summary generated successfully!")

                        # Read the file content for display and download
                        with open(summary_file, "r", encoding="utf-8") as f:
                            summary_content = f.read()

                        # Download button
                        st.download_button(
                            label="Download Conversation Summary",
                            data=summary_content,
                            file_name=os.path.basename(summary_file),
                            mime="text/markdown",
                        )

                st.success(f"Conversation ended. Summary saved to {summary_file}")
            else:
                st.info("Have a conversation first.")

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
