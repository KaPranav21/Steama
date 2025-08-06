CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE games (
    appid INT PRIMARY KEY,
    name VARCHAR(255),
    developer VARCHAR(255),
    release_date DATE,
    is_free BOOLEAN
);

CREATE TABLE user_games (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    appid INT,
    playtime_hours FLOAT DEFAULT 0, -- if you want to track how much time spent
    rating INT, -- optional: user rating of the game (1-5 stars for example)
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (appid) REFERENCES games(appid),
    UNIQUE KEY (user_id, appid)
);
