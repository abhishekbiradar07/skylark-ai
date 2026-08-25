# Skylark frontend

This is a dependency-free, two-page frontend for the Skylark BI backend.

1. Start the backend from the `backend` directory: `python main.py`.
2. Open `frontend/index.html` in a browser, or serve the `frontend` directory through any static server.
3. The UI expects the API at `http://localhost:8000`. Use the settings button in the chat page to change it if required.

The landing page is available at the root. Click **Start asking questions** to open the ChatGPT-style workspace. The workspace calls `/api/chat`, surfaces sources and data-quality notes returned by the backend, and includes a Monday.com refresh control.
