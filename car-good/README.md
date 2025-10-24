# LuxeDrive - Premium Car Rental System

A modern, responsive car rental web application built with Python Flask and TailwindCSS.

## Features

✨ **Modern UI/UX**
- Fully responsive design that works on all devices (mobile, tablet, desktop)
- Beautiful gradient backgrounds and smooth animations
- Modern card-based layout

🚗 **Premium Car Fleet**
- 12 luxury and modern vehicles
- Multiple categories: Luxury, Electric, Sports, SUV, Sedan
- High-quality car images from Unsplash
- Detailed car specifications and features

🔐 **User Authentication**
- Login and Sign Up functionality
- Session management
- Password protected accounts
- Social login UI (Google, Facebook)

📱 **Responsive Design**
- Mobile-first approach
- Hamburger menu for mobile devices
- Optimized layouts for all screen sizes
- Touch-friendly interface

## Tech Stack

- **Backend**: Python Flask 3.0.0
- **Frontend**: HTML5, TailwindCSS, JavaScript
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Google Fonts (Inter)

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd car-good
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser and visit**
   ```
   http://localhost:5000
   ```

## Project Structure

```
car-good/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── templates/            # HTML templates
    ├── base.html         # Base template with navigation
    ├── index.html        # Home page
    ├── login.html        # Login page
    ├── signup.html       # Sign up page
    ├── cars.html         # Car listing page
    └── car_detail.html   # Individual car details
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
- Check features and pricing
- Click "Book Now" to start rental process (UI only)

## Notes

- This is a demo application for educational purposes
- User data is stored in memory and will be lost when the server restarts
- For production use, implement a proper database (PostgreSQL, MongoDB, etc.)
- Add proper password hashing (bcrypt, argon2)
- Implement actual booking and payment processing
- Add email verification for new accounts
- Implement proper session security

## Future Enhancements

- 🗄️ Database integration (SQLAlchemy/PostgreSQL)
- 💳 Payment processing (Stripe/PayPal)
- 📧 Email notifications
- 📅 Booking calendar system
- 👤 User dashboard
- ⭐ Car reviews and ratings
- 🔍 Advanced search and filters
- 📊 Admin panel

## License

This project is open source and available for educational purposes.

## Author

Created with ❤️ for learning and demonstration purposes.
