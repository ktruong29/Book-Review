CREATE DATABASE IF NOT EXISTS `LIBRARY` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `LIBRARY`;

CREATE TABLE IF NOT EXISTS `PERSON` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    `FirstName` varchar(50) NOT NULL,
    `LastName` varchar(50) NOT NULL,
    `Email` varchar(100) NOT NULL,
    `Role` varchar(10) NOT NULL,
    `Username` varchar(50) NOT NULL,
    `Password` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8;
