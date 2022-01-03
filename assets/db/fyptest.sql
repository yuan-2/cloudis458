DROP Database IF EXISTS `fyptest`;
Create DATABASE `fyptest`;
USE `fyptest`;

DROP TABLE IF EXISTS `carousel`;
CREATE TABLE IF NOT EXISTS `carousel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(300) NOT NULL,
  `donorname` varchar(50) NOT NULL,
  `donoradd` varchar(300) NOT NULL,
  `contactno` varchar(20) NOT NULL,
  `category` varchar(20) NOT NULL,
  `quantity` INT(4) NOT NULL,
  `requiredelivery` TINYINT(1) NOT NULL,
  `region` varchar(20) NOT NULL,
  `timesubmitted` DATETIME NOT NULL,
  `itemstatus` TINYINT(1) NOT NULL,
  PRIMARY KEY (`id`)
) ;

DROP TABLE IF EXISTS `wishlist`;
CREATE TABLE IF NOT EXISTS `wishlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `itemname` varchar(50) NOT NULL,
  `remarks` varchar(300) NOT NULL,
  `category` varchar(50) NOT NULL,
  `timesubmitted` datetime NOT NULL,
  `itemstatus` tinyint(1) NOT NULL,
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
  `contactno` varchar(50) NOT NULL,
  PRIMARY KEY (`driverid`),
  FOREIGN KEY (`driverid`) references user (`id`)
) ;

DROP TABLE IF EXISTS `migrantworker`;
CREATE TABLE IF NOT EXISTS `migrantworker` (
  `migrantid` int(11) NOT NULL AUTO_INCREMENT,
  `contactno` varchar(50) NOT NULL,
  `address` varchar(300) NOT NULL,
  `reqhistory` varchar(50) NOT NULL,
  PRIMARY KEY (`migrantid`),
  FOREIGN KEY (`migrantid`) references user (`id`)
) ;

DROP TABLE IF EXISTS `request`;
CREATE TABLE IF NOT EXISTS `request` (
  `reqid` int(11) NOT NULL AUTO_INCREMENT,
  `requestor` varchar(50) NOT NULL,
  `deliverylocation` varchar(300) NOT NULL,
  `itemcategory` varchar(300) NOT NULL,
  `requestqty` varchar(50) NOT NULL,
  `timesubmitted` datetime NOT NULL,
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


-- INSERT values

-- for carousel table
INSERT INTO carousel (`name`, `description`, `donorname`, `donoradd`, `contactno`, `category`, `quantity`, `requiredelivery`, `region`, `timesubmitted`, `itemstatus`) VALUES
('toothbrush', 'basic toiletries', 'yew wei', 'pasir ris grove', '92251521', 'toiletries', 1, 1, 'east', now(), 1);
INSERT INTO carousel (`name`, `description`, `donorname`, `donoradd`, `contactno`, `category`, `quantity`, `requiredelivery`, `region`, `timesubmitted`, `itemstatus`) VALUES
('hair dryer', 'for hair', 'yuanyuan', '510121', '12345678', 'home appliances', 1, 1, 'west', now(), 1);
INSERT INTO carousel (`name`, `description`, `donorname`, `donoradd`, `contactno`, `category`, `quantity`, `requiredelivery`, `region`, `timesubmitted`, `itemstatus`) VALUES
('t-shirts', 'free size t-shirts', 'amanda', '510425', '87654321', 'clothing', 1, 1, 'north', now(), 1);
INSERT INTO carousel (`name`, `description`, `donorname`, `donoradd`, `contactno`, `category`, `quantity`, `requiredelivery`, `region`, `timesubmitted`, `itemstatus`) VALUES
('rice cooker', 'to cook rice', 'nicole', '510180', '92251521', 'home appliances', 1, 1, 'south', now(), 1);
INSERT INTO carousel (`name`, `description`, `donorname`, `donoradd`, `contactno`, `category`, `quantity`, `requiredelivery`, `region`, `timesubmitted`, `itemstatus`) VALUES
('fan', 'for sg hot weather', 'vanessa', 'pasir ris', '92251521', 'home appliances', 1, 1, 'east', now(), 1);
INSERT INTO carousel (`name`, `description`, `donorname`, `donoradd`, `contactno`, `category`, `quantity`, `requiredelivery`, `region`, `timesubmitted`, `itemstatus`) VALUES
('jeans', 'jeans in size 40', 'mei fang', 'pasir ris', '92251521', 'clothing', 1, 1, 'east', now(), 1);

SELECT * FROM carousel;

-- for wishlist table
INSERT INTO wishlist (`itemname`, `remarks`, `category`, `timesubmitted`, `itemstatus`) VALUES
('backpack', 'my backpack broke, need a new one', 'others', now(), 1);
INSERT INTO wishlist (`itemname`, `remarks`, `category`, `timesubmitted`, `itemstatus`) VALUES
('stool', 'need a small chair to sit on', 'home furniture', now(), 1);
INSERT INTO wishlist (`itemname`, `remarks`, `category`, `timesubmitted`, `itemstatus`) VALUES
('chair', 'chair broke, need a new one', 'home furniture', now(), 1);
INSERT INTO wishlist (`itemname`, `remarks`, `category`, `timesubmitted`, `itemstatus`) VALUES
('table', 'a small table for dining and other purposes', 'home furniture', now(), 1);
INSERT INTO wishlist (`itemname`, `remarks`, `category`, `timesubmitted`, `itemstatus`) VALUES
('shoes', 'shoes for work', 'clothing', now(), 1);
INSERT INTO wishlist (`itemname`, `remarks`, `category`, `timesubmitted`, `itemstatus`) VALUES
('wardrobe', 'wardrobe to store my clothes', 'home furniture', now(), 1);
INSERT INTO wishlist (`itemname`, `remarks`, `category`, `timesubmitted`, `itemstatus`) VALUES
('drawers', 'drawers to store things', 'home furniture', now(), 1);

SELECT * FROM wishlist


