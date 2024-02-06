CREATE TABLE jrobertoperezangulo_ipn_coderhouse.pokemon (
    id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    name VARCHAR(50) NOT NULL,
    img VARCHAR(500) NOT NULL,
    description VARCHAR(50) NOT NULL,
    attack_id INTEGER,
    type_id INTEGER,
    FOREIGN KEY (attack_id) REFERENCES jrobertoperezangulo_ipn_coderhouse.attack(id),
    FOREIGN KEY (type_id) REFERENCES jrobertoperezangulo_ipn_coderhouse.type(id)
);

CREATE TABLE jrobertoperezangulo_ipn_coderhouse.attack (
    id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    description VARCHAR(50) NOT NULL
);

CREATE TABLE jrobertoperezangulo_ipn_coderhouse.type (
    id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    description VARCHAR(50) NOT NULL
);