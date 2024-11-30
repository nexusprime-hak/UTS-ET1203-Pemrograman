CREATE TABLE satellites (
	id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    satellite_id VARCHAR(20) NOT NULL,
    perigee FLOAT,
    apogee FLOAT,
    period FLOAT,
    launch_date DATE,
    launch_site VARCHAR(100),
    description TEXT
);