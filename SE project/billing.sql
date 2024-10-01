create database billing;
use billing;

CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    name VARCHAR(255),
    phone_number VARCHAR(10),
    gmail VARCHAR(255)
);

INSERT INTO accounts (username, password, name, phone_number, gmail) 
VALUES ('naren@customer', '1234', 'Naren Polavarapu', '7670933245', 'narenpolavarapu@gmail.com');

INSERT INTO accounts (username, password, name, phone_number, gmail) 
VALUES ('shreyan@manager', '1234', 'Shreyan', '3685738527', 'shreyan@gmail.com');

INSERT INTO accounts (username, password, name, phone_number, gmail) 
VALUES ('vasanth@chef', '1234', 'Vasanth', '4829473928', 'vasanth@gmail.com');

CREATE TABLE orders (
    username VARCHAR(255),
    Butter_Naan INT DEFAULT 0,
    Chapathi INT DEFAULT 0,
    Pulka INT DEFAULT 0,
    Mixed_Vegetable INT DEFAULT 0,
    Butter_Chicken INT DEFAULT 0,
    Kadhai_Paneer INT DEFAULT 0,
    Biryani INT DEFAULT 0,
    Fried_Rice INT DEFAULT 0,
    Pulao INT DEFAULT 0,
    Water INT DEFAULT 0,
    Tea INT DEFAULT 0,
    Coffee INT DEFAULT 0,
    Milk INT DEFAULT 0,
    Butter_Milk INT DEFAULT 0,
    Fruit_Juice INT DEFAULT 0,
    Soft_Drinks INT DEFAULT 0,
    Beer INT DEFAULT 0,
    Wine INT DEFAULT 0,
    Chicken_Manchow_Soup INT DEFAULT 0,
    Sweet_Corn_Soup INT DEFAULT 0,
    Tomato_Soup INT DEFAULT 0,
    Chilli_Chicken INT DEFAULT 0,
    Chicken_Manchuria INT DEFAULT 0,
    Chicken_65 INT DEFAULT 0,
    Paneer_Tikka INT DEFAULT 0,
    Veg_Manchuria INT DEFAULT 0,
    Spring_Rolls INT DEFAULT 0,
    Blue_Berry_Cheesecake INT DEFAULT 0,
    Brownie_With_Ice_Cream INT DEFAULT 0,
    Plum_Cake INT DEFAULT 0,
    Apple_Pie INT DEFAULT 0,
    Creme_Brulee INT DEFAULT 0,
    Custard INT DEFAULT 0,
    Apricot_Delight INT DEFAULT 0,
    Choco_Lava_Cake INT DEFAULT 0,
    Lotus_Biscoff INT DEFAULT 0,
    FOREIGN KEY (username) REFERENCES accounts(username)
);
SELECT * FROM accounts;
SELECT * FROM orders;
UPDATE orders SET Pulka = 0 WHERE username = 'naren@customer';
UPDATE orders SET Fried_rice= Fried_rice + 1 WHERE username = 'naren@customer';
DELETE FROM orders;
drop table orders;

CREATE TABLE manager (
    username VARCHAR(255) PRIMARY KEY,
    payment DECIMAL(10, 2),
    FOREIGN KEY (username) REFERENCES accounts(username)
);

CREATE TABLE chef (
    username VARCHAR(255) PRIMARY KEY,
    state VARCHAR(50),
    FOREIGN KEY (username) REFERENCES accounts(username)
);

CREATE TABLE records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    date DATE,
    bill DECIMAL(10, 2),
    FOREIGN KEY (username) REFERENCES accounts(username)
);


CREATE TABLE prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item VARCHAR(255),
    price DECIMAL(10, 2)
);

INSERT INTO prices (item, price) VALUES
('Butter_Naan', 30),
('Chapathi', 25),
('Pulka', 20),
('Mixed_Vegetable', 220),
('Butter_Chicken', 300),
('Kadhai_Paneer', 250),
('Biryani', 399),
('Fried_Rice', 250),
('Pulao', 99),
('Water', 50),
('Tea', 40),
('Coffee', 40),
('Milk', 30),
('Butter_Milk', 20),
('Fruit_Juice', 70),
('Soft_Drinks', 70),
('Beer', 450),
('Wine', 900),
('Chicken_Manchow_Soup', 199),
('Sweet_Corn_Soup', 169),
('Tomato_Soup', 169),
('Chilli_Chicken', 200),
('Chicken_Manchuria', 150),
('Chicken_65', 210),
('Paneer_Tikka', 169),
('Veg_Manchuria', 99),
('Spring_Rolls', 170),
('Blue_Berry_Cheesecake', 200),
('Brownie_With_Ice_Cream', 170),
('Plum_Cake', 99),
('Apple_Pie', 150),
('Creme_Brulee', 120),
('Custard', 99),
('Apricot_Delight', 170),
('Choco_Lava_Cake', 99),
('Lotus_Biscoff', 220);


SELECT * FROM accounts;
SELECT * FROM orders;
SELECT * FROM manager;
SELECT * FROM chef;
SELECT * FROM records;
SELECT * FROM prices;

drop table accounts;
drop table orders;
drop table manager;
drop table chef;
drop table records;
drop table prices;
