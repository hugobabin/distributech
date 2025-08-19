-- Adminer 5.3.0 MySQL 9.3.0 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

CREATE DATABASE `distributech` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `distributech`;

DELIMITER ;;

DROP PROCEDURE IF EXISTS `maj_stocks`;;
CREATE PROCEDURE `maj_stocks` (IN `id_production` int, IN `quantite_produit` int, IN `date_production` date, IN `id_produit` int, IN `nom_produit` varchar(255), IN `cout_unitaire` decimal(10,2), IN `quantite_commande` int, IN `prix_unitaire` decimal(10,2), IN `total_prix_commande` decimal(10,2), IN `id_commande` int, IN `numero_commande` int, IN `date_commande` date, IN `id_revendeur` int, IN `nom_revendeur` varchar(255), IN `id_region` int, IN `nom_region` varchar(255), IN `id_panier` int, IN `total_prix_panier` decimal(10,2))
BEGIN
        INSERT INTO produits (id_produit, nom_produit, cout_unitaire)
        VALUES (id_produit, nom_produit, cout_unitaire)
        ON DUPLICATE KEY UPDATE nom_produit=VALUES(nom_produit), cout_unitaire=VALUES(cout_unitaire);

        INSERT INTO productions (id_production, quantite_produit, date_production, id_produit)
        VALUES (id_production, quantite_produit, date_production, id_produit);

        INSERT INTO commandes_produits (id_commande, id_produit, prix_unitaire, quantite_commande, total_prix_commande)
        VALUES (id_commande, id_produit, prix_unitaire, quantite_commande, total_prix_commande);

        INSERT INTO regions (id_region, nom_region)
        VALUES (id_region, nom_region)
        ON DUPLICATE KEY UPDATE nom_region=VALUES(nom_region);

        INSERT INTO revendeurs (id_revendeur, nom_revendeur, id_region)
        VALUES (id_revendeur, nom_revendeur, id_region)
        ON DUPLICATE KEY UPDATE nom_revendeur=VALUES(nom_revendeur), id_region=VALUES(id_region);

        INSERT INTO paniers (id_panier, total_prix_panier)
        VALUES (id_panier, total_prix_panier)
        ON DUPLICATE KEY UPDATE total_prix_panier=VALUES(total_prix_panier);

        INSERT INTO commandes (id_commande, id_region, id_revendeur, id_panier)
        VALUES (id_commande, id_region, id_revendeur, id_panier);
    END;;

DELIMITER ;

DROP TABLE IF EXISTS `commandes`;
CREATE TABLE `commandes` (
  `commande_id` int NOT NULL AUTO_INCREMENT,
  `numero_commande` varchar(255) NOT NULL,
  `commande_date` date NOT NULL,
  `revendeur_id` int NOT NULL,
  `panier_id` int NOT NULL,
  PRIMARY KEY (`commande_id`),
  UNIQUE KEY `numero_commande` (`numero_commande`),
  KEY `revendeur_id` (`revendeur_id`),
  KEY `panier_id` (`panier_id`),
  CONSTRAINT `commandes_ibfk_1` FOREIGN KEY (`revendeur_id`) REFERENCES `revendeurs` (`revendeur_id`),
  CONSTRAINT `commandes_ibfk_2` FOREIGN KEY (`panier_id`) REFERENCES `paniers` (`panier_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `commandes` (`commande_id`, `numero_commande`, `commande_date`, `revendeur_id`, `panier_id`) VALUES
(1,	'CMD-20250710-001',	'2025-07-10',	1,	1),
(2,	'CMD-20250711-001',	'2025-07-11',	1,	2);

DROP TABLE IF EXISTS `commandes_produits`;
CREATE TABLE `commandes_produits` (
  `commande_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `total_ligne` decimal(10,2) NOT NULL,
  KEY `commande_id` (`commande_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `commandes_produits_ibfk_1` FOREIGN KEY (`commande_id`) REFERENCES `commandes` (`commande_id`),
  CONSTRAINT `commandes_produits_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `produits` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `commandes_produits` (`commande_id`, `product_id`, `quantity`, `unit_price`, `total_ligne`) VALUES
(1,	101,	5,	59.90,	299.50),
(1,	102,	10,	19.90,	199.00),
(1,	105,	2,	129.90,	259.80),
(2,	108,	3,	44.90,	134.70),
(2,	103,	4,	89.90,	359.60);

DROP TABLE IF EXISTS `paniers`;
CREATE TABLE `paniers` (
  `panier_id` int NOT NULL AUTO_INCREMENT,
  `total_panier` decimal(10,2) NOT NULL,
  PRIMARY KEY (`panier_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `paniers` (`panier_id`, `total_panier`) VALUES
(1,	758.30),
(2,	494.30);

DROP TABLE IF EXISTS `productions`;
CREATE TABLE `productions` (
  `production_id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `date_production` date NOT NULL,
  PRIMARY KEY (`production_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `productions_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `produits` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `productions` (`production_id`, `product_id`, `quantity`, `date_production`) VALUES
(1,	101,	50,	'2025-07-01'),
(2,	102,	80,	'2025-07-01'),
(3,	103,	40,	'2025-07-02'),
(4,	104,	60,	'2025-07-02'),
(5,	105,	20,	'2025-07-03'),
(6,	106,	35,	'2025-07-03'),
(7,	107,	25,	'2025-07-04'),
(8,	108,	30,	'2025-07-04'),
(9,	109,	45,	'2025-07-05'),
(10,	110,	15,	'2025-07-05');

DROP TABLE IF EXISTS `produits`;
CREATE TABLE `produits` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `product_name` varchar(255) NOT NULL,
  `cout_unitaire` decimal(10,2) NOT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `produits` (`product_id`, `product_name`, `cout_unitaire`) VALUES
(101,	'Casque Bluetooth',	59.90),
(102,	'Chargeur USB-C',	19.90),
(103,	'Enceinte Portable',	89.90),
(104,	'Batterie Externe',	24.90),
(105,	'Montre Connectée',	129.90),
(106,	'Webcam HD',	49.90),
(107,	'Hub USB 3.0',	34.90),
(108,	'Clavier sans fil',	44.90),
(109,	'Souris ergonomique',	39.90),
(110,	'Station d\'accueil',	109.90);

DROP TABLE IF EXISTS `regions`;
CREATE TABLE `regions` (
  `region_id` int NOT NULL AUTO_INCREMENT,
  `region_name` varchar(255) NOT NULL,
  PRIMARY KEY (`region_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `regions` (`region_id`, `region_name`) VALUES
(1,	'Île-de-France'),
(2,	'Occitanie'),
(3,	'Auvergne-Rhône-Alpes'),
(4,	'Bretagne');

DROP TABLE IF EXISTS `revendeurs`;
CREATE TABLE `revendeurs` (
  `revendeur_id` int NOT NULL AUTO_INCREMENT,
  `revendeur_name` varchar(255) NOT NULL,
  `region_id` int NOT NULL,
  PRIMARY KEY (`revendeur_id`),
  KEY `region_id` (`region_id`),
  CONSTRAINT `revendeurs_ibfk_1` FOREIGN KEY (`region_id`) REFERENCES `regions` (`region_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `revendeurs` (`revendeur_id`, `revendeur_name`, `region_id`) VALUES
(1,	'TechExpress',	1),
(2,	'ElectroZone',	1),
(3,	'SudTech',	2),
(4,	'GadgetShop',	2),
(5,	'Connectik',	3),
(6,	'Domotik+',	3),
(7,	'BreizhTech',	4),
(8,	'SmartBretagne',	4),
(9,	'HighNord',	1),
(10,	'OuestConnect',	4);

-- 2025-08-01 14:16:32 UTC
