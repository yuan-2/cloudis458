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
  `requireDelivery` TINYINT(1) NOT NULL,
  `region` varchar(20) NOT NULL,
  `timeSubmitted` DATETIME NOT NULL,
  `itemStatus` TINYINT(1) NOT NULL,
  PRIMARY KEY (`id`)
) ;

DROP TABLE IF EXISTS `wishlist`;
CREATE TABLE IF NOT EXISTS `wishlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `itemName` varchar(50) NOT NULL,
  `remarks` varchar(300) NOT NULL,
  `category` varchar(50) NOT NULL,
  `timeSubmitted` datetime NOT NULL,
  `itemStatus` tinyint(1) NOT NULL,
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
  `accepted` tinyint(1) NOT NULL,
  `reqid` int(11) NOT NULL,
  PRIMARY KEY (`dreqid`),
  FOREIGN KEY (`reqid`) references request (`reqid`)
) ;

DROP TABLE IF EXISTS `category`;
CREATE TABLE IF NOT EXISTS `category` (
  `categoryid` int(11) NOT NULL AUTO_INCREMENT,
  `categoryName` varchar(50) NOT NULL,
  PRIMARY KEY (`categoryid`)
) ;

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


-- INSERT values

-- for carousel table
INSERT INTO carousel (`name`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`) VALUES
('toothbrush', 'basic toiletries', 'yew wei', 'pasir ris grove', '92251521', 'toiletries', 1, 1, 'east', now(), 1);
INSERT INTO carousel (`name`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`) VALUES
('hair dryer', 'for hair', 'yuanyuan', '510121', '12345678', 'home appliances', 1, 1, 'west', now(), 1);
INSERT INTO carousel (`name`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`) VALUES
('t-shirts', 'free size t-shirts', 'amanda', '510425', '87654321', 'clothing', 1, 1, 'north', now(), 1);
INSERT INTO carousel (`name`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`) VALUES
('rice cooker', 'to cook rice', 'nicole', '510180', '92251521', 'home appliances', 1, 1, 'south', now(), 1);
INSERT INTO carousel (`name`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`) VALUES
('fan', 'for sg hot weather', 'vanessa', 'pasir ris', '92251521', 'home appliances', 1, 1, 'east', now(), 1);
INSERT INTO carousel (`name`, `description`, `donorName`, `donorAddr`, `contactNo`, `category`, `quantity`, `requireDelivery`, `region`, `timeSubmitted`, `itemStatus`) VALUES
('jeans', 'jeans in size 40', 'mei fang', 'pasir ris', '92251521', 'clothing', 1, 1, 'east', now(), 1);


-- for wishlist table
INSERT INTO wishlist (`itemName`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('backpack', 'my backpack broke, need a new one', 'others', now(), 1);
INSERT INTO wishlist (`itemName`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('stool', 'need a small chair to sit on', 'home furniture', now(), 1);
INSERT INTO wishlist (`itemName`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('chair', 'chair broke, need a new one', 'home furniture', now(), 1);
INSERT INTO wishlist (`itemName`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('table', 'a small table for dining and other purposes', 'home furniture', now(), 1);
INSERT INTO wishlist (`itemName`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('shoes', 'shoes for work', 'clothing', now(), 1);
INSERT INTO wishlist (`itemName`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('wardrobe', 'wardrobe to store my clothes', 'home furniture', now(), 1);
INSERT INTO wishlist (`itemName`, `remarks`, `category`, `timeSubmitted`, `itemStatus`) VALUES
('drawers', 'drawers to store things', 'home furniture', now(), 1);


-- for category table 
INSERT INTO category(`categoryName`) VALUES ('Food');
INSERT INTO category(`categoryName`) VALUES ('Home Appliances');
INSERT INTO category(`categoryName`) VALUES ('Clothes');
INSERT INTO category(`categoryName`) VALUES ('Furniture');
INSERT INTO category(`categoryName`) VALUES ('Toiletries');
INSERT INTO category(`categoryName`) VALUES ('Kitchenware');
