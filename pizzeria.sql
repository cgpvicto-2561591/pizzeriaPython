/*
==================================================
			CREATION TABLE
==================================================
*/

CREATE DATABASE IF NOT EXISTS pizzeria
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;

USE pizzeria;

CREATE TABLE IF NOT EXISTS `client` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(60),
    numero_telephone VARCHAR(60),
    adresse_livraison VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS ingredient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(60)
);

CREATE TABLE IF NOT EXISTS type_croute(
id INT AUTO_INCREMENT PRIMARY KEY,
nom VARCHAR(60)
);

CREATE TABLE IF NOT EXISTS type_sauce(
id INT AUTO_INCREMENT PRIMARY KEY,
nom VARCHAR(60)
);

CREATE TABLE IF NOT EXISTS pizza (
    id INT AUTO_INCREMENT PRIMARY KEY,
    croute_id INT,
    sauce_id INT,
    FOREIGN KEY (croute_id) REFERENCES type_croute(id),
    FOREIGN KEY (sauce_id) REFERENCES type_sauce(id)
);

CREATE TABLE IF NOT EXISTS liste_garniture (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pizza_id INT,
    ingredient_id INT,
    FOREIGN KEY (pizza_id) REFERENCES pizza(id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredient(id)
);

CREATE TABLE IF NOT EXISTS commande (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_commande VARCHAR(60) NOT NULL UNIQUE, 
    statut VARCHAR(60) NOT NULL DEFAULT 'En préparation', #'En préparation', 'En chemin', 'Livré'
    client_id INT,
    pizza_id INT,
    FOREIGN KEY (client_id) REFERENCES client(id),
    FOREIGN KEY (pizza_id) REFERENCES pizza(id)
);


/*
==================================================
			insertion table
==================================================
*/
INSERT INTO ingredient(nom)
VALUES('Pepperoni'),
('Champignons'),
('Oignons'),
('Poivrons'),
('Olives'),
('Anchois'),
('Bacon'),
('Poulet'),
('Maïs'),
('Fromage'),
('Piments forts');

INSERT INTO type_croute(nom)
VALUES('Classique'),
('Mince'),
('Épaisse');

INSERT INTO type_sauce(nom)
VALUES('Tomate'),
('Spaghetti'),
('Alfredo');

/*
==================================================
			CREATION trigger
==================================================
*/

/**
 * Insert des informations dans list_commande avant un insert de commande et lui met le status En préparation
 *
 * @dependencies commande, list_commande
 */
DELIMITER $$

CREATE TRIGGER preparation
    BEFORE INSERT 
    ON commande 
    FOR EACH ROW
    BEGIN
	SET NEW.statut = 'En préparation';
    END;
    
DELIMITER ;



