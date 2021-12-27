-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Nov 03, 2021 at 06:55 AM
-- Server version: 8.0.18
-- PHP Version: 7.4.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `spmproject`
--
DROP Database IF EXISTS `fyptest`;
Create DATABASE `fyptest`;
USE `fyptest`;

-- --------------------------------------------------------

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `carousel`;
CREATE TABLE IF NOT EXISTS `carousel` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  `Description` varchar(300) NOT NULL,
  `DonorName` varchar(50) NOT NULL,
  `DonorAdd` varchar(300) NOT NULL,
  `ContactNo` varchar(20) NOT NULL,
  `Category` varchar(20) NOT NULL,
  `Quantity` INT(4) NOT NULL,
  `RequireDelivery` TINYINT(1) NOT NULL,
  `Region` varchar(20) NOT NULL,
  `TimeSubmitted` DATETIME NOT NULL,
  `ItemStatus` TINYINT(1) NOT NULL,
  PRIMARY KEY (`ID`)
) ;

INSERT INTO `carousel` (`name`, `description`, `donorname`, `donoradd`, `contactno`, `category`, `quantity`, `requiredelivery`, `region`, `timesubmitted`, `itemstatus`) VALUES
('toothbrush', 'basic toiletries', 'yew wei', 'pasir ris grove', '92251521', 'toiletries', 1, 1, 'east', 1);

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


