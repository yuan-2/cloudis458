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
  `subcat` varchar(30) NOT NULL,
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
  `requestorContactNo` int NOT NULL,
  `donorContactNo` int NOT NULL,
  `requestedItem` varchar(50) NOT NULL,
  `itemCategory` varchar(50) NOT NULL,
  `matchDate` datetime NOT NULL,
  PRIMARY KEY (`matchID`),
  FOREIGN KEY fk_1 (`reqID`) references request (`reqID`),
  FOREIGN KEY fk_2 (`requestorContactNo`) references user (`username`),
  FOREIGN KEY fk_3 (`donorContactNo`) references newcarousel (`donorID`),
  FOREIGN KEY fk_4 (`itemCategory`) references categoryitem (`attachedCategory`)
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
  `category` varchar(50) NOT NULL,
  `subcat` varchar(50) NOT NULL,
  PRIMARY KEY (`itemid`)
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
INSERT INTO `user` (`username`, `password`, `usertype`) VALUES ('12345678', 'test', 'migrantworker');
INSERT INTO `user` (`username`, `password`, `usertype`) VALUES ('87654321', 'test2', 'migrantworker');

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
('donate', 'Name', 'text', 'Your name or the Organization you are representing');
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
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('test', 'wishlist', '8', 'pasir ris');
INSERT INTO formanswers (`submissionID`,`formName`,`fieldID`,`answer`) VALUES ('test', 'wishlist', '9', '1');

-- for newcarousel table
INSERT INTO newcarousel (`donorID`, `submissionID`, `itemName`, `itemCategory`, `timeSubmitted`, `itemStatus`) VALUES
(92251521, '2022-02-15 21:35:42 92251521', 'Toothbrush', 'Toiletries', '2022-02-15 21:35:42', 'available');

-- for newwishlist table
INSERT INTO newwishlist (`submissionID`, `migrantID`, `itemName`, `itemCategory`, `timeSubmitted`, `itemStatus`) VALUES 
('test', 12345678, 'shirt', 'clothing', now(), 'available');

-- categoryitem table
INSERT INTO `categoryitem` (`itemname`, `category`, `subcat`) VALUES
('Mattress', 'Beddings', 'Beddings'),
('Pillow Cover', 'Beddings', 'Beddings'),
('Bedsheets', 'Beddings', 'Beddings'),
('Blanket', 'Beddings', 'Beddings'),
('Pillow', 'Beddings', 'Beddings'),
('Others', 'Beddings', 'Beddings'),
('Socks', 'Clothes', 'Accessories'),
('Belt', 'Clothes', 'Accessories'),
('Others', 'Clothes', 'Accessories'),
('Shorts', 'Clothes', 'Bottoms'),
('Pants', 'Clothes', 'Bottoms'),
('Lungi', 'Clothes', 'Bottoms'),
('Others', 'Clothes', 'Bottoms'),
('T-Shirt', 'Clothes', 'Tops'),
('Long Sleeve Shirt', 'Clothes', 'Tops'),
('Jersey', 'Clothes', 'Tops'),
('Others', 'Clothes', 'Tops'),
('Walking Shoes/Sport Shoes', 'Clothes', 'Shoes'),
('Safety Boots', 'Clothes', 'Shoes'),
('Slippers', 'Clothes', 'Shoes'),
('Others', 'Clothes', 'Shoes'),
('Headphones', 'Electronics', 'Audio'),
('Bluetooth Speaker', 'Electronics', 'Audio'),
('Others', 'Electronics', 'Audio'),
('Phone', 'Electronics', 'Devices'),
('Laptop', 'Electronics', 'Devices'),
('Camera', 'Electronics', 'Devices'),
('Tablet', 'Electronics', 'Devices'),
('Smartwatch', 'Electronics', 'Devices'),
('Others', 'Electronics', 'Devices'),
('TV', 'Electronics', 'TVs'),
('Others', 'Electronics', 'TVs'),
('Extension Cord', 'Electronics', 'Add-ons'),
('Charging Cord', 'Electronics', 'Add-ons'),
('Power Bank', 'Electronics', 'Add-ons'),
('Others', 'Electronics', 'Add-ons'),
('Coffee', 'Food', 'Drinks'),
('Tea', 'Food', 'Drinks'),
('Milo', 'Food', 'Drinks'),
('Milk', 'Food', 'Drinks'),
('Others', 'Food', 'Drinks'),
('Biscuits/Cookies', 'Food', 'Snacks'),
('Nuts', 'Food', 'Snacks'),
('Candy', 'Food', 'Snacks'),
('Chocolate', 'Food', 'Snacks'),
('Others', 'Food', 'Snacks'),
('Cakes', 'Food', 'Breads'),
('Bread', 'Food', 'Breads'),
('Others', 'Food', 'Breads'),
('Meat', 'Food', 'Cooking Ingredients'),
('Vegetables', 'Food', 'Cooking Ingredients'),
('Cooking Oil', 'Food', 'Cooking Ingredients'),
('Rice', 'Food', 'Cooking Ingredients'),
('Flour', 'Food', 'Cooking Ingredients'),
('Chicken', 'Food', 'Cooking Ingredients'),
('Fish', 'Food', 'Cooking Ingredients'),
('Dates', 'Food', 'Cooking Ingredients'),
('Others', 'Food', 'Cooking Ingredients'),
('Instant Noodles (Cup)', 'Food', 'Instant Food'),
('Instant Noodles (Packet)', 'Food', 'Instant Food'),
('Others', 'Food', 'Instant Food'),
('Fruit', 'Food', 'Fruits'),
('Others', 'Food', 'Fruits'),
('Cricket Equipment', 'Entertainment', 'Sports'),
('Food Equipment', 'Entertainment', 'Sports'),
('Football Equipment', 'Entertainment', 'Sports'),
('Gym Equipment', 'Entertainment', 'Sports'),
('Jersey', 'Entertainment', 'Sports'),
('Others', 'Entertainment', 'Sports'),
('Poker Cards', 'Entertainment', 'Card Games'),
('Others', 'Entertainment', 'Card Games'),
('Carrum', 'Entertainment', 'Board Games'),
('Others', 'Entertainment', 'Board Games'),
('Instruments', 'Entertainment', 'Music'),
('Others', 'Entertainment', 'Music'),
('Art Supplies (Paint/Brush)', 'Entertainment', 'Art'),
('Art pieces', 'Entertainment', 'Art'),
('Others', 'Entertainment', 'Art'),
('Panadol', 'Healthcare', 'Medication'),
('Others', 'Healthcare', 'Medication'),
('Hair Growth Medicine/Tea', 'Healthcare', 'Supplements'),
('Vitamins', 'Healthcare', 'Supplements'),
('Others', 'Healthcare', 'Supplements'),
('Blood Pressure Monitor', 'Healthcare', 'Health Monitors'),
('Finger Oximeter', 'Healthcare', 'Health Monitors'),
('Others', 'Healthcare', 'Health Monitors'),
('Muscle Cream', 'Healthcare', 'Ointments'),
('Others', 'Healthcare', 'Ointments'),
('Iron', 'Homecare', 'Small Appliances'),
('Table Fan', 'Homecare', 'Small Appliances'),
('Vacuum', 'Homecare', 'Small Appliances'),
('Reading Lamp', 'Homecare', 'Small Appliances'),
('Hair Dryer', 'Homecare', 'Small Appliances'),
('Others', 'Homecare', 'Small Appliances'),
('Washing Machine', 'Homecare', 'Large Appliances'),
('Aircon', 'Homecare', 'Large Appliances'),
('Ceiling Fan', 'Homecare', 'Large Appliances'),
('Others', 'Homecare', 'Large Appliances'),
('General Toolbox', 'Homecare', 'Tools and Maintenance'),
('Others', 'Homecare', 'Tools and Maintenance'),
('Water Heater/Kettle', 'Kitchen', 'Small Appliances'),
('Curry Cooker', 'Kitchen', 'Small Appliances'),
('Juicer', 'Kitchen', 'Small Appliances'),
('Small Blender', 'Kitchen', 'Small Appliances'),
('Large Blender', 'Kitchen', 'Small Appliances'),
('Rice Cooker', 'Kitchen', 'Small Appliances'),
('Electric Cooker', 'Kitchen', 'Small Appliances'),
('Air Fryer', 'Kitchen', 'Small Appliances'),
('Microwave', 'Kitchen', 'Small Appliances'),
('Electric Oven', 'Kitchen', 'Small Appliances'),
('Bread Toaster', 'Kitchen', 'Small Appliances'),
('Pressure Cooker', 'Kitchen', 'Small Appliances'),
('Pestle and Mortar', 'Kitchen', 'Small Appliances'),
('Induction Stove', 'Kitchen', 'Small Appliances'),
('Others', 'Kitchen', 'Small Appliances'),
('Refrigerator', 'Kitchen', 'Large Appliances'),
('Gas Stove', 'Kitchen', 'Large Appliances'),
('BBQ Pit', 'Kitchen', 'Large Appliances'),
('Others', 'Kitchen', 'Large Appliances'),
('Frying Pan', 'Kitchen', 'Cooking Needs and Crockery'),
('Pot', 'Kitchen', 'Cooking Needs and Crockery'),
('Plates', 'Kitchen', 'Cooking Needs and Crockery'),
('Utensils', 'Kitchen', 'Cooking Needs and Crockery'),
('Bowls', 'Kitchen', 'Cooking Needs and Crockery'),
('Spatula/Ladle', 'Kitchen', 'Cooking Needs and Crockery'),
('Others', 'Kitchen', 'Cooking Needs and Crockery'),
('Detergent', 'Laundry', 'Laundry'),
('Others', 'Laundry', 'Laundry'),
('Luggage', 'Personal Use', 'Bags'),
('Bag', 'Personal Use', 'Bags'),
('Deodorant', 'Personal Use', 'Fragrance'),
('Perfume', 'Personal Use', 'Fragrance'),
('Others', 'Personal Use', 'Fragrance'),
('Raincoat', 'Personal Use', 'Travel Use'),
('Umbrella', 'Personal Use', 'Travel Use'),
('Bicycle', 'Personal Use', 'Travel Use'),
('Others', 'Personal Use', 'Travel Use'),
('Water Bottle', 'Personal Use', 'Bottles'),
('Thermos Flask', 'Personal Use', 'Bottles'),
('Others', 'Personal Use', 'Bottles'),
('Janamaz', 'Personal Use', 'Prayer Mat'),
('Others', 'Personal Use', 'Prayer Mat'),
('Sunglasses', 'Personal Use', 'Small Items'),
('Hair Clipper', 'Personal Use', 'Small Items'),
('Napkins', 'Personal Use', 'Small Items'),
('Watch', 'Personal Use', 'Small Items'),
('Face Masks', 'Personal Use', 'Small Items'),
('Torchlight', 'Personal Use', 'Small Items'),
('Wallet', 'Personal Use', 'Small Items'),
('Others', 'Personal Use', 'Small Items'),
('Toothpaste', 'Toiletries', 'Dental Care'),
('Toothbrush', 'Toiletries', 'Dental Care'),
('Others', 'Toiletries', 'Dental Care'),
('Hair Trimmer/Shaver', 'Toiletries', 'Grooming Products'),
('Others', 'Toiletries', 'Grooming Products'),
('Body Lotion', 'Toiletries', 'Body Care'),
('Soap', 'Toiletries', 'Body Care'),
('Sunblock', 'Toiletries', 'Body Care'),
('Body Spray', 'Toiletries', 'Body Care'),
('Others', 'Toiletries', 'Body Care'),
('Face Cream', 'Toiletries', 'Facial Care'),
('Others', 'Toiletries', 'Facial Care'),
('Shampoo', 'Toiletries', 'Hair Care'),
('Hair Gel', 'Toiletries', 'Body Care'),
('Conditioner', 'Toiletries', 'Hair Care'),
('Others', 'Toiletries', 'Hair Care'),
('Towel', 'Toiletries', 'Towel'),
('Others', 'Toiletries', 'Towel'),
('Bedside Table', 'Furniture', 'Tables'),
('Dining Table', 'Furniture', 'Tables'),
('Study Table', 'Furniture', 'Tables'),
('Others', 'Furniture', 'Tables'),
('Dining Chair', 'Furniture', 'Chair'),
('Study Chair', 'Furniture', 'Chair'),
('Outdoor Chair', 'Furniture', 'Chair'),
('Others', 'Furniture', 'Chair'),
('Bedside Lamp', 'Furniture', 'Lighting'),
('Lightbulbs', 'Furniture', 'Lighting'),
('Standing Lamp', 'Furniture', 'Lighting'),
('Ceiling Lamp', 'Furniture', 'Lighting'),
('Others', 'Furniture', 'Lighting'),
('Drawer', 'Furniture', 'Bedroom Essentials'),
('Cupboard', 'Furniture', 'Bedroom Essentials'),
('Clothes Hanger', 'Furniture', 'Bedroom Essentials'),
('Bedframe', 'Furniture', 'Bedroom Essentials'),
('Others', 'Furniture', 'Bedroom Essentials'),
('Sim Card', 'Others', 'Others'),
('Care Pack', 'Others', 'Others');

select * from categoryitem;
