from datetime import datetime, timedelta
from database import db

async def get_analytics_data():
    # Get data for last 30 days
    start_date = datetime.utcnow() - timedelta(days=30)

    # Basic stats (no await needed for count_documents)
    total_users = db.users.count_documents({})
    total_messages = db.chat_history.count_documents({})

    # Sentiment distribution
    sentiment_pipeline = [
        {'$match': {'timestamp': {'$gte': start_date}}},
        {'$group': {'_id': '$sentiment.label', 'count': {'$sum': 1}}}
    ]

    # Check if using Motor (async driver)
    if hasattr(db.chat_history, 'aggregate'):  
        sentiment_dist = list(db.chat_history.aggregate(sentiment_pipeline))
    else:  
        sentiment_dist = list(db.chat_history.aggregate(sentiment_pipeline))  # PyMongo fallback

    # Daily message counts
    daily_messages_pipeline = [
        {'$match': {'timestamp': {'$gte': start_date}}},
        {
            '$group': {
                '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$timestamp'}},
                'count': {'$sum': 1}
            }
        },
        {'$sort': {'_id': 1}}
    ]

    if hasattr(db.chat_history, 'aggregate'):
        daily_messages = list(db.chat_history.aggregate(daily_messages_pipeline))
    else:
        daily_messages = list(db.chat_history.aggregate(daily_messages_pipeline))  # PyMongo fallback

    return {
        'total_users': total_users,
        'total_messages': total_messages,
        'sentiment_distribution': sentiment_dist,
        'daily_messages': daily_messages
    }
