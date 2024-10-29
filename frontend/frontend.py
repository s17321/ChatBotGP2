# frontend/frontend.py
import streamlit as st
import requests

# Page config
st.set_page_config(page_title="GPT-2 Chatbot", layout="centered")

# Initialize session state to keep track of chat history
if "history" not in st.session_state:
    st.session_state.history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Function to handle message sending
def send_message():
    user_message = st.session_state.user_input
    if user_message:
        # Send user input to the FastAPI backend
        try:
            response = requests.post("http://127.0.0.1:8000/generate/", json={"prompt": user_message})
            if response.status_code == 200:
                bot_response = response.json()["response"]
                
                # Append the user prompt and bot response to the history
                st.session_state.history.append({"user": user_message, "bot": bot_response})
                
                # Clear the input field by setting it to an empty string
                st.session_state.user_input = ""
            else:
                st.error("Error generating response.")
        except Exception as e:
            st.error(f"Could not connect to backend. Make sure the FastAPI server is running. Error: {e}")

# Display the conversation history in chat format, showing the latest messages at the bottom
for entry in st.session_state.history:  # Display messages in natural order
    # User message (align to the right)
    st.markdown(
        f"""
        <div style='text-align: right; margin: 5px; padding: 10px; background-color: #4CAF50; color: white; border-radius: 10px; width: fit-content; margin-left: auto;'>
            <strong>You:</strong> {entry['user']}
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Bot response (align to the left)
    st.markdown(
        f"""
        <div style='text-align: left; margin: 5px; padding: 10px; background-color: #333333; color: white; border-radius: 10px; width: fit-content;'>
            <strong>Bot:</strong> {entry['bot']}
        </div>
        """,
        unsafe_allow_html=True,
    )

# Divider for styling
st.write("---")

# Input field with Enter key functionality to trigger send_message
st.text_input("Type your message:", key="user_input", on_change=send_message, placeholder="Type here and press Enter...")

# Automatically scroll to the bottom to view the latest messages
st.write('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
