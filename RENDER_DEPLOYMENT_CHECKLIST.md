# ✅ Render Deployment Checklist - Laptop ML Predictor

Use this checklist to deploy your Django ML app to Render step-by-step.

---

## 📋 Pre-Deployment (Local)

### 1. Verify All Changes Are Committed

- [x] All deployment files created
- [x] Settings.py updated with environment variables
- [x] Requirements.txt includes gunicorn and whitenoise
- [x] Changes committed to git
- [x] Changes pushed to GitHub

**Run:**
```bash
git status  # Should show "nothing to commit, working tree clean"
```

---

### 2. Run Pre-Deployment Tests

- [ ] Run: `python test_deployment.py`
- [ ] All 7 tests pass (Imports, Model Files, Django Settings, WSGI, Views, Static Files, Templates)
- [ ] No errors in test output

**Expected Output:**
```
🎉 ALL TESTS PASSED - Ready for deployment!
```

---

### 3. Test Static File Collection

- [ ] Run: `python manage.py collectstatic --no-input`
- [ ] Static files collected successfully
- [ ] No errors

**Expected Output:**
```
133 static files copied to 'staticfiles', 661 post-processed.
```

---

### 4. Verify Model Files Exist

- [ ] `laptop_model.pkl` (55.98 MB) ✓
- [ ] `price_model.pkl` (31.76 MB) ✓
- [ ] All 10 .pkl files in repository ✓
- [ ] Model files NOT in .gitignore ✓

---

## 🚀 Render Dashboard Setup

### 5. Create New Web Service

1. [ ] Go to https://dashboard.render.com/
2. [ ] Click **"New +"** → **"Web Service"**
3. [ ] Click **"Connect account"** if GitHub not connected
4. [ ] Select repository: `Chandan1303/laptop-ML-model`
5. [ ] Click **"Connect"**

---

### 6. Configure Basic Settings

**Service Configuration:**

| Field | Value |
|-------|-------|
| **Name** | `laptop-ml-predictor` (or your choice) |
| **Region** | Select closest to you (e.g., Oregon, Frankfurt) |
| **Branch** | `main` |
| **Runtime** | `Python` |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn laptop_predictor.wsgi:application` |

- [ ] All fields filled correctly
- [ ] Build command is `./build.sh`
- [ ] Start command is `gunicorn laptop_predictor.wsgi:application`

---

### 7. Configure Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

#### Required Variables:

1. **SECRET_KEY**
   - [ ] Click "Generate" button to auto-generate
   - [ ] OR paste your own secure random string (50+ characters)

2. **DEBUG**
   - [ ] Key: `DEBUG`
   - [ ] Value: `False`

3. **ALLOWED_HOSTS**
   - [ ] Key: `ALLOWED_HOSTS`
   - [ ] Value: `.onrender.com`
   - [ ] Note: After first deploy, update to include your actual URL

4. **PYTHON_VERSION** (Optional, already in render.yaml)
   - [ ] Key: `PYTHON_VERSION`
   - [ ] Value: `3.11.0`

**Screenshot:** Take a screenshot of your environment variables for reference.

---

### 8. Select Instance Type

**Free Tier (Recommended for Testing):**
- [ ] Instance Type: `Free`
- [ ] 512 MB RAM
- [ ] 0.1 CPU
- [ ] Note: Spins down after 15 minutes of inactivity

**Paid Tier (For Production):**
- [ ] Instance Type: `Starter` or higher
- [ ] No cold starts
- [ ] Better performance

---

### 9. Deploy

- [ ] Review all settings
- [ ] Click **"Create Web Service"**
- [ ] Watch deployment logs in real-time

---

## 🔍 Monitor Deployment

### 10. Watch Build Logs

Deployment process (5-10 minutes):

**Expected Steps:**
1. [ ] Cloning repository from GitHub
2. [ ] Installing Python 3.11.9
3. [ ] Running `./build.sh`
   - [ ] `pip install --upgrade pip`
   - [ ] `pip install -r requirements.txt`
   - [ ] `python manage.py collectstatic --no-input`
   - [ ] `python manage.py migrate --no-input`
4. [ ] Starting Gunicorn server
5. [ ] Health check passes
6. [ ] Service goes live ✓

**Look For:**
- ✅ "Build succeeded"
- ✅ "Deploy succeeded"
- ✅ Green "Live" status indicator

---

### 11. Troubleshoot Build Errors (If Any)

**Common Issues:**

#### Error: "No such file or directory: './build.sh'"
**Solution:** 
```bash
# On Windows, ensure build.sh was committed properly
git add build.sh
git commit -m "Fix build.sh"
git push origin main
```

#### Error: "No module named 'gunicorn'"
**Solution:** Verify `requirements.txt` includes `gunicorn>=21.2.0`

#### Error: "DisallowedHost"
**Solution:** Update `ALLOWED_HOSTS` environment variable to include your Render URL

#### Error: Model file not found
**Solution:** Verify .pkl files are committed to git (not in .gitignore)

---

## ✅ Post-Deployment Verification

### 12. Access Your Application

- [ ] Copy the URL from Render dashboard (e.g., `https://laptop-ml-predictor.onrender.com`)
- [ ] Open URL in browser
- [ ] Application loads without errors

**If first request after idle:**
- Cold start may take 30-60 seconds (free tier)
- This is normal!

---

### 13. Test Home Page (Brand Prediction)

**URL:** `https://your-app-name.onrender.com/`

- [ ] Page loads successfully
- [ ] CSS styles applied correctly
- [ ] Navigation menu visible
- [ ] Form fields render properly:
  - [ ] Price input
  - [ ] Rating input
  - [ ] Screen size input
  - [ ] Storage GB input
  - [ ] RAM GB input
  - [ ] CPU dropdown (144 options)
  - [ ] OS dropdown
  - [ ] Graphics dropdown

**Test Prediction:**
- [ ] Enter test values:
  - Price: 61000
  - Rating: 4.3
  - Screen Size: 14.0
  - Storage: 512
  - RAM: 16
  - CPU: Intel Core i5
  - OS: Windows 10
  - Graphics: Integrated
- [ ] Click "Predict"
- [ ] Prediction result displays
- [ ] Top 3 brands with probabilities show

**Expected Result:** Should predict a brand like "HP", "Dell", etc.

---

### 14. Test Price Prediction Page

**URL:** `https://your-app-name.onrender.com/price/`

- [ ] Page loads successfully
- [ ] Form fields render properly:
  - [ ] Brand dropdown
  - [ ] CPU dropdown
  - [ ] OS dropdown
  - [ ] Graphics dropdown
  - [ ] Rating input
  - [ ] Screen size input
  - [ ] Storage GB input
  - [ ] RAM GB input
  - [ ] CPU speed input (optional)
  - [ ] Total sales input (optional)

**Test Prediction:**
- [ ] Enter test values:
  - Brand: HP
  - CPU: Intel Core i5
  - OS: Windows 10
  - Graphics: Integrated
  - Rating: 4.3
  - Screen Size: 14.0
  - Storage: 512
  - RAM: 16
- [ ] Click "Predict Price"
- [ ] Price prediction displays
- [ ] Formatted price shown correctly

**Expected Result:** Should predict a price (e.g., ₹55,000 - ₹65,000)

---

### 15. Test Design Patterns Page

**URL:** `https://your-app-name.onrender.com/patterns/`

- [ ] Page loads successfully
- [ ] All 10 design patterns display
- [ ] Patterns grouped by category:
  - [ ] Creational (3 patterns)
  - [ ] Structural (3 patterns)
  - [ ] Behavioral (4 patterns)
- [ ] Code snippets render correctly
- [ ] Icons display
- [ ] Navigation works

---

### 16. Test Static Files

- [ ] CSS file loads: Check page styling
- [ ] JavaScript file loads: Check console for errors (F12)
- [ ] Images load: Amazon logo visible
- [ ] No 404 errors in Network tab

**Verify:**
```
Open browser DevTools (F12) → Network tab
Reload page
All static files should return 200 OK
```

---

### 17. Check Error Logs

**In Render Dashboard:**
- [ ] Go to Logs tab
- [ ] No Python errors or exceptions
- [ ] No Django warnings
- [ ] Request logs show 200 status codes

**Look for:**
- ✅ `GET / HTTP/1.1 200`
- ✅ `GET /price/ HTTP/1.1 200`
- ✅ `GET /patterns/ HTTP/1.1 200`
- ❌ No 500 Internal Server Error
- ❌ No module import errors

---

## 🔧 Post-Deployment Configuration

### 18. Update ALLOWED_HOSTS

After first successful deployment:

1. [ ] Copy your exact Render URL (e.g., `laptop-ml-predictor.onrender.com`)
2. [ ] In Render dashboard → Environment
3. [ ] Update `ALLOWED_HOSTS` variable:
   ```
   laptop-ml-predictor.onrender.com,.onrender.com,localhost
   ```
4. [ ] Save changes (auto-redeploys)

---

### 19. Update README.md with Live URL

**In GitHub:**

1. [ ] Edit README.md
2. [ ] Replace placeholder:
   ```markdown
   🚀 **[Live Demo](https://laptop-ml-predictor.onrender.com)**
   ```
3. [ ] Commit and push
4. [ ] Render auto-redeploys

---

### 20. Test After Auto-Redeploy

- [ ] Wait for redeploy to complete (~3-5 minutes)
- [ ] Test all pages again
- [ ] Verify no errors

---

## 📱 Share Your Work

### 21. Update Portfolio/LinkedIn

- [ ] Copy live demo URL
- [ ] Post on LinkedIn with the caption template provided
- [ ] Add to portfolio website
- [ ] Share with teammates
- [ ] Share with professors

---

### 22. Documentation

- [ ] Repository README includes live demo link ✓
- [ ] DEPLOYMENT.md guide available ✓
- [ ] Code is well-commented ✓
- [ ] All .pkl files in repo ✓

---

## 🎯 Final Verification

### 23. Complete Feature Test

Run through complete user journey:

1. **Visitor Flow:**
   - [ ] Visit home page
   - [ ] Read description
   - [ ] Submit brand prediction
   - [ ] View results
   - [ ] Navigate to price prediction
   - [ ] Submit price prediction
   - [ ] View results
   - [ ] Navigate to design patterns
   - [ ] Read pattern explanations

2. **Technical Verification:**
   - [ ] No JavaScript errors (F12 console)
   - [ ] No broken images
   - [ ] All links work
   - [ ] Forms submit successfully
   - [ ] Predictions are reasonable
   - [ ] Page load time acceptable (<5s after warm-up)

3. **Multiple Devices:**
   - [ ] Test on desktop
   - [ ] Test on mobile (responsive)
   - [ ] Test on different browsers (Chrome, Firefox, Safari)

---

### 24. Performance Check

**Free Tier Expectations:**
- First request after idle: 30-60 seconds (cold start)
- Subsequent requests: <3 seconds
- Model inference: <1 second

**If Performance Issues:**
- [ ] Check Render logs for errors
- [ ] Verify model files loaded correctly
- [ ] Consider upgrading to paid tier

---

## 🎉 Deployment Complete!

### 25. Success Criteria

All items checked off:

- [x] Build succeeded
- [x] Application deployed
- [x] All pages load correctly
- [x] Brand prediction works
- [x] Price prediction works
- [x] Design patterns display
- [x] Static files serve correctly
- [x] No errors in logs
- [x] Live URL shared

---

## 📊 Monitoring (Ongoing)

### 26. Regular Checks

**Daily (First Week):**
- [ ] Check error logs
- [ ] Monitor performance
- [ ] Test predictions

**Weekly:**
- [ ] Review usage statistics
- [ ] Check for deployment issues
- [ ] Update dependencies if needed

**Monthly:**
- [ ] Verify free tier hours remaining
- [ ] Consider upgrading if needed
- [ ] Update documentation

---

## 🆘 Get Help

**If you encounter issues:**

1. **Check DEPLOYMENT.md** - Troubleshooting section
2. **Render Documentation** - https://render.com/docs/deploy-django
3. **Render Community** - https://community.render.com/
4. **Django Deployment Docs** - https://docs.djangoproject.com/en/stable/howto/deployment/

---

## 🎯 Quick Commands Reference

```bash
# Local testing
python test_deployment.py
python manage.py collectstatic --no-input
python manage.py check --deploy

# Git workflow
git add .
git commit -m "Your changes"
git push origin main

# Manual redeploy (Render dashboard)
Settings → Manual Deploy → Deploy latest commit
```

---

**Deployment Checklist Created:** June 2, 2026  
**For Repository:** Chandan1303/laptop-ML-model  
**Target Platform:** Render  
**Status:** Ready to Deploy! 🚀

---

**Good luck with your deployment!**

Once deployed, don't forget to:
1. ✅ Update README with live URL
2. ✅ Post on LinkedIn
3. ✅ Add to portfolio
4. ✅ Celebrate! 🎉
