from flask import Flask, jsonify, make_response
from flask_cors import CORS
from analytics_service import get_analytics_data
import asyncio
from asgiref.wsgi import WsgiToAsgi
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
        "methods": ["GET", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/api/analytics')
async def analytics():
    try:
        logger.info("Received analytics request")
        data = await get_analytics_data()
        
        # Handle case where data is None
        if data is None:
            logger.error("No data returned from analytics service")
            return jsonify({'error': 'No data available'}), 404
            
        # Convert ObjectId to string if present
        for item in data.get('sentiment_distribution', []):
            if '_id' in item:
                item['_id'] = str(item['_id'])
        
        for item in data.get('daily_messages', []):
            if '_id' in item:
                item['_id'] = str(item['_id'])
        
        response = make_response(jsonify(data))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
        
    except Exception as e:
        logger.error(f"Error in analytics endpoint: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

def run_api():
    try:
        logger.info("Starting API server...")
        asgi_app = WsgiToAsgi(app)
        uvicorn.run(asgi_app, host='0.0.0.0', port=5000, log_level="info")
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}", exc_info=True)
        raise

if __name__ == '__main__':
    run_api()