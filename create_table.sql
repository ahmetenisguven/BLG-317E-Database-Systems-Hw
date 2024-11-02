CREATE TABLE countries (
    country_code CHAR(3) PRIMARY KEY,
    country VARCHAR(50),
    country_long VARCHAR(100)
);

CREATE TABLE coaches (
    code INT PRIMARY KEY,
    current BOOLEAN,
    name VARCHAR(100),
    name_short VARCHAR(50),
    gender ENUM('Male', 'Female', 'Other'),
    job_title VARCHAR(50), -- Renamed from "function" cuz function name can't be used.
    category CHAR(1),
    country_code CHAR(3), 
    disciplines VARCHAR(100),
    events VARCHAR(50),
    birth_date DATE,
    FOREIGN KEY (country_code) REFERENCES countries(country_code)
);

CREATE TABLE athletes (
    code INT PRIMARY KEY,
    name VARCHAR(255),
    name_short VARCHAR(50),
    name_tv VARCHAR(100),
    gender VARCHAR(10),
    job_title VARCHAR(50),
    country_code CHAR(3),
    height_ FLOAT,
    weight_ FLOAT,
    disciplines TEXT,
    events TEXT,
    birth_date DATE,
    lang TEXT,
    coach_code INT,
    FOREIGN KEY (country_code) REFERENCES countries(country_code),
    FOREIGN KEY (coach_code) REFERENCES coaches(code)
);
