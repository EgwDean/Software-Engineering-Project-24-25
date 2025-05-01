-- Εισαγωγή Εγγραφών στον Πίνακα user
INSERT INTO user (username, password, phone, email, balance, bank_id, message)
VALUES
('user1', 'password1', '1234567890', 'user1@example.com', 1000.0, 123456789, NULL),
('user2', 'password2', '1234567891', 'user2@example.com', 1500.0, 987654321, NULL),
('user3', 'password3', '1234567892', 'user3@example.com', 2000.0, 112233445, NULL),
('user4', 'password4', '1234567893', 'user4@example.com', 2500.0, 998877665, NULL),
('user5', 'password5', '1234567894', 'user5@example.com', 3000.0, 443322110, NULL),
('user6', 'password6', '1234567895', 'user6@example.com', 3500.0, 556677889, NULL),
('user7', 'password7', '1234567896', 'user7@example.com', 4000.0, 998822330, NULL),
('user8', 'password8', '1234567897', 'user8@example.com', 4500.0, 667788990, NULL),
('user9', 'password9', '1234567898', 'user9@example.com', 5000.0, 778899665, NULL),
('user10', 'password10', '1234567899', 'user10@example.com', 5500.0, 223344556, NULL);

-- Εισαγωγή Εγγραφών στον Πίνακα admin
INSERT INTO admin (username, password)
VALUES
('admin1', 'adminpassword1'),
('admin2', 'adminpassword2'),
('admin3', 'adminpassword3'),
('admin4', 'adminpassword4'),
('admin5', 'adminpassword5'),
('admin6', 'adminpassword6'),
('admin7', 'adminpassword7'),
('admin8', 'adminpassword8'),
('admin9', 'adminpassword9'),
('admin10', 'adminpassword10');

-- Εισαγωγή Εγγραφών στον Πίνακα subscription
INSERT INTO subscription (plan, price, commission)
VALUES
('basic', 100, 5.0),
('standard', 200, 10.0),
('premium', 300, 15.0),
('deluxe', 400, 20.0),
('super', 500, 25.0),
('pro', 600, 30.0),
('ultimate', 700, 35.0),
('luxury', 800, 40.0),
('economy', 50, 3.0),
('exclusive', 900, 50.0);

-- Εισαγωγή Εγγραφών στον Πίνακα commissions
INSERT INTO commissions (balance)
VALUES
(5000);

-- Εισαγωγή Εγγραφών στον Πίνακα address
INSERT INTO address (username_address, country, city, street)
VALUES
('user1', 'USA', 'New York', '5th Avenue'),
('user2', 'UK', 'London', 'Baker Street'),
('user3', 'Germany', 'Berlin', 'Alexanderplatz'),
('user4', 'France', 'Paris', 'Champs-Élysées'),
('user5', 'Italy', 'Rome', 'Via del Corso'),
('user6', 'Spain', 'Madrid', 'Gran Vía'),
('user7', 'Canada', 'Toronto', 'Yonge Street'),
('user8', 'Australia', 'Sydney', 'George Street'),
('user9', 'Japan', 'Tokyo', 'Shibuya'),
('user10', 'China', 'Beijing', 'Wangfujing');

-- Εισαγωγή Εγγραφών στον Πίνακα pays_subscription
INSERT INTO pays_subscription (user_name, sub_plan, start_date, end_date)
VALUES
('user1', 'basic', '2025-01-01', '2025-12-31'),
('user2', 'standard', '2025-01-01', '2025-12-31'),
('user3', 'premium', '2025-01-01', '2025-12-31'),
('user4', 'deluxe', '2025-01-01', '2025-12-31'),
('user5', 'super', '2025-01-01', '2025-12-31'),
('user6', 'pro', '2025-01-01', '2025-12-31'),
('user7', 'ultimate', '2025-01-01', '2025-12-31'),
('user8', 'luxury', '2025-01-01', '2025-12-31'),
('user9', 'economy', '2025-01-01', '2025-12-31'),
('user10', 'exclusive', '2025-01-01', '2025-12-31');

-- Εισαγωγή Εγγραφών στον Πίνακα vehicle_listing
INSERT INTO vehicle_listing (name_of_user, price_per_day, vehicle_type, brand, model, year, total_km, fuel_type, description, from_date, to_date, status)
VALUES
('user1', 50.0, 'Car', 'Toyota', 'Corolla', '2020', '15000', 'Gasoline', 'Compact car in great condition', '2025-01-01', '2025-12-31', 'listed'),
('user2', 70.0, 'Truck', 'Ford', 'F-150', '2019', '50000', 'Diesel', 'Large truck with towing capacity', '2025-01-01', '2025-12-31', 'active'),
('user3', 90.0, 'Motorcycle', 'Harley-Davidson', 'Sportster', '2022', '2000', 'Gasoline', 'Cruiser bike with great performance', '2025-01-01', '2025-12-31', 'listed'),
('user4', 60.0, 'Car', 'BMW', 'X5', '2021', '10000', 'Diesel', 'Luxury SUV for comfortable drives', '2025-01-01', '2025-12-31', 'pending'),
('user5', 80.0, 'Truck', 'Chevrolet', 'Silverado', '2018', '70000', 'Diesel', 'Heavy-duty truck for large loads', '2025-01-01', '2025-12-31', 'active'),
('user6', 120.0, 'Car', 'Mercedes', 'E-Class', '2023', '5000', 'Electric', 'Luxury electric sedan', '2025-01-01', '2025-12-31', 'listed'),
('user7', 110.0, 'Motorcycle', 'Ducati', 'Panigale', '2021', '3000', 'Gasoline', 'High-performance motorcycle', '2025-01-01', '2025-12-31', 'active'),
('user8', 150.0, 'Truck', 'Mack', 'Anthem', '2022', '15000', 'Diesel', 'Long-haul truck with powerful engine', '2025-01-01', '2025-12-31', 'listed'),
('user9', 100.0, 'Car', 'Audi', 'A4', '2020', '20000', 'Gasoline', 'Compact luxury car for daily use', '2025-01-01', '2025-12-31', 'pending'),
('user10', 200.0, 'Truck', 'Kenworth', 'T680', '2022', '25000', 'Diesel', 'Heavy-duty truck with great mileage', '2025-01-01', '2025-12-31', 'completed');

-- Εισαγωγή Εγγραφών στον Πίνακα rents
INSERT INTO rents (user_who_rents, from_date, number_of_days, id_of_listing)
VALUES
('user1', '2025-01-01', 7, 1),
('user2', '2025-02-01', 5, 2),
('user3', '2025-03-01', 3, 3),
('user4', '2025-04-01', 10, 4),
('user5', '2025-05-01', 8, 5),
('user6', '2025-06-01', 12, 6),
('user7', '2025-07-01', 4, 7),
('user8', '2025-08-01', 15, 8),
('user9', '2025-09-01', 6, 9),
('user10', '2025-10-01', 20, 10);

-- Εισαγωγή Εγγραφών στον Πίνακα reports
INSERT INTO reports (name_reporter, comment, date_of_report, id_list_report)
VALUES
('user1', 'Vehicle listed with great condition', '2025-01-01', 1),
('user2', 'Price is too high for the truck', '2025-02-01', 2),
('user3', 'The bike is awesome but needs some repairs', '2025-03-01', 3),
('user4', 'SUV is in excellent condition', '2025-04-01', 4),
('user5', 'Truck needs servicing but still good', '2025-05-01', 5),
('user6', 'Car is well-maintained and efficient', '2025-06-01', 6),
('user7', 'Motorcycle is fantastic', '2025-07-01', 7),
('user8', 'Truck is solid but noisy', '2025-08-01', 8),
('user9', 'Car is smooth, just needs better fuel efficiency', '2025-09-01', 9),
('user10', 'Great truck for long hauls', '2025-10-01', 10);

-- Εισαγωγή Εγγραφών στον Πίνακα reviews
INSERT INTO reviews (name_reviewer, comment, date_of_review, id_list_review, stars)
VALUES
('user1', 'Amazing vehicle!', '2025-01-01', 1, 5),
('user2', 'Good but too expensive', '2025-02-01', 2, 3),
('user3', 'Not bad but requires more power', '2025-03-01', 3, 4),
('user4', 'Very comfortable ride', '2025-04-01', 4, 5),
('user5', 'Great but needs some improvements', '2025-05-01', 5, 4),
('user6', 'Smooth and efficient', '2025-06-01', 6, 5),
('user7', 'High performance bike', '2025-07-01', 7, 5),
('user8', 'Good but not as powerful as expected', '2025-08-01', 8, 3),
('user9', 'Luxury car for everyday use', '2025-09-01', 9, 4),
('user10', 'Best truck for long distances', '2025-10-01', 10, 5);