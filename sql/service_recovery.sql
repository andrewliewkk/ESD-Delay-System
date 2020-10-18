-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 09, 2020 at 06:52 AM
-- Server version: 5.7.23
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `service_recovery`
--
CREATE DATABASE IF NOT EXISTS `service_recovery` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `service_recovery`;

-- --------------------------------------------------------

--
-- Table structure for table `eligibility`
--

DROP TABLE IF EXISTS `eligibility`;
CREATE TABLE IF NOT EXISTS `eligibility` (
  `fare_class` varchar(30) NOT NULL,
  `hotel_voucher` tinyint(1) NOT NULL,
  `meal_voucher` int(11) NOT NULL,
  `lounge_voucher` tinyint(1) NOT NULL,
  `transport_voucher` tinyint(1) NOT NULL,
  `update_datetime` datetime NOT NULL,
  PRIMARY KEY (`fare_class`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `hotel_list`
--

DROP TABLE IF EXISTS `hotel_list`;
CREATE TABLE IF NOT EXISTS `hotel_list` (
  `hid` int(11) NOT NULL,
  `hotel_name` varchar(500) NOT NULL,
  `hotel_address` varchar(1000) NOT NULL,
  `economy_room_qty` int(11) NOT NULL,
  `business_room_qty` int(11) NOT NULL,
  `first_room_qty` int(11) NOT NULL,
  `total_economy_room` int(11) NOT NULL,
  `total_business_room` int(11) NOT NULL,
  `total_first_room` int(11) NOT NULL,
  `remarks` varchar(2000) NOT NULL,
  PRIMARY KEY (`hid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `hotel_list`
--

INSERT INTO `hotel_list` (`hid`, `hotel_name`, `hotel_address`, `economy_room_qty`, `business_room_qty`, `first_room_qty`, `total_economy_room`, `total_business_room`, `total_first_room`, `remarks`) VALUES
(1, 'MBS', 'Marina Boulevard 123', 10, 8, 3, 11, 8, 3, 'Booked till 24/3'),
(2, 'Orchard', 'Orchard road', 0, 2, 3, 15, 8, 3, 'Booked till 24/5'),
(3, 'SMU', 'Penang road', 5, 0, 0, 10, 1, 1, 'Booked till 24/5');

-- --------------------------------------------------------

--
-- Table structure for table `voucher`
--

DROP TABLE IF EXISTS `voucher`;
CREATE TABLE IF NOT EXISTS `voucher` (
  `vid` varchar(100) NOT NULL,
  `pid` int(11) NOT NULL,
  `voucher_type` varchar(500) NOT NULL,
  `issue_date` date NOT NULL,
  `entitlement` varchar(1000) NOT NULL,
  `remarks` varchar(1000) NOT NULL,
  `is_redeemed` tinyint(1) NOT NULL DEFAULT '0',
  `hid` int(11) DEFAULT NULL,
  PRIMARY KEY (`vid`),
  KEY `voucher_fk` (`hid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `voucher`
--

INSERT INTO `voucher` (`vid`, `pid`, `voucher_type`, `issue_date`, `entitlement`, `remarks`, `is_redeemed`, `hid`) VALUES
('H5', 1002, 'Hotel', '2020-08-03', 'Free stay at MBS', '-', 0, 1),
('l0000005', 1002, 'Lounge', '2020-02-19', 'Lounge voucher free food', '-', 0, NULL),
('l0000009', 1002, 'Meal', '2020-03-09', 'Andrew free two night', '-', 0, NULL),
('L003', 1001, 'Lounge', '2020-03-08', 'Free 3', '-', 0, NULL),
('L121212', 1001, 'Lounge', '2020-03-02', 'Lounge voucher free food and drinkssss', 'CHANGE IS MADE', 0, NULL),
('M001', 1001, 'Meal', '2020-03-08', 'Free 1', '-', 0, NULL),
('M002', 1001, 'Meal', '2020-03-08', 'Free 2', '-', 1, NULL),
('m10012458', 1001, 'Meal', '2020-03-02', '$10 off Flight meals', '-', 0, NULL),
('M10101023', 1001, 'Meal', '2020-03-08', 'Free macs ice cream', '-', 0, NULL),
('M1223', 1001, 'Meal', '2020-03-03', 'Free Free Free stuff at Suntec', '-', 0, NULL),
('M123', 1001, 'Meal', '2020-03-03', 'Free Free Free stuff at MBS', '-', 1, NULL),
('M888', 1001, 'Meal', '2020-03-02', 'freeeeeee fooood', '-', 0, NULL);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `voucher`
--
ALTER TABLE `voucher`
  ADD CONSTRAINT `voucher_fk` FOREIGN KEY (`hid`) REFERENCES `hotel_list` (`hid`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
