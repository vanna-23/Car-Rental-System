from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
from db_config import get_db_connection
import json
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Sample car data with modern vehicles (keep this in memory as it's static)
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
    # ... rest of the cars
]

# ====== USER MANAGEMENT WITH MYSQL ======

def create_user(name, email, password):
    """Create a new user in the database"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, password))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_user_by_email(email):
    """Get user from database by email"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"Error getting user: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# ====== BOOKING MANAGEMENT WITH MYSQL ======

def create_booking_db(booking_data):
    """Create a new booking in the database"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO bookings (user_email, user_name, car_id, car_name, car_image,
                                pickup_date, return_date, days, total_cost, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            booking_data['user_email'],
            booking_data['user_name'],
            booking_data['car_id'],
            booking_data['car_name'],
            booking_data['car_image'],
            booking_data['pickup_date'],
            booking_data['return_date'],
            booking_data['days'],
            booking_data['total_cost'],
            booking_data['status']
        ))
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error creating booking: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_user_bookings(user_email):
    """Get all bookings for a user"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM bookings WHERE user_email = %s ORDER BY booking_date DESC"
        cursor.execute(query, (user_email,))
        bookings = cursor.fetchall()
        return bookings
    except Exception as e:
        print(f"Error getting bookings: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_booking_status(booking_id, user_email, status):
    """Update booking status"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = "UPDATE bookings SET status = %s WHERE id = %s AND user_email = %s"
        cursor.execute(query, (status, booking_id, user_email))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating booking: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# ====== ROUTES ======

@app.route('/')
def index():
    return render_template('index.html', cars=CARS)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        user = get_user_by_email(email)
        
        if user and user['password'] == password:
            session['user'] = email
            session['name'] = user['name']
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
        
        # Check if user exists
        if get_user_by_email(email):
            return jsonify({'success': False, 'message': 'Email already exists'}), 400
        
        # Create new user
        if create_user(name, email, password):
            session['user'] = email
            session['name'] = name
            return jsonify({'success': True, 'message': 'Account created successfully'})
        else:
            return jsonify({'success': False, 'message': 'Error creating account'}), 500
    
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
    booking_data = {
        'user_email': session['user'],
        'user_name': session['name'],
        'car_id': car_id,
        'car_name': car['name'],
        'car_image': car['image'],
        'pickup_date': pickup_date,
        'return_date': return_date,
        'days': days,
        'total_cost': total_cost,
        'status': 'confirmed'
    }
    
    booking_id = create_booking_db(booking_data)
    
    if booking_id:
        return jsonify({
            'success': True, 
            'message': 'Booking confirmed!',
            'booking_id': booking_id,
            'total_cost': total_cost,
            'days': days
        })
    else:
        return jsonify({'success': False, 'message': 'Error creating booking'}), 500

@app.route('/bookings')
def my_bookings():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user_bookings = get_user_bookings(session['user'])
    return render_template('bookings.html', bookings=user_bookings)

@app.route('/api/cancel-booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    success = update_booking_status(booking_id, session['user'], 'cancelled')
    
    if success:
        return jsonify({'success': True, 'message': 'Booking cancelled successfully'})
    else:
        return jsonify({'success': False, 'message': 'Booking not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
