DROP DATABASE IF EXISTS car_rental;
CREATE DATABASE IF NOT EXISTS car_rental;

USE car_rental;

CREATE TABLE user (
	username VARCHAR(50) NOT NULL PRIMARY KEY,
	password VARCHAR(50) NOT NULL,
    phone VARCHAR(50),
	email VARCHAR(50),
    balance FLOAT,
    bank_id BIGINT,
    message TEXT
);

CREATE TABLE admin (
	username VARCHAR(50) NOT NULL PRIMARY KEY,
	password VARCHAR(50) NOT NULL
);

CREATE TABLE subscription (
	plan VARCHAR(50) NOT NULL PRIMARY KEY,
    price INT NOT NULL,
	commission FLOAT NOT NULL
);

CREATE TABLE commissions (
	balance INT NOT NULL
);

CREATE TABLE address (
	username_address VARCHAR(50) NOT NULL PRIMARY KEY,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    street VARCHAR(50) NOT NULL,
    number INT NOT NULL,
    FOREIGN KEY (username_address) REFERENCES user(username)
);

CREATE TABLE pays_subscription (
	user_name VARCHAR(50) NOT NULL,
    sub_plan VARCHAR(50) NOT NULL,
    start_date DATE,
    end_date DATE,
    PRIMARY KEY (user_name, sub_plan),
    FOREIGN KEY (user_name) REFERENCES user(username),
	FOREIGN KEY (sub_plan) REFERENCES subscription(plan)
);

CREATE TABLE vehicle_listing (
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name_of_user VARCHAR(50) NOT NULL,
    price_per_day FLOAT NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year VARCHAR(50) NOT NULL,
    total_km VARCHAR(50) NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    from_date DATE NOT NULL,
    to_date DATE NOT NULL,
    status ENUM('listed', 'active', 'deleted', 'pending', 'completed'),
	FOREIGN KEY (name_of_user) REFERENCES user(username)
);

CREATE TABLE rents (
	user_who_rents VARCHAR(50) NOT NULL,
    from_date DATE NOT NULL,
    number_of_days INT NOT NULL,
	id_of_listing INT NOT NULL,
    PRIMARY KEY(user_who_rents, from_date, id_of_listing),
	FOREIGN KEY (user_who_rents) REFERENCES user(username),
	FOREIGN KEY (id_of_listing) REFERENCES vehicle_listing(id)   
);

CREATE TABLE reports (
	name_reporter VARCHAR(50) NOT NULL,
    comment TEXT,
    date_of_report DATE,
    id_list_report INT NOT NULL,
    PRIMARY KEY (name_reporter, id_list_report),
	FOREIGN KEY (name_reporter) REFERENCES user(username),
	FOREIGN KEY (id_list_report) REFERENCES vehicle_listing(id)  
);

CREATE TABLE reviews (
	name_reviewer VARCHAR(50) NOT NULL,
    comment TEXT,
    date_of_review DATE,
    id_list_review INT NOT NULL,
    stars INT CHECK (stars BETWEEN 1 AND 5),
    PRIMARY KEY (name_reviewer, id_list_review),
	FOREIGN KEY (name_reviewer) REFERENCES user(username),
	FOREIGN KEY (id_list_review) REFERENCES vehicle_listing(id)  
);
