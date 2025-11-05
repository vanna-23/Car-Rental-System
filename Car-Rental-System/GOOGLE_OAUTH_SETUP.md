# 🔐 Google OAuth Setup Guide

Complete guide to enable Google Sign-In for your Car Rental System.

---

## 📋 What You'll Get

After setup, users can:
- ✅ **Sign up** with their Google account (1-click)
- ✅ **Login** with their Google account (1-click)
- ✅ **Auto-create account** when signing in with Google
- ✅ **No password needed** for Google users
- ✅ **Secure authentication** via Google OAuth 2.0

---

## 🚀 Quick Start (3 Steps)

### **Step 1: Get Google OAuth Credentials**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Get your Client ID and Client Secret

### **Step 2: Configure Your App**

Create a `.env` file in your project root:

```bash
GOOGLE_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret_here
```

### **Step 3: Install Dependencies**

```bash
pip install -r requirements.txt
```

**That's it! Google Sign-In is ready!** 🎉

---

## 📝 Detailed Setup Instructions

### **1. Create Google Cloud Project**

#### **a. Go to Google Cloud Console**
- Visit: https://console.cloud.google.com/
- Sign in with your Google account

#### **b. Create New Project**
```
1. Click "Select a project" (top bar)
2. Click "NEW PROJECT"
3. Enter project name: "Car Rental System"
4. Click "CREATE"
```

#### **c. Enable APIs**
```
1. Go to "APIs & Services" → "Library"
2. Search for "Google+ API"
3. Click on it and click "ENABLE"
```

---

### **2. Create OAuth 2.0 Credentials**

#### **a. Configure OAuth Consent Screen**

```
1. Go to "APIs & Services" → "OAuth consent screen"
2. Select "External" (for testing)
3. Click "CREATE"

4. Fill in Application Information:
   - App name: Car Rental System
   - User support email: your_email@gmail.com
   - Developer contact: your_email@gmail.com

5. Click "SAVE AND CONTINUE"

6. Scopes (leave default):
   - Click "SAVE AND CONTINUE"

7. Test users (optional for development):
   - Add your test email addresses
   - Click "SAVE AND CONTINUE"

8. Click "BACK TO DASHBOARD"
```

#### **b. Create OAuth Client ID**

```
1. Go to "APIs & Services" → "Credentials"
2. Click "CREATE CREDENTIALS" → "OAuth client ID"
3. Select "Web application"

4. Configure:
   Name: Car Rental System Web Client
   
   Authorized JavaScript origins:
   - http://localhost:5000
   - http://127.0.0.1:5000
   
   Authorized redirect URIs:
   - http://localhost:5000/auth/google/callback
   - http://127.0.0.1:5000/auth/google/callback

5. Click "CREATE"

6. **SAVE YOUR CREDENTIALS:**
   - Client ID: xxxxx.apps.googleusercontent.com
   - Client Secret: xxxxx
```

---

### **3. Configure Your Application**

#### **Option A: Using Environment Variables (Recommended)**

Create `.env` file in project root:

```bash
# .env
GOOGLE_CLIENT_ID=your_actual_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_actual_client_secret
```

Then install python-dotenv:
```bash
pip install python-dotenv
```

Update `app.py` at the top:
```python
from dotenv import load_dotenv
load_dotenv()
```

#### **Option B: Direct Configuration**

Edit `app.py` (line 19-20):

```python
google = oauth.register(
    name='google',
    client_id='YOUR_ACTUAL_CLIENT_ID.apps.googleusercontent.com',
    client_secret='YOUR_ACTUAL_CLIENT_SECRET',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)
```

---

### **4. Install Dependencies**

```bash
pip install -r requirements.txt
```

Dependencies added:
- `authlib==1.2.1` - OAuth library
- `requests==2.31.0` - HTTP library

---

### **5. Test Your Setup**

#### **Start Your Application**
```bash
python app.py
```

#### **Test Google Sign-In**

1. **From Signup Page:**
   ```
   http://localhost:5000/signup
   Click "Continue with Google" button
   ```

2. **From Login Page:**
   ```
   http://localhost:5000/login
   Click "Continue with Google" button
   ```

3. **Expected Flow:**
   ```
   1. User clicks "Continue with Google"
   2. Redirected to Google login
   3. User selects Google account
   4. User grants permissions
   5. Redirected back to your app
   6. Account auto-created (if new user)
   7. User logged in ✅
   ```

---

## 🔄 How It Works

### **Complete Google OAuth Flow:**

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User clicks "Continue with Google"                       │
│    Location: /signup or /login                              │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. App redirects to: /auth/google                           │
│    Backend initiates OAuth flow                             │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. User redirected to Google                                │
│    URL: https://accounts.google.com/o/oauth2/v2/auth        │
│    User sees Google account selector                        │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. User selects account & grants permissions                │
│    Permissions: email, profile, openid                      │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Google redirects back to callback                        │
│    URL: /auth/google/callback?code=xxxxx                    │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. Backend exchanges code for token                         │
│    Gets user info from Google:                              │
│    - Email: user@gmail.com                                  │
│    - Name: John Doe                                         │
│    - Google ID: 123456789                                   │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. Check if user exists in MySQL                            │
│    SELECT * FROM users WHERE email = 'user@gmail.com'       │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
         ┌─────────┴─────────┐
         ↓                   ↓
   User Exists          New User
         ↓                   ↓
   ┌──────────┐      ┌────────────────┐
   │ Login    │      │ Create Account │
   │ User     │      │ in MySQL       │
   └────┬─────┘      └────────┬───────┘
         │                     │
         └──────────┬──────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. Create session                                            │
│    session['user'] = email                                  │
│    session['name'] = name                                   │
│    session['google_user'] = True                            │
└──────────────────┬──────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ 9. Redirect to homepage                                      │
│    User is now logged in! ✅                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 💾 Database Integration

### **How Google Users Are Stored:**

```python
# When new Google user signs in:
{
    'name': 'John Doe',              # From Google profile
    'email': 'john@gmail.com',       # From Google (primary key)
    'phone': 'GOOGLE_1234567890',    # Placeholder (Google doesn't provide)
    'password': '<random_hash>',     # Random secure password (not used)
}
```

### **MySQL Storage:**

```sql
INSERT INTO users (name, email, phone, password)
VALUES (
    'John Doe',
    'john@gmail.com',
    'GOOGLE_1234567890',
    'pbkdf2:sha256:600000$abc...'  -- Random, never used
);
```

### **Why Store a Password?**

- Database requires password field (NOT NULL)
- Google users never use this password
- Generated randomly with `secrets.token_urlsafe(32)`
- Allows database schema consistency

---

## 🔐 Security Features

### **✅ Secure OAuth 2.0**
- Industry-standard authentication
- No passwords stored for Google users
- Tokens handled by Google

### **✅ Email Verification**
- Google verifies email addresses
- No need for email confirmation

### **✅ Session Management**
- Secure Flask sessions
- `session['google_user'] = True` flag
- Automatic login/logout

### **✅ Data Privacy**
- Only request necessary scopes (email, profile)
- User controls permissions
- No password exposure

---

## 🧪 Testing Checklist

### **Test 1: New User Signup**
```bash
□ Click "Continue with Google" on /signup
□ Select Google account
□ Grant permissions
□ Verify redirect to homepage
□ Check user created in MySQL:
  SELECT * FROM users WHERE email = 'your@gmail.com';
□ Verify session created (name visible in navbar)
```

### **Test 2: Existing User Login**
```bash
□ Logout
□ Click "Continue with Google" on /login
□ Select same Google account
□ Verify instant login (no signup)
□ Check session created
```

### **Test 3: Mixed Auth**
```bash
□ Can Google users also use manual login? No (no password)
□ Can manual users also use Google? Yes (if same email)
□ Test switching between auth methods
```

---

## 🚨 Common Issues & Solutions

### **Issue 1: "Redirect URI mismatch"**

**Error:**
```
Error 400: redirect_uri_mismatch
```

**Solution:**
```
1. Go to Google Cloud Console
2. APIs & Services → Credentials
3. Edit your OAuth client
4. Add exact redirect URI:
   http://localhost:5000/auth/google/callback
5. Save and try again
```

---

### **Issue 2: "Access blocked: Authorization Error"**

**Error:**
```
This app hasn't been verified by Google
```

**Solution (Development):**
```
1. Click "Advanced"
2. Click "Go to [Your App] (unsafe)"
3. This is normal for development
```

**Solution (Production):**
```
1. Go through Google's app verification process
2. Submit app for review
3. Add privacy policy and terms of service
```

---

### **Issue 3: Client ID/Secret not working**

**Solution:**
```
1. Verify .env file exists and has correct values
2. Check no extra spaces in credentials
3. Restart Flask app after changing .env
4. Try hardcoding values temporarily to test
```

---

### **Issue 4: "Failed to get user info from Google"**

**Solution:**
```
1. Check internet connection
2. Verify Google+ API is enabled
3. Check server_metadata_url is correct
4. Try regenerating OAuth credentials
```

---

## 📊 Feature Comparison

### **Manual Signup/Login vs Google OAuth**

| Feature | Manual | Google OAuth |
|---------|--------|--------------|
| **Fields Required** | Name, Email, Phone, Password | Just click button |
| **Password** | User creates | Auto-generated (not used) |
| **Email Verification** | Manual (if implemented) | ✅ By Google |
| **Phone Number** | Required | Placeholder created |
| **Security** | Password hash in DB | ✅ Google OAuth 2.0 |
| **User Experience** | Fill 4 fields | 1-click |
| **Setup Time** | ~2 minutes | ~5 seconds |

---

## 🌐 Production Deployment

### **1. Update Redirect URIs**

Add your production domain to Google Cloud Console:

```
Authorized JavaScript origins:
- https://yourdomain.com

Authorized redirect URIs:
- https://yourdomain.com/auth/google/callback
```

### **2. Use Environment Variables**

```bash
# Production .env
GOOGLE_CLIENT_ID=your_prod_client_id
GOOGLE_CLIENT_SECRET=your_prod_client_secret
FLASK_SECRET_KEY=your_secure_random_key
```

### **3. Get App Verified (Optional)**

For public apps:
```
1. Go to OAuth consent screen
2. Click "PUBLISH APP"
3. Submit for verification (if needed)
4. Add privacy policy URL
5. Add terms of service URL
```

---

## 📁 Files Modified

### **1. `requirements.txt`** ✅
```
authlib==1.2.1
requests==2.31.0
```

### **2. `app.py`** ✅
- Added OAuth imports
- Configured Google OAuth client
- Added `/auth/google` route
- Added `/auth/google/callback` route
- Auto-creates accounts for Google users

### **3. `templates/signup.html`** ✅
- Added "Continue with Google" button
- Links to `/auth/google`

### **4. `templates/login.html`** ✅
- Added "Continue with Google" button
- Links to `/auth/google`

---

## 🎯 Summary

**Your Google OAuth integration is complete!**

✅ **Easy Signup** - 1-click with Google account  
✅ **Fast Login** - No password to remember  
✅ **Auto Account Creation** - New users created automatically  
✅ **Secure** - OAuth 2.0 industry standard  
✅ **MySQL Connected** - All data stored properly  
✅ **Production Ready** - Just add your credentials  

**Users can now sign up and login with Google in 5 seconds!** 🎉

---

## 📞 Support

### **Still Need Help?**

1. **Check Google Cloud Console** - Verify credentials and URIs
2. **Check Flask logs** - Look for OAuth errors
3. **Test with .env** - Use environment variables
4. **Verify MySQL** - Check users table has data

### **Useful Links**

- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Authlib Documentation](https://docs.authlib.org/)
- [Google Cloud Console](https://console.cloud.google.com/)

---

**Last Updated:** November 2025  
**Version:** 1.0
