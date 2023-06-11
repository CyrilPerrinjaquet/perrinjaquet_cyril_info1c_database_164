-- --------------------------------------------------------
-- Hôte:                         127.0.0.1
-- Version du serveur:           8.0.30 - MySQL Community Server - GPL
-- SE du serveur:                Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Listage de la structure de la base pour cyril_perrinjaquet_info_1c_164
DROP DATABASE IF EXISTS `cyril_perrinjaquet_info_1c_164`;
CREATE DATABASE IF NOT EXISTS `cyril_perrinjaquet_info_1c_164` /*!40100 DEFAULT CHARACTER SET latin1 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `cyril_perrinjaquet_info_1c_164`;

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_allergie
DROP TABLE IF EXISTS `t_allergie`;
CREATE TABLE IF NOT EXISTS `t_allergie` (
  `id_allergie` int NOT NULL AUTO_INCREMENT,
  `nom_allergie` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `allergene_allergie` varchar(50) DEFAULT NULL,
  `gravite_allergie` varchar(50) DEFAULT NULL,
  `symptomes_allergie` varchar(50) DEFAULT NULL,
  `precautions_allergie` varchar(50) DEFAULT NULL,
  `traitement_allergie` varchar(50) DEFAULT NULL,
  `notes_allergie` longtext CHARACTER SET latin1 COLLATE latin1_swedish_ci,
  PRIMARY KEY (`id_allergie`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_allergie : ~3 rows (environ)
DELETE FROM `t_allergie`;
INSERT INTO `t_allergie` (`id_allergie`, `nom_allergie`, `allergene_allergie`, `gravite_allergie`, `symptomes_allergie`, `precautions_allergie`, `traitement_allergie`, `notes_allergie`) VALUES
	(22, 'polen', 'poudre polen', 'dure', 'atchoum', 'pas respirer', 'pas respirer', 'pas de notes'),
	(24, 'poudreescampette', 'perlinpinpin', 'tresgrave', 'ilsenfui', 'disparaitre', 'brulerlapoudre', 'pas de notes'),
	(25, 'arachides ', 'cacahuetes', 'severe', 'eruptionscutanees', 'informerlespersonnesproches', 'eviterarachides ', 'pas de notes');

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_ingre
DROP TABLE IF EXISTS `t_ingre`;
CREATE TABLE IF NOT EXISTS `t_ingre` (
  `id_ingre` int NOT NULL AUTO_INCREMENT,
  `nom_ingre` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_ingre`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_ingre : ~3 rows (environ)
DELETE FROM `t_ingre`;
INSERT INTO `t_ingre` (`id_ingre`, `nom_ingre`) VALUES
	(4, 'tomate'),
	(5, 'salade'),
	(7, 'oigon');

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_ingre_contenir_allergie
DROP TABLE IF EXISTS `t_ingre_contenir_allergie`;
CREATE TABLE IF NOT EXISTS `t_ingre_contenir_allergie` (
  `id_ingre_contenir_allergie` int NOT NULL AUTO_INCREMENT,
  `fk_ingre` int DEFAULT NULL,
  `fk_allergie` int DEFAULT NULL,
  PRIMARY KEY (`id_ingre_contenir_allergie`) USING BTREE,
  KEY `fk_allergie` (`fk_allergie`),
  KEY `fk_ingredient_allergie` (`fk_ingre`) USING BTREE,
  CONSTRAINT `fk_allergie` FOREIGN KEY (`fk_allergie`) REFERENCES `t_allergie` (`id_allergie`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_ingre_allergie` FOREIGN KEY (`fk_ingre`) REFERENCES `t_ingre` (`id_ingre`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_ingre_contenir_allergie : ~0 rows (environ)
DELETE FROM `t_ingre_contenir_allergie`;

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_pers
DROP TABLE IF EXISTS `t_pers`;
CREATE TABLE IF NOT EXISTS `t_pers` (
  `id_pers` int NOT NULL AUTO_INCREMENT,
  `nom_pers` varchar(30) DEFAULT NULL,
  `prenom_pers` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_pers`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_pers : ~3 rows (environ)
DELETE FROM `t_pers`;
INSERT INTO `t_pers` (`id_pers`, `nom_pers`, `prenom_pers`) VALUES
	(6, 'thomas', 'ferguson'),
	(7, 'henry', 'du-buisson'),
	(8, 'matt', 'dupont');

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_pers_avoir_allergie
DROP TABLE IF EXISTS `t_pers_avoir_allergie`;
CREATE TABLE IF NOT EXISTS `t_pers_avoir_allergie` (
  `id_pers_avoir_allergie` int NOT NULL AUTO_INCREMENT,
  `fk_pers` int DEFAULT NULL,
  `fk_allergie` int DEFAULT NULL,
  PRIMARY KEY (`id_pers_avoir_allergie`),
  KEY `fk_allergie_pers` (`fk_allergie`),
  KEY `fk_pers` (`fk_pers`),
  CONSTRAINT `fk_allergie_pers` FOREIGN KEY (`fk_allergie`) REFERENCES `t_allergie` (`id_allergie`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_pers` FOREIGN KEY (`fk_pers`) REFERENCES `t_pers` (`id_pers`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_pers_avoir_allergie : ~4 rows (environ)
DELETE FROM `t_pers_avoir_allergie`;
INSERT INTO `t_pers_avoir_allergie` (`id_pers_avoir_allergie`, `fk_pers`, `fk_allergie`) VALUES
	(22, 7, 22),
	(23, 8, 22),
	(24, 6, 25),
	(25, 8, 24);

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_plat
DROP TABLE IF EXISTS `t_plat`;
CREATE TABLE IF NOT EXISTS `t_plat` (
  `id_plat` int NOT NULL AUTO_INCREMENT,
  `nom_plat` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `description_plat` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `informations_nutritionnelles_plat` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  `image_plat` mediumtext CHARACTER SET latin1 COLLATE latin1_swedish_ci,
  `prix_plat` int DEFAULT NULL,
  PRIMARY KEY (`id_plat`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_plat : ~1 rows (environ)
DELETE FROM `t_plat`;
INSERT INTO `t_plat` (`id_plat`, `nom_plat`, `description_plat`, `informations_nutritionnelles_plat`, `image_plat`, `prix_plat`) VALUES
	(1, 'travers_de_porc', 'travers de porc a la sauce champignons', 'travers de port 300 calories 32g proteines', 'https://res.cloudinary.com/hv9ssmzrz/image/fetch/c_fill,f_auto,h_387,q_auto,w_650/https://s3-eu-west-1.amazonaws.com/images-ca-1-0-1-eu/tag_photos/original/9517/ribs-flickr-5870696558_52a7862cc7_b.jpg', 20);

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_plat_avoir_ingre
DROP TABLE IF EXISTS `t_plat_avoir_ingre`;
CREATE TABLE IF NOT EXISTS `t_plat_avoir_ingre` (
  `id_plat_avoir_ingre` int NOT NULL AUTO_INCREMENT,
  `fk_plat` int DEFAULT NULL,
  `fk_ingre` int DEFAULT NULL,
  PRIMARY KEY (`id_plat_avoir_ingre`) USING BTREE,
  KEY `fk_ingredient` (`fk_ingre`) USING BTREE,
  KEY `fk_plat_ingre` (`fk_plat`),
  CONSTRAINT `fk_ingre` FOREIGN KEY (`fk_ingre`) REFERENCES `t_ingre` (`id_ingre`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_plat_ingre` FOREIGN KEY (`fk_plat`) REFERENCES `t_plat` (`id_plat`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_plat_avoir_ingre : ~0 rows (environ)
DELETE FROM `t_plat_avoir_ingre`;

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_plat_avoir_restri_diet
DROP TABLE IF EXISTS `t_plat_avoir_restri_diet`;
CREATE TABLE IF NOT EXISTS `t_plat_avoir_restri_diet` (
  `id_plat_avoir_restri_diet` int NOT NULL AUTO_INCREMENT,
  `fk_restri_diet` int DEFAULT NULL,
  `fk_plat` int DEFAULT NULL,
  PRIMARY KEY (`id_plat_avoir_restri_diet`) USING BTREE,
  KEY `fk_restriction_dietetique` (`fk_restri_diet`) USING BTREE,
  KEY `fk_plat_restri` (`fk_plat`),
  CONSTRAINT `fk_plat_restri` FOREIGN KEY (`fk_plat`) REFERENCES `t_plat` (`id_plat`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_restri_diet` FOREIGN KEY (`fk_restri_diet`) REFERENCES `t_restri_diet` (`id_restri_diet`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_plat_avoir_restri_diet : ~0 rows (environ)
DELETE FROM `t_plat_avoir_restri_diet`;

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_plat_etre_type
DROP TABLE IF EXISTS `t_plat_etre_type`;
CREATE TABLE IF NOT EXISTS `t_plat_etre_type` (
  `id_plat_etre_type` int NOT NULL AUTO_INCREMENT,
  `fk_type` int DEFAULT NULL,
  `fk_plat` int DEFAULT NULL,
  PRIMARY KEY (`id_plat_etre_type`),
  KEY `fk_type` (`fk_type`),
  KEY `fk_plat` (`fk_plat`),
  CONSTRAINT `fk_plat` FOREIGN KEY (`fk_plat`) REFERENCES `t_plat` (`id_plat`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_type` FOREIGN KEY (`fk_type`) REFERENCES `t_type` (`id_type`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_plat_etre_type : ~0 rows (environ)
DELETE FROM `t_plat_etre_type`;

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_restri_diet
DROP TABLE IF EXISTS `t_restri_diet`;
CREATE TABLE IF NOT EXISTS `t_restri_diet` (
  `id_restri_diet` int NOT NULL AUTO_INCREMENT,
  `nom_restri_diet` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  PRIMARY KEY (`id_restri_diet`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_restri_diet : ~0 rows (environ)
DELETE FROM `t_restri_diet`;

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_type
DROP TABLE IF EXISTS `t_type`;
CREATE TABLE IF NOT EXISTS `t_type` (
  `id_type` int NOT NULL AUTO_INCREMENT,
  `nom_type` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  PRIMARY KEY (`id_type`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_type : ~3 rows (environ)
DELETE FROM `t_type`;
INSERT INTO `t_type` (`id_type`, `nom_type`) VALUES
	(4, 'dessert'),
	(5, 'entrée'),
	(6, 'plat principal');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
