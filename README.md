# AI Telegram Bot with Analytics Dashboard

An intelligent Telegram bot powered by Google's Gemini API, featuring a full-stack analytics dashboard that provides insights into user interactions, sentiment analysis, and usage metrics. The bot's conversations are stored in MongoDB, and the analytics are visualized through an interactive web interface.

## Features

### Bot Features
- 🤖 AI-powered conversations using Gemini API
- 💬 Natural language processing capabilities
- 📊 Conversation history tracking
- 🎯 Sentiment analysis of messages
- 🔄 Real-time response generation
- 💾 MongoDB integration for data persistence

### Analytics Dashboard Features
- 📈 User engagement metrics
- 🔍 Sentiment distribution visualization
- 📊 Message volume trends
- 👥 User growth tracking
- 🔄 Auto-refreshing data
- 📱 Responsive design

## Tech Stack

### Bot Backend
- Python Telegram Bot API
- Google Gemini API
- MongoDB
- Python 3.x
- asyncio

### Analytics Backend
- Flask
- Flask-CORS
- MongoDB connectivity
- Uvicorn
- Async support

### Frontend Dashboard
- React 18
- TypeScript
- Vite
- Tailwind CSS
- Recharts for data visualization
- shadcn/ui components

## Prerequisites

- Python 3.8 or higher
- Node.js (v16 or higher)
- MongoDB instance
- Telegram Bot Token
- Google Gemini API Key
- npm or yarn

## Installation

1. Clone the repository
```bash
git clone [https://github.com/nightfury7653]
cd [Telegram-AI-Chatbo]
```

2. Setup Bot Backend
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. Setup Analytics Dashboard Frontend
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

4. Environment Configuration

Create a `.env` file in the root directory:
```
# Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
MONGODB_URI=your_mongodb_connection_string

# Analytics API Configuration
FLASK_APP=app.py
FLASK_ENV=development
```

Create a `.env` file in the frontend directory:
```
VITE_API_URL=http://localhost:5000/api
```

## Running the Application

1. Start the Telegram Bot
```bash
# From the root directory
python bot.py
```

2. Start the Analytics Backend Server
```bash
# From the root directory
python app.py
```

3. Start the Frontend Development Server
```bash
# From the frontend directory
npm run dev
```

## Project Structure

```
telegram-bot/
├── backend/
│   ├── api.py
│   ├── analytics_service.py
│   ├── database.py
│   ├── gemini_service.py
│   ├── main.py
│   ├── sentiment_service.py
│   ├── web_search.py
│   ├── config.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.ts
│   └── .env
└── README.md
```

## Bot Commands

- `/start` - Start the bot and get welcome message
- `/help` - Display available commands
- (Add other bot commands here)

## API Endpoints

### GET /api/analytics
Returns analytics data including:
- Total users count
- Total messages count
- Sentiment distribution
- Daily message trends

### GET /api/health
Health check endpoint

## MongoDB Schema

### Conversations Collection
```javascript
{
  user_id: String,
  message: String,
  timestamp: DateTime,
  sentiment: String,
  response: String
}
```

### Users Collection
```javascript
{
  user_id: String,
  username: String,
  first_interaction: DateTime,
  last_interaction: DateTime
}
```

## Development

### Bot Development
- Implements Telegram Bot API for message handling
- Uses Gemini API for generating responses
- Stores conversations in MongoDB
- Includes sentiment analysis of messages

### Analytics Development
- Processes MongoDB data for insights
- Generates real-time analytics
- Implements caching for performance
- Features comprehensive error handling

## Error Handling

The application implements comprehensive error handling for:
- Telegram API rate limits
- Gemini API connectivity
- MongoDB operations
- Analytics data processing
- Dashboard connectivity

## Future Improvements

- Add user preference settings
- Implement conversation context management
- Add more advanced analytics metrics
- Support multiple language analysis
- Add user feedback collection
- Implement conversation export functionality
- Add administrative controls

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Contact

Your Name - [gauravayu7@gmail.com]
Project Link: [https://github.com/nightfury7653/Telegram-AI-Chatbot]

## Acknowledgments

- Google Gemini API Documentation
- Python Telegram Bot Library
- MongoDB Documentation
- React and Vite communities
