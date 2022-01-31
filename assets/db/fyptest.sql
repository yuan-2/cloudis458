DROP Database IF EXISTS `fyptest`;
Create DATABASE `fyptest`;
USE `fyptest`;

DROP TABLE IF EXISTS `carousel`;
CREATE TABLE IF NOT EXISTS `carousel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(300) NOT NULL,
  `donorName` varchar(50) NOT NULL,
  `donorAddr` varchar(300) NOT NULL,
  `contactNo` varchar(20) NOT NULL,
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
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `itemName` varchar(50) NOT NULL,
  `remarks` varchar(300) NOT NULL,
  `category` varchar(50) NOT NULL,
  `timeSubmitted` datetime NOT NULL,
  `itemStatus` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ;

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `username` varchar(300) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ;

DROP TABLE IF EXISTS `driver`;
CREATE TABLE IF NOT EXISTS `driver` (
  `driverid` int(11) NOT NULL AUTO_INCREMENT,
  `contactNo` varchar(50) NOT NULL,
  PRIMARY KEY (`driverid`),
  FOREIGN KEY (`driverid`) references user (`id`)
) ;

DROP TABLE IF EXISTS `migrantworker`;
CREATE TABLE IF NOT EXISTS `migrantworker` (
  `migrantid` int(11) NOT NULL AUTO_INCREMENT,
  `contactNo` varchar(50) NOT NULL,
  `address` varchar(300) NOT NULL,
  `reqHistory` varchar(50) NOT NULL,
  PRIMARY KEY (`migrantid`),
  FOREIGN KEY (`migrantid`) references user (`id`)
) ;

DROP TABLE IF EXISTS `request`;
CREATE TABLE IF NOT EXISTS `request` (
  `reqid` int(11) NOT NULL AUTO_INCREMENT,
  `requestor` varchar(50) NOT NULL,
  `deliveryLocation` varchar(300) NOT NULL,
  `itemCategory` varchar(300) NOT NULL,
  `requestQty` varchar(50) NOT NULL,
  `timeSubmitted` datetime NOT NULL,
  PRIMARY KEY (`reqid`)
) ;

DROP TABLE IF EXISTS `delivery`;
CREATE TABLE IF NOT EXISTS `delivery` (
  `dreqid` int(11) NOT NULL AUTO_INCREMENT,
  `accepted` varchar(50) NOT NULL,
  `reqid` int(11) NOT NULL,
  PRIMARY KEY (`dreqid`),
  FOREIGN KEY (`reqid`) references request (`reqid`)
) ;

-- DROP TABLE IF EXISTS `category`;
-- CREATE TABLE IF NOT EXISTS `category` (
--   `categoryid` int(11) NOT NULL AUTO_INCREMENT,
--   `categoryName` varchar(50) NOT NULL,
--   PRIMARY KEY (`categoryid`)
-- ) ;

DROP TABLE IF EXISTS `matches`;
CREATE TABLE IF NOT EXISTS `matches` (
  `matchid` int(11) NOT NULL AUTO_INCREMENT,
  `reqid` int(11) NOT NULL,
  `requestorName` varchar(50) NOT NULL,
  `requestorContactNo` varchar(50) NOT NULL,
  `donorName` varchar(50) NOT NULL,
  `donorContactNo` varchar(50) NOT NULL,
  `requestedItem` varchar(50) NOT NULL,
  `itemCategory` varchar(50) NOT NULL,
  `dateSubmitted` varchar(50) NOT NULL,
  PRIMARY KEY (`matchid`)
) ;


-- DROP TABLE IF EXISTS `fixedItem`;
-- CREATE TABLE IF NOT EXISTS `fixedItem` (
--   `itemID` int(11) NOT NULL AUTO_INCREMENT,
--   `itemName` varchar(50) NOT NULL,
--   PRIMARY KEY (`itemID`)
-- ) ;
-- 

DROP TABLE IF EXISTS `categoryitem`;
CREATE TABLE IF NOT EXISTS `categoryitem` (
  `itemid` int(11) NOT NULL AUTO_INCREMENT,
  `itemname` varchar(50) NOT NULL,
  `attachedcategory` varchar(50) NOT NULL,
  PRIMARY KEY (`itemid`, `attachedCategory`)
) ;

DROP TABLE IF EXISTS `faq`;
CREATE TABLE IF NOT EXISTS `faq` (
  `faqID` int(11) NOT NULL AUTO_INCREMENT,
  `question` varchar(300) NOT NULL,
  `answer` varchar(300) NOT NULL,
  `section` varchar(10) NOT NULL,
  PRIMARY KEY (`faqID`)
) ;

DROP TABLE IF EXISTS `formbuilder`;
CREATE TABLE IF NOT EXISTS `formbuilder` (
  `fieldID` int(11) NOT NULL AUTO_INCREMENT,
  `formName` varchar(15) NOT NULL,
  `fieldName` varchar(50) NOT NULL,
  `fieldType` varchar(15) NOT NULL,
  `placeholder` varchar(50),
  `options` varchar(200),
  PRIMARY KEY (`fieldID`)
) ;


-- INSERT values

-- for carousel table
INSERT INTO carousel (`name`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
('toothbrush', 'basic toiletries', 'yew wei', 'pasir ris grove', '92251521', 'toiletries', 1, 'yes', 'east', now(), 'available', 'toothbrush.png');
INSERT INTO carousel (`name`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
('hair dryer', 'for hair', 'yuanyuan', '510121', '12345678', 'home appliances', 1, 'yes', 'west', now(), 'available', 'hairdryer.jpg');
INSERT INTO carousel (`name`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
('t-shirts', 'free size t-shirts', 'amanda', '510425', '87654321', 'clothing', 1, 'yes', 'north', now(), 'available', 't-shirt.jpg');
INSERT INTO carousel (`name`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
('rice cooker', 'to cook rice', 'nicole', '510180', '92251521', 'home appliances', 1, 'yes', 'south', now(), 'available', 'ricecooker.jpg');
INSERT INTO carousel (`name`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
('fan', 'for sg hot weather', 'vanessa', 'pasir ris', '92251521', 'home appliances', 1, 'yes', 'east', now(), 'available', 'fan.jpg');
INSERT INTO carousel (`name`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`, `fileName`) VALUES
('jeans', 'jeans in size 40', 'mei fang', 'pasir ris', '92251521', 'clothing', 1, 'yes', 'east', now(), 'available', 'jeans.jpg');


-- for wishlist table
INSERT INTO wishlist (`itemName`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('backpack', 'my backpack broke, need a new one', 'others', now(), 'available');
INSERT INTO wishlist (`itemName`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('stool', 'need a small chair to sit on', 'home furniture', now(), 'available');
INSERT INTO wishlist (`itemName`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('chair', 'chair broke, need a new one', 'home furniture', now(), 'available');
INSERT INTO wishlist (`itemName`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('table', 'a small table for dining and other purposes', 'home furniture', now(), 'available');
INSERT INTO wishlist (`itemName`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('shoes', 'shoes for work', 'clothing', now(), 'available');
INSERT INTO wishlist (`itemName`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('wardrobe', 'wardrobe to store my clothes', 'home furniture', now(), 'available');
INSERT INTO wishlist (`itemName`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('drawers', 'drawers to store things', 'home furniture', now(), 'available');


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
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `placeholder`) VALUES
('donate', 'Name', 'text', 'Enter Name');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `placeholder`) VALUES
('donate', 'Contact Number', 'text', 'Enter Contact Number');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `placeholder`) VALUES
('donate', 'Address', 'text', 'Enter Address');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `options`) VALUES
('donate', 'Area', 'radio', 'North;South;East;West;Central');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`) VALUES
('donate', 'Item Category', 'dropdown');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`) VALUES
('donate', 'Item Name', 'dropdown');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`) VALUES
('donate', 'Upload Photo', 'file');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `options`) VALUES
('donate', 'Quantity', 'dropdown', '1;2;3;4');
INSERT INTO formbuilder (`formName`, `fieldName`, `fieldType`, `options`) VALUES
('donate', 'Require delivery from home?', 'dropdown', 'Yes;No');


-- categoryitem table
INSERT INTO `categoryitem` (`itemname`, `attachedcategory`) VALUES
('Toothbrush', 'Toiletries'), ('Blender', 'Electronics'), ('Television', 'Electronics'), ('T-Shirt', 'Clothes')
;

select * from categoryitem;