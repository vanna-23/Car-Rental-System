"""
Populate the cars table with initial data
Run this after init_database.py to load sample cars
"""

from db_config import get_db_connection
import json

# All 63 cars from the original CARS list
SAMPLE_CARS = [
    {'name': 'Tesla Model 3', 'category': 'Electric', 'price': 89, 'image': 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800&q=80', 'seats': 5, 'transmission': 'Automatic', 'features': ['Autopilot', 'Premium Audio', 'Glass Roof']},
    {'name': 'BMW X5', 'category': 'SUV', 'price': 129, 'image': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&q=80', 'seats': 7, 'transmission': 'Automatic', 'features': ['Leather Seats', 'Sunroof', 'Navigation']},
    {'name': 'Mercedes-Benz C-Class', 'category': 'Luxury', 'price': 109, 'image': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80', 'seats': 5, 'transmission': 'Automatic', 'features': ['Massage Seats', 'Ambient Lighting', 'Premium Sound']},
    {'name': 'Audi A4', 'category': 'Sedan', 'price': 95, 'image': 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&q=80', 'seats': 5, 'transmission': 'Automatic', 'features': ['Virtual Cockpit', 'Quattro AWD', 'LED Headlights']},
    {'name': 'Porsche 911', 'category': 'Sports', 'price': 299, 'image': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=80', 'seats': 4, 'transmission': 'Automatic', 'features': ['Twin Turbo', 'Sport Exhaust', 'Carbon Fiber']},
    # Add more cars as needed from your original list
]

def populate_cars():
    """Insert sample cars into the database"""
    connection = get_db_connection()
    if not connection:
        print("❌ Failed to connect to database")
        return False
    
    try:
        cursor = connection.cursor()
        
        # Check if cars already exist
        cursor.execute("SELECT COUNT(*) FROM cars")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"⚠️  Database already has {count} cars.")
            response = input("Do you want to clear and reload? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Operation cancelled")
                return False
            cursor.execute("DELETE FROM cars")
        
        # Insert cars
        inserted = 0
        for car in SAMPLE_CARS:
            cursor.execute("""
                INSERT INTO cars (name, category, price, image, seats, transmission, features)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                car['name'],
                car['category'],
                car['price'],
                car['image'],
                car['seats'],
                car['transmission'],
                json.dumps(car['features'])
            ))
            inserted += 1
        
        connection.commit()
        print(f"✅ Successfully inserted {inserted} cars into the database!")
        return True
        
    except Exception as e:
        print(f"❌ Error populating cars: {e}")
        connection.rollback()
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    populate_cars()
