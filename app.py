from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from flask_cors import CORS
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__, template_folder='templates')
CORS(app)

# Configure JWT
app.config['JWT_SECRET_KEY'] = 'DBMT@123'

# JWT authorization
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)


pass_word = "ABCDabcd123$"

conn = mysql.connector.connect(
host="localhost",
user="root",
password=pass_word,
database="TMS"
)

cursor = conn.cursor()


# login signup code --------------------------------------------------

@app.route('/')
def home():
    return redirect(url_for('welcome_page'))

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@app.route('/welcome', methods=['GET'])
def welcome_page():
    return render_template('welcome.html')

@app.route('/signup_user', methods=['GET'])
def signup_user():
    return render_template('signup_user.html')

@app.route('/signup_user_submission', methods=['POST'])
def signup_user_submission():
    data = request.get_json()
    print("Received JSON data:", data)

    # Step 2: Insert into CUSTOMER table
    insert_customer = """
    INSERT INTO CUSTOMER (customer_email, customer_status, customer_latitude, customer_longitude)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_customer, (
        data['email'],
        'Active',
        '0.0',
        '0.0'
    ))

 
    insert_registration = """
    INSERT INTO CUSTOMER_REGISTRATION (
        customer_email, customer_registration_date,
        first_name, middle_name, last_name,
        phone_number, gender, password, age, dob
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    dob = datetime.strptime(data['birthdate'], "%Y-%m-%d").date()
    age = datetime.now().year - dob.year

    cursor.execute(insert_registration, (
        data['email'],
        datetime.now().date(),
        data['firstname'],
        data['middlename'],
        data['lastname'],
        data['phone'],
        data['gender'],
        data['password'],  # Password
        age,
        dob
    ))
    conn.commit()


    
    return jsonify({'message': 'Success'}), 200




@app.route('/signup_driver', methods=['GET'])
def signup_driver():
    return render_template('signup_driver.html')

@app.route('/signup_driver_submission', methods=['POST'])
def submit_driver():
    print("getting the call")
    data = request.get_json()
    print("Received Driver Data:", data)
    
    
    vehicle = data['vehicle']
    insert_vehicle = """
    INSERT INTO VEHICLE (make, model, plate_number, type, ac_non, ownership)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    vehicle_values = (
        vehicle['make'],  # Make is not in the frontend data
        vehicle['model'],
        vehicle['plate_number'],
        vehicle['type'],
        vehicle['ac_non'],
        'personal' if data['vehicle_type'] == 'vehicle' else 'company'
    )
    cursor.execute(insert_vehicle, vehicle_values)
    
    
    insert_driver = """
        INSERT INTO DRIVER (
            driver_email, plate_number, driver_status, driver_availability,
            driver_latitude, driver_longitude, avg_earnings, avg_rating,
            positve_review_count, negative_review_count
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    driver_values = (
        data['email'],
        vehicle['plate_number'],
        'Active',
        'available',
        '0.0',    # Default location
        '0.0',    # Default location
        0.0,      # Default earnings
        0,        # Default rating
        0,        # Default positive reviews
        0         # Default negative reviews
    )
    cursor.execute(insert_driver, driver_values)

    # Step 4: Insert into DRIVER_REGISTRATION table
    insert_registration = """
    INSERT INTO DRIVER_REGISTRATION (
        driver_email, license_id, first_name, middle_name, last_name,
        phone_number, license_expiry, gender, dob, password,
        age, address, city, pincode, registration_date
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    registration_values = (
        data['email'],
        data['license_id'],
        data['first_name'],
        data['middle_name'],
        data['last_name'],
        data['phone_number'],
        data['license_expiry'],
        data['gender'],
        data['dob'],
        data['password'],
        data['age'],
        data['address'],
        data['city'],
        data['pincode'],
        datetime.now().date()
    )
    cursor.execute(insert_registration, registration_values)

    # Commit all inserts
    conn.commit()
    print("Driver data inserted successfully!")
    return jsonify({'message': 'Driver license data received'}), 200


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get("role")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    
    print(email)
    print(password)
    print(role)
    print(latitude)
    print(longitude)
    
    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400
    
    if role == "user":
        cursor.execute("SELECT customer_email, password FROM CUSTOMER_REGISTRATION WHERE customer_email = %s", (email,))
        user = cursor.fetchone()
        if user is None:
            return jsonify({"msg": "User not found"}), 404
        db_email, db_password = user[0], user[1]
    else:
        cursor.execute("SELECT driver_email, password FROM DRIVER_REGISTRATION WHERE driver_email = %s", (email,))
        user = cursor.fetchone()
        if user is None:
            return jsonify({"msg": "User not found"}), 404
        db_email, db_password = user[0], user[1]
    if password == db_password:
        token = create_access_token(identity=email)
        if role == "user":
            print(latitude, longitude)
            cursor.execute("UPDATE CUSTOMER SET customer_latitude = %s , customer_longitude = %s WHERE customer_email = %s",(latitude, longitude, email))
            conn.commit()
        else:
            cursor.execute("UPDATE Driver SET driver_latitude = %s , driver_longitude = %s WHERE driver_email = %s",(latitude, longitude, email))
            conn.commit()
            
        return jsonify({"access_token" : token, "role": role}), 200
    else:
        return jsonify({"msg": "Incorrect password"}), 401
    
# ------------------------------------------------------------------------------


# customer driver code
# --------------------------------------------------------------------



@app.route('/customer_dashboard', methods=['GET'])
def cusomter_dashboard():
    print("customer dashboard")
    return render_template('customer_dashboard.html')

@app.route("/api/ride_history", methods=["GET"])
@jwt_required()
def ride_history():
    current_user = get_jwt_identity()  
    print(f"Fetching rides for: {current_user}")
    cursor.execute("""
            SELECT pickup_location, drop_location, start_time, end_time,
                   fare, ride_status
            FROM RIDE
            WHERE customer_email = %s
              AND ride_status IN ('completed', 'canceled')
            ORDER BY end_time DESC
        """, (current_user,))

    past_rides = cursor.fetchall()
    formatted = []
    for row in past_rides:
        formatted.append({
            "starting_location": row[0],
            "destination": row[1],
            "starting_time": row[2].strftime("%Y-%m-%d %H:%M:%S"),
            "ending_time": row[3].strftime("%Y-%m-%d %H:%M:%S"),
            "fare": float(row[4]) if row[4] else None,
            "status": row[5]
        })
    print(formatted)        
    return jsonify(formatted), 200

from geopy.geocoders import Nominatim

def get_address(lat, lon):
    geolocator = Nominatim(user_agent="taxi_app")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    return location.address if location else "Address not found"

@app.route("/api/customer_dashboard", methods=["GET"])
@jwt_required()
def api_customer_dashboard():
    print("API customer dashboard")
    current_user = get_jwt_identity()
    resp = check_payment_status(current_user)
    review_resp = check_review_status(current_user)
    print("payment status", resp)
    print("review status", review_resp)
    if resp["status"] == True:
        query = """
            SELECT
                dr.phone_number
            FROM driver_registration dr
            WHERE dr.driver_email = %s
        """
        cursor.execute(query, (resp["payment_details"]["driver_email"],))
        user_info = cursor.fetchone()
        return jsonify({
            "status": "payment_pending",
            "payment_details": resp["payment_details"],
            "driver": user_info[0]
        })
    elif review_resp["status"] == True:
        return jsonify({
            "status": "review_pending",
        })
    else:
        query = """
            SELECT
                c.customer_email,
                c.customer_status,
                c.customer_latitude,
                c.customer_longitude,
                r.first_name,
                r.middle_name,
                r.last_name,
                r.phone_number,
                r.gender,
                r.age,
                r.dob
            FROM CUSTOMER c
            JOIN CUSTOMER_REGISTRATION r ON c.customer_email = r.customer_email
            WHERE c.customer_email = %s
        """
        cursor.execute(query, (current_user,))
        user_info = cursor.fetchone()
        print(user_info)
        start_point  = get_address(user_info[2], user_info[3])
        return jsonify({
            "status": "ok",
            "user": user_info,
            "start_point": start_point
        })
        
        
def check_payment_status(x):
    try:
        print(x)
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT * FROM RIDE
            WHERE customer_email = %s AND fare_status = 'pending' AND ride_status IN ('start_ride', 'completed')
        """
        cursor.execute(query, (x,))
        ride = cursor.fetchone()
        if ride:
            ride['start_time'] = str(ride['start_time'])
            ride['end_time'] = str(ride['end_time'])
            ride['total_time'] = str(ride['total_time'])
            return {"status": True, "payment_details": ride}
        else:
            return {"status": False}

    except mysql.connector.Error as err:
        print("DB Error:", err)
        return {"status": False, "error": str(err)}

        
def check_review_status(x):
    try:
        print(x)
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT * FROM RIDE
            WHERE customer_email = %s AND review_status = 'pending' and  ride_status IN ('start_ride', 'completed')
        """
        cursor.execute(query, (x,))
        ride = cursor.fetchone()
        if ride:
            ride['start_time'] = str(ride['start_time'])
            ride['end_time'] = str(ride['end_time'])
            ride['total_time'] = str(ride['total_time'])
            return {"status": True, "review_details": ride}
        else:
            return {"status": False}

    except mysql.connector.Error as err:
        print("DB Error:", err)
        return {"status": False, "error": str(err)}



import openrouteservice

def get_road_distance_ors(client, coords):
    route = client.directions(
        coordinates=coords,
        profile='driving-car',
        format='geojson'
    )
    dist = route['features'][0]['properties']['segments'][0]['distance']  # in meters
    dur = route['features'][0]['properties']['segments'][0]['duration']  # in seconds
    return dist, dur

client = openrouteservice.Client(key='5b3ce3597851110001cf6248643e4b831fe946878759ceb53567e481')
from geopy.geocoders import Nominatim

def get_lat_lon(address):
    geolocator = Nominatim(user_agent="taxi_app")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None, None

            
@app.route("/book_ride", methods=["POST"])
@jwt_required()
def book_ride():
    data = request.get_json()  
    source = data.get('starting_location')
    destination = data.get('destination')
    seats = data.get('seats')

    fare = 9.22 
    duration = ''
    miles = 0.0
    try:
        source_lat, source_lon = get_lat_lon(source)
        dest_lat, dest_lon = get_lat_lon(destination)
      
        coords = [[source_lon, source_lat], [dest_lon, dest_lat]]
        distance, duration = get_road_distance_ors(client, coords)
        duration = str(round(duration/60, 2))+' mins'

        miles = distance / 1609.34
        if miles<5:
            fare=5.34
        elif miles<10:
            fare = 8.99
    except:
        pass
    start_time = data.get('starting_time')
    current_user = get_jwt_identity()
        
    print("Book ride API")
    print(source, destination, start_time, current_user, seats)  
    print(miles)
    print(duration)  
    cursor = conn.cursor()
    if len(source) > 100:
        source = source[0:99]
    query = """
    INSERT INTO RIDE (
    customer_email, driver_email, pickup_location, drop_location,
    start_time, ride_status, fare, fare_status,review_status, total_time, duration, distance, seat_requested
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)
    """

    values = (
        current_user,         # customer_email
        None,                 # driver_email (to be assigned later)
        source,               # pickup_location
        destination,          # drop_location
        start_time,           # start_time
                   # end_time (same initially)
        'scheduled',          # ride_status
        fare,                 # fare 
        'pending',            # fare status
        'pending',            # review_status
        '00:00:00',            # total_time (placeholder)
        duration,
        miles,
        seats
    )

    cursor.execute(query, values)
    conn.commit()
    return jsonify({
        "status": "success"
    })


@app.route("/process_payment", methods=["POST"])
@jwt_required()
def process_payment():
    data = request.get_json()

    card_holder = data.get("card_holder")
    card_number = data.get("card_number")
    expiry_date = data.get("expiry_date")
    cvv = data.get("cvv")
    customer_email = get_jwt_identity()

    print("Processing payment for:", customer_email)
    print("Card Holder:", card_holder)
    print("Card Number:", card_number)
    print("Expiry:", expiry_date)
    print("CVV:", cvv)

    cursor.execute("""
            SELECT ride_id, driver_email FROM RIDE
            WHERE customer_email = %s AND ride_status IN ('start_ride', 'completed') AND fare_status = 'pending' 
            ORDER BY end_time DESC
            LIMIT 1
        """, (customer_email,))
    ride = cursor.fetchone()
    print(ride)
    ride_id, driver_email = ride
    
    cursor.execute("""
            UPDATE RIDE
            SET fare_status = %s
            WHERE ride_id = %s
        """, ('completed',ride_id))
    
    cursor.execute("""
            INSERT INTO PAYMENT (
                ride_id, payment_method, payment_date,
                payment_status, customer_email, driver_email
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            ride_id,
            'card',
            datetime.now(),  # current datetime
            'completed',
            customer_email,
            driver_email
        ))

    conn.commit()

        
    return jsonify({"status": "success", "message": "Payment processed"})


@app.route('/review_page', methods=['GET'])
def review_page_auth():
    return render_template('review_page.html')

@app.route('/api/review_page', methods=['GET'])
@jwt_required()
def review_page():
    current_user = get_jwt_identity()
    review_resp = check_review_status(current_user)
    
    return jsonify({"review_resp": review_resp}), 200

from transformers import pipeline
sentiment_model = pipeline(model="AshBunny/finetuning-sentiment-model-5000-samples")

def generate_sentiment(text):
    if text:
        res = sentiment_model([text])
        ans = ""
        if res[0]["label"] == "LABEL_1":
            ans = "positive"
        else:
            ans = "negative"
        
        return ans
    else:
        return "no"

@app.route("/rate_driver", methods=["POST"])
@jwt_required()
def rate_driver():
    data = request.get_json()
    ride_id = data.get("ride_id")
    customer_email = data.get("customer_email")
    driver_email = data.get("driver_email")
    customer_rating = data.get("customer_rating")
    feedback = data.get("feedback")
    sentiment = generate_sentiment(feedback)
    print("ride id ", ride_id)
    print(customer_email)
    print(driver_email)
    print(customer_rating)
    print(feedback)
    print("sentiment ",sentiment)
    
    cursor.execute("""
            INSERT INTO RATINGS (
                ride_id, customer_email, driver_email, customer_rating, feedback
            ) VALUES (%s, %s, %s, %s, %s)
        """, (ride_id, customer_email, driver_email, customer_rating, feedback))

    cursor.execute("""
        UPDATE RIDE
        SET review_status = 'completed'
        WHERE ride_id = %s
    """, (ride_id,))

    cursor.execute("""
        SELECT avg_rating, positve_review_count, negative_review_count
        FROM DRIVER WHERE driver_email = %s
    """, (driver_email,))
    result = cursor.fetchone()

    if result:
        current_avg, pos_count, neg_count = result
        if current_avg is None:
            current_avg = customer_rating
            pos_count = 0
            neg_count = 0
        else:
            current_avg = int((int(current_avg) + int(customer_rating)) / 2)

        if sentiment == "positive":
            pos_count += 1
        elif sentiment == "negative":
            neg_count += 1

        cursor.execute("""
            UPDATE DRIVER
            SET avg_rating = %s,
                positve_review_count = %s,
                negative_review_count = %s
            WHERE driver_email = %s
        """, (current_avg, pos_count, neg_count, driver_email))

    conn.commit()
    
    return jsonify({"status":"success"})
    

@app.route("/driver_dashboard", methods=["GET"])
def driver_dashboard_auth():
    return render_template("driver_dashboard.html")


@app.route("/api/driver_dashboard", methods= ["GET", "POST"])
@jwt_required()
def driver_dashboard():
    driver_email = get_jwt_identity()
    cursor.execute("""
            SELECT
                ride_id,
                customer_email,
                driver_email,
                pickup_location,
                drop_location,
                start_time,
                seat_requested,
                end_time,
                ride_status,
                fare,
                review_status,
                total_time,
                duration,
                distance
            FROM RIDE
        """)
    all_rides = cursor.fetchall()
    columns = [
    "ride_id", "customer_email", "driver_email",
    "pickup_location", "drop_location",
    "start_time", "seats", "end_time", "ride_status",
    "fare", "review_status", "total_time", "duration", "distance"
    ]
    ride_dicts = [dict(zip(columns, row)) for row in all_rides]
    now = datetime.now()
    threshold = now + timedelta(minutes=10)
    print(ride_dicts)
    unassigned = []
    for ride in ride_dicts:
        start_time = ride["start_time"]
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

        if ride["driver_email"] is None and start_time - timedelta(minutes=30) <= now <= start_time + timedelta(minutes=30):
            print(ride["customer_email"])
            unassigned.append(ride)
    print(unassigned)

    for ride in unassigned:
        ride["start_time"] = ride["start_time"].strftime("%Y-%m-%d %H:%M:%S")
        # ride["end_time"] = ride["end_time"].strftime("%Y-%m-%d %H:%M:%S")
        ride["fare"] = float(ride["fare"]) if ride["fare"] else None
        ride["total_time"] = str(ride["total_time"]) if ride["total_time"] else None
        ride["duration"] = str(ride["duration"]) if ride["duration"] else None
    print(driver_email)
    cursor.execute("SELECT * FROM driver_registration dr INNER JOIN driver d ON dr.driver_email = d.driver_email WHERE dr.driver_email = %s",(driver_email,))
    drivers = cursor.fetchone()
    # print("drivers", drivers)
    return jsonify({"unassigned":unassigned, "driver_details": drivers}), 200

@app.route("/api/driver_dashboard_stats", methods= ["GET", "POST"])
@jwt_required()
def driver_dashboard_stats():
    driver_email = get_jwt_identity()
    cursor.execute("SELECT * FROM driver_registration dr INNER JOIN driver d ON dr.driver_email = d.driver_email WHERE dr.driver_email = %s",(driver_email,))
    drivers = cursor.fetchone()
    return jsonify({"driver_details": drivers}), 200

    
    
@app.route("/give_ride", methods=["POST"])
@jwt_required()
def give_ride():
    data = request.get_json()
    ride_id = data.get("ride_id")
    driver_email = get_jwt_identity()
    print(ride_id)
    print(driver_email)
    cursor.execute("SELECT driver_availability FROM DRIVER WHERE driver_email = %s", (driver_email,))
    result = cursor.fetchone()

    if not result:
        return jsonify({"status": "error", "message": "Driver not found"}), 404

    availability = result[0]
    if availability != "available":
        return jsonify({
            "status": "error",
            "message": f"Driver is currently '{availability}' and cannot pick a new ride."
        }), 400
        
    
    cursor.execute("""
        UPDATE RIDE SET driver_email = %s, ride_status = %s WHERE ride_id = %s AND driver_email IS NULL
    """, (driver_email, 'active',ride_id))
    conn.commit()
    
    # SMS code
    # code for sending the sms message  
    # from twilio.rest import Client

    # # Twilio credentials from your Twilio account
    # account_sid = 'ACe5ee06752d24c0439be0076a72c36734'
    # auth_token = '3c709a8a80d38189df5b562f9662457a'
    # client = Client(account_sid, auth_token)

    # message = client.messages.create(
    # body="Driver accepted your ride!",
    # from_='+18334365086', # twilio generated number
    # to='+17132563352'      # Your phone number
    # )

    # print(f"Message sent with SID: {message.sid}")


    return jsonify({"status": "success", "message": "Ride successfully assigned"})


@app.route("/api/driver_active_rides", methods=["GET"])
@jwt_required()
def driver_active_rides():
    driver_email = get_jwt_identity()
    cursor.execute("""
        SELECT * FROM RIDE
        WHERE driver_email = %s AND ride_status IN ('active', 'start_ride')
        ORDER BY start_time DESC
    """, (driver_email,))
    rows = cursor.fetchall()

    formatted = []
    for ride in rows:
        formatted.append({
            "ride_id": ride[0],
            "customer_email": ride[1],
            "driver_email": ride[2],
            "pickup_location": ride[3],
            "drop_location": ride[4],
            "start_time": ride[5].strftime("%Y-%m-%d %H:%M:%S"),
            'seats': ride[6],
            "end_time": '',
            "ride_status": ride[8],
            "fare": float(ride[9]) if ride[8] is not None else None,
            "review_status": ride[10],
            "total_time": str(ride[11]),
            "duration": str(ride[12]),
            "distance" : str(ride[13])
        })
    print(formatted)
    return jsonify({"unassigned": formatted}), 200


@app.route('/api/driver_past_rides')
@jwt_required()
def get_past_rides():
    driver_email = get_jwt_identity()
    query = """
            SELECT ride_id, customer_email, pickup_location, drop_location,
                   start_time, end_time, fare, ride_status, distance, duration
            FROM RIDE
            WHERE driver_email = %s AND ride_status = 'completed'
            ORDER BY end_time DESC
        """
    cursor.execute(query, (driver_email,))
    rides = cursor.fetchall()

    result = []
    for ride in rides:
        result.append({
            'ride_id': ride[0],
            'customer_email': ride[1],
            'pickup_location': ride[2],
            'drop_location': ride[3],
            'start_time': ride[4].strftime('%Y-%m-%d %H:%M'),
            'end_time': ride[5].strftime('%Y-%m-%d %H:%M'),
            'fare': float(ride[6]) if ride[6] is not None else 0.0,
            'ride_status': ride[7],
            'distance' : float(ride[8]),
            'duration' : ride[9]
        })

    return jsonify(result), 200




    
@app.route("/update_ride_status", methods=["POST"])
@jwt_required()
def update_ride_status():
    data = request.get_json()
    ride_id = data.get("ride_id")
    action = data.get("action")
    driver_email = get_jwt_identity()
    print(ride_id)
    print(action)
    print(driver_email)
    if action == "start":
        cursor.execute("""
        UPDATE DRIVER SET driver_availability = %s WHERE driver_email = %s
        """, ('on_ride',driver_email))

        cursor.execute("""
            UPDATE RIDE
            SET start_time = NOW(), ride_status = %s
            WHERE ride_id = %s AND driver_email = %s
        """, ('start_ride',ride_id, driver_email))
    elif action == "complete":
        cursor.execute("""
                SELECT start_time, fare FROM RIDE
                WHERE ride_id = %s AND driver_email = %s
            """, (ride_id, driver_email))
        start_time_result = cursor.fetchone()   

        if start_time_result and start_time_result[0]:
            start_time = start_time_result[0]
        
        fare = start_time_result[1]
        cursor.execute("""
                SELECT avg_earnings FROM driver
                WHERE driver_email = %s
            """, (driver_email,))
        avg_earning = cursor.fetchone()
        if int(avg_earning[0]) == 0:
            avg_earning = fare
        else:
            avg_earning = (avg_earning[0] + fare )  / 2
         
        from datetime import datetime

        now = datetime.now()
        duration_delta = now - start_time
        total_time_datetime = datetime(1970, 1, 1) + duration_delta
        cursor.execute("""UPDATE RIDE
                        SET end_time = %s,
                        ride_status = 'completed',
                        total_time = %s
                        WHERE ride_id = %s AND driver_email = %s
        """, (now, total_time_datetime, ride_id, driver_email))
        
        cursor.execute("""
            UPDATE DRIVER SET avg_earnings = %s, driver_availability = 'available'
            WHERE driver_email = %s
        """, (avg_earning, driver_email,))
    else:
        return jsonify({"status": "error", "message": "Invalid action"}), 400

    conn.commit()
    return jsonify({"status": "success"})

    
    
# --------------------------------------------------------------------------------------------------


# admin routes.


@app.route('/admin')
def admin():
    return render_template("admin_login.html")

DUMMY_CREDENTIALS = {
    "admin@example.com": "admin123"
}


@app.route("/admin-login", methods=["POST"])
def admin_login():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON"}), 400

    username = data.get("username")
    password = data.get("password")
    print(username)
    print(password)
    cursor.execute("SELECT admin_email, password FROM admin WHERE admin_email = %s", (username,))
    user = cursor.fetchone()
    print(user)
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    db_email, db_password = user[0], user[1]
    if db_password == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401
    

@app.route("/admin_dashboard")
def admin_index():
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=pass_word,
    database="TMS"
    )

    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM CUSTOMER_REGISTRATION cr JOIN CUSTOMER c on cr.customer_email = c.customer_email")
    users = cursor.fetchall()
    cursor.execute("SELECT * FROM DRIVER_REGISTRATION dr JOIN DRIVER d on dr.driver_email = d.driver_email")
    drivers = cursor.fetchall()
    customer_columns = [
    "customer_registration_id", "customer_email", "customer_registration_date",
    "first_name", "middle_name", "last_name", "phone_number", "gender",
    "password", "age", "dob", "customer_email", "customer_status",
    "customer_latitude", "customer_longitude"
    ]
    customer_dicts = [dict(zip(customer_columns, row)) for row in users]

    driver_columns = [
     "driver_registration_id", "driver_email", "license_id", "first_name", "middle_name", "last_name", "phone_number",
    "license_expiry", "gender", "dob", "password", "age", "address", "city", "pincode", "registration_date","driver_email",
    "plate_number", "driver_status", "driver_availability", "driver_latitude", "driver_longitude",
    "avg_earnings", "avg_rating", "positve_review_count", "negative_review_count"
    ]
    driver_dicts = [dict(zip(driver_columns, row)) for row in drivers]
    return render_template("admin_dashboard.html", users=customer_dicts, drivers=driver_dicts)


@app.route("/update_user", methods=["POST"])
def update_user():
    data = request.json
    
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=pass_word,
    database="TMS"
    )

    cursor = conn.cursor()
    
    
    query = """
        UPDATE CUSTOMER_REGISTRATION
        SET first_name=%s,
            last_name=%s,
            phone_number=%s,
            age=%s,
            gender=%s,
            password=%s
        WHERE customer_registration_id=%s
    """
    cursor.execute(query, (
        data['first_name'],
        data['last_name'],
        data['phone_number'],
        data['age'],
        data['gender'],
        data['password'],
        data['id']
    ))
    conn.commit()
    return jsonify({"status": "success"})


@app.route("/update_driver", methods=["POST"])
def update_driver():
    data = request.json
    reg_query = """
        UPDATE DRIVER_REGISTRATION
        SET first_name=%s,
            last_name=%s,
            phone_number=%s,
            age=%s,
            gender=%s,
            password=%s
        WHERE driver_registration_id=%s
    """
    cursor.execute(reg_query, (
        data['first_name'],
        data['last_name'],
        data['phone_number'],
        data['age'],
        data['gender'],
        data['password'],
        data['id']
    ))

# Update DRIVER table
    driver_status_query = """
        UPDATE DRIVER
        SET driver_status=%s
        WHERE driver_email = (
            SELECT driver_email FROM DRIVER_REGISTRATION WHERE password=%s
        )
        """
    cursor.execute(driver_status_query, (
        data['driver_status'],
        data['password']
    ))

    conn.commit()
    return jsonify({"status": "success"})


@app.route('/custom_api', methods=['POST'])
def custom_api():
    data = request.get_json()
    text = data.get('text', '').strip()

    try:
        if not text:
            return jsonify({"status": "error", "message": "Empty query received"}), 400

        cursor.execute(text)

        if text.lower().startswith("select"):
            result = cursor.fetchall()
            return jsonify({
                "status": "success",
                "rows_returned": len(result),
                "data": result
            }), 200
        else:
            conn.commit()
            return jsonify({
                "status": "success",
                "message": "Query executed successfully"
            }), 200

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return jsonify({
            "status": "error",
            "message": str(err)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
