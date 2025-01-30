# analytics_service.py
from datetime import datetime, timedelta
from database import db

async def get_analytics_data():
    # Get data for last 30 days
    start_date = datetime.utcnow() - timedelta(days=30)
    
    # Basic stats
    total_users = await db.users.count_documents({})
    total_messages = await db.chat_history.count_documents({})
    
    # Sentiment distribution
    sentiment_pipeline = [
        {
            '$match': {'timestamp': {'$gte': start_date}}
        },
        {
            '$group': {
                '_id': '$sentiment.label',
                'count': {'$sum': 1}
            }
        }
    ]
    sentiment_dist = await db.chat_history.aggregate(sentiment_pipeline).to_list(None)
    
    # Daily message counts
    daily_messages_pipeline = [
        {
            '$match': {'timestamp': {'$gte': start_date}}
        },
        {
            '$group': {
                '_id': {
                    '$dateToString': {
                        'format': '%Y-%m-%d',
                        'date': '$timestamp'
                    }
                },
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {'_id': 1}
        }
    ]
    daily_messages = await db.chat_history.aggregate(daily_messages_pipeline).to_list(None)
    
    return {
        'total_users': total_users,
        'total_messages': total_messages,
        'sentiment_distribution': sentiment_dist,
        'daily_messages': daily_messages
    }