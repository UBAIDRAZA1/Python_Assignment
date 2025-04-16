import streamlit as st
import zxcvbn

# Set a background image using online image (you can replace with your own)
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1607746882042-944635dfe10e");
        background-size: cover;
        background-position: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: white;
    }
    .password-bar {
        border-radius: 10px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .footer {
        position: fixed;
        bottom: 10px;
        right: 20px;
        font-size: 14px;
        color: white;
        opacity: 0.7;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to evaluate password strength
def evaluate_password_strength(password):
    result = zxcvbn.zxcvbn(password)
    score = result['score']  # score ranges from 0 (weak) to 4 (strong)
    feedback = result['feedback']['suggestions']
    return score, feedback

# Function to display password strength
def get_strength_color(score):
    if score == 0:
        return "red", "Weak 💔"
    elif score == 1:
        return "orange", "Weak 💔"
    elif score == 2:
        return "yellow", "Medium 💪"
    elif score == 3:
        return "lightgreen", "Strong 💪"
    else:
        return "green", "Very Strong 💥"

# Streamlit UI
st.markdown("<h1 style='text-align: center;'>🔐 Password Strength Meter</h1>", unsafe_allow_html=True)

password = st.text_input("Enter your password:", type="password")

if password:
    score, feedback = evaluate_password_strength(password)
    strength_color, strength_label = get_strength_color(score)
    
    bar_width = (score + 1) * 20
    st.markdown(
        f"""
        <div class="password-bar" style="background: linear-gradient(to right, {strength_color}, white); height: 20px; width:{bar_width}%;"></div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(f"<h4 style='color:{strength_color}'>Strength: {strength_label}</h4>", unsafe_allow_html=True)
    
    if feedback:
        st.markdown("### Suggestions to improve your password:")
        for suggestion in feedback:
            st.markdown(f"- {suggestion}")

# Instructions
st.markdown("""
### 📋 Password Guidelines:
- At least 8 characters  
- Include **Uppercase**, **Lowercase**, **Numbers**, and **Special Characters**
""")

# Footer branding
st.markdown("<div class='footer'>Created by <b>Ubaid Raza</b></div>", unsafe_allow_html=True)
