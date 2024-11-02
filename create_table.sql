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
    sport VARCHAR(100),
    events VARCHAR(50),
    birth_date DATE,
    FOREIGN KEY (country_code) REFERENCES countries(country_code),
    FOREIGN KEY (sport) REFERENCES sports(sport)
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
    sport VARCHAR(100), -- in database table, this column is in ['<sport>'] template. dont forget to delete when inserting
    events TEXT,
    birth_date DATE,
    lang TEXT,
    coach_code INT,
    FOREIGN KEY (country_code) REFERENCES countries(country_code),
    FOREIGN KEY (coach_code) REFERENCES coaches(code),
    FOREIGN KEY (sport) REFERENCES sports(sport)
);

CREATE TABLE sports (
    sport VARCHAR(100) PRIMARY KEY,
    sport_code CHAR(3), 
    sport_URL VARCHAR(255)
);