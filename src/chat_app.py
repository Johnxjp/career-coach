from datetime import datetime

import streamlit as st
from streamlit_extras.bottom_container import bottom


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


def generate_assistant_response(user_message: str) -> str:
    """Generate a simple assistant response (you can replace this with AI integration later)"""
    # Simple responses for demonstration
    responses = {
        "hello": "Hello! How can I help you today?",
        "hi": "Hi there! What would you like to chat about?",
        "how are you": "I'm doing well, thank you for asking! How are you?",
        "bye": "Goodbye! Have a great day!",
        "help": "I'm here to help! You can ask me questions or just have a conversation.",
    }

    user_lower = user_message.lower().strip()

    # Check for exact matches first
    for key, response in responses.items():
        if key in user_lower:
            return response

    # Default response
    return f"That's interesting! You said: '{user_message}'. I'm a simple chatbot, but I'm here to chat with you!"


def main():
    """Main function to run the Streamlit chat app"""
    # Page configuration
    st.set_page_config(
        page_title="AI Coach Chat", 
        page_icon="💬", 
        layout="wide", 
        initial_sidebar_state="collapsed"
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

            # Generate and add assistant response
            assistant_response = generate_assistant_response(user_input)
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
