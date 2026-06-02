# ⚡ Quick Deploy Guide - Laptop ML Predictor

## 🚀 Deploy in 5 Minutes

### Prerequisites
- ✅ GitHub repository: `Chandan1303/laptop-ML-model`
- ✅ Render account (free): https://dashboard.render.com/

---

## 📝 Step-by-Step

### 1️⃣ Open Render Dashboard
```
https://dashboard.render.com/
```

### 2️⃣ Create Web Service
- Click **"New +"** → **"Web Service"**
- Connect: `Chandan1303/laptop-ML-model`
- Branch: `main`

### 3️⃣ Configure Service

| Setting | Value |
|---------|-------|
| **Name** | `laptop-ml-predictor` |
| **Runtime** | `Python` |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn laptop_predictor.wsgi:application` |

### 4️⃣ Set Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

```env
SECRET_KEY      → Click "Generate" button
DEBUG           → False
ALLOWED_HOSTS   → .onrender.com
```

### 5️⃣ Deploy

- Click **"Create Web Service"**
- Wait 5-10 minutes
- ✅ Done!

---

## 🔗 Access Your App

```
https://your-app-name.onrender.com/          → Brand Prediction
https://your-app-name.onrender.com/price/    → Price Prediction
https://your-app-name.onrender.com/patterns/ → Design Patterns
```

---

## 🧪 Test After Deployment

### Brand Prediction
1. Go to homepage
2. Enter:
   - Price: 61000
   - Rating: 4.3
   - Screen Size: 14.0
   - Storage: 512
   - RAM: 16
   - CPU: Intel Core i5
   - OS: Windows 10
   - Graphics: Integrated
3. Click "Predict"
4. ✅ Should predict a brand (e.g., "HP", "Dell")

### Price Prediction
1. Go to `/price/`
2. Enter:
   - Brand: HP
   - CPU: Intel Core i5
   - OS: Windows 10
   - Graphics: Integrated
   - Rating: 4.3
   - Screen Size: 14.0
   - Storage: 512
   - RAM: 16
3. Click "Predict Price"
4. ✅ Should predict a price (e.g., ₹55,000 - ₹65,000)

---

## ⚠️ First Request Note

**Free Tier:** First request after 15 min idle takes 30-60 seconds (cold start). This is normal!

---

## 🐛 Troubleshooting

### Error: DisallowedHost at /

**Fix:** Update `ALLOWED_HOSTS` environment variable:
```
your-app-name.onrender.com,.onrender.com
```

### Static Files Not Loading

**Fix:** Check build logs for:
```
133 static files copied to 'staticfiles'
```

### Build Failed

**Check:**
1. Build logs in Render dashboard
2. All .pkl files are in repository
3. requirements.txt is correct

---

## 📚 More Help

| Document | Purpose |
|----------|---------|
| `RENDER_DEPLOYMENT_CHECKLIST.md` | Full interactive checklist (26 steps) |
| `DEPLOYMENT.md` | Complete deployment guide |
| `DEPLOYMENT_SUMMARY.md` | Quick reference |
| `test_deployment.py` | Run local tests |

---

## ✅ Success Checklist

After deployment:

- [ ] App loads without errors
- [ ] Brand prediction works
- [ ] Price prediction works
- [ ] Design patterns page displays
- [ ] Static files (CSS, JS) load correctly
- [ ] No errors in Render logs

---

## 🎯 Next Steps

1. **Update README** with live URL
2. **Post on LinkedIn** with demo link
3. **Add to portfolio**
4. **Share with team**

---

## 🔗 Important Links

- **Repository:** https://github.com/Chandan1303/laptop-ML-model
- **Render Dashboard:** https://dashboard.render.com/
- **Django Deployment:** https://docs.djangoproject.com/en/stable/howto/deployment/

---

**Time to Deploy:** ~10 minutes (first time)  
**Status:** ✅ Ready to deploy now!

🚀 **Go deploy and share your ML app with the world!**
