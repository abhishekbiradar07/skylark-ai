# Deployment Guide

This guide will help you deploy Skylark BI Agent with backend on Render and frontend on Vercel.

## Prerequisites

- GitHub account (already done ✅)
- Render account: https://render.com (free tier available)
- Vercel account: https://vercel.com (free tier available)
- Your API keys ready (Monday.com and Groq)

---

## Part 1: Deploy Backend to Render

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### Step 2: Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `abhishekbiradar07/skylark-ai`
3. Render will detect the `render.yaml` file

### Step 3: Configure Service
- **Name**: `skylark-backend` (or your choice)
- **Region**: Oregon (or closest to you)
- **Branch**: `main`
- **Root Directory**: Leave empty (renders from root)
- **Runtime**: Python 3
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 4: Add Environment Variables
Click **"Environment"** and add these variables:

```
MONDAY_API_TOKEN=your_monday_token_here
MONDAY_DEALS_BOARD_ID=5030845871
MONDAY_WORK_ORDERS_BOARD_ID=5030845875
GROQ_API_KEY=your_groq_key_here
FRONTEND_URL=https://your-app.vercel.app
CACHE_DURATION_MINUTES=5
```

### Step 5: Deploy
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for the build to complete
3. Your backend URL will be: `https://skylark-backend.onrender.com`
4. Test it: `https://skylark-backend.onrender.com/api/health`

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Create Vercel Account
1. Go to https://vercel.com
2. Sign up with your GitHub account
3. Authorize Vercel to access your repositories

### Step 2: Import Project
1. Click **"Add New..."** → **"Project"**
2. Import `abhishekbiradar07/skylark-ai`
3. Vercel will auto-detect it's a Vite project

### Step 3: Configure Project
- **Framework Preset**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### Step 4: Add Environment Variable
Click **"Environment Variables"** and add:

```
VITE_API_URL=https://skylark-backend.onrender.com/api
```

**Important**: Replace `skylark-backend` with your actual Render service name!

### Step 5: Deploy
1. Click **"Deploy"**
2. Wait 2-3 minutes for build
3. Your frontend URL will be: `https://skylark-ai-xxx.vercel.app`

### Step 6: Update Backend CORS
Go back to Render and update the `FRONTEND_URL` environment variable:
```
FRONTEND_URL=https://skylark-ai-xxx.vercel.app
```

Replace with your actual Vercel URL, then click **"Save Changes"**. Render will automatically redeploy.

---

## Part 3: Verify Deployment

### Test Backend
```bash
curl https://skylark-backend.onrender.com/api/health
```

Should return:
```json
{
  "status": "healthy",
  "llm_provider": "Groq",
  "monday_configured": true,
  "groq_configured": true
}
```

### Test Frontend
1. Open your Vercel URL: `https://skylark-ai-xxx.vercel.app`
2. You should see the dashboard
3. Click "Sync Data" to load data from Monday.com
4. Navigate to "AI Assistant" and ask a question

---

## Troubleshooting

### Backend Issues

**Problem**: "Application failed to start"
- Check Render logs: Dashboard → Your Service → Logs
- Verify all environment variables are set
- Check Python version is 3.12

**Problem**: "502 Bad Gateway"
- Backend is still starting (wait 2-3 minutes on free tier)
- Check if all dependencies installed correctly

**Problem**: "401 Unauthorized from Monday.com"
- Verify `MONDAY_API_TOKEN` is correct
- Regenerate token if expired

### Frontend Issues

**Problem**: "Failed to load stats"
- Check browser console for errors
- Verify `VITE_API_URL` points to your Render backend
- Check CORS: Make sure `FRONTEND_URL` in Render matches your Vercel URL

**Problem**: "Cannot connect to backend"
- Open browser DevTools → Network tab
- Check if API calls are going to the correct URL
- Verify Render backend is running

### CORS Issues

If you see CORS errors:
1. Go to Render Dashboard
2. Update `FRONTEND_URL` environment variable to your Vercel URL
3. Add `https://` prefix
4. Save changes (Render will redeploy)

---

## Post-Deployment

### Custom Domain (Optional)

**Vercel**:
1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

**Render**:
1. Go to Service Settings → Custom Domain
2. Add your domain
3. Update DNS records

### Monitoring

**Render**:
- Free tier: Service sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- Upgrade to paid tier for 24/7 uptime

**Vercel**:
- Always active
- Check Analytics in dashboard
- Monitor bandwidth usage

### Updates

To update your deployment:
1. Push changes to GitHub main branch
2. Render: Auto-deploys on push
3. Vercel: Auto-deploys on push

Or redeploy manually from dashboards.

---

## URLs Reference

After deployment, save these URLs:

- **Frontend**: `https://your-app.vercel.app`
- **Backend API**: `https://your-service.onrender.com/api`
- **API Docs**: `https://your-service.onrender.com/docs`
- **GitHub**: `https://github.com/abhishekbiradar07/skylark-ai`

---

## Cost

- **Render Free Tier**: 
  - 750 hours/month
  - Spins down after 15 min inactivity
  - 512 MB RAM
  
- **Vercel Free Tier**:
  - 100 GB bandwidth/month
  - Unlimited deployments
  - Always active

Both are FREE for this project! 🎉

---

## Support

If you encounter issues:
1. Check Render logs
2. Check Vercel deployment logs
3. Check browser console
4. Verify all environment variables

The deployment should take about 15-20 minutes total.
