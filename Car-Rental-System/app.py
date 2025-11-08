from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, timedelta
import json
import os
import mysql.connector
from mysql.connector import Error, IntegrityError
from db_config import get_db_connection, init_database
from werkzeug.security import generate_password_hash, check_password_hash
from authlib.integrations.flask_client import OAuth
import secrets

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Google OAuth Configuration
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET', 'YOUR_GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)


def get_user_by_email(email):
    """Fetch a single user by email."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def normalize_phone(value):
    """Normalize phone numbers by stripping non-digit characters."""
    if not value:
        return ''
    return ''.join(ch for ch in value if ch.isdigit())


def create_user(fullname, email, phone, password_hash):
    """Insert a new user account."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
            (fullname, email, phone, password_hash)
        )
        conn.commit()
        return True
    except IntegrityError as e:
        print(f"Integrity error creating user: {e}")
        return False
    except Error as e:
        print(f"Error creating user: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Ensure required tables exist before handling requests
if not init_database():
    print("⚠️  Warning: Database initialization failed. Check MySQL service and credentials.")

# Database helper functions for cars
def get_all_cars():
    """Fetch all cars from database"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cars ORDER BY id")
        cars = cursor.fetchall()
        # Convert features from TEXT to list
        for car in cars:
            if car.get('features') and isinstance(car['features'], str):
                try:
                    car['features'] = json.loads(car['features'])
                except:
                    car['features'] = car['features'].split(',')
            car['price'] = float(car['price'])
        return cars
    except Error as e:
        print(f"Error fetching cars: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_car_by_id(car_id):
    """Fetch a single car by ID"""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
        car = cursor.fetchone()
        if car:
            if car.get('features') and isinstance(car['features'], str):
                try:
                    car['features'] = json.loads(car['features'])
                except:
                    car['features'] = car['features'].split(',')
            car['price'] = float(car['price'])
        return car
    except Error as e:
        print(f"Error fetching car: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Legacy CARS list for backward compatibility (will be replaced by database)
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
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQGtLLwBUnBDqn-MkvQQ_KkezWeRuHwcSGtQ&s',
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
        'image': 'https://image.klikk.no/2773779.webp?imageId=2773779&x=0.00&y=0.00&cropw=0.00&croph=0.00&width=1200&height=684&format=jpg',
        'seats': 7,
        'transmission': 'Automatic',
        'features': ['Falcon Doors', 'Autopilot', 'Bioweapon Defense']
    },
    {
        'id': 12,
        'name': 'Audi e-tron GT',
        'category': 'Electric',
        'price': 139,
        'image': 'https://www.topgear.com/sites/default/files/2025/04/2-Audi-e-tron-GT-performance-US-review-2025.jpg',
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
        'image': 'https://bugatti.imgix.net/677aa8b9531541bbada7c4e0e/chiron-sport-og.jpg',
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
        'image': 'https://media.autoexpress.co.uk/image/private/s--X-WVjvBW--/f_auto,t_content-image-full-desktop@1/v1689949597/evo/2023/07/Lucid%20Air%20Sapphire%20review-6.jpg',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['1200 HP', 'Ultra-Fast Charging', '500+ Mile Range']
    },
    {
        'id': 25,
        'name': 'Rivian R1T',
        'category': 'Electric',
        'price': 169,
        'image': 'https://www.gtplanet.net/wp-content/uploads/2018/11/Rivian-R1T-001.jpg',
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
        'image': 'https://www.pcarmarket.com/static/media/uploads/czmpydzvc3k24uh9m4pima0kga39m7sg-2024-10-14-5NJtDlDt/.thumbnails/Cover%20Photo%20Ratio.png/Cover%20Photo%20Ratio-tiny-1200x0.png',
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
        'image': 'https://car-images.bauersecure.com/wp-images/13039/amggtblack_050.jpg',
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
        'image': 'https://www.bentleymotors.com/content/dam/bm/websites/bmcom/bentleymotors-com/models/26my/bentayga-speed/Gallery%201.jpg/_jcr_content/renditions/original.image_file.1440.810.file/Gallery%201.jpg',
        'seats': 7,
        'transmission': 'Automatic',
        'features': ['W12 Engine', 'Luxury Interior', 'All-Terrain']
    },
    {
        'id': 38,
        'name': 'BMW i8',
        'category': 'Sports',
        'price': 259,
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgy268e2jTgzxURARYw2LDxWfJlhDxsSEHbQ&s',
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
        'image': 'https://article.images.consumerreports.org/image/upload/t_article_tout/v1750704800/prod/content/dam/CRO-Images-2025/Cars/CR-Cars-InlineHero-2025-Cadillac-Escalade-IQ-f-driving-6-25',
        'seats': 7,
        'transmission': 'Automatic',
        'features': ['V8 Engine', 'Premium Luxury', 'OLED Display']
    },
    {
        'id': 41,
        'name': 'Genesis GV80',
        'category': 'SUV',
        'price': 159,
        'image': 'https://preview.thenewsmarket.com/Previews/GEME/StillAssets/1920x1080/640485_v2.jpg',
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
        'id': 46,
        'name': 'Polestar 2',
        'category': 'Electric',
        'price': 149,
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Polestar_2_Genf_2019_1Y7A6000.jpg/1200px-Polestar_2_Genf_2019_1Y7A6000.jpg',
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
    },
    {
        'id': 51,
        'name': 'Mercedes-Benz S-Class',
        'category': 'Sedan',
        'price': 179,
        'image': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['V8 Engine', 'Executive Comfort', 'MBUX System']
    },
    {
        'id': 52,
        'name': 'BMW 7 Series',
        'category': 'Sedan',
        'price': 169,
        'image': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Luxury Seating', 'Gesture Control', 'Laser Headlights']
    },
    {
        'id': 53,
        'name': 'Audi A8',
        'category': 'Sedan',
        'price': 159,
        'image': 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Quattro AWD', 'Virtual Cockpit', 'Matrix LED']
    },
    {
        'id': 54,
        'name': 'Lexus ES 350',
        'category': 'Sedan',
        'price': 89,
        'image': 'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Smooth Ride', 'Luxury Interior', 'Safety Sense']
    },
    {
        'id': 55,
        'name': 'Porsche Panamera',
        'category': 'Sedan',
        'price': 219,
        'image': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=80',
        'seats': 4,
        'transmission': 'Automatic',
        'features': ['Twin-Turbo V8', 'Sport Chrono', 'Adaptive Air Suspension']
    },
    {
        'id': 56,
        'name': 'Tesla Model S',
        'category': 'Sedan',
        'price': 139,
        'image': 'https://images.unsplash.com/photo-1617788138017-80ad40651399?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Plaid Mode', 'Autopilot', '400+ Mile Range']
    },
    {
        'id': 57,
        'name': 'Genesis G90',
        'category': 'Sedan',
        'price': 149,
        'image': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['V6 Engine', 'Premium Luxury', 'Advanced Safety']
    },
    {
        'id': 58,
        'name': 'Cadillac CT5-V',
        'category': 'Sedan',
        'price': 129,
        'image': 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Supercharged V8', '668 HP', 'Magnetic Ride Control']
    },
    {
        'id': 59,
        'name': 'Jaguar XF',
        'category': 'Sedan',
        'price': 99,
        'image': 'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['British Elegance', 'Touch Pro Duo', 'All-Wheel Drive']
    },
    {
        'id': 60,
        'name': 'Maserati Quattroporte',
        'category': 'Sedan',
        'price': 189,
        'image': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Twin-Turbo V8', 'Italian Luxury', 'Sport Mode']
    },
    {
        'id': 61,
        'name': 'Lucid Air Grand Touring',
        'category': 'Sedan',
        'price': 199,
        'image': 'https://images.unsplash.com/photo-1617788138017-80ad40651399?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['800+ HP', 'Glass Canopy', 'DreamDrive Pro']
    },
    {
        'id': 62,
        'name': 'BMW i4 M50',
        'category': 'Sedan',
        'price': 119,
        'image': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Dual Motor', 'Curved Display', 'M Sport Brakes']
    },
    {
        'id': 63,
        'name': 'Mercedes-Benz EQS',
        'category': 'Sedan',
        'price': 209,
        'image': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80',
        'seats': 5,
        'transmission': 'Automatic',
        'features': ['Hyperscreen', 'Air Suspension', '350+ Mile Range']
    }
]

# Database helper functions for bookings
def get_all_bookings():
    """Fetch all bookings from database"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM bookings ORDER BY booking_date DESC")
        bookings = cursor.fetchall()
        # Convert dates and decimals to strings for JSON compatibility
        for booking in bookings:
            if booking.get('pickup_date'):
                booking['pickup_date'] = str(booking['pickup_date'])
            if booking.get('return_date'):
                booking['return_date'] = str(booking['return_date'])
            if booking.get('booking_date'):
                booking['booking_date'] = str(booking['booking_date'])
            if booking.get('base_cost'):
                booking['base_cost'] = float(booking['base_cost'])
            if booking.get('total_cost'):
                booking['total_cost'] = float(booking['total_cost'])
            if booking.get('discount_amount'):
                booking['discount_amount'] = float(booking['discount_amount'])
        return bookings
    except Error as e:
        print(f"Error fetching bookings: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_user_bookings(user_email):
    """Fetch bookings for a specific user"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM bookings WHERE user_email = %s ORDER BY booking_date DESC", (user_email,))
        bookings = cursor.fetchall()
        for booking in bookings:
            if booking.get('pickup_date'):
                booking['pickup_date'] = str(booking['pickup_date'])
            if booking.get('return_date'):
                booking['return_date'] = str(booking['return_date'])
            if booking.get('booking_date'):
                booking['booking_date'] = str(booking['booking_date'])
            if booking.get('base_cost'):
                booking['base_cost'] = float(booking['base_cost'])
            if booking.get('total_cost'):
                booking['total_cost'] = float(booking['total_cost'])
            if booking.get('discount_amount'):
                booking['discount_amount'] = float(booking['discount_amount'])
        return bookings
    except Error as e:
        print(f"Error fetching user bookings: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def create_booking(booking_data):
    """Create a new booking in database"""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bookings 
            (user_email, user_name, phone, car_id, car_name, car_image, 
             pickup_date, return_date, days, base_cost, discount_amount, 
             total_cost, discounts_applied, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            booking_data['user_email'],
            booking_data['user_name'],
            booking_data.get('phone', ''),
            booking_data['car_id'],
            booking_data['car_name'],
            booking_data.get('car_image', ''),
            booking_data['pickup_date'],
            booking_data['return_date'],
            booking_data['days'],
            booking_data['base_cost'],
            booking_data.get('discount_amount', 0),
            booking_data['total_cost'],
            booking_data.get('discounts_applied', ''),
            booking_data.get('status', 'confirmed')
        ))
        conn.commit()
        booking_id = cursor.lastrowid
        return booking_id
    except Error as e:
        print(f"Error creating booking: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def update_booking_status(booking_id, status):
    """Update booking status"""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE bookings SET status = %s WHERE id = %s", (status, booking_id))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating booking: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_booking_by_id(booking_id, user_email=None):
    """Fetch a specific booking by ID"""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        if user_email:
            cursor.execute("SELECT * FROM bookings WHERE id = %s AND user_email = %s", (booking_id, user_email))
        else:
            cursor.execute("SELECT * FROM bookings WHERE id = %s", (booking_id,))
        booking = cursor.fetchone()
        if booking:
            if booking.get('pickup_date'):
                booking['pickup_date'] = str(booking['pickup_date'])
            if booking.get('return_date'):
                booking['return_date'] = str(booking['return_date'])
            if booking.get('booking_date'):
                booking['booking_date'] = str(booking['booking_date'])
            if booking.get('base_cost'):
                booking['base_cost'] = float(booking['base_cost'])
            if booking.get('total_cost'):
                booking['total_cost'] = float(booking['total_cost'])
            if booking.get('discount_amount'):
                booking['discount_amount'] = float(booking['discount_amount'])
        return booking
    except Error as e:
        print(f"Error fetching booking: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def add_car_to_db(car_data):
    """Add a new car to database"""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        features_json = json.dumps(car_data.get('features', []))
        cursor.execute("""
            INSERT INTO cars (name, category, price, image, seats, transmission, features, color, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            car_data['name'],
            car_data['category'],
            car_data['price'],
            car_data.get('image', ''),
            car_data['seats'],
            car_data['transmission'],
            features_json,
            car_data.get('color', ''),
            car_data.get('status', 'available')
        ))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error adding car: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def update_car_in_db(car_id, car_data):
    """Update a car in database"""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        features_json = json.dumps(car_data.get('features', []))
        cursor.execute("""
            UPDATE cars 
            SET name = %s, category = %s, price = %s, image = %s, 
                seats = %s, transmission = %s, features = %s, color = %s
            WHERE id = %s
        """, (
            car_data['name'],
            car_data['category'],
            car_data['price'],
            car_data.get('image', ''),
            car_data['seats'],
            car_data['transmission'],
            features_json,
            car_data.get('color', ''),
            car_id
        ))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating car: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def delete_car_from_db(car_id):
    """Delete a car from database"""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cars WHERE id = %s", (car_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error deleting car: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Backward compatibility - will use database functions instead
bookings = []
booking_id_counter = 1

def get_admin_accounts():
    """Get all admin accounts from database"""
    conn = get_db_connection()
    if not conn:
        return {}
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin_accounts")
        admins = cursor.fetchall()
        # Convert to dictionary format keyed by normalized email
        admin_dict = {}
        for admin in admins:
            email_key = (admin.get('email') or '').strip().lower()
            if email_key:
                admin['email'] = email_key
                admin_dict[email_key] = admin
        return admin_dict
    except Error as e:
        print(f"Error fetching admins: {e}")
        return {}
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def create_admin(fullname, email, phone, password_hash):
    """Create a new admin account"""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO admin_accounts (fullname, email, phone, password) VALUES (%s, %s, %s, %s)",
            (fullname, email, phone, password_hash)
        )
        conn.commit()
        return True
    except Error as e:
        print(f"Error creating admin: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def is_car_available(car_id):
    """
    Check if a car is currently available (not booked).
    Returns True if the car has no active bookings.
    """
    today = datetime.now().date()
    all_bookings = get_all_bookings()
    
    for booking in all_bookings:
        if booking['car_id'] == car_id and booking['status'] == 'confirmed':
            # Parse booking dates
            pickup = datetime.strptime(booking['pickup_date'], '%Y-%m-%d').date()
            return_date = datetime.strptime(booking['return_date'], '%Y-%m-%d').date()
            
            # Check if today falls within the booking period
            if pickup <= today <= return_date:
                return False
    
    return True

def get_available_cars():
    """
    Get list of all available cars (not currently booked).
    """
    all_cars = get_all_cars()
    return [car for car in all_cars if is_car_available(car['id'])]

def check_weekend_discount(pickup_date, return_date):
    """
    Check if the rental period includes Saturday or Sunday.
    Returns True if any day in the rental period is Saturday or Sunday.
    🎉 30% OFF for weekend rentals!
    """
    try:
        pickup = datetime.strptime(pickup_date, '%Y-%m-%d')
        return_dt = datetime.strptime(return_date, '%Y-%m-%d')
        
        # Check each day in the rental period
        current_date = pickup
        while current_date <= return_dt:
            # weekday(): Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4, Saturday=5, Sunday=6
            day_of_week = current_date.weekday()
            # Check if it's Saturday (5) or Sunday (6)
            if day_of_week in [5, 6]:
                return True
            current_date += timedelta(days=1)
        
        return False
    except:
        return False

@app.route('/')
def index():
    available_cars = get_available_cars()
    featured_cars = available_cars[:6]  # Show first 6 available cars as featured
    return render_template('index.html', featured_cars=featured_cars)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Customer login - only requires email and password"""
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form or {}

        if not isinstance(data, dict):
            data = data.to_dict()

        email = (data.get('email') or '').strip()
        password = data.get('password')

        # Only require email and password (normal login)
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400

        # Get user from MySQL database
        user = get_user_by_email(email)
        if not user:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

        # Verify password with MySQL stored hash
        stored_password = user.get('password')
        password_matches = False

        if stored_password:
            try:
                # Verify hashed password from MySQL
                password_matches = check_password_hash(stored_password, password)
            except (ValueError, TypeError):
                # Fall back to plain text comparison for old accounts
                password_matches = stored_password == password

        if not password_matches:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

        # Login successful - Create session
        session['user'] = email
        session['name'] = user.get('name') or email
        session['login_discount'] = True  # Set 20% login discount
        
        return jsonify({'success': True, 'message': 'Login successful'})

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Customer signup - requires password confirmation"""
    if request.method == 'POST':
        data = request.get_json()
        fullname = data.get('fullname')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if not all([fullname, email, phone, password, confirm_password]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        # Check if passwords match
        if password != confirm_password:
            return jsonify({'success': False, 'message': 'Passwords do not match'}), 400
            
        if get_user_by_email(email):
            return jsonify({'success': False, 'message': 'Email already exists'}), 400
        
        password_hash = generate_password_hash(password)
        if not create_user(fullname, email, phone, password_hash):
            return jsonify({'success': False, 'message': 'Unable to create account at this time. Please try again.'}), 500

        session['user'] = email
        session['name'] = fullname
        session['login_discount'] = True
        return jsonify({'success': True, 'message': 'Account created successfully'})
    
    return render_template('signup.html')

# Google OAuth Routes
@app.route('/auth/google')
def google_login():
    """Initiate Google OAuth login"""
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/google/callback')
def google_callback():
    """Handle Google OAuth callback"""
    try:
        # Get token from Google
        token = google.authorize_access_token()
        
        # Get user info from Google
        user_info = token.get('userinfo')
        
        if not user_info:
            return jsonify({'success': False, 'message': 'Failed to get user info from Google'}), 400
        
        email = user_info.get('email')
        name = user_info.get('name', email)
        google_id = user_info.get('sub')
        
        if not email:
            return jsonify({'success': False, 'message': 'Email not provided by Google'}), 400
        
        # Check if user exists
        user = get_user_by_email(email)
        
        if user:
            # User exists - just login
            session['user'] = email
            session['name'] = user.get('name') or name
            session['login_discount'] = True
            session['google_user'] = True
            return redirect(url_for('index'))
        else:
            # New user - create account with Google info
            # Generate a random phone placeholder since Google doesn't provide it
            phone = f"GOOGLE_{google_id[:10]}"
            
            # Create account with random secure password (user won't need it for Google login)
            random_password = secrets.token_urlsafe(32)
            password_hash = generate_password_hash(random_password)
            
            if create_user(name, email, phone, password_hash):
                # Account created successfully
                session['user'] = email
                session['name'] = name
                session['login_discount'] = True
                session['google_user'] = True
                return redirect(url_for('index'))
            else:
                return jsonify({'success': False, 'message': 'Failed to create account'}), 500
                
    except Exception as e:
        print(f"Google OAuth error: {e}")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/cars')
def cars():
    category = request.args.get('category', 'all')
    available_cars = get_available_cars()
    
    if category == 'all':
        filtered_cars = available_cars
    else:
        filtered_cars = [car for car in available_cars if car['category'].lower() == category.lower()]
    return render_template('cars.html', cars=filtered_cars, selected_category=category)

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = get_car_by_id(car_id)
    if car:
        available = is_car_available(car_id)
        return render_template('car_detail.html', car=car, available=available)
    return "Car not found", 404

@app.route('/api/check-session')
def check_session():
    if 'admin' in session:
        return jsonify({'logged_in': False, 'admin': True, 'admin_name': session.get('admin_name')})
    if 'user' in session:
        return jsonify({'logged_in': True, 'name': session.get('name'), 'admin': False})
    return jsonify({'logged_in': False, 'admin': False})

@app.route('/book/<int:car_id>', methods=['POST'])
def book_car(car_id):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Please login to book a car'}), 401
    
    data = request.get_json()
    pickup_date = data.get('pickup_date')
    return_date = data.get('return_date')
    
    if not pickup_date or not return_date:
        return jsonify({'success': False, 'message': 'Please provide pickup and return dates'}), 400
    
    # Find the car
    car = get_car_by_id(car_id)
    if not car:
        return jsonify({'success': False, 'message': 'Car not found'}), 404
    
    # Check if car is available for the requested dates
    try:
        pickup = datetime.strptime(pickup_date, '%Y-%m-%d').date()
        return_dt = datetime.strptime(return_date, '%Y-%m-%d').date()
        
        # Check for conflicting bookings
        all_bookings = get_all_bookings()
        for booking in all_bookings:
            if booking['car_id'] == car_id and booking['status'] == 'confirmed':
                booking_pickup = datetime.strptime(booking['pickup_date'], '%Y-%m-%d').date()
                booking_return = datetime.strptime(booking['return_date'], '%Y-%m-%d').date()
                
                # Check if dates overlap
                if not (return_dt < booking_pickup or pickup > booking_return):
                    return jsonify({'success': False, 'message': 'Car is not available for the selected dates. Please choose different dates.'}), 400
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid date format'}), 400
    
    # Calculate total days and cost
    try:
        pickup = datetime.strptime(pickup_date, '%Y-%m-%d')
        return_dt = datetime.strptime(return_date, '%Y-%m-%d')
        days = (return_dt - pickup).days
        
        if days <= 0:
            return jsonify({'success': False, 'message': 'Return date must be after pickup date'}), 400
        
        # Calculate base cost
        base_cost = car['price'] * days
        total_cost = base_cost
        
        # Apply discounts
        discounts_applied = []
        discount_amount = 0
        
        # Check for weekend discount (Saturday & Sunday) - 30% off
        weekend_discount = check_weekend_discount(pickup_date, return_date)
        if weekend_discount:
            weekend_discount_amount = base_cost * 0.3
            discount_amount += weekend_discount_amount
            discounts_applied.append('🎉 Weekend Special (30%)')
        
        # Check for login/signup discount - 20% off
        if session.get('login_discount', False):
            login_discount_amount = base_cost * 0.2
            discount_amount += login_discount_amount
            discounts_applied.append('Login Bonus (20%)')
            # Remove the discount flag after first use
            session.pop('login_discount', None)
        
        # Apply total discount
        total_cost = base_cost - discount_amount
        # Ensure cost doesn't go below 0
        total_cost = max(total_cost, 0)
        
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid date format'}), 400
    
    # Get user info from database
    user = get_user_by_email(session['user'])
    
    # Create booking data
    booking_data = {
        'user_email': session['user'],
        'user_name': session['name'],
        'phone': user.get('phone', '') if user else '',
        'car_id': car_id,
        'car_name': car['name'],
        'car_image': car.get('image', ''),
        'pickup_date': pickup_date,
        'return_date': return_date,
        'days': days,
        'base_cost': base_cost,
        'discount_amount': discount_amount,
        'discounts_applied': ', '.join(discounts_applied),
        'total_cost': total_cost,
        'status': 'confirmed'
    }
    
    # Save to database
    booking_id = create_booking(booking_data)
    
    if not booking_id:
        return jsonify({'success': False, 'message': 'Failed to create booking'}), 500
    
    return jsonify({
        'success': True, 
        'message': 'Booking confirmed!',
        'booking_id': booking_id,
        'base_cost': base_cost,
        'discount_amount': discount_amount,
        'discounts_applied': discounts_applied,
        'total_cost': total_cost,
        'days': days
    })

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
    
    booking = get_booking_by_id(booking_id, session['user'])
    
    if not booking:
        return jsonify({'success': False, 'message': 'Booking not found'}), 404
    
    if update_booking_status(booking_id, 'cancelled'):
        return jsonify({'success': True, 'message': 'Booking cancelled successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to cancel booking'}), 500

# ---------- Admin Authentication ----------

@app.route('/admin/login', methods=['GET'])
def admin_login_page():
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/login.html')


@app.route('/admin/login', methods=['POST'])
def admin_login():
    """Admin login - requires all 4 fields: fullname, email, phone, and password"""
    data = request.get_json(silent=True) or request.form or {}

    if not isinstance(data, dict):
        data = data.to_dict()

    fullname = (data.get('fullname') or '').strip()
    email = (data.get('email') or '').strip().lower()
    phone = (data.get('phone') or '').strip()
    password = data.get('password')

    # Require all 4 fields
    if not fullname or not email or not phone or not password:
        return jsonify({'success': False, 'message': 'All fields are required (Full Name, Email, Phone, Password)'}), 400

    # Get admin from MySQL database
    admins = get_admin_accounts()
    admin = admins.get(email)

    if not admin:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    # Validate all 4 fields match the database
    stored_fullname = (admin.get('fullname') or '').strip()
    stored_phone = normalize_phone(admin.get('phone') or '')
    input_phone = normalize_phone(phone)
    stored_password = admin.get('password')
    
    # Check fullname match (case-insensitive)
    if stored_fullname.lower() != fullname.lower():
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    # Check phone match
    if stored_phone != input_phone:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    # Check password (supports both hashed and plain text)
    password_matches = False
    if stored_password:
        try:
            # Try hashed password first
            password_matches = check_password_hash(stored_password, password)
        except (ValueError, TypeError):
            # Fallback to plain text comparison (for legacy accounts)
            password_matches = stored_password == password

    if not password_matches:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    # Login successful - all 4 fields matched
    session['admin'] = email
    session['admin_name'] = admin.get('fullname')
    return jsonify({'success': True, 'message': 'Admin login successful'})

# Admin dashboard route
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login_page'))
    
    # Fetch all cars from database
    cars = get_all_cars()
    
    # Get total bookings count
    total_bookings = 0
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as count FROM bookings")
            result = cursor.fetchone()
            total_bookings = result['count'] if result else 0
            cursor.close()
            conn.close()
    except Exception as e:
        print(f"Error fetching bookings count: {e}")

    return render_template('admin/dashboard.html', 
                         cars=cars, 
                         total_cars=len(cars),
                         total_bookings=total_bookings)


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    session.pop('admin_name', None)
    return redirect(url_for('admin_login_page'))


@app.route('/admin/create', methods=['POST'])
def admin_create():
    if 'admin' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    data = request.get_json(silent=True) or request.form or {}

    if not isinstance(data, dict):
        data = data.to_dict()

    fullname = (data.get('fullname') or '').strip()
    email = (data.get('email') or '').strip().lower()
    phone = (data.get('phone') or '').strip()
    password = data.get('password')

    if not all([fullname, email, phone, password]):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    admins = get_admin_accounts()
    if email in admins:
        return jsonify({'success': False, 'message': 'Admin with this email already exists'}), 400

    password_hash = generate_password_hash(password)
    if not create_admin(fullname, email, phone, password_hash):
        return jsonify({'success': False, 'message': 'Failed to create admin account'}), 500

    return jsonify({'success': True, 'message': 'Admin account created successfully'})


@app.route('/admin/update/<int:admin_id>', methods=['PUT'])
def admin_update(admin_id):
    if 'admin' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    data = request.get_json()
    updates = {key: value for key, value in data.items() if value}

    if not updates:
        return jsonify({'success': False, 'message': 'No updates provided'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        fields = []
        values = []

        if 'fullname' in updates:
            fields.append('fullname = %s')
            values.append(updates['fullname'])

        if 'email' in updates:
            fields.append('email = %s')
            values.append(updates['email'].strip().lower())

        if 'phone' in updates:
            fields.append('phone = %s')
            values.append(updates['phone'])

        if 'password' in updates:
            fields.append('password = %s')
            values.append(generate_password_hash(updates['password']))

        if not fields:
            return jsonify({'success': False, 'message': 'No valid fields to update'}), 400

        values.append(admin_id)
        query = f"UPDATE admin_accounts SET {', '.join(fields)} WHERE id = %s"
        cursor.execute(query, tuple(values))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'success': False, 'message': 'Admin not found'}), 404

        return jsonify({'success': True, 'message': 'Admin updated successfully'})
    except Error as e:
        print(f"Error updating admin: {e}")
        return jsonify({'success': False, 'message': 'Failed to update admin'}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/admin/delete/<int:admin_id>', methods=['DELETE'])
def admin_delete(admin_id):
    if 'admin' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM admin_accounts WHERE id = %s", (admin_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'success': False, 'message': 'Admin not found'}), 404

        return jsonify({'success': True, 'message': 'Admin deleted successfully'})
    except Error as e:
        print(f"Error deleting admin: {e}")
        return jsonify({'success': False, 'message': 'Failed to delete admin'}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/admin/add-car', methods=['GET', 'POST'])
def admin_add_car():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        data = request.get_json()
        
        car_data = {
            'name': data.get('name'),
            'category': data.get('category'),
            'price': data.get('price'),
            'image': data.get('image', ''),
            'seats': data.get('seats'),
            'transmission': data.get('transmission'),
            'features': data.get('features', []),
            'color': data.get('color', ''),
            'status': 'available'
        }
        
        car_id = add_car_to_db(car_data)
        if car_id:
            return jsonify({'success': True, 'message': 'Car added successfully', 'car_id': car_id})
        else:
            return jsonify({'success': False, 'message': 'Failed to add car'}), 500
    
    return render_template('admin/add_car.html')

@app.route('/admin/edit-car/<int:car_id>', methods=['GET', 'POST'])
def admin_edit_car(car_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    
    car = get_car_by_id(car_id)
    if not car:
        return "Car not found", 404
    
    if request.method == 'POST':
        data = request.get_json()
        
        car_data = {
            'name': data.get('name'),
            'category': data.get('category'),
            'price': data.get('price'),
            'seats': data.get('seats'),
            'transmission': data.get('transmission'),
            'image': data.get('image', ''),
            'features': data.get('features', []),
            'color': data.get('color', '')
        }
        
        if update_car_in_db(car_id, car_data):
            return jsonify({'success': True, 'message': 'Car updated successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to update car'}), 500
    
    return render_template('admin/edit_car.html', car=car)

@app.route('/admin/delete-car/<int:car_id>', methods=['POST'])
def admin_delete_car(car_id):
    if 'admin' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    if delete_car_from_db(car_id):
        return jsonify({'success': True, 'message': 'Car deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Car not found or failed to delete'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
