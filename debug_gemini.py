
import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

try:
    import google.generativeai as genai
    print("SUCCESS: google.generativeai imported")
except ImportError as e:
    print(f"ERROR: Import failed: {e}")
    sys.exit(1)

api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("ERROR: No API Key found in env")
    sys.exit(1)

print(f"API Key found (starts with: {api_key[:5]}...)")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    print("Model initialized. Sending prompt...")
    
    response = model.generate_content("Hello, this is a test. Reply with 'OK'.")
    print(f"Response: {response.text}")
    print("SUCCESS: API is working")
except Exception as e:
    print(f"ERROR: API Call failed: {e}")
