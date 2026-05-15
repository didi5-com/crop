# 🔑 API Setup Guide - Get Real Crop Disease Detection

This guide will help you set up **FREE** API access for accurate crop disease detection.

## 🌟 Recommended: Plant.id API (Best for Crop Diseases)

Plant.id is the **most accurate** API for crop disease detection with comprehensive disease information.

### Step 1: Create Free Account

1. Go to: **https://web.plant.id/**
2. Click **"Sign Up"** or **"Get Started"**
3. Fill in your details:
   - Email address
   - Password
   - Name (optional)
4. Verify your email address

### Step 2: Get Your API Key

1. After logging in, go to your **Dashboard**
2. Click on **"API Keys"** or **"My API Keys"**
3. You'll see your API key displayed
4. Copy the API key (it looks like: `aBcDeFgHiJkLmNoPqRsTuVwXyZ123456`)

### Step 3: Add API Key to Your Application

1. Open the `.env` file in your project folder
2. Find the line: `PLANT_ID_API_KEY=your-plant-id-api-key`
3. Replace `your-plant-id-api-key` with your actual API key:
   ```
   PLANT_ID_API_KEY=aBcDeFgHiJkLmNoPqRsTuVwXyZ123456
   ```
4. Save the file

### Step 4: Restart the Application

```bash
# Stop the current server (Ctrl+C)
# Then restart:
run_app.bat
```

### Free Tier Limits

- **100 requests per month** (FREE)
- Perfect for testing and small-scale use
- Upgrade available for more requests

---

## 🌿 Alternative: PlantNet API

PlantNet is another good option, though less specialized in diseases.

### Step 1: Create Account

1. Go to: **https://my.plantnet.org/**
2. Click **"Register"**
3. Fill in your information
4. Verify your email

### Step 2: Get API Key

1. Log in to your account
2. Go to **"API Keys"** section
3. Create a new API key
4. Copy the key

### Step 3: Add to .env

```
PLANTNET_API_KEY=your-plantnet-api-key-here
```

---

## 🧪 Testing Without API Key

The system includes **mock detection** that works without any API key. It returns realistic sample data for testing purposes.

**Mock detection is automatically used when:**
- No API key is configured
- API request fails
- API rate limit is exceeded

---

## 🔍 How to Verify API is Working

### Method 1: Check Application Logs

When you upload an image, look for these messages in the terminal:

**With API Key (Working):**
```
Sending request to Plant.id API...
Successfully received Plant.id API response
```

**Without API Key (Mock):**
```
No Plant.id API key found. Using mock detection.
```

### Method 2: Check Detection Results

**Real API Results:**
- More specific disease names
- Accurate confidence scores
- Detailed scientific descriptions
- Specific treatment recommendations

**Mock Results:**
- Generic disease names
- Fixed confidence scores (87.5%)
- Generic descriptions

---

## 💡 Pro Tips

### 1. Start with Free Tier
The free tier (100 requests/month) is perfect for:
- Testing the system
- Personal use
- Small farms
- Demonstrations

### 2. Monitor Your Usage
- Check your Plant.id dashboard regularly
- Track remaining requests
- Plan upgrades if needed

### 3. Optimize API Calls
- Don't upload the same image multiple times
- Use good quality images for better results
- Crop images to focus on affected areas

### 4. Handle Rate Limits
The system automatically falls back to mock detection if:
- Rate limit exceeded
- API is down
- Network issues

---

## 🆘 Troubleshooting

### "Invalid API Key" Error

**Problem:** API returns 401 error

**Solutions:**
1. Check if API key is correct in `.env`
2. Make sure there are no extra spaces
3. Verify key is active in Plant.id dashboard
4. Try regenerating the API key

### "Rate Limit Exceeded" Error

**Problem:** API returns 429 error

**Solutions:**
1. Wait until next month (free tier resets)
2. Upgrade to paid plan
3. Use mock detection temporarily

### API Not Being Used

**Problem:** System still shows mock results

**Solutions:**
1. Verify `.env` file has correct API key
2. Restart the application after adding key
3. Check terminal logs for error messages
4. Ensure no typos in variable name

---

## 📊 API Comparison

| Feature | Plant.id | PlantNet | Mock |
|---------|----------|----------|------|
| **Accuracy** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Disease Info** | Comprehensive | Basic | Generic |
| **Free Tier** | 100/month | 500/day | Unlimited |
| **Setup Time** | 5 minutes | 5 minutes | 0 minutes |
| **Best For** | Production | Testing | Development |

---

## 🎯 Recommended Setup

### For Development/Testing
```env
# Use mock detection (no API key needed)
PLANT_ID_API_KEY=
```

### For Production/Real Use
```env
# Use Plant.id API
PLANT_ID_API_KEY=your-actual-api-key-here
```

---

## 📞 Need Help?

### Plant.id Support
- **Website:** https://web.plant.id/
- **Documentation:** https://plant.id/docs
- **Support:** support@plant.id

### Application Support
- **Email:** support@cropcareai.com
- **Documentation:** See README.md

---

## ✅ Quick Setup Checklist

- [ ] Created Plant.id account
- [ ] Verified email address
- [ ] Got API key from dashboard
- [ ] Added key to `.env` file
- [ ] Restarted application
- [ ] Tested with crop image
- [ ] Verified real API is being used (check logs)
- [ ] Bookmarked Plant.id dashboard

---

## 🚀 You're Ready!

Once you've added your API key and restarted the application, you'll get:

✅ **Accurate disease detection**
✅ **Scientific disease names**
✅ **Detailed symptoms**
✅ **Specific treatments**
✅ **Prevention methods**
✅ **Confidence scores**

**Happy farming! 🌾**
