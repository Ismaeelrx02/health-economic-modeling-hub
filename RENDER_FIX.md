# 🚨 RENDER DEPLOYMENT FIX - CRITICAL

## ❌ Error
```
gunicorn.errors.AppImportError: Application object must be callable.
```

## 🔍 Root Cause
Render is running `gunicorn app:app` but the correct command should be `gunicorn app:server`.

The Dash application exposes the WSGI server as `server`, not `app`:
```python
# In app.py
server = app.server  # This is the WSGI server for Gunicorn
```

## ✅ IMMEDIATE FIX - Update Render Dashboard

**You MUST manually update the Start Command in Render dashboard:**

### Step-by-Step Instructions:

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. **Select your service**: `health-economic-modeling-hub`
3. **Click "Settings"** (left sidebar)
4. **Scroll to "Build & Deploy" section**
5. **Find "Start Command"** field
6. **Replace the current command with:**
   ```bash
   gunicorn app:server --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 60
   ```
7. **Click "Save Changes"**
8. **Go back to service page**
9. **Click "Manual Deploy"** → **"Deploy latest commit"**

## 📋 Additional Settings to Verify

While in the Render Settings, also verify these:

### Python Version
- **Field**: Python Version
- **Value**: `3.12.7`
- **Location**: Settings → Build & Deploy → Python Version

### Environment Variables
Add these if not present (Settings → Environment):
- `PYTHON_VERSION` = `3.12.7`
- `PORT` = `8050`

## 🔧 Why This Happened

Render does **NOT** automatically read `render.yaml` or `.render.yaml` for existing services. These files are only used when creating a **new service** via "New → Blueprint" deployment.

For existing services, you must update settings manually in the dashboard.

## 📚 Official Documentation References

1. [Render - Deploy a Dash App](https://render.com/docs/deploy-dash)
   - Confirms the correct command: `gunicorn app:server`

2. [Render - Python Version](https://render.com/docs/python-version)
   - Python version must be set in dashboard Settings

3. [Gunicorn with Dash](https://dash.plotly.com/deployment)
   - Official Dash deployment guide
   - Specifies: "expose the server variable"

## ✅ Expected Result

After updating the Start Command, you should see:

```
==> Running 'gunicorn app:server --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 60'
🚀 Starting Health Economic Modeling Hub on 0.0.0.0:8050
📊 Dashboard: http://0.0.0.0:8050
🤖 AI Chat: Available
💾 Database: Initialized
...
Booting worker with pid: XXXX
```

## 🆘 If It Still Fails

If you still see errors after fixing the Start Command, check the logs for:

1. **Import errors**: Missing dependencies
2. **Database errors**: PostgreSQL connection issues
3. **Port binding errors**: $PORT variable not set

Run this in Render Shell to test:
```bash
python -c "from app import server; print('✅ Server object found:', server)"
```

---

**DO NOT skip updating the Start Command in the dashboard - the YAML files alone will not fix this!**
