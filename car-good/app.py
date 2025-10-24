from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Sample car data with modern vehicles
CARS = [
    {
        'id': 1,
        'name': 'Tesla Model 3',
        'category': 'Electric',
        'price': 89,
        'image': 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Autopilot', 'Premium Audio', 'Glass Roof']
    },
    {
        'id': 2,
        'name': 'BMW X5',
        'category': 'SUV',
        'price': 129,
        'image': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&q=80',
        'seats': 7,
        'transmission': 'Automatic',
        'features': ['Leather Seats', 'Sunroof', 'Navigation']
    },
    {
        'id': 3,
        'name': 'Mercedes-Benz C-Class',
        'category': 'Luxury',
        'price': 109,
        'image': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Massage Seats', 'Ambient Lighting', 'Premium Sound']
    },
    {
        'id': 4,
        'name': 'Audi A4',
        'category': 'Sedan',
        'price': 95,
        'image': 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Virtual Cockpit', 'Quattro AWD', 'LED Headlights']
    },
    {
        'id': 5,
        'name': 'Porsche 911',
        'category': 'Sports',
        'price': 299,
        'image': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['Sport Exhaust', 'Carbon Brakes', 'Track Mode']
    },
    {
        'id': 6,
        'name': 'Range Rover Sport',
        'category': 'SUV',
        'price': 149,
        'image': 'https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=800&q=80',
        'seats': 7,
        'transmission': 'Automatic',
        'features': ['Terrain Response', 'Meridian Audio', 'Air Suspension']
    },
    {
        'id': 7,
        'name': 'Lamborghini Huracán',
        'category': 'Sports',
        'price': 499,
        'image': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['Carbon Fiber', 'Launch Control', 'Sport Mode']
    },
    {
        'id': 8,
        'name': 'Lamborghini Aventador',
        'category': 'Sports',
        'price': 599,
        'image': 'https://images.unsplash.com/photo-1621135802920-133df287f89c?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['V12 Engine', 'Scissor Doors', 'All-Wheel Drive']
    },
    {
        'id': 9,
        'name': 'Lamborghini Urus',
        'category': 'SUV',
        'price': 399,
        'image': 'https://www.autoforum.cz/tmp/magazin/ls/Lamborghini_Urus_nove_01_660_0.jpg',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Twin-Turbo V8', 'Sport Seats', 'Dynamic Steering']
    },
    {
        'id': 10,
        'name': 'Lamborghini Revuelto',
        'category': 'Sports',
        'price': 699,
        'image': 'https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['Hybrid V12', 'Active Aero', 'Carbon Monocoque']
    },
    {
        'id': 11,
        'name': 'Tesla Model X',
        'category': 'Electric',
        'price': 119,
        'image': 'https://images.unsplash.com/photo-1617788138017-80ad40651399?w=800&q=80',
        'seats': 7,
        'transmission': 'Automatic',
        'features': ['Falcon Doors', 'Autopilot', 'Bioweapon Defense']
    },
    {
        'id': 12,
        'name': 'Audi e-tron GT',
        'category': 'Electric',
        'price': 139,
        'image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Fast Charging', 'Matrix LED', 'Sport Suspension']
    },
    {
        'id': 13,
        'name': 'Bentley Continental GT',
        'category': 'Luxury',
        'price': 399,
        'image': 'https://images.unsplash.com/photo-1563720360172-67b8f3dce741?w=800&q=80',
        'seats': 4,
        'transmission': 'Automatic',
        'features': ['Handcrafted Interior', 'Rotating Display', 'Naim Audio']
    },
    {
        'id': 14,
        'name': 'Ford Mustang Mach-E',
        'category': 'Electric',
        'price': 79,
        'image': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['BlueCruise', 'B&O Sound', 'Panoramic Roof']
    },
    {
        'id': 15,
        'name': 'Lexus LS 500',
        'category': 'Luxury',
        'price': 119,
        'image': 'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Mark Levinson Audio', 'Kiriko Glass', 'Safety System+']
    },
    {
        'id': 16,
        'name': 'Lamborghini Gallardo ',
        'category': 'Sports',
        'price': 449,
        'image': 'https://images.unsplash.com/photo-1525609004556-c46c7d6cf023?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['V10 Engine', 'Sport Exhaust', 'Carbon Ceramic Brakes'],
        'color': 'Red'
    },
    {
        'id': 17,
        'name': 'Lamborghini Sián',
        'category': 'Sports',
        'price': 799,
        'image': 'https://images.unsplash.com/photo-1544829099-b9a0c07fad1a?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['Hybrid V12', 'Supercapacitor Tech', 'Limited Edition'],
        'color': 'Red'
    },
    {
        'id': 18,
        'name': 'Lamborghini Murciélago',
        'category': 'Sports',
        'price': 549,
        'image': 'https://cdn-ds.com/blogs-media/sites/350/2023/06/21145221/DSC6730-Edit-3-1024x683.jpg',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['V12 Engine', 'Scissor Doors', 'Race Inspired Design'],
        'color': 'Red'
    },
    {
        'id': 19,
        'name': 'Ferrari SF90 Stradale',
        'category': 'Sports',
        'price': 899,
        'image': 'https://images.unsplash.com/photo-1592198084033-aade902d1aae?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['Hybrid V8', 'Electric AWD', '986 HP'],
        'color': 'Rosso Corsa'
    },
    {
        'id': 20,
        'name': 'McLaren 720S',
        'category': 'Sports',
        'price': 649,
        'image': 'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['Twin-Turbo V8', 'Dihedral Doors', 'Carbon Fiber Body']
    },
    {
        'id': 21,
        'name': 'Bugatti Chiron',
        'category': 'Sports',
        'price': 1999,
        'image': 'https://bugatti.imgix.net/677aa8b9531541bbada7c4e0/chiron-sport-og.jpg',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['Quad-Turbo W16', '1500 HP', 'Ultra-Luxury Interior']
    },
    {
        'id': 22,
        'name': 'Rolls-Royce Phantom',
        'category': 'Luxury',
        'price': 599,
        'image': 'https://images.unsplash.com/photo-1631295868223-63265b40d9e4?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['V12 Engine', 'Starlight Headliner', 'Bespoke Interior']
    },
    {
        'id': 23,
        'name': 'Aston Martin DB12',
        'category': 'Luxury',
        'price': 449,
        'image': 'https://images.unsplash.com/photo-1609521263047-f8f205293f24?w=800&q=80',
        'seats': 4,
        'transmission': 'Automatic',
        'features': ['Twin-Turbo V8', 'Luxury Craftsmanship', 'British Elegance']
    },
    {
        'id': 24,
        'name': 'Lucid Air Sapphire',
        'category': 'Electric',
        'price': 259,
        'image': 'https://images.unsplash.com/photo-1617788138017-80ad40651399?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['1200 HP', 'Ultra-Fast Charging', '500+ Mile Range']
    },
    {
        'id': 25,
        'name': 'Rivian R1T',
        'category': 'Electric',
        'price': 169,
        'image': 'https://images.unsplash.com/photo-1664574654529-b60630f33fdb?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Quad-Motor', 'Off-Road Package', 'Adventure Gear Tunnel']
    },
    {
        'id': 26,
        'name': 'Maserati MC20',
        'category': 'Sports',
        'price': 549,
        'image': 'https://images.unsplash.com/photo-1619767886558-efdc259cde1a?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['V6 Nettuno Engine', 'Butterfly Doors', 'Italian Design']
    },
    {
        'id': 27,
        'name': 'Bugatti Chiron Sport',
        'category': 'Sports',
        'price': 2199,
        'image': 'https://p.turbosquid.com/ts-thumb/kd/BgAxfs/RCjQ5G0e/bugatti_chiron_pur_sport_2021_0000/jpg/1585905496/600x600/fit_q87/c9abf198fd6a69e7ad1dfbdeb76edf7ca9a3e963/bugatti_chiron_pur_sport_2021_0000.jpg',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['W16 Engine', 'Lighter Weight', 'Sport Handling Package'],
        'color': 'Atlantic Blue'
    },
    {
        'id': 28,
        'name': 'Bugatti Chiron Pur Sport',
        'category': 'Sports',
        'price': 2499,
        'image': 'https://exclusivecarregistry.com/images/gallery/car/full/370222',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['W16 Engine', 'Track-Focused', '1500 HP', 'Lightweight Build'],
        'color': 'Black'
    },
    {
        'id': 29,
        'name': 'Bugatti Chiron Super Sport 300+',
        'category': 'Sports',
        'price': 2799,
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWXrq9prWLa0-1G2KCusKRTNeInXT_x03DRH_C6EUApSAvMYSKvRzpvff5f9rUrsWovCc&usqp=CAU',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['W16 Engine', '304 MPH Top Speed', 'Long Tail Design', '1600 HP'],
        'color': 'Orange'
    },
    {
        'id': 30,
        'name': 'Bugatti Chiron Profilée',
        'category': 'Sports',
        'price': 2999,
        'image': 'https://i.bstr.es/highmotor/2022/12/04-BUGATTI_CHIRON-Profilee-1220x813.jpg',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['W16 Engine', 'Limited Edition', 'Aerodynamic Design', 'Final Chiron'],
        'color': 'Blue'
    },
    {
        'id': 31,
        'name': 'Ferrari 296 GTB',
        'category': 'Sports',
        'price': 749,
        'image': 'https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['Hybrid V6', 'Plug-in Electric', '819 HP']
    },
    {
        'id': 32,
        'name': 'Porsche Taycan Turbo S',
        'category': 'Electric',
        'price': 289,
        'image': 'https://images.unsplash.com/photo-1614162692292-7ac56d7f3c8d?w=800&q=80',
        'seats': 4,
        'transmission': 'Automatic',
        'features': ['750 HP', 'Fast Charging', 'Sport Chrono']
    },
    {
        'id': 33,
        'name': 'McLaren Artura',
        'category': 'Sports',
        'price': 599,
        'image': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['Hybrid V6', 'Carbon Fiber', '671 HP']
    },
    {
        'id': 34,
        'name': 'Mercedes-AMG GT Black Series',
        'category': 'Sports',
        'price': 699,
        'image': 'https://images.unsplash.com/photo-1606016159991-4a1a7d5bfa6d?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['Twin-Turbo V8', '720 HP', 'Track Performance']
    },
    {
        'id': 35,
        'name': 'Koenigsegg Jesko',
        'category': 'Sports',
        'price': 3499,
        'image': 'https://images.unsplash.com/photo-1542282088-fe8426682b8f?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['Twin-Turbo V8', '1600 HP', 'Swedish Engineering']
    },
    {
        'id': 36,
        'name': 'Pagani Huayra',
        'category': 'Sports',
        'price': 2799,
        'image': 'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['Twin-Turbo V12', 'Carbon-Titanium', 'Italian Art']
    },
    {
        'id': 37,
        'name': 'Bentley Bentayga Speed',
        'category': 'SUV',
        'price': 449,
        'image': 'https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=800&q=80',
        'seats': 7,
        'transmission': 'Automatic',
        'features': ['W12 Engine', 'Luxury Interior', 'All-Terrain']
    },
    {
        'id': 38,
        'name': 'BMW i8',
        'category': 'Sports',
        'price': 259,
        'image': 'https://images.unsplash.com/photo-1555652510-d8e4692b86c5?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['Hybrid', 'Butterfly Doors', 'Futuristic Design']
    },
    {
        'id': 39,
        'name': 'Acura NSX',
        'category': 'Sports',
        'price': 329,
        'image': 'https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['Hybrid V6', 'AWD', 'Sport Hybrid SH-AWD']
    },
    {
        'id': 40,
        'name': 'Cadillac Escalade',
        'category': 'SUV',
        'price': 189,
        'image': 'https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=800&q=80',
        'seats': 7,
        'transmission': 'Automatic',
        'features': ['V8 Engine', 'Premium Luxury', 'OLED Display']
    },
    {
        'id': 41,
        'name': 'Genesis GV80',
        'category': 'SUV',
        'price': 159,
        'image': 'https://images.unsplash.com/photo-1617788138017-80ad40651399?w=800&q=80',
        'seats': 7,
        'transmission': 'Automatic',
        'features': ['Twin-Turbo V6', 'Luxury Craftsmanship', 'Advanced Safety']
    },
    {
        'id': 42,
        'name': 'Jaguar F-Type R',
        'category': 'Sports',
        'price': 379,
        'image': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['Supercharged V8', '575 HP', 'British Style']
    },
    {
        'id': 43,
        'name': 'Alfa Romeo Giulia Quadrifoglio',
        'category': 'Sedan',
        'price': 229,
        'image': 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Twin-Turbo V6', '505 HP', 'Italian Performance']
    },
    {
        'id': 44,
        'name': 'Lotus Evora GT',
        'category': 'Sports',
        'price': 299,
        'image': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['Supercharged V6', 'Lightweight', 'Track Ready']
    },
    {
        'id': 45,
        'name': 'Chevrolet Corvette C8',
        'category': 'Sports',
        'price': 249,
        'image': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800&q=80',
        'seats': 2,
        'transmission': 'Automatic',
        'features': ['Mid-Engine V8', '495 HP', 'American Supercar']
    },
    {
        'id': 46,
        'name': 'Polestar 2',
        'category': 'Electric',
        'price': 149,
        'image': 'https://images.unsplash.com/photo-1617788138017-80ad40651399?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Dual Motor', 'Google Integration', 'Scandinavian Design']
    },
    {
        'id': 47,
        'name': 'BMW M5 Competition',
        'category': 'Sedan',
        'price': 329,
        'image': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Twin-Turbo V8', '617 HP', 'M xDrive AWD']
    },
    {
        'id': 48,
        'name': 'Mercedes-Maybach S-Class',
        'category': 'Luxury',
        'price': 549,
        'image': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['V12 Engine', 'Executive Rear Seats', 'Ultimate Luxury']
    },
    {
        'id': 49,
        'name': 'Nissan GT-R Nismo',
        'category': 'Sports',
        'price': 349,
        'image': 'https://images.unsplash.com/photo-1544829099-b9a0c07fad1a?w=800&q=80',
        'seats': 4,
        'transmission': 'Automatic',
        'features': ['Twin-Turbo V6', '600 HP', 'Godzilla Performance']
    },
    {
        'id': 50,
        'name': 'Aston Martin DBS Superleggera',
        'category': 'Sports',
        'price': 699,
        'image': 'https://images.unsplash.com/photo-1609521263047-f8f205293f24?w=800&q=80',
        'seats': 4,
        'transmission': 'Automatic',
        'features': ['Twin-Turbo V12', '715 HP', 'James Bond Style']
    }
]

# Simple user storage (in production, use a database)
users = {}
bookings = []
booking_id_counter = 1

@app.route('/')
def index():
    return render_template('index.html', cars=CARS)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if email in users and users[email]['password'] == password:
            session['user'] = email
            session['name'] = users[email]['name']
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if email in users:
            return jsonify({'success': False, 'message': 'Email already exists'}), 400
        
        users[email] = {'name': name, 'password': password}
        session['user'] = email
        session['name'] = name
        return jsonify({'success': True, 'message': 'Account created successfully'})
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/cars')
def cars():
    category = request.args.get('category', 'all')
    if category == 'all':
        filtered_cars = CARS
    else:
        filtered_cars = [car for car in CARS if car['category'].lower() == category.lower()]
    return render_template('cars.html', cars=filtered_cars, selected_category=category)

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = next((car for car in CARS if car['id'] == car_id), None)
    if car:
        return render_template('car_detail.html', car=car)
    return "Car not found", 404

@app.route('/api/check-session')
def check_session():
    if 'user' in session:
        return jsonify({'logged_in': True, 'name': session.get('name')})
    return jsonify({'logged_in': False})

@app.route('/book/<int:car_id>', methods=['POST'])
def create_booking(car_id):
    global booking_id_counter
    
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Please login to book a car'}), 401
    
    data = request.get_json()
    pickup_date = data.get('pickup_date')
    return_date = data.get('return_date')
    
    if not pickup_date or not return_date:
        return jsonify({'success': False, 'message': 'Please provide pickup and return dates'}), 400
    
    # Find the car
    car = next((car for car in CARS if car['id'] == car_id), None)
    if not car:
        return jsonify({'success': False, 'message': 'Car not found'}), 404
    
    # Calculate total days and cost
    try:
        pickup = datetime.strptime(pickup_date, '%Y-%m-%d')
        return_dt = datetime.strptime(return_date, '%Y-%m-%d')
        days = (return_dt - pickup).days
        
        if days <= 0:
            return jsonify({'success': False, 'message': 'Return date must be after pickup date'}), 400
        
        total_cost = car['price'] * days
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid date format'}), 400
    
    # Create booking
    booking = {
        'id': booking_id_counter,
        'user_email': session['user'],
        'user_name': session['name'],
        'car_id': car_id,
        'car_name': car['name'],
        'car_image': car['image'],
        'pickup_date': pickup_date,
        'return_date': return_date,
        'days': days,
        'total_cost': total_cost,
        'status': 'confirmed',
        'booking_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    bookings.append(booking)
    booking_id_counter += 1
    
    return jsonify({
        'success': True, 
        'message': 'Booking confirmed!',
        'booking_id': booking['id'],
        'total_cost': total_cost,
        'days': days
    })

@app.route('/bookings')
def my_bookings():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user_bookings = [b for b in bookings if b['user_email'] == session['user']]
    return render_template('bookings.html', bookings=user_bookings)

@app.route('/api/cancel-booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    booking = next((b for b in bookings if b['id'] == booking_id and b['user_email'] == session['user']), None)
    
    if not booking:
        return jsonify({'success': False, 'message': 'Booking not found'}), 404
    
    booking['status'] = 'cancelled'
    return jsonify({'success': True, 'message': 'Booking cancelled successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
