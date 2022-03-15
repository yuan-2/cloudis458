DROP Database IF EXISTS `cloud`;
Create DATABASE `cloud`;
USE `cloud`;

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`username`)
) ;

DROP TABLE IF EXISTS `item`;
CREATE TABLE IF NOT EXISTS `item` (
  `itemID` int NOT NULL AUTO_INCREMENT,
  `itemName` varchar(50) NOT NULL,
  `category` varchar(50) NOT NULL,
  `description` varchar(50) NOT NULL,
  `itemImg` varchar(50) NOT NULL,
  PRIMARY KEY (`itemID`)
) ;

DROP TABLE IF EXISTS `purchase`;
CREATE TABLE IF NOT EXISTS `purchase` (
  `purchaseID` varchar(30) NOT NULL,
  `username` int NOT NULL,
  `itemID` int NOT NULL,
  PRIMARY KEY (`purchaseID`),
  FOREIGN KEY (`username`) references user (`username`)
) ;


-- INSERT values
INSERT INTO user (`username`, `password`) VALUES 
('amanda', 'amanda1');
INSERT INTO user (`username`, `password`) VALUES 
('yuanyuan', 'yuanyuan1');