import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="b9789078ba3b4414cc4e24295ac921d7")  # Replace with your actual API key

def get_baby_names(country, gender):
    """Get baby names using Gemini 2.5 Pro"""
    prompt = f"Generate 15 {gender} baby names from {country}. Only list names, no additional text or explanations."
    
    try:
        model = genai.GenerativeModel("gemini-2.5-pro-preview-03-25")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("🌍 Baby Name Generator")
st.write("Discover beautiful baby names from around the world!")

# Input fields
country = st.text_input("Enter country:")
gender = st.selectbox("Select gender:", ["boy", "girl"])

if st.button("Generate Names"):
    if country and gender:
        with st.spinner("Finding beautiful names..."):
            names = get_baby_names(country, gender)
        st.success("Here are 15 names:")
        st.text_area("Names:", names, height=200)
    else:
        st.warning("Please enter both country and gender!")
