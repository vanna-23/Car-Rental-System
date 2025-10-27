# 🚗 LuxeDrive - Premium Car Rental System

A modern, full-featured car rental web application built with Python Flask, TailwindCSS, and MySQL.

## ✨ Features

### **Modern UI/UX**
- 🎨 Fully responsive design (mobile, tablet, desktop)
- ✨ Beautiful gradient backgrounds and smooth animations
- 🎯 Modern card-based layout with hover effects
- 🌈 Custom CSS with advanced animations

### **Premium Car Fleet**
- 🚗 63+ luxury and modern vehicles
- 📂 5 categories: Electric, SUV, Sports, Luxury, Sedan
- 🖼️ High-quality car images
- 📝 Detailed specifications and features

### **Smart Booking System**
- 📅 Automatic availability tracking
- 🔒 Booked cars disappear from listings
- ⚡ Real-time conflict detection
- 🎁 20% signup discount + 50% weekend discount
- 📊 Booking history and management

### **User Authentication**
- 🔐 Customer login and signup
- 👤 Session-based authentication
- 🛡️ Password protected accounts
- 💾 Persistent user data (with database)

### **Admin Panel**
- 🛡️ Separate admin authentication (admin/0707200717)
- ➕ Admin signup with access code
- ➕ Add new cars via navbar button
- ✏️ Edit existing cars
- 🗑️ Delete cars
- 📊 Dashboard with statistics
- 👥 View all bookings
- Social login UI (Google, Facebook)

📱 **Responsive Design**
- Mobile-first approach
- Hamburger menu for mobile devices
- Optimized layouts for all screen sizes
- Touch-friendly interface

## 🛠️ Tech Stack

- **Backend**: Python Flask 3.0.0
- **Database**: MySQL (optional - falls back to in-memory)
- **Frontend**: HTML5, TailwindCSS, JavaScript
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Google Fonts (Inter)

## 🚀 Quick Start

### **Option 1: Run Without Database (In-Memory)**
```bash
# 1. Navigate to project
cd "c:\Users\VANNA.LEN\Desktop\car-good - Copy\car-good"

# 2. Install dependencies
pip install Flask

# 3. Run application
python app.py

# 4. Open browser
http://localhost:5000
```

### **Option 2: Run With Database (Recommended)**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run database setup wizard
python setup_database.py

# 3. Run application
python app.py

# 4. Open browser
http://localhost:5000
```

**Default Admin:** `admin` / `0707200717`

## 📚 Documentation

- **START_HERE.md** - Complete getting started guide
- **QUICK_START.md** - Quick reference  
- **DATABASE_SETUP.md** - Database setup guide
- **QUICK_DATABASE_SETUP.md** - 5-minute database setup
- **ADMIN_GUIDE.md** - Admin panel documentation
- **BOOKING_SYSTEM.md** - How the booking system works

## 📁 Project Structure

```
car-good/
├── app.py                      # Main Flask application
├── db_config.py                # Database configuration
├── setup_database.py           # Database setup wizard
├── populate_cars.py            # Populate sample cars
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── static/
│   └── css/
│       └── custom.css          # Custom styles & animations
└── templates/
    ├── base.html               # Base template with navigation
    ├── index.html              # Home page
    ├── cars.html               # Car listing page
    ├── car_detail.html         # Car details page
    ├── login.html              # Customer login
    ├── signup.html             # Customer signup
    ├── bookings.html           # User bookings
    ├── about.html              # About page
    ├── contact.html            # Contact page
    └── admin/
        ├── login.html          # Admin login
        ├── signup.html         # Admin signup
        ├── dashboard.html      # Admin dashboard
        ├── add_car.html        # Add car form
        └── edit_car.html       # Edit car form
```

## Features Overview

### Home Page
- Hero section with call-to-action buttons
- Feature highlights (Premium Fleet, Fully Insured, 24/7 Support)
- Featured cars showcase
- Promotional CTA section

### Car Listing
- Filter by category (All, Luxury, Electric, Sports, SUV, Sedan)
- Grid layout with car cards
- Quick view of price and features

### Car Details
- Full car specifications
- Large car image
- Feature list
- Booking button
- Additional information (Insurance, Fuel, Mileage)

### Authentication
- Beautiful login form with email/password
- Sign up form with validation
- Password confirmation
- Social login buttons (UI only)
- Session management

## Car Categories

1. **Luxury** - Premium vehicles like Mercedes-Benz, Bentley, Lexus
2. **Electric** - Eco-friendly options like Tesla, Audi e-tron, Ford Mustang Mach-E
3. **Sports** - High-performance cars like Porsche 911, Lamborghini Huracán
4. **SUV** - Spacious vehicles like BMW X5, Range Rover Sport
5. **Sedan** - Elegant sedans like Audi A4

## Usage

### Creating an Account
1. Click "Sign Up" in the navigation
2. Fill in your name, email, and password
3. Accept terms and conditions
4. Click "Create Account"

### Logging In
1. Click "Login" in the navigation
2. Enter your email and password
3. Click "Sign In"

### Browsing Cars
1. Click "Cars" in the navigation or "Browse Cars" button
2. Filter by category using the filter buttons
3. Click "View Details" on any car for more information

### Viewing Car Details
- See full specifications
- Check availability status
- Features list
- Book the car if available

### Admin Panel Access
1. Go to http://localhost:5000/admin/login
2. Login with: `admin` / `0707200717`
3. Or signup with access code: `0707200717`

### Managing Cars (Admin)
- **Add Car**: Click green "Add Car" button in navbar
- **Edit Car**: Click "Edit" on any car in dashboard
- **Delete Car**: Click "Delete" with confirmation
- **View Stats**: Dashboard shows total cars, categories, bookings

## 🎯 Key Features Explained

### Smart Booking System
- Cars disappear when booked
- Return automatically when rental period ends
- Date conflict prevention
- Real-time availability checking

### Discount System
- **20% OFF**: First booking after signup/login
- **50% OFF**: Weekend bookings (Friday-Monday)
- **Auto-apply**: Discounts calculated automatically

### Security
- Session-based authentication
- Separate admin and customer sessions
- Admin access code required (`0707200717`)
- Password protected accounts

## 🌐 Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Homepage with featured cars |
| Browse Cars | `/cars` | All available cars with filters |
| Car Details | `/car/<id>` | Individual car information |
| Customer Login | `/login` | Customer authentication |
| Customer Signup | `/signup` | New customer registration |
| My Bookings | `/bookings` | User's rental history |
| Admin Login | `/admin/login` | Admin authentication |
| Admin Signup | `/admin/signup` | New admin registration |
| Admin Dashboard | `/admin/dashboard` | Car management |
| Add Car | `/admin/add-car` | Add new vehicle |
| Edit Car | `/admin/edit-car/<id>` | Modify vehicle |
| About | `/about` | About the company |
| Contact | `/contact` | Contact information |

## 🗄️ Database Schema (Optional)

### Tables
- **users** - Customer accounts
- **admin_accounts** - Admin users
- **cars** - Vehicle inventory
- **bookings** - Rental reservations

### Default Admin
- Username: `admin`
- Email: `admin@luxedrive.com`
- Password: `0707200717`

## 📱 Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🎨 Color Scheme

- **Primary**: Purple gradient (#667eea to #764ba2)
- **Admin**: Orange/Red gradient (#f97316 to #ea580c)
- **Success**: Green (#10b981)
- **Warning**: Yellow (#f59e0b)
- **Danger**: Red (#ef4444)

## 🚀 Deployment

For production deployment:
1. Change `app.secret_key` in app.py
2. Set up proper MySQL database
3. Configure environment variables
4. Use production WSGI server (e.g., Gunicorn)
5. Set `debug=False` in app.run()

## 📝 License

This project is for educational purposes.

## 👨‍💻 Developer

Built with ❤️ using Flask, TailwindCSS, and modern web technologies.

---

**Need help?** Check the documentation files or read START_HERE.md for complete setup instructions!
