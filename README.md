# Skylark Business Intelligence Agent

AI-powered business intelligence from Monday.com with ChatGPT-like interface and Databricks theming.

## Features

- 🤖 **AI Agent Chat** - Natural language queries about your business data
- 📊 **Analytics Dashboard** - Interactive charts for pipeline, operations, and billing
- 🎨 **Databricks Theme** - Modern dark UI with orange/red gradients
- 🔄 **Real-time Data** - Direct Monday.com integration with caching
- 📈 **Smart Metrics** - Automated calculations across deals and work orders

## Tech Stack

### Backend
- FastAPI (Python)
- Groq LLM (fast inference)
- Monday.com GraphQL API
- Pydantic data models

### Frontend
- React 18 + Vite
- Recharts for data visualization
- React Markdown for chat rendering
- Axios for API calls

## Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables
# Edit backend/.env and add your API keys:
# - MONDAY_API_TOKEN
# - GROQ_API_KEY

# Start backend server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Backend runs on: http://localhost:8000

### 2. Frontend Setup

```bash
cd frontend

# Install Node dependencies
npm install

# Start development server
npm run dev
```

Frontend runs on: http://localhost:5173

## Configuration

### Backend Environment Variables (.env)

```env
# Monday.com Configuration
MONDAY_API_TOKEN=your_monday_api_token_here
MONDAY_DEALS_BOARD_ID=5030842785
MONDAY_WORK_ORDERS_BOARD_ID=5030843474

# Groq LLM Configuration
GROQ_API_KEY=your_groq_api_key_here

# Server Configuration
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:5173

# Cache Configuration
CACHE_DURATION_MINUTES=5
```

### Getting API Keys

1. **Monday.com API Token**: 
   - Go to Monday.com → Profile → Admin → API
   - Generate a Personal API Token

2. **Groq API Key**:
   - Visit https://console.groq.com
   - Sign up and generate an API key

## API Endpoints

- `GET /api/health` - Health check and configuration status
- `POST /api/refresh` - Refresh data from Monday.com
- `GET /api/data/deals` - Get deals summary
- `GET /api/data/work-orders` - Get work orders summary
- `GET /api/data-quality` - Data quality report
- `POST /api/chat` - Chat with AI agent

## Usage

### Home Page
- View business statistics
- Quick action buttons for common queries
- Data quality metrics

### Agent Chat
- Ask natural language questions:
  - "What's our pipeline summary?"
  - "Show me top 10 deals by value"
  - "Compare pipeline and execution by sector"
  - "What's the billing status?"

### Analytics Dashboard
- Pipeline by Sector (Bar Chart)
- Operations by Sector (Bar Chart)
- Billing Overview (Pie Chart)
- Sector Health Matrix (Multi-Bar Chart)

## Project Structure

```
.
├── backend/
│   ├── agent/              # AI agent logic
│   │   ├── prompts.py      # LLM prompts
│   │   ├── reasoning.py    # Groq integration
│   │   └── router.py       # Query routing
│   ├── analytics/          # Business metrics
│   │   ├── metrics.py      # Calculations
│   │   └── cross_board.py  # Cross-board analytics
│   ├── data/               # Data layer
│   │   ├── models.py       # Pydantic models
│   │   ├── normalizer.py   # Data normalization
│   │   ├── validator.py    # Data validation
│   │   ├── quality.py      # Quality analysis
│   │   └── cache.py        # In-memory cache
│   ├── monday/             # Monday.com integration
│   │   ├── client.py       # GraphQL client
│   │   ├── queries.py      # GraphQL queries
│   │   └── service.py      # Data transformation
│   ├── main.py             # FastAPI app
│   └── config.py           # Configuration
│
└── frontend/
    ├── src/
    │   ├── components/     # React components
    │   │   └── Sidebar.jsx
    │   ├── pages/          # Page components
    │   │   ├── HomePage.jsx
    │   │   ├── ChatPage.jsx
    │   │   └── AnalyticsPage.jsx
    │   ├── api.js          # API client
    │   ├── App.jsx         # Main app
    │   ├── App.css         # Styles
    │   └── main.jsx        # Entry point
    ├── index.html
    ├── package.json
    └── vite.config.js

```

## Development

### Backend Development
```bash
cd backend
python -m uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Build for Production
```bash
cd frontend
npm run build
```

## Troubleshooting

### Backend Issues
- Verify API keys in `.env`
- Check Python dependencies: `pip install -r requirements.txt`
- Ensure Monday.com board IDs are correct

### Frontend Issues
- Clear node_modules: `rm -rf node_modules && npm install`
- Check backend is running on port 8000
- Verify API base URL in `src/api.js`

### CORS Issues
- Backend allows origins: `http://localhost:5173`, `http://localhost:3000`
- Check `main.py` CORS middleware configuration

## License

MIT
