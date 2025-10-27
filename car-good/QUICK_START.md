# 🚀 Quick Start Guide - LuxeDrive Car Rental

## Start the Application

```bash
python app.py
```

Visit: **http://localhost:5000**

---

## 👥 Customer Access

### Customer Login
- **URL**: http://localhost:5000/login
- **Action**: Sign up for a new account or login with existing account
- **Features**: Browse cars, make bookings, view booking history

### Customer Sign Up
- **URL**: http://localhost:5000/signup
- **Required**: Name, Email, Password
- **Bonus**: Get 20% discount on first booking after signup!

---

## 🛡️ Admin Access

### Default Admin Account
- **URL**: http://localhost:5000/admin/login
- **Username**: `admin`
- **Password**: `0707200717`

### Create New Admin Account
- **URL**: http://localhost:5000/admin/signup
- **Required Fields**:
  - Full Name
  - Username (unique)
  - Email (unique)
  - **Admin Access Code**: `0707200717` ⚠️ **REQUIRED**

### Admin Features
- ✅ View all cars in dashboard
- ✅ Add new cars
- ✅ Edit existing cars
- ✅ Delete cars
- ✅ View statistics (total cars, bookings, etc.)

---

## 🎯 Key Differences

| Feature | Customer | Admin |
|---------|----------|-------|
| **Theme Color** | Purple | Orange/Red |
| **Can Book Cars** | ✅ Yes | ❌ No |
| **Manage Inventory** | ❌ No | ✅ Yes |
| **Signup Requirement** | Email only | Access Code Required |
| **Password** | Custom | Must be `0707200717` |

---

## ⚡ Quick Actions

### For Customers:
1. Click "Customer Login" or "Sign Up" (purple button)
2. Browse cars by category
3. Select a car and book it
4. View your bookings in "My Bookings"

### For Admins:
1. Click "Admin" (orange button) or go to `/admin/login`
2. Login or signup with access code `0707200717`
3. Add/Edit/Delete cars from dashboard
4. View booking statistics

---

## 🔐 Security Note

**Admin Access Code `0707200717` is required for:**
- Creating new admin accounts
- This code becomes the password for all admin accounts
- Cannot create admin account without it
- Protects against unauthorized admin registration

---

## 📝 Important Notes

1. **In-Memory Storage**: All data (cars, bookings, accounts) is stored in memory
   - Data will be lost when server restarts
   - For production, implement database storage

2. **Discount System**:
   - 20% discount for new signups/logins (first booking only)
   - 50% discount for weekend bookings (Friday-Monday)

3. **Default Cars**: Application comes with 63 pre-loaded cars across 5 categories

4. **Mobile Friendly**: Fully responsive design works on all devices
