import streamlit as st
import requests
import json

# Your Bytez API configuration
API_KEY = "b9789078ba3b4414cc4e24295ac921d7"
API_URL = "https://api.bytez.com/chat/completions"  # Corrected endpoint

def get_baby_names(country, gender):
    """Get baby names using Qwen3-4B via Bytez API"""
    prompt = f"Generate exactly 15 {gender} baby names from {country}. Return only the names separated by commas, no numbers, no explanations, no additional text."
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "Qwen/Qwen3-4B-Instruct-2507",  # Model specified in the request body
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        
        # Print debug info
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code != 200:
            return f"API Error: {response.status_code} - {response.text}"
        
        result = response.json()
        print(f"Full Response: {result}")
        
        # Extract the content from the response
        if 'choices' in result and len(result['choices']) > 0:
            names = result['choices'][0]['message']['content'].strip()
            return names
        else:
            return "Error: Unexpected response format"
            
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("🌍 Baby Name Generator - Qwen3-4B")
st.write("Discover beautiful baby names from around the world using Bytez API!")

# Input fields
country = st.text_input("Enter country:")
gender = st.selectbox("Select gender:", ["boy", "girl"])

if st.button("Generate Names"):
    if country and gender:
        with st.spinner("Finding beautiful names..."):
            names = get_baby_names(country, gender)
        
        if not names.startswith("Error") and not names.startswith("API Error"):
            st.success("Here are 15 names:")
            
            # Clean up the response
            import re
            cleaned_names = re.sub(r'\d+\.', '', names)  # Remove numbers like "1."
            cleaned_names = re.sub(r'[-•]', '', cleaned_names)  # Remove bullets
            cleaned_names = ' '.join(cleaned_names.split())  # Remove extra whitespace
            
            st.text_area("Generated Names:", cleaned_names, height=150)
        else:
            st.error(names)
            
        # Show debug info
        with st.expander("Debug Info"):
            st.write("Response:", names)
    else:
        st.warning("Please enter both country and gender!")
