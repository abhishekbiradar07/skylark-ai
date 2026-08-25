# Setup Instructions - Skylark BI Agent

## Prerequisites
- Python 3.12+
- Node.js 18+
- Monday.com account with API access
- Groq API account

## Step 1: Configure Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Open the `.env` file and add your API credentials:
```env
# Monday.com Configuration
MONDAY_API_TOKEN=your_actual_monday_token_here
MONDAY_DEALS_BOARD_ID=5030842785
MONDAY_WORK_ORDERS_BOARD_ID=5030843474

# Groq LLM Configuration  
GROQ_API_KEY=your_actual_groq_key_here

# Server Configuration (keep as is)
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:5173

# Cache Configuration (keep as is)
CACHE_DURATION_MINUTES=5
```

### Getting Your API Keys:

**Monday.com API Token:**
1. Log into your Monday.com account
2. Click your profile picture (bottom left)
3. Go to "Admin" → "API"
4. Click "Generate" or "Copy" your API token
5. Paste it in the `.env` file as `MONDAY_API_TOKEN`

**Groq API Key:**
1. Visit https://console.groq.com
2. Sign up or log in
3. Navigate to API Keys section
4. Click "Create API Key"
5. Copy the key and paste it in `.env` as `GROQ_API_KEY`

## Step 2: Install Dependencies

### Backend Dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### Frontend Dependencies:
```bash
cd frontend
npm install
```

## Step 3: Start the Servers

### Option A: Manual Start (Recommended for first time)

**Terminal 1 - Start Backend:**
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm run dev
```

### Option B: Using Batch File (Windows)
```bash
start.bat
```

## Step 4: Access the Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## Step 5: Test the Connection

1. Open http://localhost:5173 in your browser
2. The home page should load with statistics from your Monday.com boards
3. Click "Refresh Data" in the sidebar to fetch latest data
4. Navigate to "Agent Chat" and ask: "What's our pipeline summary?"

## Troubleshooting

### Issue: Backend shows 401 Unauthorized
**Solution:** Check your `MONDAY_API_TOKEN` in `.env` file
- Make sure there are no extra spaces
- Verify the token is still valid in Monday.com
- Regenerate a new token if needed

### Issue: Backend shows no data
**Solution:** Verify your board IDs
- Check that `MONDAY_DEALS_BOARD_ID` and `MONDAY_WORK_ORDERS_BOARD_ID` are correct
- You can find board IDs in the URL when viewing a board: `https://your-workspace.monday.com/boards/{BOARD_ID}`

### Issue: Chat not working
**Solution:** Check Groq API key
- Verify `GROQ_API_KEY` is correctly set in `.env`
- Check you have API credits at https://console.groq.com

### Issue: Frontend can't connect to backend
**Solution:** 
- Make sure backend is running on port 8000
- Check backend terminal for errors
- Try accessing http://localhost:8000/api/health directly

### Issue: Port already in use
**Solution:**
- Backend: Change `BACKEND_PORT` in `.env` and update `frontend/src/api.js`
- Frontend: Change port in `frontend/vite.config.js`

## Verifying Everything Works

### 1. Check Backend Health:
```bash
curl http://localhost:8000/api/health
```

Should return:
```json
{
  "status": "healthy",
  "llm_provider": "Groq",
  "monday_configured": true,
  "groq_configured": true,
  "cache_info": {...}
}
```

### 2. Test Data Endpoints:
```bash
curl http://localhost:8000/api/data/deals
curl http://localhost:8000/api/data/work-orders
```

### 3. Test Chat:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is our pipeline summary?"}'
```

## Next Steps

Once everything is running:

1. **Home Page** - View your business statistics at a glance
2. **Agent Chat** - Ask questions about your data in natural language
3. **Analytics** - View interactive charts and dashboards
4. **Refresh Data** - Click the refresh button to sync latest data from Monday.com

## Common Questions

**Q: How often does data refresh?**
A: Data is cached for 5 minutes (configurable in `.env`). Click "Refresh Data" to force update.

**Q: Can I use a different LLM provider?**
A: Currently only Groq is supported for fast inference. OpenAI support can be added if needed.

**Q: Is my data secure?**
A: Yes, all data stays between your Monday.com account and your local server. No data is stored permanently.

**Q: Can I customize the board mappings?**
A: Yes, edit `backend/monday/service.py` to adjust field mappings for your board structure.

## Support

If you encounter issues:
1. Check backend terminal logs for detailed error messages
2. Check frontend browser console for errors
3. Verify all `.env` values are correct
4. Ensure Python and Node.js versions meet requirements

---

**Ready to use Skylark BI Agent!** 🚀
