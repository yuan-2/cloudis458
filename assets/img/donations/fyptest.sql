DROP Database IF EXISTS `fyptest`;
Create DATABASE `fyptest`;
USE `fyptest`;

DROP TABLE IF EXISTS `carousel`;
CREATE TABLE IF NOT EXISTS `carousel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `itemName` varchar(50) NOT NULL,
  `description` varchar(300) NOT NULL,
  `donorName` varchar(50) NOT NULL,
  `donorAddr` varchar(300) NOT NULL,
  `contactNo` int NOT NULL,
  `category` varchar(20) NOT NULL,
  `quantity` INT(4) NOT NULL,
  `requireDelivery` varchar(50) NOT NULL,
  `region` varchar(20) NOT NULL,
  `timeSubmitted` DATETIME NOT NULL,
  `itemStatus` varchar(50) NOT NULL,
  `fileName` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ;

DROP TABLE IF EXISTS `wishlist`;
CREATE TABLE IF NOT EXISTS `wishlist` (
  `id` int NOT NULL AUTO_INCREMENT,
  `itemName` varchar(50) NOT NULL,
  `quantity` int NOT NULL,
  `remarks` varchar(300) NOT NULL,
  `category` varchar(50) NOT NULL,
  `timeSubmitted` datetime NOT NULL,
  `itemStatus` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ;

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `username` int NOT NULL,
  `password` varchar(100) NOT NULL,
  `usertype` varchar(20)  NOT NULL,
  PRIMARY KEY (`username`)
) ;

DROP TABLE IF EXISTS `driver`;
CREATE TABLE IF NOT EXISTS `driver` (
  `contactNo` int NOT NULL,
  PRIMARY KEY (`contactNo`),
  FOREIGN KEY (`contactNo`) references user (`username`)
) ;

DROP TABLE IF EXISTS `migrantworker`;
CREATE TABLE IF NOT EXISTS `migrantworker` (
  `contactNo` int NOT NULL,
  `address` varchar(300) NOT NULL,
  `reqHistory` varchar(50) NOT NULL,
  PRIMARY KEY (`contactNo`),
  FOREIGN KEY (`contactNo`) REFERENCES user (`username`)
) ;

DROP TABLE IF EXISTS `request`;
CREATE TABLE IF NOT EXISTS `request` (
  `reqID` int NOT NULL AUTO_INCREMENT,
  `requestorContactNo` int NOT NULL,
  `deliveryLocation` varchar(300) NOT NULL,
  `itemCategory` varchar(300) NOT NULL,
  `requestQty` varchar(50) NOT NULL,
  `timeSubmitted` datetime NOT NULL,
  PRIMARY KEY (`reqID`),
  FOREIGN KEY (`requestorContactNo`) REFERENCES user (`username`)
) ;

DROP TABLE IF EXISTS `delivery`;
CREATE TABLE IF NOT EXISTS `delivery` (
  `deliveryReqID` int NOT NULL AUTO_INCREMENT,
  `accepted` varchar(50) NOT NULL,
  `reqID` int NOT NULL,
  PRIMARY KEY (`deliveryReqID`),
  FOREIGN KEY (`reqID`) references request (`reqID`)
) ;

-- DROP TABLE IF EXISTS `category`;
-- CREATE TABLE IF NOT EXISTS `category` (
--   `categoryid` int NOT NULL AUTO_INCREMENT,
--   `categoryName` varchar(50) NOT NULL,
--   PRIMARY KEY (`categoryid`)
-- ) ;

DROP TABLE IF EXISTS `matches`;
CREATE TABLE IF NOT EXISTS `matches` (
  `matchID` int NOT NULL AUTO_INCREMENT,
  `reqID` int NOT NULL,
--   `requestorName` varchar(50) NOT NULL,
  `requestorContactNo` int NOT NULL,
  `donorName` varchar(50) NOT NULL,
  `donorContactNo` int NOT NULL,
  `requestedItem` varchar(50) NOT NULL,
  `itemCategory` varchar(50) NOT NULL,
  `matchDate` datetime NOT NULL,
  PRIMARY KEY (`matchID`)
) ;


-- DROP TABLE IF EXISTS `fixedItem`;
-- CREATE TABLE IF NOT EXISTS `fixedItem` (
--   `itemID` int NOT NULL AUTO_INCREMENT,
--   `itemName` varchar(50) NOT NULL,
--   PRIMARY KEY (`itemID`)
-- ) ;
-- 

DROP TABLE IF EXISTS `categoryitem`;
CREATE TABLE IF NOT EXISTS `categoryitem` (
  `itemid` int NOT NULL AUTO_INCREMENT,
  `itemname` varchar(50) NOT NULL,
  `attachedcategory` varchar(50) NOT NULL,
  PRIMARY KEY (`itemid`, `attachedCategory`)
) ;

DROP TABLE IF EXISTS `faq`;
CREATE TABLE IF NOT EXISTS `faq` (
  `faqID` int NOT NULL AUTO_INCREMENT,
  `question` varchar(300) NOT NULL,
  `answer` varchar(300) NOT NULL,
  `section` varchar(10) NOT NULL,
  PRIMARY KEY (`faqID`)
) ;

DROP TABLE IF EXISTS `formbuilder`;
CREATE TABLE IF NOT EXISTS `formbuilder` (
  `fieldID` int NOT NULL AUTO_INCREMENT,
  `formName` varchar(15) NOT NULL,
  `fieldName` varchar(50) NOT NULL,
  `fieldType` varchar(15) NOT NULL,
  `placeholder` varchar(50),
  `options` varchar(200),
  PRIMARY KEY (`fieldID`)
) ;

-- DROP TABLE IF EXISTS `criteria`;
-- CREATE TABLE IF NOT EXISTS `criteria` (
--   `migrantID` int NOT NULL,
--   `successMatchCount` varchar(15) NOT NULL,
--   `failMatchCount` varchar(15) NOT NULL,
--   `daysFromLastItem` varchar(50) NOT NULL,
--   PRIMARY KEY (`migrantID`),
--   FOREIGN KEY (`migrantID`) references migrantworker (`contactNo`)
-- ) ;

DROP TABLE IF EXISTS `formanswers`;
CREATE TABLE IF NOT EXISTS `formanswers` (
  `answerID` int NOT NULL AUTO_INCREMENT,
  `submissionID` varchar(30) NOT NULL,
  `formName` varchar(15) NOT NULL,
  `fieldID` int NOT NULL,
  `answer` varchar(50) NOT NULL,
  PRIMARY KEY (`answerID`),
  FOREIGN KEY (`fieldID`) references formbuilder (`fieldID`)
) ;

DROP TABLE IF EXISTS `newcarousel`;
CREATE TABLE IF NOT EXISTS `newcarousel` (
  `carouselID` int NOT NULL AUTO_INCREMENT,
  `donorID` int NOT NULL,
  `submissionID` varchar(30) NOT NULL,
  `itemName` varchar(50) NOT NULL,
  `itemCategory` varchar(20) NOT NULL,
  `timeSubmitted` DATETIME NOT NULL,
  `itemStatus` varchar(50) NOT NULL,
  PRIMARY KEY (`carouselID`)
) ;

DROP TABLE IF EXISTS `newwishlist`;
CREATE TABLE IF NOT EXISTS `newwishlist` (
  `submissionID` varchar(30) NOT NULL,
  `migrantID` int NOT NULL,
  `itemName` varchar(50) NOT NULL,
  `itemCategory` varchar(20) NOT NULL,
  `timeSubmitted` datetime NOT NULL,
  `itemStatus` varchar(50) NOT NULL,
  PRIMARY KEY (`submissionID`),
  FOREIGN KEY (`migrantID`) references user (`username`)
) ;


-- INSERT values

-- for carousel table
-- INSERT INTO carousel (`itemName`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
-- ('toothbrush', 'basic toiletries', 'yew wei', 'pasir ris grove', '92251521', 'toiletries', 1, 'yes', 'east', now(), 'available', 'toothbrush.png');
-- INSERT INTO carousel (`itemName`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
-- ('hair dryer', 'for hair', 'yuanyuan', '510121', '12345678', 'home appliances', 1, 'yes', 'west', now(), 'available', 'hairdryer.jpg');
-- INSERT INTO carousel (`itemName`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
-- ('t-shirts', 'free size t-shirts', 'amanda', '510425', '87654321', 'clothing', 1, 'yes', 'north', now(), 'available', 't-shirt.jpg');
-- INSERT INTO carousel (`itemName`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
-- ('rice cooker', 'to cook rice', 'nicole', '510180', '92251521', 'home appliances', 1, 'yes', 'south', now(), 'available', 'ricecooker.jpg');
-- INSERT INTO carousel (`itemName`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
-- ('fan', 'for sg hot weather', 'vanessa', 'pasir ris', '92251521', 'home appliances', 1, 'yes', 'east', now(), 'available', 'fan.jpg');
-- INSERT INTO carousel (`itemName`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
-- ('jeans', 'jeans in size 40', 'mei fang', 'pasir ris', '92251521', 'clothing', 1, 'yes', 'east', now(), 'available', 'jeans.jpg');


-- for wishlist table
INSERT INTO wishlist (`itemName`, `quantity`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('backpack', 1, 'my backpack broke, need a new one', 'others', now(), 'available');
INSERT INTO wishlist (`itemName`, `quantity`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('stool', 2, 'need a small chair to sit on', 'home furniture', now(), 'available');
INSERT INTO wishlist (`itemName`, `quantity`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('chair', 1, 'chair broke, need a new one', 'home furniture', now(), 'available');
INSERT INTO wishlist (`itemName`, `quantity`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('table', 1, 'a small table for dining and other purposes', 'home furniture', now(), 'available');
INSERT INTO wishlist (`itemName`, `quantity`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('shoes', 2, 'shoes for work', 'clothing', now(), 'available');
INSERT INTO wishlist (`itemName`, `quantity`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('wardrobe', 1, 'wardrobe to store my clothes', 'home furniture', now(), 'available');
INSERT INTO wishlist (`itemName`, `quantity`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('drawers', 1, 'drawers to store things', 'home furniture', now(), 'available');


-- for user table
-- INSERT INTO user(`username`, `password`, `userType`) VALUES 
-- (93261073, ENCRYPT('cheah1124'), 'admin');

-- for category table 
-- INSERT INTO category(`categoryName`) VALUES ('Food');
-- INSERT INTO category(`categoryName`) VALUES ('Home Appliances');
-- INSERT INTO category(`categoryName`) VALUES ('Clothes');
-- INSERT INTO category(`categoryName`) VALUES ('Furniture');
-- INSERT INTO category(`categoryName`) VALUES ('Toiletries');
-- INSERT INTO category(`categoryName`) VALUES ('Kitchenware');


-- fixed Item table
-- INSERT INTO fixedItem(`itemName`) VALUES ('Clothes');
-- INSERT INTO fixedItem(`itemName`) VALUES ('microwave');
-- INSERT INTO fixedItem(`itemName`) VALUES ('toothbrush');
-- INSERT INTO fixedItem(`itemName`) VALUES ('water bottle');
-- INSERT INTO fixedItem(`itemName`) VALUES ('handphone');


-- for faq
INSERT INTO faq (`question`, `answer`, `section`) VALUES ('How do I donate?', 'Just do it!', 'donor');
INSERT INTO faq (`question`, `answer`, `section`) VALUES ('What do I donate?', 'Check out our wishlist', 'donor');
INSERT INTO faq (`question`, `answer`, `section`) VALUES ('How do I request for an item?', 'Just do it!', 'worker');
INSERT INTO faq (`question`, `answer`, `section`) VALUES ('How do I drive?', 'Just do it!', 'driver');


-- for formbuilder table
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`) VALUES
('donate', 'Address', 'text');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `options`) VALUES
('donate', 'Area', 'radio', 'North;South;East;West;Central');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`) VALUES
('donate', 'Item Photo', 'file');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `placeholder`) VALUES
('donate', 'Item Description', 'text', 'Brief description of the item you are donating');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`) VALUES
('donate', 'Quantity', 'number');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `options`) VALUES
('donate', 'Delivery Method', 'dropdown', 'Delivery required;Arranged by donor');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `placeholder`) VALUES
('wishlist', 'Address', 'text', 'Enter Address');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`) VALUES
('wishlist', 'Quantity', 'number');


-- for formanswers table
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'donate', '1', 'yew wei');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'donate', '2', 'pasir ris grove');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'donate', '3', 'East');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'donate', '4', 'toothbrush.png');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'donate', '5', 'can make teeth sparkle sparkle');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'donate', '6', '3');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 92251521', 'donate', '7', 'Arranged by donor');
-- INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 93213234', 'wishlist', '8', 'pasir ris');
-- INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('2022-02-15 21:35:42 93213234', 'wishlist', '9', '1');

-- for newcarousel table
INSERT INTO newcarousel (`donorID`, `submissionID`, `itemName`, `itemCategory`, `timeSubmitted`, `itemStatus`) VALUES
(92251521, '2022-02-15 21:35:42 92251521', 'Toothbrush', 'Toiletries', '2022-02-15 21:35:42', 'available');

-- categoryitem table
INSERT INTO `categoryitem` (`itemname`, `attachedcategory`) VALUES
('Toothbrush', 'Toiletries'), ('Blender', 'Electronics'), ('Television', 'Electronics'), ('T-Shirt', 'Clothes')
;

select * from user;