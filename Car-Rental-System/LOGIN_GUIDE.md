# 🔐 Complete Login & Signup Guide

## ✅ BOTH Customer & Admin Login FIXED!

Both login systems now work with **email + password only** (normal login).

---

## 👥 CUSTOMER LOGIN & SIGNUP

### **Customer Login** (Simple: Email + Password)
- **URL:** http://localhost:5000/login
- **Required:** Email, Password only
- **Bonus:** Get 20% discount on first booking!

### **Customer Signup** (Create Account)
- **URL:** http://localhost:5000/signup
- **Required:** Full Name, Email, Phone, Password
- **After Signup:** Automatically logged in with 20% discount

---

## 🧪 Test Customer Accounts

You have 4 customer accounts in your database:

### **Test Account #1**
```
Email: test@customer.com
Password: password123
```

### **Test Account #2**
```
Email: vanna@gmail.com
Password: (your password)
```

### **Test Account #3**
```
Email: vich@gmail.com
Password: (your password)
```

### **Test Account #4**
```
Email: bivimareh@mailinator.com
Password: (your password)
```

---

## 🛡️ ADMIN LOGIN & SIGNUP

### **Admin Login** (Simple: Email + Password)
- **URL:** http://localhost:5000/admin/login
- **Required:** Email, Password only

### **Admin Signup** (Create Admin Account)
- **URL:** http://localhost:5000/admin/signup
- **Required:** Full Name, Email, Phone, Password, Access Code
- **Access Code:** `0707200717` (required to create admin)

---

## 🧪 Test Admin Accounts

You have 2 admin accounts in your database:

### **Admin #1 (Default)**
```
Email: admin@luxedrive.com
Password: 0707200717
```

### **Admin #2 (Your Account)**
```
Email: vanna@gmail.com
Password: 0707200717
```

---

## 🎯 Quick Test Guide

### Test Customer Login:
1. Go to: http://localhost:5000/login
2. Enter:
   - Email: `test@customer.com`
   - Password: `password123`
3. Click **Login**
4. Browse cars and make bookings!

### Test Admin Login:
1. Go to: http://localhost:5000/admin/login
2. Enter:
   - Email: `admin@luxedrive.com`
   - Password: `0707200717`
3. Click **Login**
4. Manage cars and bookings!

---

## 📋 Feature Comparison

| Feature | Customer | Admin |
|---------|----------|-------|
| **Login** | Email + Password | Email + Password |
| **Signup** | Name + Email + Phone + Password | Name + Email + Phone + Password + Access Code |
| **Browse Cars** | ✅ Yes | ✅ Yes |
| **Book Cars** | ✅ Yes | ❌ No |
| **Add/Edit Cars** | ❌ No | ✅ Yes |
| **View All Bookings** | Own bookings only | ✅ All bookings |
| **Dashboard** | My Bookings | Admin Dashboard |

---

## 🔧 What Was Fixed:

### Before (Broken):
- ❌ Login required 4 fields: Full Name, Email, Phone, Password
- ❌ Had to remember and type all info every time
- ❌ Very annoying and unusual

### After (Fixed):
- ✅ Login only requires: Email + Password (normal!)
- ✅ Simple and standard login experience
- ✅ Works like every other website

---

## 📝 Important Notes:

**For Customers:**
- Signup requires full info (to create account)
- Login only needs email + password
- Get 20% discount on first booking
- Weekend bookings get 50% discount

**For Admins:**
- Access code `0707200717` required to create new admin
- Login only needs email + password
- Full control over car inventory
- Can view all bookings and statistics

---

## 🚀 URLs Summary

| Page | URL |
|------|-----|
| 🏠 Home | http://localhost:5000 |
| 👤 Customer Login | http://localhost:5000/login |
| ✍️ Customer Signup | http://localhost:5000/signup |
| 🚗 Browse Cars | http://localhost:5000/cars |
| 📋 My Bookings | http://localhost:5000/bookings |
| 🛡️ Admin Login | http://localhost:5000/admin/login |
| ✍️ Admin Signup | http://localhost:5000/admin/signup |
| 📊 Admin Dashboard | http://localhost:5000/admin/dashboard |

---

## 💾 Database Info

**MySQL Database:** `car_rental_db`
- ✅ **users** table: Customer accounts
- ✅ **admin_accounts** table: Admin accounts
- ✅ **cars** table: Vehicle inventory
- ✅ **bookings** table: Rental reservations

**All passwords are securely hashed using bcrypt!** 🔒

---

**Everything is now simple and working perfectly! 🎉**
