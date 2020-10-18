-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 16, 2020 at 07:10 AM
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
-- Database: `passenger`
--
CREATE DATABASE IF NOT EXISTS `passenger` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `passenger`;
-- --------------------------------------------------------

--
-- Table structure for table `passenger`
--

DROP TABLE IF EXISTS `passenger`;
CREATE TABLE IF NOT EXISTS `passenger` (
  `pid` int(11) NOT NULL,
  `pnr` int(11) NOT NULL,
  `passport_number` varchar(100) NOT NULL,
  `family_name` varchar(100) NOT NULL,
  `given_name` varchar(100) NOT NULL,
  `title` varchar(20) NOT NULL,
  `contact_number` varchar(50) NOT NULL,
  `eticket_number` varchar(100) NOT NULL,
  `email` varchar(200) NOT NULL,
  `seat_number` varchar(10) NOT NULL,
  `fare_class` varchar(30) NOT NULL,
  `remarks` varchar(1000) NOT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='pnr -> Passenger Numeric Record';

--
-- Dumping data for table `passenger`
--

INSERT INTO `passenger` (`pid`, `pnr`, `passport_number`, `family_name`, `given_name`, `title`, `contact_number`, `eticket_number`, `email`, `seat_number`, `fare_class`, `remarks`) VALUES
(1001, 2001, 'E159159159', 'Tan', 'John', 'Mr', '91591590', 'S159Q15', 'john@gmail.com', '24D', 'Economy', 'Vegetarian'),
(1002, 2002, 'E123456789', 'Lim', 'Nancy', 'Miss', '91234567', 'S12Q15C', 'nancy@gmail.com', '2B', 'First', 'Allergic to Chicken'),
(1003, 2002, 'E888777666', 'Lim', 'David', 'Mr', '81001000', 'S874Q1', 'david@gmail.com', '2A', 'First', '-'),
(1004, 2004, 'E100015000', 'Loh', 'Kenny', 'Dr', '98009123', 'S89Q1X', 'kenny@gmail.com', '8B', 'Business', '-');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
