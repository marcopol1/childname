import streamlit as st
import requests
import json
import os

# Better approach - set API key as environment variable or use secrets
# For local testing, you can set: export QWEN_API_KEY="your_key_here"
API_KEY = os.getenv('QWEN_API_KEY', 'b9789078ba3b4414cc4e24295ac921d7')
API_URL = "https://api.openrouter.ai/api/v1/chat/completions"

def get_baby_names(country, gender):
    """Get baby names using Qwen3-4B via API"""
    prompt = f"Generate exactly 15 {gender} baby names from {country}. Return only the names separated by commas, no numbers, no explanations, no additional text."
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site.com",  # Required by OpenRouter
        "X-Title": "Baby Name Generator"  # Required by OpenRouter
    }
    
    data = {
        "model": "qwen/qwen-3-4b-instruct-2507",
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
        response.raise_for_status()
        
        result = response.json()
        names = result['choices'][0]['message']['content'].strip()
        return names
    except requests.exceptions.RequestException as e:
        return f"API Error: {str(e)}"
    except KeyError:
        return "Error: Unexpected response format from API"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Streamlit UI
st.title("🌍 Baby Name Generator - Qwen3-4B")
st.write("Discover beautiful baby names from around the world!")

country = st.text_input("Enter country:")
gender = st.selectbox("Select gender:", ["boy", "girl"])

if st.button("Generate Names"):
    if country and gender:
        with st.spinner("Finding beautiful names..."):
            names = get_baby_names(country, gender)
        
        if not names.startswith("Error"):
            st.success("Here are 15 names:")
            # Clean the response
            cleaned_names = ' '.join(names.split())  # Remove extra whitespace
            st.text_area("Names:", cleaned_names, height=150)
            
            # Show raw response for debugging
            with st.expander("Debug - Raw Response"):
                st.write(names)
        else:
            st.error(names)
    else:
        st.warning("Please enter both country and gender!")
