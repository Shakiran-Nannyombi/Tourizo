-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jul 29, 2025 at 09:21 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `travel_app`
--

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `account_locked` tinyint(1) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `bio` text DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `email_notifications` tinyint(1) DEFAULT NULL,
  `newsletter` tinyint(1) DEFAULT NULL,
  `sms_notifications` tinyint(1) DEFAULT NULL,
  `language` varchar(10) DEFAULT NULL,
  `timezone` varchar(20) DEFAULT NULL,
  `two_factor_auth` tinyint(1) DEFAULT NULL,
  `public_profile` tinyint(1) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password_hash`, `is_admin`, `last_login`, `account_locked`, `first_name`, `last_name`, `phone`, `date_of_birth`, `bio`, `is_active`, `email_notifications`, `newsletter`, `sms_notifications`, `language`, `timezone`, `two_factor_auth`, `public_profile`, `date_created`) VALUES
(11, 'NONO', 'noelaankunda@gmail.com', 'scrypt:32768:8:1$dhRp5WnCchG5n2F6$241a277d394a9953febf8fed2b6d41fa87bc84a0dc36bb3c002e08f5f4db0c0bfaef6489c39da54d5920c37aed3cc758e11baedb7e070164a23b1dce620a6ce9', 0, '2025-07-23 21:30:45', 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(12, 'SSEKIZIYIVU GRACE', 'ssekiziyivugrace55@gmail.com', 'scrypt:32768:8:1$2a0Som5MAtsSt77d$b79ba25564501c7febc260fb516b40f92c7e3409a677671a1545382ec910d53b0874d8ff42ed458ae961ce98296e1edf687b9b1f18418cd2ef981a21cb923726', 1, '2025-07-24 16:01:45', 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(13, 'praise butsilo', 'butsilo@gmail.com', 'scrypt:32768:8:1$QueekLgaAx8O3yhC$768d486f137573bf50887918be4035405f83e3941c0fe486d4107b719aaaf836ed7678678b992b2affeaf287613e9b7429b8f4138f4c470f1e1537aee86724fd', 0, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(14, 'Shakiran Nannyombi', 'shakirannannyombi@gmail.com', 'scrypt:32768:8:1$nQSacbUpb6J3h1iO$a0903b9a57995ea52670ceac755dd8f1541629c2b69c55b0b61105d5c91efefc0db548f28a38e9591db3767a0c869319fc6f65c15ea27a7131d185de54c7af41', 0, '2025-07-28 20:57:54', 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(15, 'Shakiran', 'devkiran256@gmail.com', 'scrypt:32768:8:1$oTURYidcmyGBfpPe$3194675f44be7f43bc555349536f7a80796cde7e874fa27c2042d0c5d84c921a1842b197a1354f65686827a1ba84f5fde807858acd66160109d82cfdc36720d8', 1, '2025-07-28 21:04:27', 0, 'Shakiran', 'Nannyombi', NULL, NULL, NULL, NULL, 1, 0, 0, 'en', 'UTC', 0, 1, '2025-07-28 14:45:04');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
