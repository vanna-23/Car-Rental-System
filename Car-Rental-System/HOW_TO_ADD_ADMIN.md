# 📝 How to Add New Admin Accounts

## Method 1: Using Python Script (EASIEST) ✅

### Step 1: Run the add_admin.py script

```bash
python add_admin.py
```

### Step 2: Enter your details when prompted

```
👤 Full Name: [Enter your name]
📧 Email:     [Enter your email]
📱 Phone:     [Enter your phone]
🔑 Password:  [Enter your password]
```

### Step 3: Confirm and done!

The script will:
- ✅ Hash your password securely
- ✅ Add the account to MySQL database
- ✅ Show confirmation with login details

---

## Method 2: Direct in Script (QUICK)

### Edit `add_admin.py` and add this line:

```python
add_admin_account("Your Name", "your@email.com", "1234567890", "your_password")
```

### Then run:

```bash
python add_admin.py
```

---

## Method 3: Using phpMyAdmin (MANUAL)

### Step 1: Open phpMyAdmin
- Go to: `http://localhost/phpmyadmin`

### Step 2: Navigate to the table
- Click on database: `car_rental_db`
- Click on table: `admin_accounts`
- Click "Insert" tab

### Step 3: Fill in the data

**⚠️ IMPORTANT: For password, use the hashed version!**

Run this first to get hashed password:

```bash
python hash_password.py
```

Enter your password, and it will give you the hashed version.

Then insert:
- fullname: Your Name
- email: your@email.com
- phone: 1234567890
- password: [paste the hashed password here]

---

## Method 4: Direct SQL Query

### Run this in phpMyAdmin SQL tab:

```sql
INSERT INTO admin_accounts (fullname, email, phone, password)
VALUES ('Your Name', 'your@email.com', '1234567890', 'scrypt:...[hashed_password]');
```

**Note:** You need to hash the password first using `hash_password.py`

---

## 🎯 Quick Examples

### Example 1: Add yourself as admin

```bash
python add_admin.py
```

Then enter:
```
Full Name: Len Vanna
Email: vanna@gmail.com
Phone: 0123456789
Password: MySecurePass123
```

### Example 2: Add multiple admins at once

Edit `add_admin.py` and add at the bottom:

```python
# Add multiple admins
add_admin_account("Manager", "manager@company.com", "1111111111", "manager123")
add_admin_account("Supervisor", "supervisor@company.com", "2222222222", "super456")
add_admin_account("Admin", "admin@company.com", "3333333333", "admin789")
```

Then run: `python add_admin.py`

---

## 🔒 Security Notes

- ✅ Passwords are automatically hashed
- ✅ Email is converted to lowercase
- ✅ Duplicate emails are prevented
- ✅ All fields are required

---

## 📊 View All Admin Accounts

Run this script to see all admins:

```bash
python verify_admin.py
```

---

## ✅ After Adding Admin

You can login with:

1. Go to: **http://localhost:5000/admin/login**
2. Enter ALL 4 fields:
   - Full Name
   - Email
   - Phone
   - Password
3. Click Login
4. Success! → Admin Dashboard

---

## 🎉 That's it!

Now you can easily add as many admin accounts as you need!
