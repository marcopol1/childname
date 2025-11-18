import streamlit as st
import requests
import json

# Your Bytez API configuration
API_KEY = "b9789078ba3b4414cc4e24295ac921d7"

def get_baby_names(country, gender):
    """Get baby names using Bytez API with exact JS SDK format"""
    
    # Based on your JavaScript example structure
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Try the exact format from Bytez documentation
    data = {
        "model": "Qwen/Qwen3-4B-Instruct-2507",
        "messages": [
            {
                "role": "user", 
                "content": f"Generate exactly 15 {gender} baby names from {country}. Only names separated by commas, no explanations."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }
    
    # Try different possible endpoints
    endpoints = [
        "https://api.bytez.com/chat/completions",
        "https://api.bytez.com/v1/chat/completions",
        "https://api.bytez.com/models/run"
    ]
    
    for endpoint in endpoints:
        try:
            st.info(f"Trying endpoint: {endpoint}")
            response = requests.post(endpoint, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result:
                    names = result['choices'][0]['message']['content'].strip()
                    return names
            else:
                st.write(f"Endpoint {endpoint} failed: {response.status_code}")
                continue
                
        except Exception as e:
            st.write(f"Endpoint {endpoint} error: {str(e)}")
            continue
    
    return "Error: All endpoints failed. Please check the API documentation."

# Streamlit UI
st.title("🌍 Baby Name Generator")
st.write("Using Bytez API with Qwen3-4B-Instruct-2507")

country = st.text_input("Enter country:")
gender = st.selectbox("Select gender:", ["boy", "girl"])

if st.button("Generate 15 Names"):
    if country and gender:
        result = get_baby_names(country, gender)
        
        if not result.startswith("Error"):
            st.success(f"15 {gender} names from {country}:")
            st.text_area("Names:", result, height=200)
        else:
            st.error(result)
    else:
        st.warning("Please enter both country and gender!")
