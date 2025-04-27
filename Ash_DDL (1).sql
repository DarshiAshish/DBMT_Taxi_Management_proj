-- Creating Taxi Management System Database


CREATE DATABASE TMS;

USE TMS;

-- 1. Creating Vehicle Table


CREATE TABLE VEHICLE (
  make VARCHAR(50) NOT NULL,
  model VARCHAR(50) NOT NULL,
  plate_number VARCHAR(50) NOT NULL,
  type VARCHAR(50) NOT NULL,
  ac_non VARCHAR(50) NULL,
  ownership ENUM('personal', 'company') NOT NULL,
  PRIMARY KEY (plate_number)
);
INSERT INTO VEHICLE
(make, model, plate_number, type, ac_non, ownership) 
VALUES ('Honda', 'Model 3', '683 AF7', 'Sedan', 'ac', 'personal'),
	   ('Tesla', 'Model 3', 'CLE 031', 'SUV', 'ac', 'personal'),
       ('Tesla', 'F-150', '703 2VM', 'Sedan', 'ac', 'personal'),
       ('Toyota', 'Camry', 'QY 6093', 'SUV', 'ac', 'personal'),
	   ('Toyota', 'Model 3', '177-OTC', 'SUV', 'ac', 'personal');
	  
select * from VEHICLE;




-- 4. Creating CUSTOMER TABLE
CREATE TABLE CUSTOMER (
  customer_email VARCHAR(50) NOT NULL,
  customer_status ENUM('Active','Blocked') NOT NULL,
  customer_latitude VARCHAR(250) NOT NULL,
  customer_longitude VARCHAR(250) NOT NULL,
  PRIMARY KEY (customer_email)
);
INSERT INTO CUSTOMER 
(customer_email, customer_status, customer_latitude, customer_longitude) 
VALUES ('danielle70@gmail.com', 'Active', 58.446598, 171.538608),
	   ('stevenbrown@gmail.com', 'Active', -11.449282, -166.967023),
       ('westhaley@gmail.com', 'Active', 55.222952, 101.313938),
       ('stephanieburke@gmail.com', 'Blocked', -59.454850, -7.770537),
       ('stevenstonya@gmail.com', 'Active', -17.746360, -89.024907);

select * from customer;



-- 5. Creating CUSTOMER_REGISTRATION TABLE
CREATE TABLE CUSTOMER_REGISTRATION (
  customer_registration_id INT NOT NULL AUTO_INCREMENT,
  customer_email VARCHAR(50) NOT NULL,
  customer_registration_date DATE NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  middle_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  phone_number VARCHAR(50) NOT NULL,
  gender VARCHAR(10) NOT NULL,
  password VARCHAR(50) NOT NULL,
  age INT NOT NULL,
  dob DATE NOT NULL,
  PRIMARY KEY (customer_registration_id),
  FOREIGN KEY (customer_email) REFERENCES Customer(customer_email)
);


INSERT INTO CUSTOMER_REGISTRATION 
(customer_email, customer_registration_date, first_name, middle_name, last_name, phone_number, gender, password, age, dob)
VALUES ('danielle70@gmail.com', '2024-12-24', 'Howell', 'Fitzpatrick', 'Miller', '892-7342-344', 'Male', '&&&D9#b+v6', 36, '1989-12-08'),
	   ('stevenbrown@gmail.com', '2024-10-17', 'Harrington', 'Baker', 'Black', '234-7384-427', 'Male', 'S&A5^BnXWk', 44, '1981-10-02'),
       ('westhaley@gmail.com', '2024-02-12', 'Parker', 'Garza', 'Davis', '974-9833-233', 'Female', '+fH95LzpK1', 26, '1999-11-01'),
       ('stephanieburke@gmail.com', '2024-03-24', 'Stout', 'Smith', 'Nichols', '783-2633-873', 'Male', '(8YqGDLDRu', 36, '1989-10-10'),
       ('stevenstonya@gmail.com', '2024-04-04', 'Jones', 'Moore', 'Gonzalez', '0834-2386-342', 'Female', '+m$PRpv40l', 51, '1974-10-12');

select * from customer_registration;




-- 6. Creating DRIVER TABLE
CREATE TABLE DRIVER (
  driver_email VARCHAR(50) NOT NULL,
  plate_number VARCHAR(50) NOT NULL,
  driver_status ENUM('Active','Blocked') NOT NULL,
  driver_availability ENUM('on_ride','available','unavailble') NOT NULL,
  driver_latitude VARCHAR(250) NOT NULL,
  driver_longitude VARCHAR(250) NOT NULL,
  avg_earnings DECIMAL NOT NULL,
  avg_rating INT NULL,
  positve_review_count	INT,
  negative_review_count	INT,
  PRIMARY KEY (driver_email),
  FOREIGN KEY (plate_number) REFERENCES VEHICLE(plate_number)
);

INSERT INTO DRIVER 
(driver_email, plate_number, driver_status, driver_availability, driver_latitude, driver_longitude, avg_earnings, avg_rating, positve_review_count, negative_review_count) 
VALUES ('wheelerantonio@gmail.com', '683 AF7', 'Active', 'on_ride', 76.847518, -38.238793, 856.44, 5, 2, 1),
	   ('jennifer33@gmail.com', '703 2VM', 'Active', 'available', -7.621488, -37.988463, 833.43, 2, 5, 2),
       ('mckeejoseph@gmail.com', 'CLE 031','Active', 'available', 53.736842, 34.014641, 432.41, 5, 4, 5),
       ('aaronblack@gmail.com', '177-OTC','Active', 'available', -0.596569, 56.974846, 577.43, 2, 6, 5),
       ('lschultz@gmail.com', 'QY 6093','Active', 'available', -22.248988, 116.525702, 542.63, 1, 8, 2);

select * from driver;


-- 7. Creating DRIVER_REGISTRATION TABLE  
CREATE TABLE DRIVER_REGISTRATION (
  driver_registration_id INT NOT NULL AUTO_INCREMENT,
  driver_email VARCHAR(50) NOT NULL,
  license_id varchar(50) NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  middle_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  phone_number VARCHAR(50) NOT NULL,
  license_expiry DATE NOT NULL,
  gender VARCHAR(10) NOT NULL,
  dob DATE NOT NULL,
  password VARCHAR(50) NOT NULL,
  age INT NOT NULL,
  address VARCHAR(50) NOT NULL,
  city VARCHAR(50) NOT NULL,
  pincode VARCHAR(10) NOT NULL,
  registration_date DATE NOT NULL,
  PRIMARY KEY (driver_registration_id),
  FOREIGN KEY (driver_email) REFERENCES Driver(driver_email)
);


INSERT INTO DRIVER_REGISTRATION 
(driver_email, license_id, first_name, middle_name, last_name, phone_number, license_expiry, gender, dob, password, age, address, city, pincode, registration_date) 
VALUES ('wheelerantonio@gmail.com', '32480246', 'Jennifer', 'Tapia', 'Simpson', '789-4577-337', '2030-08-04', 'Female', '2000-08-04', 'm*pc0DizPP', 25, 'Port William', 'Stuarttown', '51652', '2021-05-06'),
       ('jennifer33@gmail.com', 183, '89935860', 'Bridges', 'Carpenter', '978-7634-993', '2030-02-10', 'Male', '2000-02-10', '5#g4fRQk&0', 25, 'Megantown', 'East Amanda', '09877', '2022-06-06'),
       ('mckeejoseph@gmail.com', '96738851', 'Jessica', 'Adams', 'Hill', '937-3684-237', '2030-05-17', 'Male', '1999-05-17', 'X15GZu+M*q', 26, 'Garyton', 'West Toddbury', '29996', '2023-09-21'),
       ('aaronblack@gmail.com', '93591107', 'Madison', 'Bauer', 'Crawford', '723-2724-283', '2030-05-17', 'Male', '2000-05-17', 'I6oqEQym&H', 25, 'Nicolasland', 'West Tommy', '99920', '2022-05-11'),
       ('lschultz@gmail.com', '83009810', 'Summer', 'Williams', 'Gilbert', '297-7823-232', '2030-05-27', 'Male', '1999-05-27', '9hxK6R7ei%', 26, 'Reedport', 'Robertburgh', '69691', '2020-03-06');

select * from driver_registration;

select * from driver;


-- 8. Creating RIDE Table
CREATE TABLE RIDE (
  ride_id INT NOT NULL AUTO_INCREMENT,
  customer_email VARCHAR(50) NOT NULL,
  driver_email VARCHAR(50) NULL,
  pickup_location VARCHAR(100) NOT NULL,
  drop_location VARCHAR(100) NOT NULL,
  start_time DATETIME NOT NULL,
  seat_requested int null,
  end_time DATETIME NULL,
  ride_status ENUM('scheduled','active','start_ride','completed','canceled') NOT NULL,
  fare	DECIMAL(10, 2) NULL,
  fare_status ENUM('completed', 'pending'),
  review_status	ENUM('completed','pending'),
  total_time TIME NOT NULL,
  duration varchar(100) null,
  distance decimal(10, 2) null,
  PRIMARY KEY (ride_id),
  FOREIGN KEY (customer_email) REFERENCES Customer(customer_email),
  FOREIGN KEY (driver_email) REFERENCES Driver(driver_email)
);

INSERT INTO RIDE 
(customer_email, driver_email, pickup_location, drop_location, start_time,seat_requested, end_time, ride_status, fare, fare_status,review_status, total_time, duration, distance)
VALUES
('danielle70@gmail.com', 'wheelerantonio@gmail.com', 'Downtown', 'Uptown', '2025-04-12 08:00:00', 1,'2025-04-12 08:30:00',  'completed', 15.75,'completed', 'completed',  '00:30:00', '12 mins', 2.34),
('stevenbrown@gmail.com', 'jennifer33@gmail.com', 'Green Street', 'Maple Avenue', '2025-04-12 09:00:00', 2,'2025-04-12 09:45:00', 'completed', 20.50,'completed', 'pending', '00:45:00','15 mins', 3.34),
('westhaley@gmail.com', 'mckeejoseph@gmail.com', 'Airport', 'Central Station', '2025-04-12 10:15:00', 1,'2025-04-12 10:55:00', 'completed', 18.00, 'completed','pending', '00:40:00','10 mins', 1.18),
('stephanieburke@gmail.com', 'aaronblack@gmail.com', 'City Mall', 'Tech Park', '2025-04-12 11:00:00', 3,'2025-04-12 11:30:00', 'completed', 22.30, 'completed','pending', '00:30:00','20 mins', 5.1),
('stevenstonya@gmail.com', 'lschultz@gmail.com', 'Harbor Front', 'Hilltop', '2025-04-12 12:10:00', 4,'2025-04-12 12:40:00', 'completed', 19.99, 'completed','pending', '00:30:00','12 mins', 2.0);

select * from ride;

UPDATE RIDE
SET ride_status = 'active', driver_email='wheelerantonio@gmail.com'  -- or 'active', 'canceled', 'scheduled'
WHERE customer_email = 'darshiashishcolab@gmail.com';




-- 9. Creating PAYMENT Table
CREATE TABLE PAYMENT (
  PaymentID INT NOT NULL AUTO_INCREMENT,
  ride_id INT NOT NULL,
  payment_method ENUM('cash','card','wallet') NOT NULL,
  payment_date DATETIME NOT NULL,
  payment_status ENUM('pending','completed','failed') NOT NULL,
  customer_email VARCHAR(50) NOT NULL,
  driver_email VARCHAR(50) NOT NULL,
  PRIMARY KEY (PaymentID),
  FOREIGN KEY (ride_id) REFERENCES Ride(ride_id),
  FOREIGN KEY (customer_email) REFERENCES Customer(customer_email),
  FOREIGN KEY (driver_email) REFERENCES Driver(driver_email)
);

INSERT INTO PAYMENT 
(ride_id, payment_method, payment_date, payment_status, customer_email, driver_email)
VALUES
(1, 'card', '2025-04-12 08:31:00', 'completed', 'danielle70@gmail.com', 'wheelerantonio@gmail.com'),
(2, 'wallet', '2025-04-12 09:46:00', 'completed', 'stevenbrown@gmail.com', 'jennifer33@gmail.com'),
(3, 'cash',  '2025-04-12 10:56:00', 'pending', 'westhaley@gmail.com', 'mckeejoseph@gmail.com'),
(4, 'card',  '2025-04-12 11:31:00', 'pending', 'stephanieburke@gmail.com', 'aaronblack@gmail.com'),
(5, 'wallet', '2025-04-12 12:41:00', 'failed', 'stevenstonya@gmail.com', 'lschultz@gmail.com');

select * from payment;


-- 10. Creating RATINGS Table
CREATE TABLE RATINGS (
  rating_id INT NOT NULL AUTO_INCREMENT,
  ride_id INT NOT NULL,
  customer_email VARCHAR(50) NOT NULL,
  driver_email VARCHAR(50) NOT NULL,
  customer_rating INT NOT NULL,
  feedback TEXT NULL,
  PRIMARY KEY (rating_id),
  FOREIGN KEY (ride_id) REFERENCES Ride(ride_id),
  FOREIGN KEY (customer_email) REFERENCES Customer(customer_email),
  FOREIGN KEY (driver_email) REFERENCES Driver(driver_email)
);


INSERT INTO RATINGS 
 (ride_id, customer_email, driver_email, customer_rating, feedback)
VALUES
(1, 'danielle70@gmail.com', 'wheelerantonio@gmail.com', 5, 'Excellent ride. Very professional driver.'),
(2, 'stevenbrown@gmail.com', 'jennifer33@gmail.com', 4, 'Good service, slightly late pickup.'),
(3, 'westhaley@gmail.com', 'mckeejoseph@gmail.com', 3, 'Driver was fine, but took a longer route.'),
(4, 'stephanieburke@gmail.com', 'aaronblack@gmail.com', 5, 'Scheduled ride, smooth communication.'),
(5, 'stevenstonya@gmail.com', 'lschultz@gmail.com', 2, 'Ride was canceled unexpectedly.');

select * from ratings;


-- 3. Creating Admin Table
CREATE TABLE ADMIN (
  admin_id INT NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  middle_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  admin_email VARCHAR(50) NOT NULL,
  role VARCHAR(50) NOT NULL,
  password VARCHAR(50) NOT NULL
);

-- inserting sample data
INSERT INTO ADMIN 
(admin_id, first_name, middle_name, last_name, admin_email, role, password)
VALUES
(10, 'Alice', 'Marie', 'Johnson', 'alice.johnson@taxicompany.com', 'System Admin', 'admin123'),
(21, 'Brian', 'Lee', 'Smith', 'brian.smith@taxicompany.com', 'Ride Manager', 'pass456'),
(32, 'Cathy', 'Ann', 'Williams', 'cathy.williams@taxicompany.com', 'Finance Admin', 'secure789'),
(45, 'David', 'James', 'Clark', 'david.clark@taxicompany.com', 'Support Admin', 'helpdesk321'),
(58, 'Ella', 'Rose', 'Taylor', 'ella.taylor@taxicompany.com', 'Operations Manager', 'opsmanager');



select * from admin;
