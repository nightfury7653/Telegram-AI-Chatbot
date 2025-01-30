import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
vision_model = genai.GenerativeModel('gemini-pro-vision')

async def get_chat_response(prompt):
    response = model.generate_content(prompt)
    return response.text

async def analyze_image(image_data):
    response = vision_model.generate_content([image_data])
    return response.text