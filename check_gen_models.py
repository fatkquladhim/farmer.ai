import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("GOOGLE_API_KEY not found in .env")
else:
    genai.configure(api_key=api_key)
    print("Listing available generation models...")
    try:
        found = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Generation Model: {m.name}")
                if "gemini-1.5-flash" in m.name:
                    found = True
        
        if not found:
            print("\nWARNING: 'gemini-1.5-flash' not found! We might need to change the model in agent.py.")
        else:
            print("\nSUCCESS: 'gemini-1.5-flash' is available.")
            
    except Exception as e:
        print(f"Error listing models: {e}")
