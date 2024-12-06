CREATE TABLE countries (
    country_code CHAR(3) PRIMARY KEY NOT NULL,
    country VARCHAR(50) NOT NULL,
    country_long VARCHAR(100)
);

CREATE TABLE sports (
    sport VARCHAR(100) PRIMARY KEY NOT NULL,
    sport_code CHAR(3) NOT NULL, 
    sport_URL VARCHAR(255)
);

CREATE TABLE coaches (
    code VARCHAR(50) PRIMARY KEY NOT NULL,
    current_status BOOLEAN,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(10),
    job_title VARCHAR(50), -- Renamed from "function" cuz function name can't be used.
    category CHAR(1),
    country_code CHAR(3), 
    sport VARCHAR(100),
    events TEXT,
    birth_date DATE,
    FOREIGN KEY (country_code) REFERENCES countries(country_code),
    FOREIGN KEY (sport) REFERENCES sports(sport)
);

CREATE TABLE athletes (
    code VARCHAR(50) PRIMARY KEY NOT NULL,
    current_status BOOLEAN,
    name VARCHAR(255) NOT NULL,
    name_short VARCHAR(50),
    name_tv VARCHAR(100),
    gender VARCHAR(10),
    job_title VARCHAR(50),
    country_code CHAR(3),
    height_ FLOAT,
    weight_ FLOAT,
    sport VARCHAR(100), -- in database table, this column is in ['<sport>'] template. don't forget to delete when inserting
    events TEXT,
    birth_date DATE,
    lang TEXT,
    FOREIGN KEY (country_code) REFERENCES countries(country_code),
    FOREIGN KEY (sport) REFERENCES sports(sport),
    CHECK(sport NOT LIKE '[%,%]')
);

CREATE TABLE teams (
    code VARCHAR(50) PRIMARY KEY NOT NULL,
    current_status BOOLEAN,
    team VARCHAR(100) NOT NULL,
    team_gender VARCHAR(2),
    country_code CHAR(3),
    sport VARCHAR(100),
    events TEXT,
    num_athletes INT,
    num_coaches INT,
    
    FOREIGN KEY (country_code) REFERENCES countries(country_code),
    FOREIGN KEY (sport) REFERENCES sports(sport)
    
);

CREATE TABLE teams_member ( 
    teams_code VARCHAR(50),
    roles BOOLEAN, -- if true(1) coaches_code = NULL else athletes_code = NULL
    athletes_code VARCHAR(50),
    coaches_code VARCHAR(50),
    FOREIGN KEY (teams_code) REFERENCES teams(code),
    FOREIGN KEY (athletes_code) REFERENCES athletes(code),
    FOREIGN KEY (coaches_code) REFERENCES coaches(code)
)

CREATE TABLE medals (
    medal_date DATE,
    medal_type ENUM('Gold Medal', 'Silver Medal', 'Bronze Medal'), -- 1 Gold 2 Silver 3 Bronze
    sport VARCHAR(100),
    athletes_code VARCHAR(50),
    teams_code VARCHAR(50),
    FOREIGN KEY (teams_code) REFERENCES teams (code),
    FOREIGN KEY (athletes_code) REFERENCES athletes (code),
    FOREIGN KEY (sport) REFERENCES sports (sport)
)

CREATE TABLE users (
    user_name VARCHAR(50),
    password_ VARCHAR(50), -- 1 Gold 2 Silver 3 Bronze
    register_date DATE,
    high_score INT
)

