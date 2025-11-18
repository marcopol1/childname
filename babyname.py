import streamlit as st
import requests
import json

# Your Bytez API configuration
API_KEY = "b9789078ba3b4414cc4e24295ac921d7"
BASE_URL = "https://api.bytez.com"

def get_baby_names(country, gender):
    """Get baby names using Qwen3-4B via Bytez API"""
    prompt = f"Generate exactly 15 {gender} baby names from {country}. Only names, no explanations."
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
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
        # Using the model endpoint as shown in your JS example
        response = requests.post(
            f"{BASE_URL}/models/Qwen/Qwen3-4B-Instruct-2507/chat/completions",
            headers=headers,
            json=data
        )
        
        # Print response for debugging
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        
        response.raise_for_status()
        result = response.json()
        
        # Extract content based on Bytez response format
        if 'choices' in result and result['choices']:
            message = result['choices'][0].get('message', {})
            names = message.get('content', '').strip()
            return names
        else:
            return "Error: No choices in response"
            
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("🌍 Baby Name Generator")
st.write("Get baby names using Qwen3-4B via Bytez API")

country = st.text_input("Enter country (e.g., India, France, Japan):")
gender = st.selectbox("Select gender:", ["boy", "girl"])

if st.button("Generate 15 Names"):
    if country.strip():
        with st.spinner(f"Generating {gender} names from {country}..."):
            result = get_baby_names(country, gender)
        
        if result and not result.startswith("Error"):
            st.success(f"15 {gender} names from {country}:")
            st.text_area("Names:", result, height=200)
        else:
            st.error(f"Failed to generate names: {result}")
    else:
        st.warning("Please enter a country name!")
