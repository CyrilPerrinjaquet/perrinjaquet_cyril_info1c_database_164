-- OM 2021.02.17
-- FICHIER MYSQL POUR FAIRE FONCTIONNER LES EXEMPLES
-- DE REQUETES MYSQL
-- Database: cyril_perrinjaquet_info_1c_164

-- Destruction de la BD si elle existe.
-- Pour être certain d'avoir la dernière version des données

DROP DATABASE IF EXISTS cyril_perrinjaquet_info_1c_164;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS cyril_perrinjaquet_info_1c_164;

-- Utilisation de cette base de donnée

USE cyril_perrinjaquet_info_1c_164;
-- --------------------------------------------------------
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
  `notes_allergie` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_allergie`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_allergie : ~0 rows (environ)
DELETE FROM `t_allergie`;
INSERT INTO `t_allergie` (`id_allergie`, `nom_allergie`, `allergene_allergie`, `gravite_allergie`, `symptomes_allergie`, `precautions_allergie`, `traitement_allergie`, `notes_allergie`) VALUES
	(1, 'asthme', 'acariens ', 'severe', 'respiration sifflante', 'aspirez_poussiere', 'ventolin', NULL);

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_ingredients_menu_stamm
DROP TABLE IF EXISTS `t_ingredients_menu_stamm`;
CREATE TABLE IF NOT EXISTS `t_ingredients_menu_stamm` (
  `id_ingredients_menu_stamm` int NOT NULL AUTO_INCREMENT,
  `nom_ingredients_menu_stamm` int DEFAULT NULL,
  PRIMARY KEY (`id_ingredients_menu_stamm`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_ingredients_menu_stamm : ~0 rows (environ)
DELETE FROM `t_ingredients_menu_stamm`;

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_menu
DROP TABLE IF EXISTS `t_menu`;
CREATE TABLE IF NOT EXISTS `t_menu` (
  `id_menu` int NOT NULL AUTO_INCREMENT,
  `nom_menu` varchar(50) NOT NULL DEFAULT '0',
  `description_menu` varchar(50) DEFAULT NULL,
  `type_menu` tinytext CHARACTER SET latin1 COLLATE latin1_swedish_ci,
  `prix_menu` varchar(50) DEFAULT NULL,
  `ingredient_menu` varchar(50) DEFAULT NULL,
  `informations_nutritionnelles_menu` varchar(50) DEFAULT NULL,
  `restrictions_dietetiques_menu` varchar(50) DEFAULT NULL,
  `image_menu` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_menu`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_menu : ~0 rows (environ)
DELETE FROM `t_menu`;
INSERT INTO `t_menu` (`id_menu`, `nom_menu`, `description_menu`, `type_menu`, `prix_menu`, `ingredient_menu`, `informations_nutritionnelles_menu`, `restrictions_dietetiques_menu`, `image_menu`) VALUES
	(1, 'travers_de_porc', 'travers de porc a la sauce champignons', 'plat_principale', '20_chf', 'travers de porc 250g', 'travers de port 300 calories 32g proteines', NULL, NULL);

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_menu_stamm
DROP TABLE IF EXISTS `t_menu_stamm`;
CREATE TABLE IF NOT EXISTS `t_menu_stamm` (
  `id_menu_stamm` int NOT NULL AUTO_INCREMENT,
  `nom_menu_stamm` varchar(100) DEFAULT NULL,
  `restrictions_dietetiques_menu_stamm` varchar(50) DEFAULT NULL,
  `informations_nutritionnelles_menu_stamm` varchar(50) DEFAULT NULL,
  `description_menu_stamm` varchar(120) DEFAULT NULL,
  `image_menu_stamm` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_menu_stamm`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_menu_stamm : ~0 rows (environ)
DELETE FROM `t_menu_stamm`;

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_menu_stamm_avoir_ingredients
DROP TABLE IF EXISTS `t_menu_stamm_avoir_ingredients`;
CREATE TABLE IF NOT EXISTS `t_menu_stamm_avoir_ingredients` (
  `id_pers_commander_menu_stamm` int NOT NULL AUTO_INCREMENT,
  `fk_ingredients` int NOT NULL,
  `fk_menu_stamm` int NOT NULL,
  PRIMARY KEY (`id_pers_commander_menu_stamm`),
  KEY `FK_t_ingredients` (`fk_menu_stamm`),
  KEY `FK_t_menu_stamm_` (`fk_ingredients`),
  CONSTRAINT `FK_t_ingredients` FOREIGN KEY (`fk_menu_stamm`) REFERENCES `t_menu_stamm` (`id_menu_stamm`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_t_menu_stamm_` FOREIGN KEY (`fk_ingredients`) REFERENCES `t_ingredients_menu_stamm` (`id_ingredients_menu_stamm`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_menu_stamm_avoir_ingredients : ~0 rows (environ)
DELETE FROM `t_menu_stamm_avoir_ingredients`;

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_menu_stamm_etre_type
DROP TABLE IF EXISTS `t_menu_stamm_etre_type`;
CREATE TABLE IF NOT EXISTS `t_menu_stamm_etre_type` (
  `id_menu_stamm_etre_type` int NOT NULL AUTO_INCREMENT,
  `fk_type` int DEFAULT NULL,
  `fk_menu_stamm` int DEFAULT NULL,
  PRIMARY KEY (`id_menu_stamm_etre_type`),
  KEY `FK_t_type` (`fk_type`),
  KEY `FK_t_menu_stamm_type` (`fk_menu_stamm`),
  CONSTRAINT `FK_t_type` FOREIGN KEY (`fk_type`) REFERENCES `t_type_menu_stamm` (`id_type_menu_stamm`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_menu_stamm_etre_type : ~0 rows (environ)
DELETE FROM `t_menu_stamm_etre_type`;

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_personne
DROP TABLE IF EXISTS `t_personne`;
CREATE TABLE IF NOT EXISTS `t_personne` (
  `id_pers` int NOT NULL AUTO_INCREMENT,
  `nom_pers` varchar(30) DEFAULT NULL,
  `prenom_pers` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_pers`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_personne : ~0 rows (environ)
DELETE FROM `t_personne`;
INSERT INTO `t_personne` (`id_pers`, `nom_pers`, `prenom_pers`) VALUES
	(1, 'turlututu', 'chapeau');

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_pers_annuler_menu_stamm
DROP TABLE IF EXISTS `t_pers_annuler_menu_stamm`;
CREATE TABLE IF NOT EXISTS `t_pers_annuler_menu_stamm` (
  `id_pers_annuler_menu_stamm` int NOT NULL AUTO_INCREMENT,
  `date_pers_annuler_menu_stamm` timestamp NULL DEFAULT NULL,
  `fk_pers` int DEFAULT NULL,
  `fk_menu_stamm` int DEFAULT NULL,
  PRIMARY KEY (`id_pers_annuler_menu_stamm`),
  KEY `FK_t_personne_annuler_menu_stamm` (`fk_pers`),
  KEY `FK_t_menu_stamm_annuler` (`fk_menu_stamm`),
  CONSTRAINT `FK_t_menu_stamm_annuler` FOREIGN KEY (`fk_menu_stamm`) REFERENCES `t_menu_stamm` (`id_menu_stamm`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_t_personne_annuler_menu_stamm` FOREIGN KEY (`fk_pers`) REFERENCES `t_personne` (`id_pers`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_pers_annuler_menu_stamm : ~0 rows (environ)
DELETE FROM `t_pers_annuler_menu_stamm`;

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_pers_commander_menu_stamm
DROP TABLE IF EXISTS `t_pers_commander_menu_stamm`;
CREATE TABLE IF NOT EXISTS `t_pers_commander_menu_stamm` (
  `id_pers_commander_menu_stamm` int NOT NULL AUTO_INCREMENT,
  `date_pers_commander_menu_stamm` timestamp NULL DEFAULT NULL,
  `fk_pers` int DEFAULT NULL,
  `fk_menu_stamm` int DEFAULT NULL,
  PRIMARY KEY (`id_pers_commander_menu_stamm`),
  KEY `FK_t_menu_stamm_commander` (`fk_menu_stamm`),
  KEY `FK_t_personne_commander_menu_stamm` (`fk_pers`),
  CONSTRAINT `FK_t_menu_stamm_commander` FOREIGN KEY (`fk_menu_stamm`) REFERENCES `t_menu_stamm` (`id_menu_stamm`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_t_personne_commander_menu_stamm` FOREIGN KEY (`fk_pers`) REFERENCES `t_personne` (`id_pers`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_pers_commander_menu_stamm : ~0 rows (environ)
DELETE FROM `t_pers_commander_menu_stamm`;

-- Listage de la structure de table cyril_perrinjaquet_info_1c_164. t_type_menu_stamm
DROP TABLE IF EXISTS `t_type_menu_stamm`;
CREATE TABLE IF NOT EXISTS `t_type_menu_stamm` (
  `id_type_menu_stamm` int NOT NULL AUTO_INCREMENT,
  `nom_type_menu_stamm` int DEFAULT NULL,
  PRIMARY KEY (`id_type_menu_stamm`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Listage des données de la table cyril_perrinjaquet_info_1c_164.t_type_menu_stamm : ~0 rows (environ)
DELETE FROM `t_type_menu_stamm`;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
