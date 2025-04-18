import streamlit as st
from dotenv import load_dotenv
import requests
import os
import random
import time
import json

# Load environment variables
load_dotenv()

# Custom CSS with enhanced space theme
st.markdown("""
<style>
    /* Modern Space Theme with Dark Purple Base */
    .main {
        background: linear-gradient(135deg, #0F0C29 0%, #302B63 50%, #24243E 100%);
        color: white !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Glassmorphism Cards with Purple Tint */
    .mission-card {
        color: white !important;
        background: rgba(123, 104, 238, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(138, 43, 226, 0.3);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px 0 rgba(75, 0, 130, 0.37);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .mission-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(138, 43, 226, 0.45);
    }
    
    /* Purple Gradient Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #8A2BE2 30%, #9400D3 90%);
        color: white;
        font-weight: 600;
        border-radius: 30px;
        padding: 15px 30px;
        border: none;
        box-shadow: 0 0 15px rgba(138, 43, 226, 0.5);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 0 25px rgba(148, 0, 211, 0.7);
    }
    
    /* Progress Tracker */
    .progress-milestone {
        background: rgba(138, 43, 226, 0.2);
        border-radius: 50%;
        width: 45px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        transition: all 0.3s ease;
        border: 2px solid rgba(138, 43, 226, 0.3);
    }
    
    .milestone-active {
        background: linear-gradient(45deg, #8A2BE2, #9400D3);
        border-color: rgba(255, 255, 255, 0.3);
        animation: pulse 2s infinite;
    }
    
    /* Achievement Badge */
    .achievement-badge {
        color: white !important;
        font-size: 3em;
        text-align: center;
        margin: 15px;
        padding: 20px;
        background: rgba(138, 43, 226, 0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(138, 43, 226, 0.3);
        animation: float 3s ease-in-out infinite;
    }
    
    /* Quote Box */
    .quote-box {
        color: white !important;
        background: linear-gradient(135deg, rgba(138, 43, 226, 0.1), rgba(148, 0, 211, 0.1));
        border-left: 5px solid #8A2BE2;
        padding: 20px;
        margin: 25px 0;
        border-radius: 0 20px 20px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Animations */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(138, 43, 226, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(138, 43, 226, 0); }
        100% { box-shadow: 0 0 0 0 rgba(138, 43, 226, 0); }
    }
    
    /* Creator Signature */
    .creator-signature {
        position: fixed;
        bottom: 10px;
        right: 10px;
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.8em;
        font-style: italic;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .mission-card {
            padding: 15px;
            margin: 10px 0;
        }
        
        .progress-milestone {
            width: 35px;
            height: 35px;
        }
        
        .achievement-badge {
            font-size: 2em;
            padding: 15px;
        }
    }
    
    /* Enhanced Text Styles */
    h1, h2, h3 {
        background: linear-gradient(120deg, #8A2BE2, #9400D3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        background: rgba(255, 255, 255, 0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #8A2BE2, #9400D3);
        border-radius: 5px;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(138, 43, 226, 0.3) !important;
        border-radius: 10px !important;
        color: white !important;
        padding: 15px !important;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #8A2BE2 !important;
        box-shadow: 0 0 10px rgba(138, 43, 226, 0.3) !important;
    }
    
    /* Checkbox Custom Style */
    .stCheckbox>div>div>label {
        color: white !important;
    }
    
    /* Progress Bar */
    .stProgress>div>div>div {
        background: linear-gradient(45deg, #8A2BE2, #9400D3) !important;
    }
</style>
""", unsafe_allow_html=True)

# Add creator signature
st.markdown('<div class="creator-signature">Created by Ubaid Raza</div>', unsafe_allow_html=True)

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/facebook/opt-350m"

import os
headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_TOKEN')}"}
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access the token
token = os.getenv("HUGGINGFACE_TOKEN")
headers = {"Authorization": f"Bearer {token}"}

def query_huggingface(payload):
    try:
        # Simplify payload
        if isinstance(payload, dict):
            text = payload.get('inputs', '')
        else:
            text = str(payload)
            
        simple_payload = {
            "inputs": text,
            "options": {
                "wait_for_model": True
            }
        }
        
        # Make API request
        response = requests.post(API_URL, headers=headers, json=simple_payload)
        
        # Handle different response cases
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and result:
                return result[0].get('generated_text', '')
            return get_fallback_response(text)
            
        elif response.status_code == 503:
            st.warning("Model is loading... Please try again in a few seconds.")
            time.sleep(5)  # Wait for model to load
            return get_fallback_response(text)
            
        else:
            st.error(f"API Error: Status code {response.status_code}")
            return get_fallback_response(text)
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return get_fallback_response(text)

def test_api_connection():
    try:
        test_response = query_huggingface("Generate a short motivational message")
        if test_response and not test_response.startswith("API Error"):
            return True, "API connection successful!"
        return False, "API connection failed"
    except Exception as e:
        return False, f"Connection Error: {str(e)}"

# Add this at the start of your app to test the connection
with st.sidebar:
    if st.button("🔄 Test API Connection"):
        with st.spinner("Testing API connection..."):
            is_connected, message = test_api_connection()
            if is_connected:
                st.success(message)
            else:
                st.error(message)

def get_fallback_response(prompt):
    responses = {
        "mission": [
            "Embark on a cosmic journey of continuous learning and growth.",
            "Push beyond your current limits and explore new galaxies of possibility.",
            "Transform challenges into stars to navigate by in your advancement."
        ],
        "challenge": [
            "Break down your mission into daily interstellar explorations.",
            "Track your progress like a space mission - one milestone at a time.",
            "Maintain mission logs to document your cosmic growth journey."
        ],
        "motivation": [
            "The universe of possibilities awaits your exploration, brave astronaut.",
            "Every small step is a light-year leap toward your greater potential.",
            "Your growth journey spans galaxies of opportunity."
        ]
    }
    
    if "mission" in prompt.lower():
        return random.choice(responses["mission"])
    elif "challenge" in prompt.lower():
        return random.choice(responses["challenge"])
    else:
        return random.choice(responses["motivation"])

# Sidebar for Explorer Profile
with st.sidebar:
    st.title("🚀 Mission Control")
    if 'explorer_name' not in st.session_state:
        st.session_state.explorer_name = st.text_input("Enter Explorer Name:", "Cosmic Pioneer")
    
    st.subheader("Mission Stats")
    if 'missions_completed' not in st.session_state:
        st.session_state.missions_completed = 0
    
    st.metric("Missions Launched", st.session_state.missions_completed)
    
    # Achievement ranks
    st.subheader("Explorer Rank")
    ranks = {
        5: "🛰️ Nebula Scout",
        10: "✨ Star Navigator",
        20: "🌌 Galaxy Pioneer",
        30: "⚡ Cosmic Legend"
    }
    
    current_rank = max([level for level in ranks.keys() 
                       if st.session_state.missions_completed >= level] or [0])
    
    if current_rank > 0:
        st.markdown(f"<div class='achievement-badge'>{ranks[current_rank]}</div>", 
                   unsafe_allow_html=True)

# Main Mission Control
st.title("🌌 Cosmic Growth Explorer")
st.write(f"Welcome, Explorer {st.session_state.explorer_name}! Ready for your next interstellar mission?")

# Mission Planning
with st.container():
    st.header("🎯 Launch New Mission")
    mission = st.text_area("What's your next cosmic growth mission?", 
                          placeholder="Example: Master the art of public speaking across the galaxy...")
    
    if st.button("Initialize Mission Plan"):
        if mission:
            with st.spinner("Calculating interstellar mission parameters..."):
                # Get AI responses
                refined_mission = query_huggingface({"inputs": f"Refine this cosmic growth mission: {mission}"})
                strategy = query_huggingface({"inputs": f"Create a 30-day interstellar strategy for: {mission}"})
                cosmic_wisdom = query_huggingface({"inputs": "Share profound cosmic wisdom about growth and space exploration"})
                
                # Display mission briefing
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("<div class='mission-card'>", unsafe_allow_html=True)
                    st.subheader("🌠 Mission Objectives")
                    st.write(refined_mission)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<div class='mission-card'>", unsafe_allow_html=True)
                    st.subheader("📡 30-Day Flight Plan")
                    st.write(strategy)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='quote-box'>", unsafe_allow_html=True)
                st.write(f"💫 *{cosmic_wisdom}*")
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.session_state.missions_completed += 1
        else:
            st.warning("Please define your mission objectives!")

# Mission Progress Tracking
if 'mission_progress' not in st.session_state:
    st.session_state.mission_progress = [False] * 30

st.header("📡 Mission Progress Tracker")

# Create an interactive space journey tracker
progress_cols = st.columns(10)
for i in range(30):
    col_index = i % 10
    with progress_cols[col_index]:
        milestone_class = "progress-milestone milestone-active" if st.session_state.mission_progress[i] else "progress-milestone"
        st.markdown(f"<div class='{milestone_class}'>", unsafe_allow_html=True)
        day_complete = st.checkbox(f"D{i+1}", value=st.session_state.mission_progress[i], key=f"day_{i}", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
        if day_complete != st.session_state.mission_progress[i]:
            st.session_state.mission_progress[i] = day_complete
            st.rerun()

# Progress visualization
completed = sum(st.session_state.mission_progress)
progress_percentage = (completed / 30) * 100

st.progress(progress_percentage / 100)
st.write(f"🌠 Mission Progress: {completed}/30 milestones achieved! ({progress_percentage:.1f}%)")

# Mission Status
if progress_percentage == 100:
    st.balloons()
    st.success("🌌 Mission Accomplished! You've navigated all cosmic milestones!")
elif progress_percentage >= 75:
    st.info("🚀 Warp speed achieved! The final frontier approaches!")
elif progress_percentage >= 50:
    st.info("💫 Halfway through your cosmic journey! Maintain course!")
elif progress_percentage >= 25:
    st.info("✨ Successful liftoff! Your journey has begun!")
else:
    st.info("🛸 Pre-launch sequence initiated! Prepare for takeoff!")

# Cosmic Tips
st.header("🌠 Cosmic Wisdom Transmission")
cosmic_tips = [
    "The universe expands for those who dare to grow beyond limits.",
    "Each challenge is a new star system to explore and conquer.",
    "Your potential stretches across galaxies, waiting to be discovered.",
    "Navigate through asteroid fields of difficulty with skill and courage.",
    "Light-years of growth begin with a single step forward.",
    "The unknown holds the greatest treasures of self-discovery.",
    "Your mindset is the warp drive propelling you through challenges.",
    "Chart your unique course among the infinite stars of possibility.",
    "Every meteor of failure contains valuable stardust for learning.",
    "Your growth journey is creating new constellations in the universe."
]
st.info(random.choice(cosmic_tips))

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: rgba(255,255,255,0.7);'>"
    "Exploring the infinite cosmos of growth potential "
    "</div>", 
    unsafe_allow_html=True
)


# Footer branding
st.markdown("<div class='footer'>Created by <b>Ubaid Raza</b></div>", unsafe_allow_html=True)
