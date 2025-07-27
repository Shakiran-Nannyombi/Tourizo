-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: travel_app
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('144b19ab5fde');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `payment_status` varchar(20) DEFAULT NULL,
  `reference` varchar(100) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `num_people` int(11) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `payment_reference` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `payment_method` varchar(50) NOT NULL,
  `booking_date` date NOT NULL,
  `booking_time` time NOT NULL,
  `payment_details` text DEFAULT NULL,
  `tour_id` int(11) NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `order_tracking_id` varchar(100) DEFAULT NULL,
  `special_requests` text DEFAULT NULL,
  `cancellation_reason` text DEFAULT NULL,
  `cancellation_notes` text DEFAULT NULL,
  `cancelled_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reference` (`reference`),
  KEY `tour_id` (`tour_id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking`
--

LOCK TABLES `booking` WRITE;
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
INSERT INTO `booking` VALUES (2,'ANKUNDA NOELA','noelaankunda@gmail.com','0758413210','paid','f05310f8-f6b7-4eae-b41c-482bc22c46c1',1,1,300.00,'SIM-2','2025-07-06 09:30:59','','0000-00-00','00:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(3,'ANKUNDA NOELA','noelaankunda@gmail.com','0758413210','paid','5de0ade1-369c-48d8-8465-44a9b5c608e7',1,1,350.00,'momo_token_airtel_9de42fcf22044713','2025-07-06 17:42:23','','0000-00-00','00:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(4,'ella','ella@gmail.com','0758413211','paid','f0c30263-7cac-4568-9c5f-8074b401c3b3',1,1,350.00,'card_token_a501fc8d63a948cc','2025-07-06 17:47:47','','0000-00-00','00:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(5,'ella','ella@gmail.com','0758413211','paid','60af8f34-b08d-4057-94fb-7b897eb02960',1,1,350.00,'card_token_a501fc8d63a948cc','2025-07-06 17:50:44','','0000-00-00','00:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(6,'ANKUNDA NOELA','noelaankunda@gmail.com','0758413210','paid','1a9f905e-688e-4b4d-98f2-8675c6a2df12',1,1,350.00,'momo_token_airtel_86d8f084c2244a40','2025-07-06 18:16:30','','0000-00-00','00:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(7,'larry','larr@gmail.com','0758413210','paid','29d38e20-d9d6-4428-a8b6-9ac371d20b03',1,1,350.00,'momo_token_mtn_8f6040fd39c948d7','2025-07-06 18:26:41','','0000-00-00','00:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(8,'larry','larr@gmail.com','0758413210','paid','eded8dbf-3853-4338-8552-c910a61f1d8d',1,1,350.00,'momo_token_mtn_8f6040fd39c948d7','2025-07-06 18:33:33','','0000-00-00','00:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(9,'ANKUNDA NOELA','noelaankunda@gmail.com','0758413210','paid','5f7f854a-d106-4221-a19f-0f8c2556d233',1,1,350.00,'momo_token_airtel_4912edfa68f94e53','2025-07-07 16:19:42','','0000-00-00','00:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(10,'ANKUNDA NOELA','noelaankunda@gmail.com','0758413210','paid','ff1c19b9-b0f1-4121-9e6a-5dea0ddbdf0f',1,1,350.00,'momo_token_airtel_6bdec7f21edd45d4','2025-07-07 17:08:10','','0000-00-00','00:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(11,'ANKUNDA NOELA','noelaankunda@gmail.com','0758413210','paid','5b4134b7-b40b-486a-8e96-a8eaa5715974',1,1,350.00,'momo_token_airtel_6bdec7f21edd45d4','2025-07-07 17:09:36','','0000-00-00','00:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(12,'ANKUNDA NOELA','noelaankunda@gmail.com','0758413210','paid','814fc72a-3c17-4bd0-a631-a9d5d75b50b7',1,1,350.00,'momo_token_airtel_b8eecd98694d410e','2025-07-07 17:15:11','','0000-00-00','00:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(13,'ANKUNDA NOELA','noelaankunda@gmail.com','0758413210','paid','ba0c1a0a-df80-48e2-bad5-a714b349bcba',1,1,350.00,'momo_token_airtel_b8eecd98694d410e','2025-07-07 17:20:53','','0000-00-00','00:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(14,'ANKUNDA NOELA','noelaankunda@gmail.com','0758413210','paid','f194fbad-ccfe-4244-999d-8e431af0d58a',1,1,350.00,'momo_token_airtel_b8eecd98694d410e','2025-07-07 17:25:44','','0000-00-00','00:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(15,'ANKUNDA NOELA','noelaankunda@gmail.com','0758413210','paid','4c56a5ea-6dc3-4989-8d0f-a7e768bac40d',1,1,350.00,'momo_token_airtel_b8eecd98694d410e','2025-07-07 17:29:09','','0000-00-00','00:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(16,'ANKUNDA NOELA','noelaankunda@gmail.com','0758413210','cancelled','2ba69612-a7d4-4edd-b3d3-e19c5f2b2ed5',1,1,350.00,'momo_token_airtel_611e2cdd768d413b','2025-07-07 17:31:44','','0000-00-00','00:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(44,'Ankunda NONO Noelakkk','noelaankunda@gmail.com','+256758413210','paid','8391d55f-77d5-4cab-9819-7d7e0e624f6a',1,1,20.00,'card_token_4042ef72','2025-07-11 23:03:15','card','2025-07-12','02:03:00','Provider: airtel, Number: ***3210',0,'2025-07-13 20:58:58',NULL,NULL,NULL,NULL,NULL),(26,'Ankunda Noela','noelaankunda@gmail.com','0758413210','paid','e7ee94df-569b-49b9-88c6-71f73a1922b1',1,1,50.00,'momo_token_airtel_5361c9b78cd74ea8','2025-07-09 22:19:47','','2025-07-10','09:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(27,'Ankunda Noela','noelaankunda@gmail.com','+256758413210','paid','f71b897a-141c-46c1-a86e-c9b1ba8190d3',1,1,20.00,'momo_token_2248f4d1','2025-07-10 16:41:25','momo','2025-07-10','09:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(28,'Ankunda Noela','noelaankunda@gmail.com','+256758413210','pending','745fcac1-2086-4da3-9fe5-f81cb8f879d4',1,1,20.00,NULL,'2025-07-10 17:31:28','momo','2025-07-10','09:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(21,'AS','anna@gmail.com','0756734567','cancelled','e4a14688-508f-4287-9151-04615be4f825',1,1,350.00,'momo_token_airtel_ee9df4ea113f46ff','2025-07-07 19:02:35','','2025-07-09','23:26:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(30,'Ankunda Noela','noelaankunda@gmail.com','+256758413210','cancelled','34e79942-36d9-4e39-b8f1-a2b02c29c172',1,1,350.00,NULL,'2025-07-10 17:49:03','momo','2025-07-10','09:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(31,'Ankunda Noela','noelaankunda@gmail.com','+256758413210','cancelled','f44643ae-9cdd-4955-9ebd-ea469eeb3420',1,1,350.00,NULL,'2025-07-10 18:03:59','momo','2025-07-10','09:00:00',NULL,0,'2025-07-13 20:59:27',NULL,NULL,NULL,NULL,NULL),(29,'Ankunda Noela','noelaankunda@gmail.com','+256758413210','pending','3a896a07-e964-43b3-89e0-283f63255310',1,1,350.00,NULL,'2025-07-10 17:43:26','momo','2025-07-10','09:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(32,'Ankunda Noela','noelaankunda@gmail.com','+256758413210','pending','a87730e4-4297-4b5c-8181-ddc01f3127da',1,1,20.00,NULL,'2025-07-10 18:11:43','momo','2025-07-10','09:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(33,'Ankunda Noela','noelaankunda@gmail.com','+256758413210','pending','ea3a869d-362e-4b02-afc9-3c368101cfc2',1,1,20.00,NULL,'2025-07-10 19:27:32','momo','2025-07-10','09:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(34,'Ankunda Noela','noelaankunda@gmail.com','+256758413210','pending','2b22f541-4715-4206-bab8-2168ebdaf5ad',1,1,20.00,NULL,'2025-07-10 19:30:59','momo','2025-07-10','09:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(36,'Ankunda Noela','noelaankunda@gmail.com','+256758413210','pending','f4e80dc3-c6ca-4d00-a04b-f77bfcd8115f',1,1,20.00,NULL,'2025-07-10 19:54:11','momo','2025-07-10','09:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(37,'Ankunda Noela','noelaankunda@gmail.com','+256758413210','pending','3a06821f-defd-47c9-908c-ff651348d1d7',1,1,20.00,NULL,'2025-07-10 20:18:04','momo','2025-07-10','09:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(38,'Ankunda Noela','noelaankunda@gmail.com','+256758413210','cancelled','3d481423-f7bf-4207-a4bb-d403632927cc',1,1,20.00,'card_token_b2475ebc','2025-07-11 17:06:40','card','2025-07-11','09:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(39,'Ankunda Noela','noelaankunda@gmail.com','+256758413210','cancelled','317c6fcb-1684-465c-b5d8-868df116bb35',1,1,350.00,NULL,'2025-07-11 17:31:55','','2025-07-11','09:00:00',NULL,0,NULL,NULL,NULL,NULL,NULL,NULL),(40,'Ankunda Noela ELAA','noelaankunda@gmail.com','+256758413210','cancelled','54e6f37c-ec16-47b1-b8b8-dc7ba672c428',1,1,20.00,'momo_8e64d4f0ae','2025-07-11 18:41:28','momo','2025-07-11','09:00:00','Provider: airtel, Number: 3210',0,NULL,NULL,NULL,NULL,NULL,NULL),(43,'Jesus','noelaankunda@gmail.com','+256758413210','paid','7a7e80e4-994a-4bae-8844-37c72aa2bd04',1,1,20.00,'momo_9395b2e00d','2025-07-11 22:36:36','momo','2025-07-12','04:35:00','Provider: airtel, Number: ***3210',0,NULL,NULL,NULL,NULL,NULL,NULL),(46,'gift','noelaankunda@gmail.com','+256758413210','cancelled','5e1a4929-d945-4295-a6a7-81ea0bacc2e2',1,1,350.00,'momo_57cb496578','2025-07-12 03:18:46','momo','2025-07-18','06:22:00','Provider: airtel, Number: ***3210',0,NULL,NULL,NULL,NULL,NULL,NULL),(48,'SSEKIZIYIVU GRACE','deogracoousssekilordgracejohns@gmail.com','+256757587161','cancelled','55059189-1d75-4935-8042-7ecfad497e94',1,5,1750.00,'card_token_acdee901','2025-07-12 15:30:38','card','2025-07-12','09:32:00','Provider: airtel, Number: ***7161',0,NULL,NULL,NULL,NULL,NULL,NULL),(49,'larry anith','noelaankunda@gmail.com','+256758413210','paid','39f6d7ac-8e60-447e-b34a-def21d36cbda',1,1,1125.00,'momo_652da9ec84','2025-07-13 20:47:00','momo','2025-07-15','23:50:00','Provider: Airtel, Number: ***3210',3,'2025-07-13 20:58:40',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Adventure Tours','Exciting adventure packages','2025-07-06 13:06:37'),(2,'Cultural Tours','Explore local culture and heritage','2025-07-06 13:06:37'),(3,'Wildlife Safari','Wildlife and nature tours','2025-07-06 13:06:37'),(4,'Beach Holidays','Relaxing beach destinations','2025-07-06 13:06:37'),(5,'Mountain Trekking','Mountain and hiking tours','2025-07-06 13:06:37');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `destination`
--

DROP TABLE IF EXISTS `destination`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `destination` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `country` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `destination`
--

LOCK TABLES `destination` WRITE;
/*!40000 ALTER TABLE `destination` DISABLE KEYS */;
/*!40000 ALTER TABLE `destination` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inquiries`
--

DROP TABLE IF EXISTS `inquiries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inquiries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `message` text NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inquiries`
--

LOCK TABLES `inquiries` WRITE;
/*!40000 ALTER TABLE `inquiries` DISABLE KEYS */;
INSERT INTO `inquiries` VALUES (1,'SSEKIZIYIVU GRACE','deogracoousssekilordgracejohns@gmail.com','can we get your contacts ','2025-07-23 15:17:14'),(2,'SSEKIZIYIVU GRACE','deogracoousssekilordgracejohns@gmail.com','can we get your contacts ','2025-07-23 15:18:57'),(3,'SSEKIZIYIVU GRACE','deogracoousssekilordgracejohns@gmail.com','thank you so much for your services\r\n','2025-07-23 15:19:53');
/*!40000 ALTER TABLE `inquiries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rating` int(11) NOT NULL,
  `comment` text DEFAULT NULL,
  `reviewer_name` varchar(100) NOT NULL,
  `reviewer_email` varchar(120) DEFAULT NULL,
  `is_verified` tinyint(1) DEFAULT NULL,
  `is_approved` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `tour_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `tour_id` (`tour_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` VALUES (1,5,'the tour was so good hope to travel with tourizo again','nono aad','noelaankunda@gmail.com',1,1,'2025-07-23 17:15:28',6,11),(2,4,'i and my family we enjoyed touring to this place it was marvelous','NONO','noelaankunda@gmail.com',1,1,'2025-07-23 21:45:38',4,11),(3,3,'thank u so much ','praise butsilo','butsilo@gmail.com',1,1,'2025-07-23 21:57:54',5,13);
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tour`
--

DROP TABLE IF EXISTS `tour`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tour` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `max_capacity` int(11) DEFAULT NULL,
  `current_bookings` int(11) DEFAULT NULL,
  `location` varchar(200) DEFAULT NULL,
  `duration_hours` int(11) DEFAULT NULL,
  `short_description` text DEFAULT NULL,
  `duration` int(11) DEFAULT NULL COMMENT 'Duration in specified units',
  `duration_type` varchar(50) DEFAULT NULL COMMENT 'Type of duration (days, hours, etc.)',
  `max_participants` int(11) DEFAULT NULL COMMENT 'Maximum number of participants',
  `min_participants` int(11) DEFAULT NULL COMMENT 'Minimum number of participants',
  `difficulty_level` varchar(50) DEFAULT NULL COMMENT 'Difficulty level of the tour',
  `departure_location` varchar(255) DEFAULT NULL COMMENT 'Tour departure location',
  `featured_image` varchar(255) DEFAULT NULL COMMENT 'Main featured image URL',
  `image_gallery` text DEFAULT NULL COMMENT 'JSON array of image URLs',
  `inclusions` text DEFAULT NULL COMMENT 'What is included in the tour',
  `exclusions` text DEFAULT NULL COMMENT 'What is excluded from the tour',
  `itinerary` text DEFAULT NULL COMMENT 'Detailed tour itinerary',
  `available_from` date DEFAULT NULL COMMENT 'Tour available from date',
  `available_to` date DEFAULT NULL COMMENT 'Tour available until date',
  `is_featured` tinyint(1) DEFAULT 0 COMMENT 'Whether tour is featured',
  `meta_title` varchar(255) DEFAULT NULL COMMENT 'SEO meta title',
  `meta_description` text DEFAULT NULL COMMENT 'SEO meta description',
  `category_id` int(11) DEFAULT NULL COMMENT 'Foreign key to tour category',
  `destination` varchar(255) DEFAULT NULL COMMENT 'Tour destination',
  `image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_tour_category_id` (`category_id`),
  KEY `idx_tour_destination` (`destination`(250)),
  KEY `idx_tour_is_featured` (`is_featured`),
  KEY `idx_tour_available_dates` (`available_from`,`available_to`),
  KEY `idx_tour_difficulty` (`difficulty_level`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tour`
--

LOCK TABLES `tour` WRITE;
/*!40000 ALTER TABLE `tour` DISABLE KEYS */;
INSERT INTO `tour` VALUES (3,'5-Day Ugandan Safari','Explore the best of Uganda in 5 days including Murchison Falls and Queen Elizabeth parks. Experience game drives, boat cruises, and top-notch lodges.',1125.00,1,'2025-07-09 14:59:30','2025-07-09 14:59:30',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL),(4,'Western Uganda Safari','Discover Queen Elizabeth National Park and the beauty of Fort Portal over a scenic journey including wildlife and crater lake adventures.',250.00,1,'2025-07-10 08:20:22','2025-07-10 08:20:22',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL),(5,'Kalangala – Brovad Sands Lodge','Relaxing 3-night getaway to Kalangala with jet skiing, nature walks and serene beach views.',350.00,1,'2025-07-10 09:07:17','2025-07-10 09:07:17',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL),(6,'3-Day Zanzibar Beach Escape','Beachfront stay with island excursions including Mnemba snorkeling, Prison Island and Stone Town tour.',1950.00,1,'2025-07-10 09:25:12','2025-07-10 09:50:55',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `tour` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tour_date`
--

DROP TABLE IF EXISTS `tour_date`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tour_date` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tour_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `available_spots` int(11) NOT NULL,
  `price_override` float DEFAULT NULL,
  `is_available` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tour_id` (`tour_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tour_date`
--

LOCK TABLES `tour_date` WRITE;
/*!40000 ALTER TABLE `tour_date` DISABLE KEYS */;
/*!40000 ALTER TABLE `tour_date` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tour_itinerary_day`
--

DROP TABLE IF EXISTS `tour_itinerary_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tour_itinerary_day` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tour_id` int(11) NOT NULL,
  `day` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tour_id` (`tour_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tour_itinerary_day`
--

LOCK TABLES `tour_itinerary_day` WRITE;
/*!40000 ALTER TABLE `tour_itinerary_day` DISABLE KEYS */;
/*!40000 ALTER TABLE `tour_itinerary_day` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(500) NOT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `otp_code` varchar(8) DEFAULT NULL,
  `otp_expiry` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `login_attempts` int(11) DEFAULT 0,
  `account_locked` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (4,'NoelaA','noelaankunda@gmail.com','scrypt:32768:8:1$3Ueq2Ed3RBPLWsOw$ad88a36330d9a23c5c2ebf7a632bc2243bb36a456123dc6da57773d6a2df5a094bccde4e231ddc6c8fbeacbd477d4c5950f14eb0c9286cb179e81e247077820a',0,'2025-07-14 18:49:03',NULL,NULL,NULL,0,0),(2,'grace','ssekiziyivugrace55@gmail.com','scrypt:32768:8:1$4VvtqEotQ1wPkt7o$611b087575343319f15c18c25ce7e2b603b4c419bea76c0e2a2ea11d8b986097e7473aa6992fdecece856ee21a4481fe26de7fc25c8288133fec68dc242d1b76',1,'2025-07-14 10:06:43',NULL,NULL,NULL,0,0),(5,'admin','admin@example.com','scrypt:32768:8:1$HwCPyaQV3IsQv2HC$9eafdac10411016e1aa35ebea0e21428e88c7919dbc5ba3441689245745644d189877aa00055645fda6327ac084d5e976b5b1c9e1d88ab432f5eb46878514045',1,'2025-07-15 00:45:57',NULL,NULL,NULL,0,0),(6,'Shakiran','shakirannannyombi@gmail.com','pbkdf2:sha256:600000$XqOF9BalqvUW1FHu$ba1a5e35786e3f75544e881f2e60d2d9b2042e5541260bcd75c7ca4a5258c24e',0,'2025-07-18 09:24:56',NULL,NULL,NULL,0,0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wishlist`
--

DROP TABLE IF EXISTS `wishlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wishlist` (
  `user_id` int(11) NOT NULL,
  `tour_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`tour_id`),
  KEY `tour_id` (`tour_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishlist`
--

LOCK TABLES `wishlist` WRITE;
/*!40000 ALTER TABLE `wishlist` DISABLE KEYS */;
INSERT INTO `wishlist` VALUES (11,3),(11,5),(11,6);
/*!40000 ALTER TABLE `wishlist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-26  8:33:43
