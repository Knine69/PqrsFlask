CREATE TABLE IF NOT EXISTS state (
    state_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS position (
    position_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);


CREATE TABLE IF NOT EXISTS department  (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    active_members INT NOT NULL
);

CREATE TABLE IF NOT EXISTS category  (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS role  (
    role_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS person (
    person_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    document_id VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    position_id INT NOT NULL,
    role_id INT NOT NULL,
    department_id INT NOT NULL,
    FOREIGN KEY (position_id) REFERENCES position (position_id),
    FOREIGN KEY (role_id) REFERENCES role (role_id),
    FOREIGN KEY (department_id) REFERENCES department (department_id)
);

create TABLE IF NOT EXISTS request (
    request_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    generated_at DATE NOT NULL,
    summary VARCHAR(200) NOT NULL,
    category_id INT NOT NULL,
    requester_id INT NOT NULL,
    solver_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES category (category_id),
    FOREIGN KEY (requester_id) REFERENCES person (person_id),
    FOREIGN KEY (solver_id) REFERENCES person (person_id)
); 
