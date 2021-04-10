DROP DATABASE `LIBRARY`;
CREATE DATABASE IF NOT EXISTS `LIBRARY` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `LIBRARY`;

CREATE TABLE IF NOT EXISTS `PERSON`
(
		`id` 				INT NOT NULL AUTO_INCREMENT,
    `FirstName` VARCHAR(50) NOT NULL,
    `LastName` 	VARCHAR(50) NOT NULL,
    `Email` 		VARCHAR(100) NOT NULL,
    `Role` 			VARCHAR(10) NOT NULL,
    `Username` 	VARCHAR(50) NOT NULL,
    `Password` 	VARCHAR(100) NOT NULL,
    `User_Picture_LINK` 		VARCHAR(255) NULL,
    PRIMARY KEY (`id`)
);


CREATE TABLE IF NOT EXISTS `BOOK`
(
  `ISBN` 					VARCHAR(20) NOT NULL,
  `Title` 				VARCHAR(255) NULL,
  `Description` 	TEXT(3000) NULL,
  `AuthorName` 		VARCHAR(100) NULL,
  `AverageRating` DECIMAL(4,2) NULL,
  `URL_LINK` 			VARCHAR(255) NULL,
  `Picture_LINK` 		VARCHAR(255) NULL,
  PRIMARY KEY (`ISBN`)
);



CREATE TABLE IF NOT EXISTS `COMMENT`
(
  `CommentID` 	INT NOT NULL,
  `DatePosted` 	DATETIME NOT NULL,
  `Comment` 		TEXT(3000) NULL,
  `Rating` 			INT NULL,
  `PersonID` 		INT NOT NULL,
  `ISBN` 				VARCHAR(20) NOT NULL,
  PRIMARY KEY (`CommentID`),
	FOREIGN KEY(`PersonID`) REFERENCES PERSON(`id`)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY(`ISBN`) REFERENCES BOOK(`ISBN`)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS `RATING`
(

);


ALTER TABLE PERSON
ADD COLUMN Profile_URL VARCHAR(50) DEFAULT "piglet.jpg" AFTER Password;

delete from `LIBRARY`.`BOOK`;
INSERT INTO BOOK(ISBN, Title, Description, AuthorName, AverageRating, URL_LINK, Picture_LINK)
VALUES ("0135235006", "Starting Out with C++: Early Objects(10th Edition)",  
"Starting Out with C++: Early Objects introduces the fundamentals of C++ programming in clear and easy-to-understand language, making it accessible to novice programming students as well as those who have worked with different languages. The text is designed for use in two- and three-term C++ programming sequences, as well as in accelerated one-term programs. Its wealth of real-world examples encourages students to think about when, why, and how to apply the features and constructs of C++.", 
"Tony Gaddis, Judy Walters, and Godfrey Muganda", "8.0", 
"https://www.amazon.com/Starting-Out-Early-Objects-10th/dp/0135235006",
"Starting Out with C++ Early Objects 10th Edition.jpeg"),
("B07VZ27MG3", 
"Hamlet", 
"One of the greatest plays of all time, the compelling tragedy of the tormented young prince of Denmark continues to capture the imaginations of modern audiences worldwide. Confronted with evidence that his uncle murdered his father, and with his mother’s infidelity, Hamlet must find a means of reconciling his longing for oblivion with his duty as avenger. The ghost, Hamlet’s feigned madness, Ophelia’s death and burial, the play within a play, the “closet scene” in which Hamlet accuses his mother of complicity in murder, and breathtaking swordplay are just some of the elements that make Hamlet an enduring masterpiece of the theater.", 
"William Shakespeare", "9.0",
"https://www.amazon.com/Hamlet-William-Shakespeare-ebook/dp/B07VZ27MG3",
"Hamlet.jpg"),
("059035342X", 
"Harry Potter and the Sorcerer's Stone", 
"Harry Potter has no idea how famous he is. That's because he's being raised by his miserable aunt and uncle who are terrified Harry will learn that he's really a wizard, just as his parents were. But everything changes when Harry is summoned to attend an infamous school for wizards, and he begins to discover some clues about his illustrious birthright. From the surprising way he is greeted by a lovable giant, to the unique curriculum and colorful faculty at his unusual school, Harry finds himself drawn deep inside a mystical world he never knew existed and closer to his own noble destiny.", 
"J.K. Rowling", "9.0",
"https://www.amazon.com/Potter-Sorcerers-Potters-Rowling-Paperback/dp/B00OHX65I2/ref=sr_1_4?dchild=1&keywords=Harry+Potter+and+the+Sorcerer%27s+Stone&qid=1617084726&s=books&sr=1-4",
"Harry Potter1.jpg");
