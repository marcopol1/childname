import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Initialize the model and tokenizer
@st.cache_resource
def load_model():
    model_name = "Qwen/Qwen3-4B-Instruct-2507"
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,  # Use float16 to save memory
            device_map="auto",
            trust_remote_code=True
        )
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None

def get_baby_names(country, gender, tokenizer, model):
    """Get baby names using Qwen3-4B-Instruct-2507"""
    prompt = f"Generate 15 {gender} baby names from {country}. Only list names, no additional text or explanations."
    
    messages = [{"role": "user", "content": prompt}]
    
    try:
        # Apply chat template
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
        
        # Generate with optimized parameters for Qwen3-4B-Instruct-2507
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=512,
            temperature=0.7,      # Recommended setting [citation:3][citation:8]
            top_p=0.8,            # Recommended setting [citation:3][citation:8]
            top_k=20,             # Recommended setting [citation:3]
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
        
        # Extract only the new tokens
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
        content = tokenizer.decode(output_ids, skip_special_tokens=True)
        
        return content
    except Exception as e:
        return f"Error generating names: {str(e)}"

# Streamlit UI
st.title("🌍 Baby Name Generator - Qwen3-4B")
st.write("Discover beautiful baby names from around the world using Qwen3-4B-Instruct-2507!")

# Load model
with st.spinner("Loading Qwen3-4B model... This may take a while."):
    tokenizer, model = load_model()

if tokenizer is None or model is None:
    st.error("Failed to load the model. Please check the error message above.")
else:
    st.success("Model loaded successfully!")
    
    # Input fields
    country = st.text_input("Enter country:")
    gender = st.selectbox("Select gender:", ["boy", "girl"])

    if st.button("Generate Names"):
        if country and gender:
            with st.spinner("Finding beautiful names..."):
                names = get_baby_names(country, gender, tokenizer, model)
            st.success("Here are your names:")
            st.text_area("Names:", names, height=200)
        else:
            st.warning("Please enter both country and gender!")
