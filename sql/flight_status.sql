-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 30, 2020 at 06:12 AM
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
-- Database: `flight_status`
--
CREATE DATABASE IF NOT EXISTS `flight_status` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `flight_status`;

-- --------------------------------------------------------

--
-- Table structure for table `current_flight`
--

DROP TABLE IF EXISTS `current_flight`;
CREATE TABLE IF NOT EXISTS `current_flight` (
  `fid` varchar(5) NOT NULL,
  `depart` varchar(3) NOT NULL,
  `arrive` varchar(3) NOT NULL,
  `std` varchar(30) NOT NULL,
  `etd` varchar(30) NOT NULL,
  `sta` varchar(30) NOT NULL,
  `eta` varchar(30) NOT NULL,
  `status` varchar(100) NOT NULL,
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `current_flight`
--

INSERT INTO `current_flight` (`fid`, `depart`, `arrive`, `std`, `etd`, `sta`, `eta`, `status`) VALUES
('SQ22', 'SIN', 'EWR', '12:40AM', '7:00AM +1', '6:30AM', '12:39PM +1', 'DELAYED');

-- --------------------------------------------------------

--
-- Table structure for table `delay_plan`
--

DROP TABLE IF EXISTS `delay_plan`;
CREATE TABLE IF NOT EXISTS `delay_plan` (
  `planid` int(11) NOT NULL AUTO_INCREMENT,
  `flight_number` varchar(115) NOT NULL,
  `delay_status` varchar(100) NOT NULL,
  `issue_datetime` datetime NOT NULL,
  `message` varchar(2000) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`planid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `delay_plan`
--

INSERT INTO `delay_plan` (`planid`, `flight_number`, `delay_status`, `issue_datetime`, `message`, `is_active`) VALUES
(1, 'SQ22', 'DELAYED', '2020-03-16 00:00:00', 'Flight is provisionally delayed', 1);

-- --------------------------------------------------------

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
CREATE TABLE IF NOT EXISTS `message` (
  `mid` int(11) NOT NULL AUTO_INCREMENT,
  `message` varchar(2000) NOT NULL,
  `issue_datetime` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`mid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `message`
--

INSERT INTO `message` (`mid`, `message`, `issue_datetime`, `is_active`) VALUES
(1, 'Flight is currently delayed due to weather in origin station.', '2020-03-16 00:00:00', 1),
(2, 'Please approach service desk 1 for flight re-booking and service desk 2 for meal vouchers ', '2020-03-16 00:00:00', 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
