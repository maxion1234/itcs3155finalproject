CREATE TABLE IF NOT EXISTS app_user (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(50),
    email VARCHAR(255),
    user_password VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS post (
    post_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    post_title VARCHAR(50),
    post_body VARCHAR(255),
    score INT,
    date_posted DATE,

    CONSTRAINT fk_post_user
    FOREIGN KEY (user_id) REFERENCES app_user (user_id)
);

CREATE TABLE IF NOT EXISTS comment (
    comment_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    post_id INTEGER,
    comment_body VARCHAR(255),
    score INT,

    CONSTRAINT fk_comment_user
    FOREIGN KEY (user_id) REFERENCES app_user (user_id),

    CONSTRAINT fk_comment_post
    FOREIGN KEY (post_id) REFERENCES post (post_id)
);

