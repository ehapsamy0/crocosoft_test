CREATE DATABASE mydatabase1;
CREATE TABLE type_vehicle(
    id TINYINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50),
    PRIMARY KEY (id));
CREATE TABLE vehicle(
    id INT NOT NULL AUTO_INCREMENT,
    model VARCHAR(50),
    type_id TINYINT,
    available BOOLEAN,
    day_cost INT,
    color VARCHAR(50),
    time_create DATETIME DEFAULT CURRENT_TIMESTAMP,
    time_update DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (type_id) REFERENCES type_vehicle(id),
    PRIMARY KEY (id));
CREATE TABLE customer(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(120),
    national_id VARCHAR(50),
    time_create DATETIME DEFAULT CURRENT_TIMESTAMP,
    time_update DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id));
CREATE TABLE booking(
    id INT NOT NULL AUTO_INCREMENT,
    vehicle_id INT,
    customer_id INT,
    start_day DATE,
    end_day DATE, 
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(id),
    FOREIGN KEY (customer_id) REFERENCES customer(id),
    PRIMARY KEY (id),
    CONSTRAINT check_return_date CHECK(end_day >= start_day AND DATEDIFF(end_day,start_day) <= 7));