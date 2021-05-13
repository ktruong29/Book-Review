BOOKDROP DATABASE `LIBRARY`;
CREATE DATABASE IF NOT EXISTS `LIBRARY` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `LIBRARY`;

CREATE TABLE IF NOT EXISTS `PERSON`
(
    `id` 		INT NOT NULL AUTO_INCREMENT,
    `FirstName` 	VARCHAR(50) NOT NULL,
    `LastName` 		VARCHAR(50) NOT NULL,
    `Email` 		VARCHAR(100) NOT NULL,
    `Role` 		VARCHAR(10) NOT NULL,
    `Username` 		VARCHAR(50) NOT NULL,
    `Password` 		VARCHAR(100) NOT NULL,
    `User_Picture_LINK` VARCHAR(255) NULL,
    PRIMARY KEY (`id`)
);
ALTER TABLE PERSON
ADD COLUMN Profile_URL VARCHAR(50) DEFAULT "piglet.jpg" AFTER Password;

-- Drop auto_increment before dropping the primary key
ALTER TABLE PERSON MODIFY id INT NOT NULL;
-- Delete primary key id
ALTER TABLE PERSON DROP PRIMARY KEY;
-- Add primary key to the table PERSON
ALTER TABLE PERSON
ADD PRIMARY KEY(Username);

CREATE TABLE IF NOT EXISTS `BOOK`
(
  `ISBN` 		VARCHAR(20) NOT NULL,
  `Title` 		VARCHAR(255) NULL,
  `Description` 	TEXT(3000) NULL,
  `AuthorName` 		VARCHAR(100) NULL,
  `AverageRating` 	DECIMAL(4,2) NULL,
  `URL_LINK` 		VARCHAR(255) NULL,
  `Picture_LINK` 	VARCHAR(255) NULL,
  PRIMARY KEY (`ISBN`)
);
-- Modify the AverageRating column to have the default value of 0.0 --
ALTER TABLE BOOK
MODIFY AverageRating DECIMAL(4,2) DEFAULT 0.0;

-- Update the AverageRating of all books to 0.0; previously had non-zero values --
UPDATE BOOK
SET AverageRating = 0.0
WHERE ISBN = '0135235006';

UPDATE BOOK
SET AverageRating = 0.0
WHERE ISBN = '059035342X';

UPDATE BOOK
SET AverageRating = 0.0
WHERE ISBN = 'B07VZ27MG3';

-- Drop COMMENT and RATING first
-- DROP TABLE RATING;
-- DROP TABLE COMMENT;

CREATE TABLE IF NOT EXISTS `COMMENT`
(
  `CommentID` 	INT NOT NULL auto_increment,
  `DatePosted` 	DATETIME NOT NULL,
  `Comment` 	TEXT(3000) NULL,
  `Username` 	VARCHAR(50) NOT NULL,
  `ISBN` 	VARCHAR(20) NOT NULL,
  PRIMARY KEY (`CommentID`),
  FOREIGN KEY(`Username`) REFERENCES PERSON(`Username`)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
  FOREIGN KEY(`ISBN`) REFERENCES BOOK(`ISBN`)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `RATING`
(
    `Rating`	DECIMAL(4,2) DEFAULT 0.0,
    `Username`	VARCHAR(50) NOT NULL,
    `ISBN` 	VARCHAR(20) NOT NULL,
    PRIMARY KEY(Username, ISBN),
    FOREIGN KEY(`Username`) REFERENCES PERSON(`Username`)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
    FOREIGN KEY(`ISBN`) REFERENCES BOOK(`ISBN`)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);


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

INSERT INTO `LIBRARY`.`BOOK` (`ISBN`, `Title`, `Description`, `AuthorName`, `URL_LINK`, `Picture_LINK`) VALUES ('1559369523', 'Fairview', 'Grandma’s birthday approaches. Beverly is organizing the perfect dinner, but everything seems doomed from the start: the silverware is all wrong, the carrots need chopping and the radio is on the fritz. What at first appears to be a family comedy takes a sharp, sly turn into a startling examination of deep-seated paradigms about race in America.', 'Jackie Sibblies Drury', 'https://www.amazon.com/dp/1559369523/ref=s9_acsd_al_bw_c2_x_1_i?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=6E3VC8GKVBKQDB2ME286&pf_rd_t=101&pf_rd_p=36c65f93-f322-4319-94c0-dc0769427bf2&pf_rd_i=6960520011', 'Fairview.PNG');
INSERT INTO `LIBRARY`.`BOOK` (`ISBN`, `Title`, `Description`, `AuthorName`, `URL_LINK`, `Picture_LINK`) VALUES ('1416590323', 'Frederick Douglass: Prophet of Freedom', 'As a young man Frederick Douglass (1818–1895) escaped from slavery in Baltimore, Maryland. He was fortunate to have been taught to read by his slave owner mistress, and he would go on to become one of the major literary figures of his time. His very existence gave the lie to slave owners: with dignity and great intelligence he bore witness to the brutality of slavery.', 'David W. Blight', 'https://www.amazon.com/dp/1416590323/ref=s9_acsd_al_bw_c2_x_2_i?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=6E3VC8GKVBKQDB2ME286&pf_rd_t=101&pf_rd_p=36c65f93-f322-4319-94c0-dc0769427bf2&pf_rd_i=6960520011', 'Frederick Douglass Prophet of Freedom.PNG');
INSERT INTO `LIBRARY`.`BOOK` (`ISBN`, `Title`, `Description`, `AuthorName`, `URL_LINK`, `Picture_LINK`) VALUES ('019508957X', 'The New Negro: The Life of Alain Locke', 'A tiny, fastidiously dressed man emerged from Black Philadelphia around the turn of the century to mentor a generation of young artists including Langston Hughes, Zora Neale Hurston, and Jacob Lawrence and call them the New Negro -- the creative African Americans whose art, literature, music, and drama would inspire Black people to greatness.', 'Jeffrey C. Stewart', 'https://www.amazon.com/dp/019508957X/ref=s9_acsd_al_bw_c2_x_3_i?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=6E3VC8GKVBKQDB2ME286&pf_rd_t=101&pf_rd_p=36c65f93-f322-4319-94c0-dc0769427bf2&pf_rd_i=6960520011', 'The New Negro The Life of Alain Locke.PNG');
INSERT INTO `LIBRARY`.`BOOK` (`ISBN`, `Title`, `Description`, `AuthorName`, `URL_LINK`, `Picture_LINK`) VALUES ('811226050', 'Be With', 'Drawing from his experience as a translator, Forrest Gander includes in the first, powerfully elegiac section a version of a poem by the Spanish mystical poet St. John of the Cross. He continues with a long multilingual poem examining the syncretic geological and cultural history of the U.S. border with Mexico. The poems of the third section―a moving transcription of Gander’s efforts to address his mother dying of Alzheimer’s―rise from the page like hymns, transforming slowly from reverence to revelation. Gander has been called one of our most formally restless poets, and these new poems express a characteristically tensile energy and, as one critic noted, “the most eclectic diction since Hart Crane.”', 'Forrest Gander', 'https://www.amazon.com/dp/0811226050/ref=s9_acsd_al_bw_c2_x_4_i?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=6E3VC8GKVBKQDB2ME286&pf_rd_t=101&pf_rd_p=36c65f93-f322-4319-94c0-dc0769427bf2&pf_rd_i=6960520011', 'Be With.PNG');
INSERT INTO `LIBRARY`.`BOOK` (`ISBN`, `Title`, `Description`, `AuthorName`, `URL_LINK`, `Picture_LINK`) VALUES ('1250215072', 'Amity and Prosperity: One Family and the Fracturing of America', 'In Amity and Prosperity, the prizewinning poet and journalist Eliza Griswold tells the story of the energy boom’s impact on a small town at the edge of Appalachia and one woman’s transformation from a struggling single parent to an unlikely activist.', 'Eliza Griswold', 'https://www.amazon.com/dp/1250215072/ref=s9_acsd_al_bw_c2_x_5_i?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=6E3VC8GKVBKQDB2ME286&pf_rd_t=101&pf_rd_p=36c65f93-f322-4319-94c0-dc0769427bf2&pf_rd_i=6960520011', 'Amity and Prosperity One Family and the Fracturing of America.PNG');
INSERT INTO `LIBRARY`.`BOOK` (`ISBN`, `Title`, `Description`, `AuthorName`, `URL_LINK`, `Picture_LINK`) VALUES ('714876453', 'Chicken and Charcoal:Yakitori, Yardbird, Hong Kong', 'Chicken is the world\'s best loved meat, and yakitori is one of the simplest, healthiest ways to cook it. At Yardbird in Hong Kong, Canadian chef Matt Abergel has put yakitori on the global culinary map. Here, in vivid style, with strong visual references to Abergel\'s passion for skateboarding, he reveals the magic behind the restaurant\'s signature recipes, together with detailed explanations of how they source, butcher, skewer, and cook the birds with no need for special equipment. Fire up the grill, and enjoy. The first comprehensive book about yakitori to be published in English, this book will appeal to home cooks and professional chefs alike.', 'Matt Abergel', 'https://www.amazon.com/dp/0714876453/ref=s9_acsd_al_bw_c2_x_0_i?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-5&pf_rd_r=6E3VC8GKVBKQDB2ME286&pf_rd_t=101&pf_rd_p=84ba7cd8-e8fa-41ed-89f6-587cfbc87ee6&pf_rd_i=6960520011', 'Chicken and Charcoal Yakitori, Yardbird, Hong Kong.PNG');
INSERT INTO `LIBRARY`.`BOOK` (`ISBN`, `Title`, `Description`, `AuthorName`, `URL_LINK`, `Picture_LINK`) VALUES ('765387522', 'Vengeful', 'Magneto and Professor X. Superman and Lex Luthor. Victor Vale and Eli Ever. Sydney and Serena Clarke. Great partnerships, now soured on the vine. But Marcella Riggins needs no one. Flush from her brush with death, she’s finally gained the control she’s always sought―and will use her new-found power to bring the city of Merit to its knees. She’ll do whatever it takes, collecting her own sidekicks, and leveraging the two most infamous EOs, Victor Vale and Eli Ever, against each other. With Marcella\'s rise, new enmities create opportunity--and the stage of Merit City will once again be set for a final, terrible reckoning.', ' V. E. Schwab', 'https://www.amazon.com/dp/0765387522/ref=s9_acsd_al_bw_c2_x_6_i?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-10&pf_rd_r=6E3VC8GKVBKQDB2ME286&pf_rd_t=101&pf_rd_p=c9ba04c7-8a60-42ba-8d20-529a6e9d69f4&pf_rd_i=6960520011', 'Vengeful.PNG');
INSERT INTO `LIBRARY`.`BOOK` (`ISBN`, `Title`, `Description`, `AuthorName`, `URL_LINK`, `Picture_LINK`) VALUES ('1481463349', 'All American Boys', 'A bag of chips. That’s all sixteen-year-old Rashad is looking for at the corner bodega. What he finds instead is a fist-happy cop, Paul Galluzzo, who mistakes Rashad for a shoplifter, mistakes Rashad’s pleadings that he’s stolen nothing for belligerence, mistakes Rashad’s resistance to leave the bodega as resisting arrest, mistakes Rashad’s every flinch at every punch the cop throws as further resistance and refusal to STAY STILL as ordered. But how can you stay still when someone is pounding your face into the concrete pavement?', 'Jason Reynolds', 'https://www.amazon.com/All-American-Boys-Jason-Reynolds/dp/1481463349/ref=pd_bkstr_rtpb_5?_encoding=UTF8&pd_rd_i=1481463349&pd_rd_r=7d38fca1-2a98-4d45-b7a5-bfbc1b1931e1&pd_rd_w=wwhdX&pd_rd_wg=sZkfc&pf_rd_p=cf35b793-d3c7-404e-8f37-f9e58567007f&pf_rd_r=XEKJQH058B0TYHMK7Q11&psc=1&refRID=XFK7AVCMMKS1RG6H740P', 'All American Boys.jpg');
INSERT INTO `LIBRARY`.`BOOK` (`ISBN`, `Title`, `Description`, `AuthorName`, `URL_LINK`, `Picture_LINK`) VALUES ('691129088', 'Game Theory: An Introduction', 'This comprehensive textbook introduces readers to the principal ideas and applications of game theory, in a style that combines rigor with accessibility. Steven Tadelis begins with a concise description of rational decision making, and goes on to discuss strategic and extensive form games with complete information, Bayesian games, and extensive form games with imperfect information. He covers a host of topics, including multistage and repeated games, bargaining theory, auctions, rent-seeking games, mechanism design, signaling games, reputation building, and information transmission games. Unlike other books on game theory, this one begins with the idea of rationality and explores its implications for multiperson decision problems through concepts like dominated strategies and rationalizability. Only then does it present the subject of Nash equilibrium and its derivatives.', 'Steven Tadelis', 'https://www.amazon.com/Game-Theory-Introduction-Steven-Tadelis/dp/0691129088/ref=pd_bkstr_rtpb_39?_encoding=UTF8&pd_rd_i=0691129088&pd_rd_r=7d38fca1-2a98-4d45-b7a5-bfbc1b1931e1&pd_rd_w=wwhdX&pd_rd_wg=sZkfc&pf_rd_p=cf35b793-d3c7-404e-8f37-f9e58567007f&pf_rd_r=XEKJQH058B0TYHMK7Q11&psc=1&refRID=YNA27HS4C8YA6S3D27XS', 'Game Theory An Introduction.jpg');
INSERT INTO `LIBRARY`.`BOOK` (`ISBN`, `Title`, `Description`, `AuthorName`, `URL_LINK`, `Picture_LINK`) VALUES ('9781250132130', 'Nevernight: Book One of the Nevernight Chronicle (The Nevernight Chronicle, 1)', 'In a land where three suns almost never set, a fledgling killer joins a school of assassins, seeking vengeance against the powers who destroyed her family. Daughter of an executed traitor, Mia Corvere is barely able to escape her father’s failed rebellion with her life. Alone and friendless, she hides in a city built from the bones of a dead god, hunted by the Senate and her father’s former comrades. But her gift for speaking with the shadows leads her to the door of a retired killer, and a future she never imagined. Now, a sixteen year old Mia is apprenticed to the deadliest flock of assassins in the entire Republic ― the Red Church. Treachery and trials await her with the Church’s halls, and to fail is to die. But if she survives to initiation, Mia will be inducted among the chosen of the Lady of Blessed Murder, and one step closer to the only thing she desires.', 'Jay Kristoff', 'https://www.amazon.com/Nevernight-Book-One-Chronicle/dp/1250132134/ref=pd_bkstr_rtpb_48?_encoding=UTF8&pd_rd_i=1250132134&pd_rd_r=7d38fca1-2a98-4d45-b7a5-bfbc1b1931e1&pd_rd_w=wwhdX&pd_rd_wg=sZkfc&pf_rd_p=cf35b793-d3c7-404e-8f37-f9e58567007f&pf_rd_r=XEKJQH058B0TYHMK7Q11&psc=1&refRID=YNA27HS4C8YA6S3D27XS', 'Nevernight 1.jpg');

