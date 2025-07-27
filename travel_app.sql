-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 25, 2025 at 03:46 PM
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
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('add_inquiry_table');

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `id` int(11) NOT NULL,
  `reference` varchar(36) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `tour_id` int(11) NOT NULL,
  `full_name` varchar(200) NOT NULL,
  `email` varchar(120) NOT NULL,
  `phone` varchar(30) NOT NULL,
  `booking_date` date NOT NULL,
  `booking_time` time DEFAULT NULL,
  `num_people` int(11) NOT NULL,
  `special_requests` text DEFAULT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `payment_method` varchar(20) DEFAULT NULL,
  `payment_status` varchar(20) NOT NULL,
  `payment_reference` varchar(100) DEFAULT NULL,
  `payment_details` varchar(255) DEFAULT NULL,
  `order_tracking_id` varchar(100) DEFAULT NULL,
  `cancellation_reason` varchar(50) DEFAULT NULL,
  `cancellation_notes` text DEFAULT NULL,
  `cancelled_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking`
--

INSERT INTO `booking` (`id`, `reference`, `user_id`, `tour_id`, `full_name`, `email`, `phone`, `booking_date`, `booking_time`, `num_people`, `special_requests`, `total_amount`, `payment_method`, `payment_status`, `payment_reference`, `payment_details`, `order_tracking_id`, `cancellation_reason`, `cancellation_notes`, `cancelled_at`, `created_at`, `updated_at`) VALUES
(2, 'TB2593AA15', 11, 5, 'Ankunda Noela', 'noelaankunda@gmail.com', '+256758413210', '2025-07-24', '14:41:00', 1, 'one extra bed', 350.00, 'momo', 'paid', NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-22 21:41:53', '2025-07-22 21:41:53'),
(3, 'TBEC1D3DD8', 11, 6, 'SSEKIZIYIVU GRACE', 'deogracoousssekilordgracejohns@gmail.com', '+256757587161', '2025-07-25', '02:47:00', 2, 'more of game drive', 3900.00, 'momo', 'paid', NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-22 21:45:43', '2025-07-22 21:45:43'),
(4, 'TB9724FF48', 11, 4, 'nono wss', 'noelaankunda@gmail.com', '+256758413210', '2025-07-24', '19:07:00', 1, NULL, 250.00, 'momo', 'cancelled', NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-23 03:08:17', '2025-07-23 03:29:19'),
(5, 'TBD38ADF4D', NULL, 3, 'Deogracious', 'deogracoousssekilordgracejohns@gmail.com', '+256757587161', '2025-07-25', '21:39:00', 4, 'am all good', 4500.00, 'momo', 'paid', NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-23 16:39:03', '2025-07-23 16:39:03'),
(6, 'TB08AB66E2', NULL, 3, 'Deogracious', 'deogracoousssekilordgracejohns@gmail.com', '+256757587161', '2025-07-25', '21:39:00', 4, 'am all good', 4500.00, 'momo', 'paid', NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-23 16:49:04', '2025-07-23 16:49:04'),
(7, 'TB96355582', 11, 6, 'Noela', 'deogracoousssekilordgracejohns@gmail.com', '+256757587161', '2025-07-31', '21:53:00', 6, 'all is well', 11700.00, 'momo', 'paid', NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-23 16:53:33', '2025-07-23 16:53:33'),
(8, 'TB0AA7AABF', 11, 4, 'SSEKIZIYIVU GRACE', 'noelaankunda@gmail.com', '+256757587161', '2025-10-24', '06:37:00', 10, 'i dont eat chicken ', 2500.00, 'momo', 'paid', NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-23 21:38:54', '2025-07-23 21:38:54'),
(9, 'TB233763F2', 13, 5, 'butsilo', 'deogracoousssekilordgracejohns@gmail.com', '+256757587161', '2025-07-25', '04:00:00', 15, 'i dont eat pork', 5250.00, 'momo', 'paid', NULL, NULL, NULL, NULL, NULL, NULL, '2025-07-23 21:57:26', '2025-07-23 21:57:26');

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`id`, `name`, `description`, `created_at`) VALUES
(1, 'Adventure Tours', 'Exciting adventure packages', '2025-07-06 13:06:37'),
(2, 'Cultural Tours', 'Explore local culture and heritage', '2025-07-06 13:06:37'),
(3, 'Wildlife Safari', 'Wildlife and nature tours', '2025-07-06 13:06:37'),
(4, 'Beach Holidays', 'Relaxing beach destinations', '2025-07-06 13:06:37'),
(5, 'Mountain Trekking', 'Mountain and hiking tours', '2025-07-06 13:06:37');

-- --------------------------------------------------------

--
-- Table structure for table `destination`
--

CREATE TABLE `destination` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `country` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `inquiries`
--

CREATE TABLE `inquiries` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `message` text NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inquiries`
--

INSERT INTO `inquiries` (`id`, `name`, `email`, `message`, `timestamp`) VALUES
(1, 'SSEKIZIYIVU GRACE', 'deogracoousssekilordgracejohns@gmail.com', 'can we get your contacts ', '2025-07-23 15:17:14'),
(2, 'SSEKIZIYIVU GRACE', 'deogracoousssekilordgracejohns@gmail.com', 'can we get your contacts ', '2025-07-23 15:18:57'),
(3, 'SSEKIZIYIVU GRACE', 'deogracoousssekilordgracejohns@gmail.com', 'thank you so much for your services\r\n', '2025-07-23 15:19:53');

-- --------------------------------------------------------

--
-- Table structure for table `review`
--

CREATE TABLE `review` (
  `id` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `comment` text DEFAULT NULL,
  `reviewer_name` varchar(100) NOT NULL,
  `reviewer_email` varchar(120) DEFAULT NULL,
  `is_verified` tinyint(1) DEFAULT NULL,
  `is_approved` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `tour_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `review`
--

INSERT INTO `review` (`id`, `rating`, `comment`, `reviewer_name`, `reviewer_email`, `is_verified`, `is_approved`, `created_at`, `tour_id`, `user_id`) VALUES
(1, 5, 'the tour was so good hope to travel with tourizo again', 'nono aad', 'noelaankunda@gmail.com', 1, 1, '2025-07-23 17:15:28', 6, 11),
(2, 4, 'i and my family we enjoyed touring to this place it was marvelous', 'NONO', 'noelaankunda@gmail.com', 1, 1, '2025-07-23 21:45:38', 4, 11),
(3, 3, 'thank u so much ', 'praise butsilo', 'butsilo@gmail.com', 1, 1, '2025-07-23 21:57:54', 5, 13);

-- --------------------------------------------------------

--
-- Table structure for table `tour`
--

CREATE TABLE `tour` (
  `id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` text NOT NULL,
  `short_description` varchar(300) DEFAULT NULL,
  `price` float NOT NULL,
  `duration` int(11) NOT NULL,
  `duration_type` varchar(20) DEFAULT NULL,
  `max_participants` int(11) DEFAULT NULL,
  `min_participants` int(11) DEFAULT NULL,
  `difficulty_level` varchar(20) DEFAULT NULL,
  `departure_location` varchar(200) DEFAULT NULL,
  `image` varchar(200) DEFAULT NULL,
  `image_gallery` text DEFAULT NULL,
  `inclusions` text DEFAULT NULL,
  `exclusions` text DEFAULT NULL,
  `itinerary` text DEFAULT NULL,
  `available_from` date DEFAULT NULL,
  `available_to` date DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `is_featured` tinyint(1) DEFAULT NULL,
  `meta_title` varchar(200) DEFAULT NULL,
  `meta_description` varchar(300) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `category_id` int(11) NOT NULL,
  `destination` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tour`
--

INSERT INTO `tour` (`id`, `title`, `description`, `short_description`, `price`, `duration`, `duration_type`, `max_participants`, `min_participants`, `difficulty_level`, `departure_location`, `image`, `image_gallery`, `inclusions`, `exclusions`, `itinerary`, `available_from`, `available_to`, `is_active`, `is_featured`, `meta_title`, `meta_description`, `created_at`, `updated_at`, `category_id`, `destination`) VALUES
(3, '5-Day Ugandan Safari', 'Explore the best of Uganda in 5 days including Murchison Falls and Queen Elizabeth parks. Experience game drives, boat cruises, and top-notch lodges.', 'Visit Murchison and Queen Elizabeth parks in 5 days!', 1125, 5, 'Days', 6, 2, 'Hard', 'Kampala', NULL, '[\"858c09326bf80e44.jpg\"]', '• Transport in a Select Vehicle\r\n• Accommodation in a Double room\r\n• Breakfast, Lunch and Dinner at Hotel\r\n• Park Entrance fees\r\n• Boat Cruise in Murchison\r\n• Game Drive in Murchison\r\n• Top of the falls Experience\r\n• Kazinga Channel Boat Cruise\r\n• Kasenyi Game Drive\r\n• Equator stop\r\n• Driver Guide\r\n', '• En-route meals\r\n• All personal expenses\r\n• Anything not listed in the inclusions\r\n', 'Day 1-3: Murchison Falls (9th to 11th March)\r\n- Game Drive, Boat Cruise, Top of the Falls\r\n\r\nDay 3-5: Queen Elizabeth (11th to 13th March)\r\n- Kazinga Channel Boat Cruise, Kasenyi Game Drive, Equator stop\r\n', '2025-08-09', '2025-08-13', 1, 1, 'Explore the Murchision falls - Adventure Tours in Uganda', 'Explore Murchision falls and feel the atmospheres of the water falls', '2025-07-09 14:59:30', '2025-07-09 14:59:30', 1, 'Murchison Falls & Queen Elizabeth'),
(4, 'Western Uganda Safari', 'Discover Queen Elizabeth National Park and the beauty of Fort Portal over a scenic journey including wildlife and crater lake adventures.', 'Queen Elizabeth to Fort Portal Safari: Game drives, crater lakes, caves.', 250, 4, 'Days', 3, 3, 'Moderate', 'Wakiso', NULL, '[\"afd20dd393f25d93.jpg\"]', 'Transport in a Safari Van\r\n• Accommodation at a selected Hotel\r\n• Breakfast, Lunch and Dinner at Hotel\r\n• Park Entrance fees\r\n• Boat Cruise\r\n• Game Drive\r\n• Amabeere Caves\r\n• Crater Lakes Exploration\r\n• Driver Guide\r\n• Drinking water in Vehicle', ' En-route meals\r\n• All personal expenses', 'March 14–16: Queen Elizabeth\r\nGame drives, boat cruise\r\n\r\nMarch 16–17: Fort Portal\r\nAmabeere Caves, crater lake tours\r\n\r\n', '2025-10-14', '2025-10-17', 1, 1, 'Explore the Queen Elizabeth  - Adventure Tours in Uganda', 'Explore the Queen Elizabeth  - Adventure Tours in Uganda', '2025-07-10 08:20:22', '2025-07-10 08:20:22', 3, 'Queen Elizabeth & Fort Portal'),
(5, 'Kalangala – Brovad Sands Lodge', 'Relaxing 3-night getaway to Kalangala with jet skiing, nature walks and serene beach views.', '3 Nights in Kalangala at Brovad Sands Lodge\r\n\r\n', 350, 4, 'Days', 2, 2, 'Moderate', 'Nakiwogo, Entebbe', NULL, '[\"c734e8a0c2a449ff.jpg\"]', 'Return Ferry Tickets\r\n• Accommodation in a Double room for 3 nights\r\n• Breakfast, Lunch and Dinner at the Hotel\r\n• Nature Walk\r\n• Jet Skiing', ' Transfers to and from Nakiwogo\r\n• Anything not listed in the inclusions\r\n\r\n', 'Day 1:\r\nDeparture from Nakiwogo via MV Kalangala Ferry\r\nArrival and check-in at Brovad Sands Lodge\r\nWelcome drink and beach walk\r\nDinner at the lodge\r\nDay 2:\r\nBreakfast\r\nJet Skiing experience\r\nLeisure afternoon at the beach\r\nDinner at the lodge\r\nDay 3:\r\nBreakfast\r\nNature walk on the island\r\nOptional visit to local craft markets\r\nSunset by the beach\r\nDinner\r\nDay 4:\r\nBreakfast\r\nCheck-out and return ferry to Entebbe', '2025-07-17', '2025-07-21', 1, 1, 'enjoy your stay ', 'enjoy your stay here', '2025-07-10 09:07:17', '2025-07-10 09:07:17', 1, 'Kalangala, Ssese Islands'),
(6, '3-Day Zanzibar Beach Escape', 'Beachfront stay with island excursions including Mnemba snorkeling, Prison Island and Stone Town tour.', 'Relax and explore Zanzibar in 3 days!', 1950, 3, 'Days', 2, 2, 'Hard', 'Nakiwogo, Entebbe', NULL, '[\"2b304994f904520f.jpg\"]', ' Return Air Tickets on Uganda Airlines\r\n• Accommodation in a Double room\r\n• Breakfast and Dinner\r\n• Airport transfers\r\n• Dolphin Tour and Mnemba Island Snorkeling\r\n• Prison Island & Stone Town Tour', '• Travel Insurance ($45 per person)\r\n• Hotel tax ($5/person/day)\r\n• Any other meals\r\n• Personal expenses', 'Day 1 (Dec 17):\r\n\r\nArrival in Zanzibar\r\n\r\nHotel check-in\r\n\r\nSunset relaxation\r\n\r\nDay 2 (Dec 18):\r\n\r\nMnemba Island Dolphin Tour & Snorkeling\r\n\r\nAfternoon at leisure\r\n\r\nDay 3 (Dec 19):\r\n\r\nPrison Island & Stone Town Tour\r\n\r\nDeparture', '2025-12-11', '2025-12-13', 1, 0, 'welcome to zanzibar', 'your most weelcome', '2025-07-10 09:25:12', '2025-07-10 09:50:55', 1, 'Zanzibar, Tanzania');

-- --------------------------------------------------------

--
-- Table structure for table `tour_date`
--

CREATE TABLE `tour_date` (
  `id` int(11) NOT NULL,
  `tour_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `available_spots` int(11) NOT NULL,
  `price_override` float DEFAULT NULL,
  `is_available` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tour_itinerary_day`
--

CREATE TABLE `tour_itinerary_day` (
  `id` int(11) NOT NULL,
  `tour_id` int(11) NOT NULL,
  `day` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `created_at` datetime DEFAULT NULL,
  `otp_code` varchar(8) DEFAULT NULL,
  `otp_expiry` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `login_attempts` int(11) DEFAULT NULL,
  `account_locked` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password_hash`, `is_admin`, `created_at`, `otp_code`, `otp_expiry`, `last_login`, `login_attempts`, `account_locked`) VALUES
(11, 'NONO', 'noelaankunda@gmail.com', 'scrypt:32768:8:1$dhRp5WnCchG5n2F6$241a277d394a9953febf8fed2b6d41fa87bc84a0dc36bb3c002e08f5f4db0c0bfaef6489c39da54d5920c37aed3cc758e11baedb7e070164a23b1dce620a6ce9', 0, '2025-07-22 12:11:21', NULL, NULL, '2025-07-23 21:30:45', 0, 0),
(12, 'SSEKIZIYIVU GRACE', 'ssekiziyivugrace55@gmail.com', 'scrypt:32768:8:1$2a0Som5MAtsSt77d$b79ba25564501c7febc260fb516b40f92c7e3409a677671a1545382ec910d53b0874d8ff42ed458ae961ce98296e1edf687b9b1f18418cd2ef981a21cb923726', 1, '2025-07-22 12:27:28', NULL, NULL, '2025-07-24 16:01:45', 0, 0),
(13, 'praise butsilo', 'butsilo@gmail.com', 'scrypt:32768:8:1$QueekLgaAx8O3yhC$768d486f137573bf50887918be4035405f83e3941c0fe486d4107b719aaaf836ed7678678b992b2affeaf287613e9b7429b8f4138f4c470f1e1537aee86724fd', 0, '2025-07-23 21:55:38', NULL, NULL, NULL, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `wishlist`
--

CREATE TABLE `wishlist` (
  `user_id` int(11) NOT NULL,
  `tour_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `wishlist`
--

INSERT INTO `wishlist` (`user_id`, `tour_id`) VALUES
(11, 3),
(11, 5),
(11, 6);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reference` (`reference`),
  ADD KEY `tour_id` (`tour_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `destination`
--
ALTER TABLE `destination`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `inquiries`
--
ALTER TABLE `inquiries`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `review`
--
ALTER TABLE `review`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tour_id` (`tour_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `tour`
--
ALTER TABLE `tour`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `tour_date`
--
ALTER TABLE `tour_date`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tour_id` (`tour_id`);

--
-- Indexes for table `tour_itinerary_day`
--
ALTER TABLE `tour_itinerary_day`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tour_id` (`tour_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `wishlist`
--
ALTER TABLE `wishlist`
  ADD PRIMARY KEY (`user_id`,`tour_id`),
  ADD KEY `tour_id` (`tour_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `booking`
--
ALTER TABLE `booking`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `destination`
--
ALTER TABLE `destination`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `inquiries`
--
ALTER TABLE `inquiries`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `review`
--
ALTER TABLE `review`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tour`
--
ALTER TABLE `tour`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `tour_date`
--
ALTER TABLE `tour_date`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tour_itinerary_day`
--
ALTER TABLE `tour_itinerary_day`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `booking`
--
ALTER TABLE `booking`
  ADD CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`tour_id`) REFERENCES `tour` (`id`);

--
-- Constraints for table `review`
--
ALTER TABLE `review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `review_ibfk_2` FOREIGN KEY (`tour_id`) REFERENCES `tour` (`id`);

--
-- Constraints for table `tour`
--
ALTER TABLE `tour`
  ADD CONSTRAINT `tour_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`);

--
-- Constraints for table `tour_date`
--
ALTER TABLE `tour_date`
  ADD CONSTRAINT `tour_date_ibfk_1` FOREIGN KEY (`tour_id`) REFERENCES `tour` (`id`);

--
-- Constraints for table `tour_itinerary_day`
--
ALTER TABLE `tour_itinerary_day`
  ADD CONSTRAINT `tour_itinerary_day_ibfk_1` FOREIGN KEY (`tour_id`) REFERENCES `tour` (`id`);

--
-- Constraints for table `wishlist`
--
ALTER TABLE `wishlist`
  ADD CONSTRAINT `wishlist_ibfk_1` FOREIGN KEY (`tour_id`) REFERENCES `tour` (`id`),
  ADD CONSTRAINT `wishlist_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
