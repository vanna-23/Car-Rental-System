# 🔐 How to Change Your Admin Password

## ✨ Super Easy - Just 3 Steps!

### Step 1: Open the File
Open this file: `db_config.py`

### Step 2: Find Line 137
Look for this section (around line 137):

```python
# ⚠️ CHANGE YOUR PASSWORD HERE ⚠️
# Set your own custom password below (change 'Admin@123' to whatever you want)
YOUR_CUSTOM_PASSWORD = 'Admin@123'  # 👈 Change this to your desired password
```

### Step 3: Change the Password
Replace `'Admin@123'` with **whatever password you want**!

## 💡 Examples:

### Example 1: Simple Password
```python
YOUR_CUSTOM_PASSWORD = 'mypassword123'
```

### Example 2: Your Birthday
```python
YOUR_CUSTOM_PASSWORD = '0707200717'
```

### Example 3: Strong Password
```python
YOUR_CUSTOM_PASSWORD = 'SuperSecure2024!'
```

### Example 4: Easy to Remember
```python
YOUR_CUSTOM_PASSWORD = 'LuxeDrive123'
```

### Example 5: Your Name
```python
YOUR_CUSTOM_PASSWORD = 'LenVanna2024'
```

---

## 🚀 After Changing:

1. **Save the file** (`db_config.py`)
2. **Run your app**: `python app.py`
3. **Login with**:
   - Email: `admin@luxedrive.com`
   - Password: `[whatever you set]`

---

## 🔄 To Change Password Again:

1. **Delete the old admin account** from database:
   ```sql
   DELETE FROM admin_accounts WHERE email = 'admin@luxedrive.com';
   ```

2. **Change the password** in `db_config.py` (line 137)

3. **Restart your app** - New admin account will be created with new password

---

## 📍 Where to Change It:

**File:** `db_config.py`
**Line:** 137
**What to Change:** The text inside quotes after `YOUR_CUSTOM_PASSWORD =`

```python
# Before:
YOUR_CUSTOM_PASSWORD = 'Admin@123'

# After (example):
YOUR_CUSTOM_PASSWORD = 'MyNewPassword123'
```

---

## ✅ That's It!

**You can use ANY password you want!**
- No restrictions
- Any length
- Any characters
- Simple or complex
- It's YOUR choice!

Just change line 137 in `db_config.py` and you're done! 🎉
