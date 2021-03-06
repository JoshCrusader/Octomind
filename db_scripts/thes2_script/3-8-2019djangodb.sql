-- MySQL dump 10.13  Distrib 5.7.12, for osx10.9 (x86_64)
--
-- Host: localhost    Database: djangodb
-- ------------------------------------------------------
-- Server version	5.7.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'Administrator'),(2,'Gamekeeper'),(3,'Operations Supervisor'),(4,'Owner');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add branch',7,'add_branch'),(20,'Can change branch',7,'change_branch'),(21,'Can delete branch',7,'delete_branch'),(22,'Can add gameroom',8,'add_gameroom'),(23,'Can change gameroom',8,'change_gameroom'),(24,'Can delete gameroom',8,'delete_gameroom'),(25,'Can add sensor',9,'add_sensor'),(26,'Can change sensor',9,'change_sensor'),(27,'Can delete sensor',9,'delete_sensor'),(28,'Can add sensor log',10,'add_sensorlog'),(29,'Can change sensor log',10,'change_sensorlog'),(30,'Can delete sensor log',10,'delete_sensorlog'),(31,'Can add room',11,'add_room'),(32,'Can change room',11,'change_room'),(33,'Can delete room',11,'delete_room'),(34,'Can add rpi',12,'add_rpi'),(35,'Can change rpi',12,'change_rpi'),(36,'Can delete rpi',12,'delete_rpi'),(37,'Can add sensor type',13,'add_sensortype'),(38,'Can change sensor type',13,'change_sensortype'),(39,'Can delete sensor type',13,'delete_sensortype'),(40,'Can view log entry',1,'view_logentry'),(41,'Can view permission',2,'view_permission'),(42,'Can view group',3,'view_group'),(43,'Can view user',4,'view_user'),(44,'Can view content type',5,'view_contenttype'),(45,'Can view session',6,'view_session'),(46,'Can view branch',7,'view_branch'),(47,'Can add clue details',14,'add_cluedetails'),(48,'Can change clue details',14,'change_cluedetails'),(49,'Can delete clue details',14,'delete_cluedetails'),(50,'Can view clue details',14,'view_cluedetails'),(51,'Can add clues',15,'add_clues'),(52,'Can change clues',15,'change_clues'),(53,'Can delete clues',15,'delete_clues'),(54,'Can view clues',15,'view_clues'),(55,'Can add game',16,'add_game'),(56,'Can change game',16,'change_game'),(57,'Can delete game',16,'delete_game'),(58,'Can view game',16,'view_game'),(59,'Can add game details',17,'add_gamedetails'),(60,'Can change game details',17,'change_gamedetails'),(61,'Can delete game details',17,'delete_gamedetails'),(62,'Can view game details',17,'view_gamedetails'),(63,'Can add players',18,'add_players'),(64,'Can change players',18,'change_players'),(65,'Can delete players',18,'delete_players'),(66,'Can view players',18,'view_players'),(67,'Can view room',11,'view_room'),(68,'Can view rpi',12,'view_rpi'),(69,'Can view sensor',9,'view_sensor'),(70,'Can view sensor type',13,'view_sensortype'),(71,'Can add teams',19,'add_teams'),(72,'Can change teams',19,'change_teams'),(73,'Can delete teams',19,'delete_teams'),(74,'Can view teams',19,'view_teams'),(75,'Can add game sequence error log',20,'add_gamesequenceerrorlog'),(76,'Can change game sequence error log',20,'change_gamesequenceerrorlog'),(77,'Can delete game sequence error log',20,'delete_gamesequenceerrorlog'),(78,'Can add auth user',21,'add_authuser'),(79,'Can change auth user',21,'change_authuser'),(80,'Can delete auth user',21,'delete_authuser'),(81,'Can add game error log',22,'add_gameerrorlog'),(82,'Can change game error log',22,'change_gameerrorlog'),(83,'Can delete game error log',22,'delete_gameerrorlog'),(84,'Can view game error log',22,'view_gameerrorlog'),(85,'Can add game warning log',23,'add_gamewarninglog'),(86,'Can change game warning log',23,'change_gamewarninglog'),(87,'Can delete game warning log',23,'delete_gamewarninglog'),(88,'Can view game warning log',23,'view_gamewarninglog'),(89,'Can add loc dictionary',24,'add_locdictionary'),(90,'Can change loc dictionary',24,'change_locdictionary'),(91,'Can delete loc dictionary',24,'delete_locdictionary'),(92,'Can view loc dictionary',24,'view_locdictionary'),(93,'Can add notifs',25,'add_notifs'),(94,'Can change notifs',25,'change_notifs'),(95,'Can delete notifs',25,'delete_notifs'),(96,'Can view notifs',25,'view_notifs'),(97,'Can add employee branch',26,'add_employeebranch'),(98,'Can change employee branch',26,'change_employeebranch'),(99,'Can delete employee branch',26,'delete_employeebranch');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$120000$79MgNsuZgyOg$PCb/KTHJHoYzy6eWsuwLO3fIC/NVR1m89JoYmT4LWA0=','2019-03-07 14:02:47.844556',1,'admin','Arianna','Grande','p@gmail.com',1,1,'2018-09-18 17:09:01.940340'),(2,'pbkdf2_sha256$100000$mmlkBLqCEbts$eUQ1qBH1dye79/HAk457DMBw4dWf/w1xk8qequ4ouzE=','2019-03-04 21:48:52.468009',0,'gk_cperez','Carlo','Perez','',0,1,'2018-09-24 16:19:25.705940'),(3,'pbkdf2_sha256$100000$mmlkBLqCEbts$eUQ1qBH1dye79/HAk457DMBw4dWf/w1xk8qequ4ouzE=','2019-03-02 01:24:30.587572',0,'os_jlazada','Jcrux','Lazada','',0,1,'2018-09-25 08:05:57.788519'),(4,'pbkdf2_sha256$100000$mmlkBLqCEbts$eUQ1qBH1dye79/HAk457DMBw4dWf/w1xk8qequ4ouzE=','2019-03-02 01:28:00.587598',0,'own_cdang','Chuck','Dang','',0,1,'2018-10-03 01:12:13.170811');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (1,1,1),(2,2,2),(3,3,3),(4,4,4);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `branch`
--

DROP TABLE IF EXISTS `branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `branch` (
  `branch_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `address` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`branch_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branch`
--

LOCK TABLES `branch` WRITE;
/*!40000 ALTER TABLE `branch` DISABLE KEYS */;
INSERT INTO `branch` VALUES (2,'Jupiter St.','Makati Jupiter St.'),(3,'Ayala 30th','Ayala 30th Street'),(4,'Century City Mall','Kalayaan Ave. Malate, Manila');
/*!40000 ALTER TABLE `branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clue_details`
--

DROP TABLE IF EXISTS `clue_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clue_details` (
  `clue_details_id` int(11) NOT NULL AUTO_INCREMENT,
  `detail` text,
  `timestamp` datetime DEFAULT NULL,
  `clue_item_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`clue_details_id`),
  KEY `clue_details_clue_item_id_fk` (`clue_item_id`),
  CONSTRAINT `clue_details_clue_item_id_fk` FOREIGN KEY (`clue_item_id`) REFERENCES `clue_item` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1674 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clue_details`
--

LOCK TABLES `clue_details` WRITE;
/*!40000 ALTER TABLE `clue_details` DISABLE KEYS */;
INSERT INTO `clue_details` VALUES (1589,'Locate a tool that would help you view white screen','2019-02-22 13:34:05',NULL),(1590,'Secure ciphers to decode 3 missing characters','2019-02-22 14:00:50',NULL),(1591,'Rotate the filter of the scope to figure out which switches needed to be ON for the colors','2019-02-10 17:40:40',NULL),(1592,'Locate a tool that would help you view white screen','2019-02-10 17:49:27',NULL),(1593,'Unlock the first room with the ship\'s serial number','2019-02-10 17:56:06',NULL),(1594,'These are the symbols on the map OC-ZD-RC-USS-SD-CyR','2019-02-10 18:15:37',NULL),(1595,'Rotate the filter of the scope to figure out which switches needed to be ON for the colors','2019-02-10 18:35:57',NULL),(1596,'These are the symbols on the map OC-ZD-RC-USS-SD-CyR','2019-02-10 19:05:11',NULL),(1597,'Locate a tool that would help you view white screen','2019-02-11 13:46:37',NULL),(1598,'Rotate the filter of the scope to figure out which switches needed to be ON for the colors','2019-02-11 13:55:42',NULL),(1599,'These are the symbols on the map OC-ZD-RC-USS-SD-CyR','2019-02-11 14:15:56',NULL),(1600,'What is the shortest term for invasion','2019-02-13 13:50:43',NULL),(1601,'Locate a tool that would help you view white screen','2019-02-13 17:35:06',NULL),(1602,'Unlock the first room with the ship\'s serial number','2019-02-13 17:53:58',NULL),(1603,'Secure ciphers to decode 3 missing characters','2019-02-13 18:00:53',NULL),(1604,'What is the shortest term for invasion','2019-02-13 18:08:44',NULL),(1605,'Unlock the first room with the ship\'s serial number','2019-02-14 15:56:03',NULL),(1606,'Locate a tool that would help you view white screen','2019-02-14 17:38:09',NULL),(1607,'Secure ciphers to decode 3 missing characters','2019-02-14 17:56:47',NULL),(1608,'These are the symbols on the map OC-ZD-RC-USS-SD-CyR','2019-02-14 18:01:12',NULL),(1609,'These are the symbols on the map OC-ZD-RC-USS-SD-CyR','2019-02-14 20:01:58',NULL),(1610,'These are the symbols on the map OC-ZD-RC-USS-SD-CyR','2019-02-14 21:03:52',NULL),(1611,'Rotate the filter of the scope to figure out which switches needed to be ON for the colors','2019-03-01 13:47:18',NULL),(1612,'There are three inverted triangles. Red Blue Yellow. These Shaded circle represent activated switches.','2019-03-01 13:49:10',NULL),(1613,'What is the shortest term for invasion. Three letter word.','2019-03-01 14:08:21',NULL),(1614,'pyramid side open','2019-03-01 14:14:34',NULL),(1615,'Locate a tool that help you view white screen. Then Find another key','2019-03-04 16:10:24',NULL),(1616,'There are three inverted triangles. Red Blue Yellow. These Shaded circle represent activated switches.','2019-03-04 16:11:47',NULL),(1617,'Rotate the filter of the scope to figure out which switches needed to be ON for the colors','2019-02-15 18:55:50',NULL),(1618,'What is the shortest term for invasion','2019-02-15 19:04:02',NULL),(1619,'These are the symbols on the map OC-ZD-RC-USS-SD-CyR','2019-02-15 19:15:34',NULL),(1620,'Locate a tool that would help you view white screen','2019-02-15 20:25:12',NULL),(1621,'Secure ciphers to decode 3 missing characters','2019-02-15 20:36:24',NULL),(1622,'These are the symbols on the map OC-ZD-RC-USS-SD-CyR','2019-02-15 21:02:42',NULL),(1623,'Locate a tool that would help you view white screen','2019-02-16 20:42:53',NULL),(1624,'These are the symbols on the map OC-ZD-RC-USS-SD-CyR','2019-02-16 21:10:39',NULL),(1625,'Unlock the first room with the ship\'s serial number','2019-02-16 14:53:55',NULL),(1626,'Secure ciphers to decode 3 missing characters','2019-02-16 14:57:45',NULL),(1627,'These are the symbols on the map OC-ZD-RC-USS-SD-CyR','2019-02-16 15:18:14',NULL),(1628,'Locate a tool that would help you view white screen','2019-02-16 20:41:34',NULL),(1629,'Rotate the filter of the scope to figure out which switches needed to be ON for the colors','2019-02-16 20:44:24',NULL),(1630,'pyramid side open','2019-02-16 21:01:39',NULL),(1631,'These are the symbols on the map OC-ZD-RC-USS-SD-CyR','2019-02-16 21:20:47',NULL),(1632,'Secure ciphers to decode 3 missing characters','2019-02-17 13:01:29',NULL),(1633,'What is the shortest term for invasion','2019-02-17 13:01:15',NULL),(1634,'pyramid side open','2019-02-17 13:12:20',NULL),(1635,'These are the symbols on the map OC-ZD-RC-USS-SD-CyR','2019-02-17 13:23:08',NULL),(1636,'These are the symbols on the map OC-ZD-RC-USS-SD-CyR','2019-02-18 15:55:59',NULL),(1637,'Locate the translator head hidden in the room','2019-02-18 16:16:38',NULL),(1638,'Decode the maze','2019-02-18 16:21:36',NULL),(1639,'Decode the maze','2019-02-20 17:15:12',NULL),(1640,'Locate a tool that would help you view white screen','2019-02-20 16:38:20',NULL),(1641,'These are the symbols on the map OC-ZD-RC-USS-SD-CyR','2019-02-20 17:05:36',NULL),(1642,'Locate a tool that would help you view white screen','2019-02-22 19:37:57',NULL),(1643,'Secure ciphers to decode 3 missing characters','2019-02-22 19:55:41',NULL),(1644,'pyramid side open','2019-02-22 20:07:47',NULL),(1645,'These are the symbols on the map OC-ZD-RC-USS-SD-CyR','2019-02-22 20:16:28',NULL),(1646,'The wire are used to map their location in the galactic map\n','2019-02-22 20:22:50',NULL),(1647,'Locate a tool that would help you view white screen','2019-02-23 15:38:26',NULL),(1648,'Locate the translator head hidden in the room','2019-02-23 16:16:28',NULL),(1649,'Locate a tool that would help you view white screen','2019-02-23 16:42:57',NULL),(1650,'These are the symbols on the map OC-ZD-RC-USS-SD-CyR','2019-02-23 17:05:10',NULL),(1651,'Unlock the first room with the ship\'s serial number','2019-02-24 17:50:59',NULL),(1652,'What is the shortest term for invasion','2019-02-24 17:57:24',NULL),(1653,'What is the shortest term for invasion. Three letter word.','2019-02-24 18:02:53',NULL),(1654,'dial the disc acording to the cipher','2019-02-24 18:11:15',NULL),(1655,'Secure ciphers to decode 3 missing characters','2019-02-24 18:22:09',NULL),(1656,'Secure ciphers to decode 3 missing characters','2019-02-24 18:01:07',NULL),(1657,'Secure ciphers to decode 3 missing characters','2019-02-24 20:05:53',NULL),(1658,'What is the shortest term for invasion','2019-02-24 20:12:17',NULL),(1659,'dial the disc acording to the cipher','2019-02-24 20:22:11',NULL),(1660,'pyramid side open','2019-02-25 17:03:17',NULL),(1661,'The wire are used to map their location in the galactic map\n','2019-02-25 17:09:19',NULL),(1662,'What is the shortest term for invasion','2019-02-25 17:53:56',NULL),(1663,'Decode the maze','2019-02-25 18:17:22',NULL),(1664,'The wire are used to map their location in the galactic map\n','2019-02-28 17:03:25',NULL),(1665,'Locate the translator head hidden in the room','2019-02-28 17:25:51',NULL),(1666,'What is the shortest term for invasion. Three letter word.','2019-02-28 18:59:52',NULL),(1667,'pyramid side open','2019-02-28 19:24:08',NULL),(1668,'Decipher the chest of revelation by searching for the keys in the closet','2019-03-06 22:33:06',NULL),(1669,'Search for the map to look for the missing pieces of the chest','2019-03-06 22:34:27',NULL),(1670,'The pentagram drawn in the map is pointing to some other dimension.','2019-03-06 22:35:07',NULL),(1671,'Use the key to discover the hidden lever','2019-03-06 22:35:35',NULL),(1672,'Rearrange the frame to activate the switch','2019-03-06 22:36:20',NULL),(1673,'The journal numbering says a hidden message','2019-03-06 22:36:47',NULL);
/*!40000 ALTER TABLE `clue_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clue_item`
--

DROP TABLE IF EXISTS `clue_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clue_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `detail` text,
  `room_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `clue_item_room_room_id_fk` (`room_id`),
  CONSTRAINT `clue_item_room_room_id_fk` FOREIGN KEY (`room_id`) REFERENCES `room` (`room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clue_item`
--

LOCK TABLES `clue_item` WRITE;
/*!40000 ALTER TABLE `clue_item` DISABLE KEYS */;
INSERT INTO `clue_item` VALUES (2,'Locate a tool that would help you view white screen',11),(3,'Rotate the filter of the scope to figure out which switches needed to be ON for the colors',11),(4,'Unlock the first room with the ship\'s serial number',11),(5,'Secure ciphers to decode 3 missing characters',11),(6,'What is the shortest term for invasion',11),(7,'pyramid side open',11),(8,'These are the symbols on the map OC-ZD-RC-USS-SD-CyR',11),(9,'There are three inverted triangles. Red Blue Yellow. These Shaded circle represent activated switches.',11),(10,'What is the shortest term for invasion. Three letter word.',11),(11,'Locate a tool that help you view white screen. Then Find another key',11),(12,'Locate the translator head hidden in the room',11),(13,'Decode the maze',11),(14,'The wire are used to map their location in the galactic map\n',11),(15,'dial the disc acording to the cipher',11),(16,'Decipher the chest of revelation by searching for the keys in the closet',3),(17,'Search for the map to look for the missing pieces of the chest',3),(18,'The pentagram drawn in the map is pointing to some other dimension.',3),(19,'Use the key to discover the hidden lever',3),(20,'Rearrange the frame to activate the switch',3),(21,'The journal numbering says a hidden message',3);
/*!40000 ALTER TABLE `clue_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clue_item_details`
--

DROP TABLE IF EXISTS `clue_item_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clue_item_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clue_id` int(11) DEFAULT NULL,
  `clue_item_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `clue_item_details_clue_item_id_fk` (`clue_item_id`),
  KEY `clue_item_details_clues_clue_id_fk` (`clue_id`),
  CONSTRAINT `clue_item_details_clue_item_id_fk` FOREIGN KEY (`clue_item_id`) REFERENCES `clue_item` (`id`),
  CONSTRAINT `clue_item_details_clues_clue_id_fk` FOREIGN KEY (`clue_id`) REFERENCES `clues` (`clue_id`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clue_item_details`
--

LOCK TABLES `clue_item_details` WRITE;
/*!40000 ALTER TABLE `clue_item_details` DISABLE KEYS */;
INSERT INTO `clue_item_details` VALUES (1,1589,2),(2,1590,5),(3,1591,3),(4,1592,2),(5,1593,4),(6,1594,8),(7,1595,3),(8,1596,8),(9,1597,2),(10,1598,3),(11,1599,8),(12,1600,6),(13,1601,2),(14,1602,4),(15,1603,5),(16,1604,6),(17,1605,4),(18,1606,2),(19,1607,5),(20,1608,8),(21,1609,8),(22,1610,8),(23,1611,3),(24,1612,9),(25,1613,10),(26,1614,7),(27,1615,11),(28,1616,9),(29,1617,3),(30,1618,6),(31,1619,8),(32,1620,2),(33,1621,5),(34,1622,8),(35,1623,2),(36,1624,8),(37,1625,4),(38,1626,5),(39,1627,8),(40,1628,2),(41,1629,3),(42,1630,7),(43,1631,8),(44,1632,5),(45,1633,6),(46,1634,7),(47,1635,8),(48,1636,8),(49,1637,12),(50,1638,13),(51,1639,13),(52,1640,2),(53,1641,8),(54,1642,2),(55,1643,5),(56,1644,7),(57,1645,8),(58,1646,14),(59,1647,2),(60,1648,12),(61,1649,2),(62,1650,8),(63,1651,4),(64,1652,6),(65,1653,10),(66,1654,15),(67,1655,5),(68,1656,5),(69,1657,5),(70,1658,6),(71,1659,15),(72,1660,7),(73,1661,14),(74,1662,6),(75,1663,13),(76,1664,14),(77,1665,12),(78,1666,10),(79,1667,7),(80,1668,16),(81,1669,17),(82,1670,18),(83,1671,19),(84,1672,20),(85,1673,21);
/*!40000 ALTER TABLE `clue_item_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clues`
--

DROP TABLE IF EXISTS `clues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clues` (
  `clue_details_id` int(11) NOT NULL,
  `game_id` int(11) NOT NULL,
  `clue_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`clue_id`),
  KEY `clues_details_id1_idx` (`clue_details_id`),
  KEY `game_id1_idx` (`game_id`),
  CONSTRAINT `clues_details_id1` FOREIGN KEY (`clue_details_id`) REFERENCES `clue_details` (`clue_details_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `game_id1` FOREIGN KEY (`game_id`) REFERENCES `game` (`game_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1674 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clues`
--

LOCK TABLES `clues` WRITE;
/*!40000 ALTER TABLE `clues` DISABLE KEYS */;
INSERT INTO `clues` VALUES (1589,262,1589),(1590,262,1590),(1591,253,1591),(1592,253,1592),(1593,253,1593),(1594,253,1594),(1595,254,1595),(1596,254,1596),(1597,255,1597),(1598,255,1598),(1599,255,1599),(1600,256,1600),(1601,257,1601),(1602,257,1602),(1603,257,1603),(1604,257,1604),(1605,258,1605),(1606,259,1606),(1607,259,1607),(1608,259,1608),(1609,260,1609),(1610,261,1610),(1611,264,1611),(1612,264,1612),(1613,264,1613),(1614,264,1614),(1615,266,1615),(1616,266,1616),(1617,268,1617),(1618,268,1618),(1619,268,1619),(1620,269,1620),(1621,269,1621),(1622,269,1622),(1623,270,1623),(1624,270,1624),(1625,271,1625),(1626,271,1626),(1627,271,1627),(1628,272,1628),(1629,272,1629),(1630,272,1630),(1631,272,1631),(1632,273,1632),(1633,273,1633),(1634,273,1634),(1635,273,1635),(1636,275,1636),(1637,275,1637),(1638,275,1638),(1639,277,1639),(1640,277,1640),(1641,277,1641),(1642,278,1642),(1643,278,1643),(1644,278,1644),(1645,278,1645),(1646,278,1646),(1647,279,1647),(1648,279,1648),(1649,280,1649),(1650,280,1650),(1651,281,1651),(1652,281,1652),(1653,281,1653),(1654,281,1654),(1655,281,1655),(1656,281,1656),(1657,282,1657),(1658,282,1658),(1659,282,1659),(1660,285,1660),(1661,285,1661),(1662,286,1662),(1663,286,1663),(1664,288,1664),(1665,288,1665),(1666,289,1666),(1667,289,1667),(1668,292,1668),(1669,292,1669),(1670,292,1670),(1671,292,1671),(1672,292,1672),(1673,292,1673);
/*!40000 ALTER TABLE `clues` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(21,'octo_site','authuser'),(7,'octo_site','branch'),(14,'octo_site','cluedetails'),(15,'octo_site','clues'),(26,'octo_site','employeebranch'),(16,'octo_site','game'),(17,'octo_site','gamedetails'),(22,'octo_site','gameerrorlog'),(8,'octo_site','gameroom'),(20,'octo_site','gamesequenceerrorlog'),(23,'octo_site','gamewarninglog'),(24,'octo_site','locdictionary'),(25,'octo_site','notifs'),(18,'octo_site','players'),(11,'octo_site','room'),(12,'octo_site','rpi'),(9,'octo_site','sensor'),(10,'octo_site','sensorlog'),(13,'octo_site','sensortype'),(19,'octo_site','teams'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-09-18 17:08:20.042279'),(2,'auth','0001_initial','2018-09-18 17:08:20.813057'),(3,'admin','0001_initial','2018-09-18 17:08:20.981176'),(4,'admin','0002_logentry_remove_auto_add','2018-09-18 17:08:21.000814'),(5,'contenttypes','0002_remove_content_type_name','2018-09-18 17:08:21.132816'),(6,'auth','0002_alter_permission_name_max_length','2018-09-18 17:08:21.168449'),(7,'auth','0003_alter_user_email_max_length','2018-09-18 17:08:21.199045'),(8,'auth','0004_alter_user_username_opts','2018-09-18 17:08:21.218330'),(9,'auth','0005_alter_user_last_login_null','2018-09-18 17:08:21.290300'),(10,'auth','0006_require_contenttypes_0002','2018-09-18 17:08:21.295159'),(11,'auth','0007_alter_validators_add_error_messages','2018-09-18 17:08:21.312015'),(12,'auth','0008_alter_user_username_max_length','2018-09-18 17:08:21.430124'),(13,'auth','0009_alter_user_last_name_max_length','2018-09-18 17:08:21.463514'),(14,'octo_site','0001_initial','2018-09-18 17:08:21.477965'),(15,'sessions','0001_initial','2018-09-18 17:08:21.539053'),(16,'octo_site','0002_room_rpi_sensortype','2018-10-01 07:57:06.765876'),(17,'admin','0003_logentry_add_action_flag_choices','2018-10-03 01:11:26.310754'),(18,'octo_site','0003_cluedetails_clues_game_gamedetails_players_teams','2018-10-12 06:00:49.709163'),(19,'octo_site','0004_gamesequenceerrorlog','2018-11-10 09:42:02.615839'),(20,'octo_site','0005_authuser','2018-11-10 09:42:02.635953'),(21,'octo_site','0002_gameerrorlog_gamewarninglog','2018-11-16 14:41:45.485098'),(22,'octo_site','0003_locdictionary','2018-11-16 22:41:23.699328'),(23,'octo_site','0004_notifs','2018-11-22 21:33:01.186700'),(24,'octo_site','0006_employeebranch_gameerrorlog_gamewarninglog_locdictionary_notifs','2019-02-05 13:26:39.619775');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('1su8efsntktbveggqppy3btd3wj17551','MzZmOWFhODg1ZGZlMDBhMjAxZjlkMjNlOWIyMTIzYjYxNzVkZTJiNTp7InVzZXJuYW1lIjoiYWRtaW4iLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZjVhMDkyYjg2MzBkOTE0ZDU4ZGY3OTg4MGQyMDdlOTM4NWQ3NGYxYSJ9','2018-11-07 15:40:20.366977'),('2o12atgu31yr5zhpl9lub7jwzpvem9xf','MmEzNzA2ZjVkZTI0OWQ2OWJkZTcyZDc1ZTI1MzNhYmUwNGM0NWYwMDp7InVzZXJuYW1lIjoiYWRtaW4iLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODZmMjQwN2Y4YjFjYjY5NWNlYjdhOTM1MDU1NDA5Y2ZiMjlmYTgwMCJ9','2018-12-13 13:08:37.022793'),('3fn9f0t20fjdlnsllswtxd8nvs39u8fh','MzZmOWFhODg1ZGZlMDBhMjAxZjlkMjNlOWIyMTIzYjYxNzVkZTJiNTp7InVzZXJuYW1lIjoiYWRtaW4iLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZjVhMDkyYjg2MzBkOTE0ZDU4ZGY3OTg4MGQyMDdlOTM4NWQ3NGYxYSJ9','2018-11-11 06:35:39.240225'),('58bgiowy964uix50e97l8cpsc2ar75a5','MGM1MWNjNjhmMTZhZGEwODQwMjU2YmI1NWNiMTQ0NjQwZjRmY2U0Yjp7InVzZXJuYW1lIjoiamMwMHgiLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiNCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYWNlNjU1ZDE1YmVmOWQ2YzhiZTNiYjc1ZmMyYjUxYmJkMDJiN2Y2NSJ9','2018-10-17 01:25:26.452038'),('5l3z0dtrp2bjdv7t7yahh08sput85q9c','MzZmOWFhODg1ZGZlMDBhMjAxZjlkMjNlOWIyMTIzYjYxNzVkZTJiNTp7InVzZXJuYW1lIjoiYWRtaW4iLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZjVhMDkyYjg2MzBkOTE0ZDU4ZGY3OTg4MGQyMDdlOTM4NWQ3NGYxYSJ9','2018-11-08 23:50:25.911558'),('6wllzxgel05ab70n98xyy91em0pk1a43','NWJhODQ2OTc0YTI4YmY5NTI1OWQxYjAzOWU3NDlmNzdiMzAwNjNiODp7InVzZXJuYW1lIjoiYWRtaW4iLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNTAyYjQxYzMxNzNlZDQ2NjlmYjgyZmFmODA2NDFhMGI4ZjIyMTg0YSJ9','2018-12-07 09:18:16.726379'),('6zj3s26cddxkuura6pkzbhuqzvzy02v7','MzZmOWFhODg1ZGZlMDBhMjAxZjlkMjNlOWIyMTIzYjYxNzVkZTJiNTp7InVzZXJuYW1lIjoiYWRtaW4iLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZjVhMDkyYjg2MzBkOTE0ZDU4ZGY3OTg4MGQyMDdlOTM4NWQ3NGYxYSJ9','2018-10-03 07:33:25.001681'),('9tow3ectc0szb473oll9sm7zyk9zpy94','MzZmOWFhODg1ZGZlMDBhMjAxZjlkMjNlOWIyMTIzYjYxNzVkZTJiNTp7InVzZXJuYW1lIjoiYWRtaW4iLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZjVhMDkyYjg2MzBkOTE0ZDU4ZGY3OTg4MGQyMDdlOTM4NWQ3NGYxYSJ9','2018-10-15 07:36:06.017212'),('bi6l6x2yceqf8gnltt3skqnn7sja9mas','MGM1MWNjNjhmMTZhZGEwODQwMjU2YmI1NWNiMTQ0NjQwZjRmY2U0Yjp7InVzZXJuYW1lIjoiamMwMHgiLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiNCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYWNlNjU1ZDE1YmVmOWQ2YzhiZTNiYjc1ZmMyYjUxYmJkMDJiN2Y2NSJ9','2018-10-17 01:12:18.022597'),('ekktbaa8y51zkimklzosdi1x4hyktk16','MmEzNzA2ZjVkZTI0OWQ2OWJkZTcyZDc1ZTI1MzNhYmUwNGM0NWYwMDp7InVzZXJuYW1lIjoiYWRtaW4iLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODZmMjQwN2Y4YjFjYjY5NWNlYjdhOTM1MDU1NDA5Y2ZiMjlmYTgwMCJ9','2018-12-24 17:29:05.019601'),('fxkhfhv76we50g58w748a1apfj4hm3in','MmEzNzA2ZjVkZTI0OWQ2OWJkZTcyZDc1ZTI1MzNhYmUwNGM0NWYwMDp7InVzZXJuYW1lIjoiYWRtaW4iLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODZmMjQwN2Y4YjFjYjY5NWNlYjdhOTM1MDU1NDA5Y2ZiMjlmYTgwMCJ9','2019-02-20 09:32:28.516863'),('iipbaj2tayzz9fvhmqool1vykxoi44up','Mzc0OWE2NWExMTYzNGY3NjU5YzE4ZmZlOTNlMjAzZjgyODBjYzc4NTp7InVzZXJuYW1lIjoib3duX2NkYW5nIiwiZ3Vlc3QiOnRydWUsImxvZ2dlZCI6dHJ1ZSwiX2F1dGhfdXNlcl9pZCI6IjQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6Ijg2ZjI0MDdmOGIxY2I2OTVjZWI3YTkzNTA1NTQwOWNmYjI5ZmE4MDAifQ==','2019-02-04 14:07:34.339788'),('k8u745rx1v1h3tffpzkr9q4mhu6x8nsz','OWZjMWEwMTA4ZjNmYzcxYTkwZWYyYjM0ZGJlZTExMTgwNWJhMjEyMjp7InVzZXJuYW1lIjoiYWRtaW4iLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMzdhZDBiMjY0MTBjNjgyYWQ1NjM0ZTdhNDNmNjEwYmM2NzM2MDgzMyJ9','2018-11-24 09:42:18.770886'),('q4ggay5vnqqg478v0exegdi8b77d5y3e','MmEzNzA2ZjVkZTI0OWQ2OWJkZTcyZDc1ZTI1MzNhYmUwNGM0NWYwMDp7InVzZXJuYW1lIjoiYWRtaW4iLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODZmMjQwN2Y4YjFjYjY5NWNlYjdhOTM1MDU1NDA5Y2ZiMjlmYTgwMCJ9','2018-12-26 21:17:58.028608'),('qmvj1dzs83yhhcqowqapcz5b3n01nzen','MWZkNDNjYzViMDY2ODIzNzg4YzEyYzhlNjIzODc1NjM2MGEzODZlNjp7InVzZXJuYW1lIjoiYWRtaW4iLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNjk1OGMwYmQ2NDRjMDI4ZmFlZDVjMzBkZjVjOGU5MjcyZjE3YTZkMyJ9','2019-03-21 14:02:47.847740'),('r45mjn75g3cux6589a8ilvi5akxtafai','MzZmOWFhODg1ZGZlMDBhMjAxZjlkMjNlOWIyMTIzYjYxNzVkZTJiNTp7InVzZXJuYW1lIjoiYWRtaW4iLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZjVhMDkyYjg2MzBkOTE0ZDU4ZGY3OTg4MGQyMDdlOTM4NWQ3NGYxYSJ9','2018-11-11 06:32:28.568515'),('rusuyxreqild3qb5q233rq775brh1wvm','MmEzNzA2ZjVkZTI0OWQ2OWJkZTcyZDc1ZTI1MzNhYmUwNGM0NWYwMDp7InVzZXJuYW1lIjoiYWRtaW4iLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODZmMjQwN2Y4YjFjYjY5NWNlYjdhOTM1MDU1NDA5Y2ZiMjlmYTgwMCJ9','2019-03-20 13:37:47.232549'),('shlcjblt0a94oxagl1yyy8hvnqga9elx','YjdjNWNiMmJhNjU1ZDk0N2YzYjQ1N2YwYmUwODBmZjc4Zjg4M2ViMjp7InVzZXJuYW1lIjoiYWRtaW4iLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMzc3MGE5YzExZGJkMjQ1YTgyMTk4NmE3ODJiMDI2NzZmZjQ3MTljMCJ9','2018-11-14 11:08:59.131083'),('twlddsx9qp0yo9rut5j4ypsc16gh9hgq','OWZjMWEwMTA4ZjNmYzcxYTkwZWYyYjM0ZGJlZTExMTgwNWJhMjEyMjp7InVzZXJuYW1lIjoiYWRtaW4iLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMzdhZDBiMjY0MTBjNjgyYWQ1NjM0ZTdhNDNmNjEwYmM2NzM2MDgzMyJ9','2018-11-26 11:18:02.196526'),('zkmh1sowk3iit9ui9t3qfdqqk82uibdu','MzZmOWFhODg1ZGZlMDBhMjAxZjlkMjNlOWIyMTIzYjYxNzVkZTJiNTp7InVzZXJuYW1lIjoiYWRtaW4iLCJndWVzdCI6dHJ1ZSwibG9nZ2VkIjp0cnVlLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZjVhMDkyYjg2MzBkOTE0ZDU4ZGY3OTg4MGQyMDdlOTM4NWQ3NGYxYSJ9','2018-11-06 13:41:13.539922');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_branch`
--

DROP TABLE IF EXISTS `employee_branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employee_branch` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `branch_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `employee_account_auth_user_id_fk` (`user_id`),
  KEY `employee_branch_branch_branch_id_fk` (`branch_id`),
  CONSTRAINT `employee_account_auth_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `employee_branch_branch_branch_id_fk` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`branch_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_branch`
--

LOCK TABLES `employee_branch` WRITE;
/*!40000 ALTER TABLE `employee_branch` DISABLE KEYS */;
INSERT INTO `employee_branch` VALUES (1,2,4),(2,3,2);
/*!40000 ALTER TABLE `employee_branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game`
--

DROP TABLE IF EXISTS `game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game` (
  `game_id` int(11) NOT NULL AUTO_INCREMENT,
  `game_keeper_id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `game_details_id` int(11) NOT NULL,
  `with_voucher` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`game_id`),
  KEY `fk_game_auth_user1_idx` (`game_keeper_id`),
  KEY `fk_game_room1_idx` (`room_id`),
  KEY `fk_game_details1_idx` (`game_details_id`),
  CONSTRAINT `fk_game_auth_user1` FOREIGN KEY (`game_keeper_id`) REFERENCES `auth_user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_game_details1` FOREIGN KEY (`game_details_id`) REFERENCES `game_details` (`game_details_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_game_room1` FOREIGN KEY (`room_id`) REFERENCES `room` (`room_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=298 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game`
--

LOCK TABLES `game` WRITE;
/*!40000 ALTER TABLE `game` DISABLE KEYS */;
INSERT INTO `game` VALUES (253,1,11,253,0),(254,1,11,254,0),(255,1,11,255,0),(256,1,11,256,0),(257,1,11,257,1),(258,1,11,258,0),(259,1,11,259,1),(260,1,11,260,0),(261,1,11,261,0),(262,1,11,262,1),(264,1,11,264,0),(266,1,11,266,0),(267,1,11,267,0),(268,1,11,268,1),(269,1,11,269,1),(270,1,11,270,0),(271,1,11,271,0),(272,1,11,272,1),(273,1,11,273,0),(275,1,11,275,0),(276,1,11,276,0),(277,1,11,277,0),(278,1,11,278,0),(279,1,11,279,0),(280,1,11,280,0),(281,1,11,281,0),(282,1,11,282,0),(283,1,11,283,0),(284,1,11,284,1),(285,1,11,285,0),(286,1,11,286,0),(287,1,11,287,0),(288,1,11,288,0),(289,1,11,289,0),(291,1,11,291,0),(292,1,3,292,0),(293,1,3,293,0),(294,1,3,294,0),(295,1,3,295,0),(296,1,3,296,0),(297,1,3,297,0);
/*!40000 ALTER TABLE `game` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_details`
--

DROP TABLE IF EXISTS `game_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_details` (
  `game_details_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestart` datetime DEFAULT NULL,
  `timeend` datetime DEFAULT NULL,
  `teamname` varchar(45) DEFAULT NULL,
  `solved` tinyint(2) DEFAULT '0',
  PRIMARY KEY (`game_details_id`)
) ENGINE=InnoDB AUTO_INCREMENT=298 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_details`
--

LOCK TABLES `game_details` WRITE;
/*!40000 ALTER TABLE `game_details` DISABLE KEYS */;
INSERT INTO `game_details` VALUES (253,'2019-02-10 17:30:00','2019-02-10 18:25:00','Gamolgasaur',1),(254,'2019-02-10 18:30:00','2019-02-10 19:25:30','Null Void',1),(255,'2019-02-11 13:30:00','2019-02-11 14:28:30','Shobelyns',1),(256,'2019-02-13 13:30:00','2019-02-13 14:25:00','yeahRight',1),(257,'2019-02-13 17:30:00',NULL,'Panic!',0),(258,'2019-02-14 15:30:00','2019-02-14 16:24:09','Blackjac',1),(259,'2019-02-14 17:30:00','2019-02-14 18:20:00','Henl0',1),(260,'2019-02-14 19:30:00',NULL,'Champs101',0),(261,'2019-02-14 20:30:00','2019-02-14 21:24:07','Mariamaria',1),(262,'2019-02-22 13:26:36','2019-02-22 14:16:34','Emirates',1),(264,'2019-03-01 13:28:49',NULL,'Team 1',0),(266,'2019-03-04 15:40:43',NULL,'Kyleanga',0),(267,NULL,NULL,'Assd',0),(268,'2019-02-15 18:30:00',NULL,'Danny\'s Angel',0),(269,'2019-02-15 20:15:00',NULL,'Adelie',0),(270,'2019-02-16 20:30:00','2019-02-16 21:27:12','We Are Young',1),(271,'2019-02-16 14:30:00','2019-02-16 15:26:20','Tanner Port',1),(272,'2019-02-16 20:30:00','2019-02-16 21:25:43','Myself, I',1),(273,'2019-02-17 12:30:00',NULL,'You Move',0),(275,'2019-02-18 15:30:00',NULL,'Restless Bois',0),(276,'2019-02-19 18:30:00',NULL,'Winneir',0),(277,'2019-02-20 16:30:00','2019-02-20 17:23:01','ComeThru',1),(278,'2019-02-22 19:30:00',NULL,'Team Mystery',0),(279,'2019-02-23 15:30:00','2019-02-23 16:27:23','Songerz',1),(280,'2019-02-23 16:30:00','2019-02-23 17:25:20','FEU SOlverz',1),(281,'2019-02-24 17:30:00',NULL,'Leroys',0),(282,'2019-02-24 19:30:00','2019-02-24 20:20:23','Sanchez Clan',0),(283,'2019-02-24 20:30:00','2019-02-24 21:28:30','ADulting',1),(284,'2019-02-25 15:30:00','2019-02-25 16:08:23','Payong Academy',1),(285,'2019-02-25 16:30:00','2019-02-25 17:13:00','Wasakan',0),(286,'2019-02-25 17:30:00',NULL,'Graduates',0),(287,'2019-02-25 19:30:00','2019-02-25 20:13:21','TwoTeeNine',1),(288,'2019-02-28 16:30:00',NULL,'Seventeen6',0),(289,'2019-02-28 18:30:00',NULL,'Sharks',0),(291,NULL,NULL,'mark',0),(292,'2019-03-06 22:29:41',NULL,'Markerino',0),(293,'2019-03-06 23:34:14',NULL,'Dedes Doll',0),(294,'2019-02-16 16:53:15','2019-02-16 16:59:15','Fork',0),(295,'2019-02-16 17:31:24',NULL,'Wander Team',0),(296,'2019-02-16 19:31:24','2019-03-07 20:27:30','Wander Team',1),(297,'2019-03-08 01:53:41',NULL,'Cholocroc',0);
/*!40000 ALTER TABLE `game_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_error_log`
--

DROP TABLE IF EXISTS `game_error_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_error_log` (
  `game_error_id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) NOT NULL,
  `sensor_id` int(11) NOT NULL,
  `details` varchar(100) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `cur_sensor_seq` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`game_error_id`,`game_id`,`sensor_id`),
  KEY `game_id_idx` (`game_id`),
  KEY `sensor_id_idx` (`sensor_id`),
  CONSTRAINT `game_id` FOREIGN KEY (`game_id`) REFERENCES `game` (`game_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `sensor_id` FOREIGN KEY (`sensor_id`) REFERENCES `sensor` (`sensor_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=272 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_error_log`
--

LOCK TABLES `game_error_log` WRITE;
/*!40000 ALTER TABLE `game_error_log` DISABLE KEYS */;
INSERT INTO `game_error_log` VALUES (265,261,28,'Maze Map Sensor not in sequence','2019-02-14 20:52:35','[26, 28, 29]'),(266,261,29,'Translator Sensor not in sequence','2019-02-14 21:21:00','[26, 28, 29]');
/*!40000 ALTER TABLE `game_error_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_warning_log`
--

DROP TABLE IF EXISTS `game_warning_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_warning_log` (
  `game_warning_id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `sensor_id` int(11) DEFAULT NULL,
  `details` varchar(45) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `time_solved` float DEFAULT NULL,
  PRIMARY KEY (`game_warning_id`),
  KEY `sensor_id_idx` (`sensor_id`),
  KEY `game_id_idx` (`game_id`),
  CONSTRAINT `log_game_id` FOREIGN KEY (`game_id`) REFERENCES `game` (`game_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `log_sensor_id` FOREIGN KEY (`sensor_id`) REFERENCES `sensor` (`sensor_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_warning_log`
--

LOCK TABLES `game_warning_log` WRITE;
/*!40000 ALTER TABLE `game_warning_log` DISABLE KEYS */;
INSERT INTO `game_warning_log` VALUES (69,262,27,'27 solved super fast','2019-02-22 14:10:49',1.85),(70,262,28,'28 solved super fast','2019-02-22 14:13:03',2.22),(71,262,29,'29 solved super fast','2019-02-22 14:16:11',3.13);
/*!40000 ALTER TABLE `game_warning_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loc_dictionary`
--

DROP TABLE IF EXISTS `loc_dictionary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `loc_dictionary` (
  `loc_dictionary_id` int(11) NOT NULL AUTO_INCREMENT,
  `loc_code` varchar(45) DEFAULT NULL,
  `loc_title` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`loc_dictionary_id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loc_dictionary`
--

LOCK TABLES `loc_dictionary` WRITE;
/*!40000 ALTER TABLE `loc_dictionary` DISABLE KEYS */;
INSERT INTO `loc_dictionary` VALUES (1,'PH-ABR','Abra'),(2,'PH-AGN','Agusan del Norte'),(3,'PH-AGS','Agusan del Sur'),(4,'PH-AKL','Aklan'),(5,'PH-ALB','Albay'),(6,'PH-ANT','Antique'),(7,'PH-APA','Apayao'),(8,'PH-AUR','Aurora'),(9,'PH-BAS','Basilan'),(10,'PH-BAN','Bataan'),(11,'PH-BTN','Batanes'),(12,'PH-BTG','Batangas'),(13,'PH-BEN','Benguet'),(14,'PH-BIL','Biliran'),(15,'PH-BOH','Bohol'),(16,'PH-BUK','Bukidnon'),(17,'PH-BUL','Bulacan'),(18,'PH-CAG','Cagayan'),(19,'PH-CAN','Camarines Norte'),(20,'PH-CAS','Camarines Sur'),(21,'PH-CAM','Camiguin'),(22,'PH-CAP','Capiz'),(23,'PH-CAT','Catanduanes'),(24,'PH-CAV','Cavite'),(25,'PH-CEB','Cebu'),(26,'PH-COM','Compostela Valley'),(27,'PH-NCO','Cotabato'),(28,'PH-DAO','Davao Oriental'),(29,'PH-DAV','Davao del Norte'),(30,'PH-DAS','Davao del Sur'),(31,'PH-DIN','Dinagat Islands'),(32,'PH-EAS','Eastern Samar'),(33,'PH-GUI','Guimaras'),(34,'PH-IFU','Ifugao'),(35,'PH-ILN','Ilocos Norte'),(36,'PH-ILS','Ilocos Sur'),(37,'PH-ILI','Iloilo'),(38,'PH-ISA','Isabela'),(39,'PH-KAL','Kalinga'),(40,'PH-LUN','La Union'),(41,'PH-LAG','Laguna'),(42,'PH-LAN','Lanao del Norte'),(43,'PH-LAS','Lanao del Sur'),(44,'PH-LEY','Leyte'),(45,'PH_MG','Maguindanao'),(46,'PH-MAD','Marinduque'),(47,'PH-MAS','Masbate'),(48,'PH-MNL','Metropolitan Manila'),(49,'PH-MDC','Mindoro Occidental'),(50,'PH-MDR','Mindoro Oriental'),(51,'PH-MSC','Misamis Occidental'),(52,'PH-MSR','Misamis Oriental'),(53,'PH-MOU','Mountain Province'),(54,'PH-NEC','Negros Occidental'),(55,'PH-NER','Negros Oriental'),(56,'PH-NSA','Northern Samar'),(57,'PH-NUE','Nueva Ecija'),(58,'PH-NUV','Nueva Vizcaya'),(59,'PH-PLW','Palawan'),(60,'PH-PAM','Pampanga'),(61,'PH-PAN','Pangasinan'),(62,'PH-QUE','Quezon'),(63,'PH-QUI','Quirino'),(64,'PH-RIZ','Rizal'),(65,'PH-ROM','Romblon'),(66,'PH-WSA','Samar'),(67,'PH-SAR','Sarangani'),(68,'PH-SIG','Siquijor'),(69,'PH-SOR','Sorsogon'),(70,'PH-SCO','South Cotabato'),(71,'PH-SLE','Southern Leyte'),(72,'PH-SUK','Sultan Kudarat'),(73,'PH-SLU','Sulu'),(74,'PH-SUN','Surigao del Norte'),(75,'PH-SUR','Surigao del Sur'),(76,'PH-TAR','Tarlac'),(77,'PH-TAW','Tawi-Tawi'),(78,'PH-ZMB','Zambales'),(79,'PH-ZSI','Zamboanga Sibugay'),(80,'PH-ZAN','Zamboanga del Norte'),(81,'PH-ZAS','Zamboanga del Sur');
/*!40000 ALTER TABLE `loc_dictionary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifs`
--

DROP TABLE IF EXISTS `notifs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notifs` (
  `notif_id` int(11) NOT NULL AUTO_INCREMENT,
  `details` varchar(150) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `viewed` tinyint(1) DEFAULT '0',
  `game_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`notif_id`),
  KEY `notif_game_game_id_fk` (`game_id`),
  CONSTRAINT `notif_game_game_id_fk` FOREIGN KEY (`game_id`) REFERENCES `game` (`game_id`)
) ENGINE=InnoDB AUTO_INCREMENT=122 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifs`
--

LOCK TABLES `notifs` WRITE;
/*!40000 ALTER TABLE `notifs` DISABLE KEYS */;
INSERT INTO `notifs` VALUES (95,'Sensor Sequence Error Detected at game 100261','2019-02-22 08:00:15',1,261),(96,'Sensor Sequence Error Detected at game 100261','2019-02-22 08:00:15',1,261),(97,'Game 100262 @ Alien Assault CCM started.','2019-02-22 13:26:36',1,262),(98,'Game Anomaly Detected at game 100262','2019-02-22 14:10:49',1,262),(99,'Game Anomaly Detected at game 100262','2019-02-22 14:13:03',1,262),(100,'Game Anomaly Detected at game 100262','2019-02-22 14:16:11',1,262),(101,'Game 100262 @ Alien Assault CCM ended.','2019-02-22 14:16:34',1,262),(103,'Game 100264 @ Alien Assault CCM started.','2019-03-01 13:28:48',1,264),(107,'Sensor Sequence Error Detected at game 100281','2019-03-03 23:49:11',1,281),(108,'Sensor Sequence Error Detected at game 100281','2019-03-03 23:49:12',1,281),(109,'Sensor Sequence Error Detected at game 100281','2019-03-03 23:49:12',1,281),(110,'Game Anomaly Detected at game 100281','2019-03-03 23:49:13',1,281),(111,'Game Anomaly Detected at game 100281','2019-03-04 00:36:24',1,281),(112,'Game 100266 @ Alien Assault CCM started.','2019-03-04 15:40:42',1,266),(115,'Game 100292 @ Debbys Doll started.','2019-03-06 22:29:40',1,292),(116,'Game 100293 @ Debbys Doll started.','2019-03-06 23:34:14',1,293),(117,'Game 100294 @ Debbys Doll started.','2019-03-07 16:53:15',1,294),(118,'Game 100294 @ Debbys Doll ended.','2019-03-07 16:59:15',1,294),(119,'Game 100296 @ Debbys Doll started.','2019-03-07 19:31:23',0,296),(120,'Game 100296 @ Debbys Doll ended.','2019-03-07 20:27:30',0,296),(121,'Game 100297 @ Debbys Doll started.','2019-03-08 01:53:41',0,297);
/*!40000 ALTER TABLE `notifs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `players` (
  `players_id` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(45) DEFAULT NULL,
  `lastname` varchar(45) DEFAULT NULL,
  `contact` varchar(45) DEFAULT NULL,
  `gender` int(1) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `loc_dictionary_id` int(11) DEFAULT NULL,
  `times_repeat` int(11) DEFAULT '1',
  PRIMARY KEY (`players_id`),
  KEY `fk_loc_id_idx` (`loc_dictionary_id`),
  CONSTRAINT `fk_loc_id` FOREIGN KEY (`loc_dictionary_id`) REFERENCES `loc_dictionary` (`loc_dictionary_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1155 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `players`
--

LOCK TABLES `players` WRITE;
/*!40000 ALTER TABLE `players` DISABLE KEYS */;
INSERT INTO `players` VALUES (9,'Ebow','Crowfoot','7809971217',1,'Ebow_Crowfoot@gmail.com',30,48,1),(10,'Daren','Clover','2839601675',1,'Daren_Clover@gmail.com',30,41,1),(11,'Gael','Futrell','5274398835',0,'Gael_Futrell@gmail.com',19,24,1),(12,'Thorfinn','Outhwaite','5572739802',1,'Thorfinn_Outhwaite@gmail.com',57,65,1),(13,'Marko','Huxtable','796162709',1,'Marko_Huxtable@gmail.com',21,24,3),(14,'Orlaith','Rockett','1578817654',0,'Orlaith_Rockett@gmail.com',21,24,2),(15,'Dylin','Crofts','7452789597',1,'Dylin_Crofts@gmail.com',9,48,5),(16,'Shannon','Mosedale','1397473884',1,'Shannon_Mosedale@gmail.com',47,41,6),(17,'Kitana','Lillis','7752908593',0,'Kitana_Lillis@gmail.com',32,42,1),(18,'Dennan','Considine','7112149652',1,'Dennan_Considine@gmail.com',35,41,10),(19,'Kaydn','Woffindin','1355384690',1,'Kaydn_Woffindin@gmail.com',28,19,1),(20,'Cassie','Codd','7561388015',0,'Cassie_Codd@gmail.com',26,48,5),(21,'Jena','Heathcote','2214413899',0,'Jena_Heathcote@gmail.com',48,41,1),(22,'Macaulay','Hordern','8236200488',1,'Macaulay_Hordern@gmail.com',53,73,1),(23,'Stephanie-Anne','Tribute','1622216987',0,'Stephanie-Anne_Tribute@gmail.com',29,48,1),(24,'Eva','Fieldstead','461177813',0,'Eva_Fieldstead@gmail.com',28,41,1),(25,'Eryk','Davies','2220343794',1,'Eryk_Davies@gmail.com',25,48,3),(26,'Aleksander','Atnicle?','8855596153',1,'Aleksander_Atnicle?@gmail.com',34,41,1),(27,'Calum-James','Bryer','7645768670',1,'Calum-James_Bryer@gmail.com',26,48,1),(28,'Sawdah','Stroud','3840291668',0,'Sawdah_Stroud@gmail.com',42,48,6),(29,'Harold','Edelston','6792238955',1,'Harold_Edelston@gmail.com',29,16,1),(1050,'Emir','Mendoza','09055165548',0,'suraba@gmail.com',16,48,1),(1051,'Chingona','Kunyo','09881233767',0,'suraba@gmail.com',20,12,1),(1052,'Harkan','Aju','09055165548',0,'leebet@gmail.com',19,12,3),(1053,'Justinz','Sarjun','09011223344',0,'ll@gmail.com',20,25,1),(1054,'Chingona','AM','123',0,'suraba@gmail.com',12,48,3),(1055,'Markk','kk','123',0,'leebet12@gmail.com',12,12,1),(1056,'The DOG','G0ud','123',0,'Dao@gmail.com',23,25,1),(1057,'dalaga','Pipi','09055165548',0,'as@gmail.com',19,5,1),(1058,'Arkansa','Soadheim','0922333159',0,'ii@gmail.com',20,5,1),(1059,'Makita','Yeh','09002234112',0,'f@mgil.com',19,12,33),(1060,'Arkham','Bait','12',0,'suraba@gmail.com',12,12,1),(1061,'Karambol','Jakol','23',0,'sdf@gmail.com',15,12,1),(1062,'Hambol','Safa','25',1,'sdf@gmail.com',20,12,1),(1063,'Ozzy','Hataki','23',0,'sdf@gmail.com',11,5,2),(1064,'Garamouche','Santos','21',1,'sdf@gmail.com',12,48,5),(1065,'Firad','Santos','32',1,'sdf@gmail.com',13,12,1),(1066,'Farash','Reyes','21',0,'sdf@gmail.com',15,5,6),(1067,'Muhamad','Jeyol','23',0,'sdf@gmail.com',21,48,1),(1068,'Hamady','Mako','25',1,'sdf@gmail.com',15,48,1),(1069,'Almaty','Hambi','16',0,'sdf@gmail.com',27,48,6),(1070,'Gaza','Teta','14',1,'sdf@gmail.com',28,48,1),(1071,'Federico','Miguel','12',0,'sdf@gmail.com',12,5,1),(1072,'Tambuch','Gabriel','26',0,'sdf@gmail.com',13,12,3),(1073,'Mark','Gambol','24',1,'sdf@gmail.com',16,5,1),(1074,'James','Gasol','27',0,'sdf@gmail.com',14,12,1),(1075,'Eman','Gumbol','28',1,'sdf@gmail.com',15,48,6),(1076,'Ian','Mirafi','21',0,'sdf@gmail.com',15,48,1),(1077,'Brian','Mirafuent','21',0,'sdf@gmail.com',11,12,1),(1078,'Lemuel','Ocasio','15',0,'sdf@gmail.com',12,5,7),(1079,'Gadaf','Cortez','16',1,'sdf@gmail.com',13,12,1),(1080,'Shardambol','Mahad','17',0,'sdf@gmail.com',14,12,1),(1081,'Josie','Mahalip','19',1,'sdf@gmail.com',15,5,1),(1082,'Jamie','Chua','20',1,'sdf@gmail.com',17,12,7),(1083,'Mark','Omar','21',0,'sdf@gmail.com',16,12,1),(1084,'Garp','tan','22',1,'sdf@gmail.com',18,48,7),(1085,'Monke','Pe','23',0,'sdf@gmail.com',19,12,1),(1086,'Akke','Te','24',1,'sdf@gmail.com',20,48,6),(1087,'Genit','Ten','25',0,'sdf@gmail.com',21,5,3),(1088,'larabab','Hua','28',0,'sdf@gmail.com',15,12,1),(1089,'Austin','Smoth','28',1,'sdf@gmail.com',26,12,1),(1090,'Texas','Jones','27',0,'sdf@gmail.com',29,12,1),(1091,'Kara','Moris','28',1,'sdf@gmail.com',25,48,1),(1092,'Karol','Rogers','15',0,'sdf@gmail.com',23,48,8),(1093,'Karl','Price','16',1,'sdf@gmail.com',28,12,7),(1094,'Kambing','Bennet','17',0,'sdf@gmail.com',31,12,7),(1095,'Camry','Cook','18',1,'sdf@gmail.com',23,48,1),(1096,'Cardu','Morgan','18',1,'sdf@gmail.com',24,48,5),(1097,'Land',' Cooper','19',0,'sdf@gmail.com',27,12,4),(1098,'Labo','Rogder','20',0,'sdf@gmail.com',29,12,5),(1099,'Lavash','Cox','21',0,'sdf@gmail.com',15,48,5),(1100,'Sanya','Ward','21',1,'sdf@gmail.com',17,12,1),(1101,'Sanay','Hua','20',1,'sdf@gmail.com',28,12,1),(1102,'Gupta','Mitche','21',0,'sdf@gmail.com',27,48,1),(1103,'Arat','Carer','20',1,'sdf@gmail.com',23,12,1),(1104,'Merili','Zhang','15',1,'sdf@gmail.com',17,48,2),(1105,'Gamal','Ling','8',0,'sdf@gmail.com',15,12,5),(1106,'Meryl','Zao','14',1,'sdf@gmail.com',12,48,1),(1107,'Maria','Chan','10',1,'sdf@gmail.com',23,24,1),(1108,'Mathilda','Chen','12',0,'sdf@gmail.com',21,48,5),(1109,'Marila','Yang','12',1,'sdf@gmail.com',23,12,1),(1110,'Marell','Zhu','13',0,'sdf@gmail.com',21,48,1),(1111,'Pharel','Zwang','13',1,'sdf@gmail.com',18,49,1),(1112,'Gamel','Mao','14',1,'sdf@gmail.com',17,12,1),(1113,'Gilgamesh','Ma','16',0,'sdf@gmail.com',16,48,5),(1114,'Franswa','Zeit','17',1,'sdf@gmail.com',14,24,1),(1115,'Far','San','12',1,'sdf@gmail.com',12,24,1),(1116,'Faruk','See','23',1,'sdf@gmail.com',15,12,5),(1117,'Farud','Li','28',0,'sdf@gmail.com',15,24,1),(1118,'Farid','Cheung','28',0,'sdf@gmail.com',15,24,4),(1119,'Fama','Tong','28',0,'sdf@gmail.com',15,48,1),(1120,'Larad','Chong','28',0,'sdf@gmail.com',15,12,1),(1121,'Lar','Vong','28',0,'sdf@gmail.com',15,48,1),(1122,'Larav','FOng','28',0,'sdf@gmail.com',15,12,5),(1123,'Pporn','Huang','28',0,'sdf@gmail.com',15,48,1),(1124,'Sako','Wong','28',0,'sdf@gmail.com',15,12,1),(1125,'Koron','Yong','28',0,'sdf@gmail.com',15,24,7),(1126,'larabab','Lau','28',0,'sdf@gmail.com',15,12,1),(1127,'Jupiter','Lao','28',0,'sdf@gmail.com',15,24,1),(1128,'Jups','Tong','28',0,'sdf@gmail.com',15,12,4),(1129,'Pyuter','Sun','28',0,'sdf@gmail.com',15,48,1),(1130,'Pweder','Xung','28',0,'sdf@gmail.com',15,48,3),(1131,'Schmi','Wukong','28',0,'sdf@gmail.com',15,12,5),(1132,'Garrosh','Chiu','28',0,'sdf@gmail.com',15,64,4),(1133,'Garom','CHu','28',0,'sdf@gmail.com',15,37,1),(1134,'Gagari','Be','28',0,'sdf@gmail.com',15,64,3),(1135,'Alein','Mar','28',0,'sdf@gmail.com',15,47,1),(1136,'Yuri','Chew','28',0,'sdf@gmail.com',15,12,2),(1137,'Lynet','Theu','28',0,'sdf@gmail.com',15,55,1),(1138,'Ament','Guo','28',0,'sdf@gmail.com',15,12,6),(1139,'Mary','Oh','28',0,'sdf@gmail.com',15,12,1),(1140,'Mary','Gaw','28',0,'sdf@gmail.com',21,48,4),(1141,'Mary','Tongwa','28',0,'sdf@gmail.com',19,48,1),(1142,'Lina Mae','Song','28',0,'sdf@gmail.com',18,47,1),(1143,'Maagaro','Harams','900',0,'suraba@gmail.com',18,25,10),(1144,'Mark','Nark','123',0,'M@gmail.c0m',21,1,4),(1145,'Markerin-Dog','Makar','0909',0,'l@gmail.com',19,10,4),(1146,'Shheen','Haren','09',1,'ad@gmail.com',12,10,4),(1147,'JudeS','Chongf','12',0,'shobe@gmail.com',15,8,4),(1148,'John','Cruz','',0,'john__12@yahoo.com',20,48,0),(1149,'Alica','Catrina','09209233048',1,'alyckingdom@gmail.com',19,48,0),(1150,'Kiana','Alexander','09193428192',1,'kiana.alexander@gmail.com',23,48,0),(1151,'Kiana','Alexander','09193428192',1,'kiana.alexander@gmail.com',23,48,0),(1152,'Miggy','Mendoza','09192412312',0,'miggy_r_mendoza@gmail.com',25,24,0),(1153,'Claire','Frank','0912341852',1,'claire_frank@uk.com',27,41,0),(1154,'Frank','Seinoma','091231211',0,'frank12@gmail.com',33,48,0);
/*!40000 ALTER TABLE `players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room`
--

DROP TABLE IF EXISTS `room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `room` (
  `room_id` int(11) NOT NULL AUTO_INCREMENT,
  `room_name` varchar(45) DEFAULT NULL,
  `branch_id` int(11) NOT NULL,
  `header_img` varchar(100) DEFAULT NULL,
  `blueprint_file` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`room_id`,`branch_id`),
  KEY `fk_room_branch1_idx` (`branch_id`),
  CONSTRAINT `fk_room_branch1` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`branch_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room`
--

LOCK TABLES `room` WRITE;
/*!40000 ALTER TABLE `room` DISABLE KEYS */;
INSERT INTO `room` VALUES (2,'OLD Alien Azsult Room',4,'imgs/treant_splash-590x334.jpg','imgs/Alien_Assault.png'),(3,'Debbys Doll',4,'imgs/dbdoll.jpg','imgs/Rebeccas_Haunting.png'),(4,'Patrick\'s Rock',4,'imgs/ROCK.png','imgs/Patrick\'s_Rock.png'),(8,'Pirates Dungeon',2,'imgs/dead_pirate.jpeg','imgs/Pirates_Dungeon_Room.png'),(9,'Aztec Escape',4,'imgs/download_Bzgm7CJ.jpeg','imgs/Aztec_Escape_Room.png'),(10,'Dark Forrest',2,'imgs/imgages_3.jpeg','imgs/images_1.jpeg'),(11,'Alien Assault CCM',4,'imgs/download.jpeg','imgs/Alien_Assault_CCM_New.png');
/*!40000 ALTER TABLE `room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rpi`
--

DROP TABLE IF EXISTS `rpi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rpi` (
  `rpi_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `room_id` int(11) NOT NULL,
  PRIMARY KEY (`rpi_id`,`room_id`),
  KEY `fk_rpi_room1_idx` (`room_id`),
  CONSTRAINT `fk_rpi_room1` FOREIGN KEY (`room_id`) REFERENCES `room` (`room_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rpi`
--

LOCK TABLES `rpi` WRITE;
/*!40000 ALTER TABLE `rpi` DISABLE KEYS */;
INSERT INTO `rpi` VALUES (1,'Door Controller','192.168.1.3',2),(2,'Digbick Cntrller','192.169.2.2',2),(3,'Pineapple Controllers','192.168.2.2',9),(4,'Aztec Escape RPI','192.168.1.2',9),(5,'Pirate Dungeon RPI','192.168.1.1',8),(6,'Patricks Rock RPI','192.168.1.2',4),(7,'Rebeccas Room RPI','192.169.1.2',3),(8,'Das','123.123.123.123',10),(9,'Alien Assault Master RPI','192.168.8.203',11);
/*!40000 ALTER TABLE `rpi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor`
--

DROP TABLE IF EXISTS `sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sensor` (
  `sensor_id` int(11) NOT NULL AUTO_INCREMENT,
  `sensor_name` varchar(45) DEFAULT NULL,
  `rpi_id` int(11) NOT NULL,
  `sensor_type_id` int(11) NOT NULL,
  `sequence_number` int(20) DEFAULT NULL,
  `top_coordinate` float DEFAULT NULL,
  `left_coordinate` float DEFAULT NULL,
  `phase_name` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`sensor_id`,`rpi_id`,`sensor_type_id`),
  KEY `fk_sensor_rpi1_idx` (`rpi_id`),
  KEY `fk_sensor_sensor_type1_idx` (`sensor_type_id`),
  CONSTRAINT `fk_sensor_rpi1` FOREIGN KEY (`rpi_id`) REFERENCES `rpi` (`rpi_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_sensor_sensor_type1` FOREIGN KEY (`sensor_type_id`) REFERENCES `sensor_type` (`sensor_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor`
--

LOCK TABLES `sensor` WRITE;
/*!40000 ALTER TABLE `sensor` DISABLE KEYS */;
INSERT INTO `sensor` VALUES (1,'Control Panel Sensor',1,1,1,66,93,'Cube Board Assembly'),(2,'Assembly Board Pin',1,1,2,3,75,'Galactice Decipher'),(3,'Ball Maze Sensor',1,1,3,48,20,'Ball Maze Phase'),(4,'Alien Head Sensor',1,2,4,4,16,'Translator Gear'),(5,'Pedestal Collision Sensor',3,3,1,63,66,'Altar Code'),(6,'Dial Ground Pin',3,4,2,13,46,'Dial Configuration'),(7,'Book Sequence Sensor',4,3,3,19,8,'Sequence Books'),(8,'Chest Sensor',4,1,4,85,13,'Unlock Secret Book'),(9,'Shamans Orb',4,3,5,28,83,'Unlocking Secret Room'),(10,'Worn Brick Sensor',5,3,1,70,2,'Find Hidden Brick'),(11,'Painting Sensor',5,4,2,65,89,'Decode Mysterious Painting'),(12,'Light Stand Sensor',5,3,3,39,73,'Activate Light Stand'),(13,'Unlock Tome',5,4,4,7,6,'Unlocking Pirates Tome'),(14,'Orifice Sensor',5,4,5,24,36,'Invoking Entity'),(15,'Pirates Chest Sensor',5,4,6,2,92,'Devils Key'),(16,'Keyhole Sensor',6,4,1,72,83,'Underfloor Keyhole'),(17,'Rock Chest Sensor',6,4,2,49,83,'Unlock Hard Chest'),(18,'Phone Dial Sensor',6,4,3,51,6,'Phone Code Dial'),(19,'Test Tube Sensor',6,4,4,9,85,'Test Tube Arrangement'),(20,'Haunted Chest Sensor',7,4,1,65,87,'Unlock Revelation'),(21,'Lever Sensor',7,4,2,4,43,'Pull Lever'),(22,'Room Light Switch Sensor',7,4,3,71,30,'Switch Combination'),(23,'Hidden Key Sensor',7,4,4,0,30,'Hidden Key'),(24,'Ace Sensoe ',8,4,2,85,9,'dfg'),(25,'Cggguh',8,4,1,8,86,'a'),(26,'Power Supply Panel',9,4,1,68,94,'Ship Activation'),(27,'Dial Discs Panel',9,1,2,84,44,'Decoding Message'),(28,'Maze Map Sensor',9,4,3,0,70,'Galatic Maze Map'),(29,'Translator Sensor',9,4,4,3,15,'Chair Translator');
/*!40000 ALTER TABLE `sensor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_type`
--

DROP TABLE IF EXISTS `sensor_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sensor_type` (
  `sensor_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `sensor_type_name` varchar(45) DEFAULT NULL,
  `val_name` varchar(45) DEFAULT NULL,
  `trigger_treshold` int(11) DEFAULT NULL,
  PRIMARY KEY (`sensor_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_type`
--

LOCK TABLES `sensor_type` WRITE;
/*!40000 ALTER TABLE `sensor_type` DISABLE KEYS */;
INSERT INTO `sensor_type` VALUES (1,'Magnetic Switch','status',1),(2,'Photo Sensor','Light Value',1),(3,'Grounded Pin','ground signal',1),(4,'Collision Sensor','Collide Value',1);
/*!40000 ALTER TABLE `sensor_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teams`
--

DROP TABLE IF EXISTS `teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teams` (
  `game_id` int(11) NOT NULL,
  `players_players_id` int(11) NOT NULL,
  `team_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`team_id`),
  KEY `fk_game_id1_idx` (`game_id`),
  KEY `fk_players_id1_idx` (`players_players_id`),
  CONSTRAINT `fk_game_id1` FOREIGN KEY (`game_id`) REFERENCES `game` (`game_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_players_id1` FOREIGN KEY (`players_players_id`) REFERENCES `players` (`players_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1236 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams`
--

LOCK TABLES `teams` WRITE;
/*!40000 ALTER TABLE `teams` DISABLE KEYS */;
INSERT INTO `teams` VALUES (253,9,1045),(254,10,1046),(254,11,1047),(254,12,1048),(254,13,1049),(255,14,1050),(255,15,1051),(255,16,1052),(256,17,1067),(256,18,1068),(257,19,1069),(257,20,1070),(258,21,1071),(258,22,1072),(258,23,1073),(259,24,1074),(259,25,1075),(260,26,1076),(260,27,1077),(261,28,1078),(261,29,1079),(262,1050,1080),(262,1051,1081),(264,1054,1084),(264,1055,1085),(266,1057,1087),(266,1058,1088),(266,1059,1089),(267,1060,1090),(267,1061,1091),(268,1062,1092),(268,1063,1093),(268,1064,1094),(269,1065,1095),(269,1066,1096),(270,1067,1097),(270,1068,1098),(271,1070,1099),(270,1069,1100),(271,1071,1101),(272,1072,1102),(272,1073,1103),(273,1074,1104),(273,1075,1105),(275,1077,1107),(275,1078,1108),(276,1079,1109),(276,1080,1110),(276,1081,1111),(277,1082,1112),(277,1083,1113),(277,1084,1114),(277,1085,1115),(278,1089,1170),(278,1090,1171),(279,1091,1172),(279,1092,1173),(279,1093,1174),(279,1094,1175),(280,1095,1176),(280,1096,1177),(280,1097,1178),(281,1098,1179),(281,1099,1180),(281,1100,1181),(281,1101,1182),(281,1102,1183),(282,1103,1184),(282,1104,1185),(282,1105,1186),(282,1106,1187),(282,1107,1188),(282,1108,1189),(283,1109,1190),(283,1110,1191),(283,1111,1192),(283,1112,1193),(284,1113,1194),(284,1114,1195),(284,1115,1196),(284,1116,1197),(284,1117,1198),(285,1118,1199),(285,1119,1200),(285,1120,1201),(285,1121,1202),(285,1122,1203),(286,1123,1204),(286,1124,1205),(286,1125,1206),(286,1126,1207),(287,1127,1208),(287,1128,1209),(287,1129,1210),(287,1130,1211),(287,1131,1212),(288,1132,1213),(288,1133,1214),(288,1134,1215),(288,1135,1216),(288,1136,1217),(289,1137,1218),(289,1138,1219),(289,1139,1220),(289,1140,1221),(289,1141,1222),(289,1142,1223),(291,1144,1225),(292,1145,1226),(292,1146,1227),(293,1147,1228),(294,1148,1229),(294,1149,1230),(295,1150,1231),(296,1151,1232),(296,1152,1233),(297,1153,1234),(297,1154,1235);
/*!40000 ALTER TABLE `teams` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-03-08 15:10:24
