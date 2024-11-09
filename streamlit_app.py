import streamlit as st
import requests
import random
import time

# Define the API URL specifically for the Interview Game model
API_URL_INTERVIEW_GAME = "https://flowise-9kx9.onrender.com/api/v1/prediction/cbf21cc5-8823-46a5-af90-66fca1c9ee32"

# List of randomized "thinking" messages
thinking_messages = [
    "Alex is Crunching the numbers…",
    "Alex: Try but you won't win.",
    "Evaluating responses, will you stand out?",
    "Checking with the HR team…",
    "The competition's heating up… recalculating strategies!",
    "Sending return offers.."
]

# Initialize session state for chat messages if not already set
if "interview_game_messages" not in st.session_state:
    st.session_state.interview_game_messages = []

# Display a unique title and description for the Interview Game
st.title("🏆 Interview Game - Challenge Yourself with Alex")
st.markdown(
    """
    Welcome to the Interview Game! This is a competitive interview experience where you compete against Alex to answer
    finance and investment banking questions under simulated high-stakes conditions. See how you stack up and learn as you go.
    
    - 💬 Chris will ask questions, provide feedback, and decide the winner for each question.
    - 🧩 Try to answer as you would in a real interview
    - 📈 Track your progress as you improve your responses.
    
    Let's begin!
    """
)

# Set a unique welcome message for the Interview Game
if not st.session_state.interview_game_messages:
    st.session_state.interview_game_messages.append({
        "role": "assistant", 
        "content": "Welcome to the interview game! I am Chris, your host. Ready to see how you stack up in a simulated interview against Alex?"
    })

# Function to query the Interview Game API
def query_interview_game(context, prompt):
    payload = {"question": f"{context}\n\nUser Question: {prompt}"}

    #Debugging output to check the payload before sending
    #st.write("Sending payload:", payload)

    response = requests.post(API_URL_INTERVIEW_GAME, json=payload)
    if response.status_code == 200:
        return response.json().get("text", "Error: No response text")
    else:
        return f"Error: {response.status_code}"

# Display the chat history for the Interview Game
for message in st.session_state.interview_game_messages:
    role = message["role"]
    avatar_url = "https://github.com/Reese0301/GIS-AI-Agent/blob/main/JackIcon.png?raw=true" if role == "assistant" else "https://github.com/Reese0301/GIS-AI-Agent/blob/main/FoxUser.png?raw=true"
    
    with st.chat_message(role, avatar=avatar_url):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Answer here..."):
    # Add user's question to chat history
    st.session_state.interview_game_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="https://github.com/Reese0301/GIS-AI-Agent/blob/main/FoxUser.png?raw=true"):
        st.markdown(prompt)

    # Show thinking message while awaiting response
    thinking_message = random.choice(thinking_messages)
    thinking_placeholder = st.empty()
    thinking_placeholder.markdown(f"💭 **{thinking_message}**")

    # Prepare context by limiting to the last few messages
    CONTEXT_LIMIT = 5
    context = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.interview_game_messages[-CONTEXT_LIMIT:]])

    # Query the Interview Game API
    start_time = time.time()
    response_content = query_interview_game(context, prompt)
    response_time = time.time() - start_time
    thinking_placeholder.empty()

    # Display Alex's response
    with st.chat_message("assistant", avatar="https://github.com/Reese0301/GIS-AI-Agent/blob/main/JackIcon.png?raw=true"):
        st.markdown(f"💭 Thought for {response_time:.2f} seconds\n\n{response_content}")

    # Add Alex's response to chat history
    st.session_state.interview_game_messages.append({"role": "assistant", "content": response_content})
