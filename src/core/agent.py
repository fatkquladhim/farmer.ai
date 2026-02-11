import os
import google.generativeai as genai
from glob import glob
from .rag import get_retriever
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Safety Settings
SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

def load_system_prompt():
    prompt_path = "prompts/system_prompt.md"
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    return "You are an expert Agronomist."

def get_rag_context(query):
    retriever = get_retriever()
    if retriever:
        try:
            docs = retriever.invoke(query)
            context = "\n".join([doc.page_content for doc in docs])
            return context
        except Exception as e:
            print(f"RAG Error: {e}")
            return ""
    return ""

def generate_response(user_input, image_data=None, weather_info=None):
    """
    Generates a response from the Agronomist Agent.
    """
    model = genai.GenerativeModel('gemini-flash-latest') # Using standard Flash for compatibility
    
    # 1. Retrieve Context (RAG)
    rag_context = get_rag_context(user_input)
    
    # 2. Build Prompt
    system_prompt = load_system_prompt()
    
    full_prompt = [system_prompt]
    
    # Add Context Section
    context_str = "\n\n### KONTEKS TAMBAHAN (Wajib Dipertimbangkan):"
    
    if weather_info:
        context_str += f"\n- Cuaca Saat Ini: {weather_info}"
    else:
        context_str += "\n- Data Cuaca: Tidak tersedia. Asumsikan cuaca rata-rata musim ini."
        
    if rag_context:
        context_str += f"\n- Referensi Manual Tani (Valid):\n{rag_context}"
    else:
        context_str += "\n- Referensi Manual Tani: Tidak ditemukan data spesifik."
        
    full_prompt.append(context_str)
    
    # Add User Input
    full_prompt.append(f"\n\n### PERTANYAAN PETANI:\n{user_input}")
    
    # 3. Generate Content
    inputs = full_prompt
    if image_data:
        inputs.append(image_data) # Image part
        
    try:
        response = model.generate_content(
            inputs,
            safety_settings=SAFETY_SETTINGS
        )
        return response.text
    except Exception as e:
        return f"Maaf, terjadi kesalahan saat menghubungi AI: {str(e)}"

def check_safety_disclaimer(response_text):
    """
    Checks if the response implies chemical usage and appends a safety disclaimer.
    """
    keywords = ["pestisida", "fungisida", "insektisida", "bahan kimia", "semprot", "racun", "dosis"]
    lower_text = response_text.lower()
    
    if any(keyword in lower_text for keyword in keywords):
        disclaimer = "\n\n⚠️ **PERINGATAN KEAMANAN PENTING:**\nJika menggunakan bahan kimia, WAJIB gunakan masker, sarung tangan, dan pakaian lengan panjang. Patuhi dosis yang tertera pada kemasan. Jangan menyemprot melawan arah angin watau saat cuaca panas terik."
        return response_text + disclaimer
    return response_text
