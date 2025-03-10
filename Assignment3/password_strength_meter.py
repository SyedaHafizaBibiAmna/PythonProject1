import re
import streamlit as st
import random
import string

def main():
    # Set page config must be the first Streamlit command
    st.set_page_config(page_title="✨ Password Strength Meter", page_icon="💝")
    
    # Custom CSS for girly theme
    st.markdown("""
        <style>
        .main {
            background-color: #fff5f7;
        }
        .stButton>button {
            background-color: #ff69b4;
            color: white;
            border-radius: 20px;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #ff1493;
        }
        .stTextInput>div>div>input {
            border-radius: 20px;
            border: 2px solid #ffb6c1;
        }
        .stProgress .st-bo {
            background-color: #ffb6c1;
        }
        .stProgress .st-br {
            background-color: #ff69b4;
        }
        .stMarkdown {
            color: #4a4a4a;
        }
        h1 {
            color: #ff69b4;
            font-family: 'Comic Sans MS', cursive;
        }
        .stExpander {
            background-color: white;
            border-radius: 20px;
            border: 2px solid #ffb6c1;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title and description with decorative elements
    st.markdown("""
        <div style='text-align: center;'>
            <h1>✨ Password Strength Meter ✨</h1>
            <p style='color: #ff69b4; font-size: 18px;'>Create and check your passwords with style! 💖</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background-color: white; padding: 20px; border-radius: 20px; border: 2px solid #ffb6c1;'>
            <p style='color: #4a4a4a;'>This tool helps you evaluate and generate strong passwords. Enter your password below or generate a secure one automatically. 💕</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Password requirements with cute styling
    with st.expander("💝 Password Requirements"):
        st.markdown("""
            <div style='background-color: #fff5f7; padding: 15px; border-radius: 15px;'>
                <p style='color: #ff69b4; font-weight: bold;'>A strong password should have:</p>
                <ul style='color: #4a4a4a;'>
                    <li>🌸 Minimum 8 characters long</li>
                    <li>🌸 Contains uppercase and lowercase letters</li>
                    <li>🌸 Includes at least one number (0-9)</li>
                    <li>🌸 Contains at least one special character (!@#$%^&*)</li>
                    <li>🌸 Longer passwords (12+) get bonus points</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    # Create two columns for input and generate button
    col1, col2 = st.columns([3, 1])
    
    with col1:
        password = st.text_input("✨ Enter Password:", type="password")
    
    with col2:
        if st.button("💝 Generate Password"):
            password = generate_password()
            st.text_input("✨ Enter Password:", value=password, type="password")
    
    # Check password button
    if st.button("🌸 Check Strength"):
        if not password:
            st.warning("💝 Please enter a password first!")
        else:
            score, feedback = check_password_strength(password)
            
            # Display score with color-coded progress bar
            st.markdown("### 💖 Password Score")
            st.progress(score/5)
            st.markdown(f"**Score: {score}/5**")
            
            # Display strength rating with cute styling
            if score == 5:
                st.success("✨ Strong Password! Your password meets all security criteria. 💖")
                st.info("🌟 You're doing great! Keep up the good work! 💝")
            elif score >= 3:
                st.warning("💝 Moderate Password")
                st.markdown("**Suggestions for improvement:**")
                for msg in feedback:
                    st.markdown(msg)
            else:
                st.error("🌸 Weak Password")
                st.markdown("**Please improve your password:**")
                for msg in feedback:
                    st.markdown(msg)
    
    # Footer with cute styling
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center;'>
            <p style='color: #ff69b4;'>Made By Amna Shah💖 </p>
        </div>
    """, unsafe_allow_html=True)

def check_password_strength(password):
    score = 0
    feedback = []
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("🌸 Password should be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("🌸 Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("🌸 Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("🌸 Include at least one special character (!@#$%^&*).")
    
    # Additional Security Checks
    if len(password) >= 12:
        score += 1
    if re.search(r"(.)\1{2,}", password):
        feedback.append("💝 Avoid repeating characters more than twice in a row.")
    
    return score, feedback

def generate_password():
    # Generate a strong password
    length = random.randint(12, 16)
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(characters) for _ in range(length))
    
    # Ensure the password meets all criteria
    while not (re.search(r"[A-Z]", password) and 
              re.search(r"[a-z]", password) and 
              re.search(r"\d", password) and 
              re.search(r"[!@#$%^&*]", password)):
        password = ''.join(random.choice(characters) for _ in range(length))
    
    return password

if __name__ == "__main__":
    main() 