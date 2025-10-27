# 🔐 Admin Panel Guide

## Admin Access

### Default Admin Account
- **Login URL**: http://localhost:5000/admin/login
- **Username**: `admin`
- **Password**: `0707200717`

### Create New Admin Account
- **Signup URL**: http://localhost:5000/admin/signup
- **Required**: Admin Access Code: `0707200717`
- **Note**: All new admin accounts must use the access code `0707200717` to sign up

## Features

### 1. **Separate Login System**
- ✅ Customer Login - For regular users to book cars
- ✅ Admin Login - For administrators to manage inventory
- Orange/Red gradient button clearly distinguishes admin access

### 2. **Admin Dashboard**
- View total cars, categories, and bookings
- See all cars in a beautiful table format
- Quick access to add/edit/delete operations

### 3. **Add New Car**
- Form with all required fields:
  - Car Name
  - Category (Sedan, SUV, Sports, Luxury, Electric)
  - Price per day
  - Number of seats
  - Transmission type
  - Image URL
  - Features (comma-separated)
  - Color (optional)
- Real-time validation
- Success/error notifications

### 4. **Edit Car**
- Pre-filled form with existing car data
- Update any car details
- Same validation as add car
- Returns to dashboard after save

### 5. **Delete Car**
- Confirmation dialog before deletion
- Instant removal from inventory
- Cannot be undone (in-memory storage)

## How to Use

### Step 1: Start the Application
```bash
python app.py
```

### Step 2: Access Admin Panel

#### Option A: Login with Default Account
1. Go to http://localhost:5000
2. Click the orange "Admin Login" button in navigation
3. Enter credentials:
   - Username: `admin`
   - Password: `0707200717`

#### Option B: Create New Admin Account
1. Go to http://localhost:5000/admin/signup
2. Fill in the form:
   - Full Name
   - Username (must be unique)
   - Email (must be unique)
   - Admin Access Code: `0707200717`
3. Submit to create account and auto-login
4. Future logins use your chosen username and the access code as password

### Step 3: Manage Cars
- **View All Cars**: Automatically shown on dashboard
- **Add New Car**: Click "Add New Car" button
- **Edit Car**: Click "Edit" next to any car
- **Delete Car**: Click "Delete" next to any car (with confirmation)

## Security Features
- ✅ Access code required for admin signup (`0707200717`)
- ✅ Password-protected admin access
- ✅ Session-based authentication
- ✅ Admin routes require login
- ✅ Separate admin and customer sessions
- ✅ Username and email uniqueness validation
- ✅ Cannot create admin account without correct access code

## UI/UX Features
- 🎨 Orange/Red gradient for admin theme (distinct from purple customer theme)
- 📱 Fully responsive design
- ✨ Smooth animations and transitions
- 🔔 Success/error notifications
- 🛡️ Shield icons for admin branding
- 📊 Dashboard statistics cards
- 🎯 Color-coded category badges

## Notes
- Admin can view the public site by clicking "View Site"
- Admin session is separate from customer session
- Changes are stored in memory (will reset on server restart)
- For production, implement database storage
