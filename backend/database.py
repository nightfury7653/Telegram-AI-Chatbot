# database.py
from pymongo import MongoClient
from datetime import datetime
from config import MONGODB_URI
from sentiment_service import analyze_sentiment

client = MongoClient(MONGODB_URI)
db = client.telegram_bot

async def save_user(user_data):
    db.users.update_one(
        {'chat_id': user_data['chat_id']},
        {'$set': user_data},
        upsert=True
    )

# In database.py, update save_chat_history
async def save_chat_history(chat_id, user_input, bot_response):
    sentiment = analyze_sentiment(user_input)
    db.chat_history.insert_one({
        'chat_id': chat_id,
        'user_input': user_input,
        'bot_response': bot_response,
        'sentiment': sentiment,
        'timestamp': datetime.utcnow()
    })

async def get_user_stats(chat_id):
    return await db.chat_history.count_documents({'chat_id': chat_id})

async def save_file_metadata(chat_id, file_data):
    db.files.insert_one({
        'chat_id': chat_id,
        'file_name': file_data['file_name'],
        'description': file_data['description'],
        'timestamp': datetime.utcnow()
    })
