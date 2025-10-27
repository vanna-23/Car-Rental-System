from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, timedelta
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

# Simple user storage (in production, use a database)
users = {}
bookings = []
booking_id_counter = 1

# Admin accounts storage
admin_accounts = {
    'admin': {
        'name': 'Administrator',
        'username': 'admin',
        'email': 'admin@luxedrive.com',
        'password': '0707200717'
    }
}

def is_car_available(car_id):
    """
    Check if a car is currently available (not booked).
    Returns True if the car has no active bookings.
    """
    today = datetime.now().date()
    
    for booking in bookings:
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
    return [car for car in CARS if is_car_available(car['id'])]

def check_weekend_discount(pickup_date, return_date):
    """
    Check if the rental period includes Friday to Monday.
    Returns True if any day in the rental period is Friday, Saturday, Sunday, or Monday.
    """
    try:
        pickup = datetime.strptime(pickup_date, '%Y-%m-%d')
        return_dt = datetime.strptime(return_date, '%Y-%m-%d')
        
        # Check each day in the rental period
        current_date = pickup
        while current_date <= return_dt:
            # weekday(): Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4, Saturday=5, Sunday=6
            day_of_week = current_date.weekday()
            # Check if it's Friday (4), Saturday (5), Sunday (6), or Monday (0)
            if day_of_week in [0, 4, 5, 6]:
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
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if email in users and users[email]['password'] == password:
            session['user'] = email
            session['name'] = users[email]['name']
            session['login_discount'] = True  # Set 20% login discount
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
        session['login_discount'] = True  # Set 20% signup discount
        return jsonify({'success': True, 'message': 'Account created successfully'})
    
    return render_template('signup.html')

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
    car = next((car for car in CARS if car['id'] == car_id), None)
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
    
    # Check if car is available for the requested dates
    try:
        pickup = datetime.strptime(pickup_date, '%Y-%m-%d').date()
        return_dt = datetime.strptime(return_date, '%Y-%m-%d').date()
        
        # Check for conflicting bookings
        for booking in bookings:
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
        
        # Check for weekend discount (Friday to Monday) - 50% off
        weekend_discount = check_weekend_discount(pickup_date, return_date)
        if weekend_discount:
            weekend_discount_amount = base_cost * 0.5
            discount_amount += weekend_discount_amount
            discounts_applied.append('Weekend Special (50%)')
        
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
        'base_cost': base_cost,
        'discount_amount': discount_amount,
        'discounts_applied': discounts_applied,
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

# Admin Routes
ADMIN_ACCESS_CODE = '0707200717'

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Check if username exists in admin_accounts
        if username in admin_accounts and admin_accounts[username]['password'] == password:
            session['admin'] = True
            session['admin_name'] = admin_accounts[username]['name']
            session['admin_username'] = username
            return jsonify({'success': True, 'message': 'Admin login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid admin credentials'}), 401
    
    return render_template('admin/login.html')

@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        username = data.get('username')
        email = data.get('email')
        access_code = data.get('accessCode')
        
        # Validate access code
        if access_code != ADMIN_ACCESS_CODE:
            return jsonify({'success': False, 'message': 'Invalid access code. Admin registration requires correct access code.'}), 403
        
        # Check if username already exists
        if username in admin_accounts:
            return jsonify({'success': False, 'message': 'Username already exists'}), 400
        
        # Check if email already exists
        for admin in admin_accounts.values():
            if admin['email'] == email:
                return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        # Create new admin account
        admin_accounts[username] = {
            'name': name,
            'username': username,
            'email': email,
            'password': access_code  # Using access code as password
        }
        
        # Auto login after signup
        session['admin'] = True
        session['admin_name'] = name
        session['admin_username'] = username
        
        return jsonify({'success': True, 'message': 'Admin account created successfully'})
    
    return render_template('admin/signup.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    session.pop('admin_name', None)
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    
    return render_template('admin/dashboard.html', cars=CARS, total_cars=len(CARS), total_bookings=len(bookings))

@app.route('/admin/add-car', methods=['GET', 'POST'])
def admin_add_car():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        data = request.get_json()
        
        # Get the next available ID
        max_id = max([car['id'] for car in CARS]) if CARS else 0
        new_id = max_id + 1
        
        new_car = {
            'id': new_id,
            'name': data.get('name'),
            'category': data.get('category'),
            'price': data.get('price'),
            'image': data.get('image'),
            'seats': data.get('seats'),
            'transmission': data.get('transmission'),
            'features': data.get('features', [])
        }
        
        if data.get('color'):
            new_car['color'] = data.get('color')
        
        CARS.append(new_car)
        return jsonify({'success': True, 'message': 'Car added successfully', 'car_id': new_id})
    
    return render_template('admin/add_car.html')

@app.route('/admin/edit-car/<int:car_id>', methods=['GET', 'POST'])
def admin_edit_car(car_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    
    car = next((car for car in CARS if car['id'] == car_id), None)
    if not car:
        return "Car not found", 404
    
    if request.method == 'POST':
        data = request.get_json()
        
        car['name'] = data.get('name')
        car['category'] = data.get('category')
        car['price'] = data.get('price')
        car['seats'] = data.get('seats')
        car['transmission'] = data.get('transmission')
        car['image'] = data.get('image')
        car['features'] = data.get('features', [])
        
        if data.get('color'):
            car['color'] = data.get('color')
        elif 'color' in car:
            del car['color']
        
        return jsonify({'success': True, 'message': 'Car updated successfully'})
    
    return render_template('admin/edit_car.html', car=car)

@app.route('/admin/delete-car/<int:car_id>', methods=['POST'])
def admin_delete_car(car_id):
    if 'admin' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    global CARS
    car = next((car for car in CARS if car['id'] == car_id), None)
    
    if not car:
        return jsonify({'success': False, 'message': 'Car not found'}), 404
    
    CARS = [car for car in CARS if car['id'] != car_id]
    return jsonify({'success': True, 'message': 'Car deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
