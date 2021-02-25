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

CREATE TABLE IF NOT EXISTS `COMMENT` (
  `CommentID` INT NOT NULL,
  `DatePosted` DATETIME NOT NULL,
  `Comment` TEXT(3000) NULL,
  `Rating` INT NULL,
  `PersonID` VARCHAR(45) NOT NULL,
  `ISBN` INT NOT NULL,
  PRIMARY KEY (`CommentID`));

CREATE TABLE IF NOT EXISTS `BOOK` (
  `ISBN` INT NOT NULL,
  `Title` VARCHAR(255) NULL,
  `Description` TEXT(3000) NULL,
  `AuthorName` VARCHAR(45) NULL,
  `AverageRating` DECIMAL(4,2) NULL,
  `URL_LINK` VARCHAR(255) NULL,
  PRIMARY KEY (`ISBN`));
