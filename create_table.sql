CREATE TABLE countries (
    country_code CHAR(3) PRIMARY KEY,
    country VARCHAR(50),
    country_long VARCHAR(100)
);

CREATE TABLE sports (
    sport VARCHAR(100) PRIMARY KEY,
    sport_code CHAR(3), 
    sport_URL VARCHAR(255)
);

CREATE TABLE coaches (
    code VARCHAR(50) PRIMARY KEY,
    current_status BOOLEAN,
    name VARCHAR(100),
    name_short VARCHAR(50),
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
    code VARCHAR(50) PRIMARY KEY,
    current_status BOOLEAN,
    name VARCHAR(255),
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
    coach_code VARCHAR(50),
    FOREIGN KEY (country_code) REFERENCES countries(country_code),
    FOREIGN KEY (coach_code) REFERENCES coaches(code),
    FOREIGN KEY (sport) REFERENCES sports(sport)
);

CREATE TABLE teams (
    code VARCHAR(50) PRIMARY KEY,
    current_status BOOLEAN,
    team VARCHAR(100),
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
    medal_type ENUM('gold', 'silver', 'bronze'), -- 1 Gold 2 Silver 3 Bronze
    sport VARCHAR(100),
    athletes_code VARCHAR(50),
    teams_code VARCHAR(50),
    FOREIGN KEY (teams_code) REFERENCES teams(code),
    FOREIGN KEY (athletes_code) REFERENCES athletes(code)
)
