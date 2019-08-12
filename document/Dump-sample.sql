-- MySQL dump 10.13  Distrib 5.7.23, for Win64 (x86_64)
--
-- Host: localhost    Database: morphology_central_db
-- ------------------------------------------------------
-- Server version	5.7.23-log

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
use three_eat_person;
--
-- Table structure for table `companies`
--

DROP TABLE IF EXISTS `companies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `companies` (
  `id` varchar(64) NOT NULL,
  `deleted` varchar(64) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `name` varchar(64) NOT NULL,
  `leader` varchar(64) NOT NULL,
  `comment` varchar(64) DEFAULT NULL,
  `seller` varchar(64) NOT NULL,
  `password` varchar(512) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  KEY `leader_user_ref_idx` (`leader`),
  KEY `seller_user_ref_idx` (`seller`),
  CONSTRAINT `leader_user_ref` FOREIGN KEY (`leader`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `seller_user_ref` FOREIGN KEY (`seller`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `companies`
--

LOCK TABLES `companies` WRITE;
/*!40000 ALTER TABLE `companies` DISABLE KEYS */;
INSERT INTO `companies` VALUES ('2e0945805fcc4c8586a94a8a008f35f6',NULL,'2019-04-29 07:10:58','333','6bf4f0f9a6d44d2c8d8dc8ed0340d955','222','7450896bb23b4f118040843882dc73a5',''),('748e8b5e70954983aa49af3b115537a4','cc1ee9b8-c87b-4b4b-8b5a-106e88399375','2019-04-26 05:08:04','天坛','44cfefc1518e4dcf85184d76732f13f5','北京的','7450896bb23b4f118040843882dc73a5','tiantanyiyuan'),('98798c54a91740699c5ff590173fc114',NULL,'2019-04-26 02:27:57','天津','44cfefc1518e4dcf85184d76732f13f5','天津的','7450896bb23b4f118040843882dc73a5','[71838869696144607006389306916760943140843982759906038041077318458107050801623, 65537, 9716339487413610578827758617424798194807115075096471102288562615439425395969, 79801351866695237529614425577694014032859, 900221211993355474002071742727407797]'),('b7263c2c1666448780435d2bd15fc307',NULL,'2019-04-29 03:15:52','南京','68d5ad8a874f432ca6d9eec6458eddd6','得到的','8b261682158a45fc8d59c380cc866d50',''),('c1d5c4adf2ec436babc9c9061821fe60',NULL,'2019-04-29 02:03:42','西青','6bf4f0f9a6d44d2c8d8dc8ed0340d955','西青的','7450896bb23b4f118040843882dc73a5','[69475396122037029485195434853390936650616226120944288357479834208961284491021, 65537, 11711921149217466496062364225708577864796954435650456922103008794361390242049, 53475353885650782069978467500289252158889, 1299204045860079693176325248568149189]');
/*!40000 ALTER TABLE `companies` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `id` varchar(64) NOT NULL,
  `deleted` varchar(64) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `name` varchar(45) NOT NULL,
  `code` varchar(32) NOT NULL,
  `level` int(11) NOT NULL DEFAULT '100',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `code_UNIQUE` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES ('0250a0ec4c25407d98a9cdbee7a89d49','241ed59d-bb39-4fb5-8032-c8112a28d05a','2019-04-25 02:08:17','22222','222222',33),('148973e55a094efe8f56599e271e76b3',NULL,'2019-04-25 02:07:57','销售经理','manager',1),('6850ef866c8848968c880689b3e5dee7',NULL,'2019-04-25 08:32:24','员工','employee',2),('7b0628726e6e4c7988e613123697f9dd','65b97f3f-a2cf-4c97-aa80-2ef1ba7bc892','2019-04-25 08:37:05','test','test3',22),('8ccc22fd4a9d4ccd8c3fa3e22e4ee0b7',NULL,'2019-04-25 08:33:59','客户员工','custom_employeer',4),('a7885449932f4e3db736e852a722e1f4',NULL,'2019-04-24 06:22:39','管理员','admin',0),('a91e49a1a3dd4df69c3a8e8eb4cf0d78',NULL,'2019-04-25 08:33:20','客户领导','custom_leader',3);
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` varchar(64) NOT NULL,
  `deleted` varchar(64) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `username` varchar(32) NOT NULL,
  `password` varchar(128) DEFAULT NULL,
  `email` varchar(64) NOT NULL,
  `phone` varchar(16) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `company` varchar(64) DEFAULT NULL,
  `role` varchar(64) NOT NULL,
  `is_valid` tinyint(4) NOT NULL DEFAULT '0',
  `is_login` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`),
  UNIQUE KEY `phone_UNIQUE` (`phone`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  KEY `role_rols_ref_idx` (`role`),
  KEY `company_user_ref_idx` (`company`),
  CONSTRAINT `role_rols_ref` FOREIGN KEY (`role`) REFERENCES `roles` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('43fe3ccd5e774709ae97e6757e994af7',NULL,'2019-04-25 07:07:17','2019-04-30 01:36:44','xxp234','pbkdf2:sha256:50000$tqhuRxAO$831dea41650e03bcfcc32a5be9e2a0f4dc6f7f0bdce55f98348e5ae4795818e9','heidong@deepcyto.cn','15622336655','黑洞','','a7885449932f4e3db736e852a722e1f4',1,0),('44cfefc1518e4dcf85184d76732f13f5',NULL,'2019-04-26 02:06:24','2019-04-29 03:05:17','custom_leader_test1','pbkdf2:sha256:50000$FV7aukGa$81a42cb003326197a80745f41a002daa9ee72bea26c21be642c4475de6351aed','leadertest@126.com','15525539999','客户测试1','98798c54a91740699c5ff590173fc114','a91e49a1a3dd4df69c3a8e8eb4cf0d78',1,0),('689ef062856c4d64b7d718d37cbb7127','340b285f-27ed-4c8e-ad14-caad0c5092ef','2019-04-26 06:52:18','2019-04-30 02:13:02','wwwwww','pbkdf2:sha256:50000$BLbFocsx$4dc3d9cad62d5a3273d1ad6bd43f41d1acb981dbe3908e28ad117333806fbb27','wwwwwwww','wwwwwwwww','wwwwwwwww','98798c54a91740699c5ff590173fc114','8ccc22fd4a9d4ccd8c3fa3e22e4ee0b7',1,0),('68d5ad8a874f432ca6d9eec6458eddd6',NULL,'2019-04-29 03:07:52','2019-05-05 08:21:17','nj','pbkdf2:sha256:50000$bIs0jrAH$0004b4368388f2fb590adcb563905efb5210431c13a51a9414156f90664698d5','ddddccdv','dsedsds','南京','b7263c2c1666448780435d2bd15fc307','a91e49a1a3dd4df69c3a8e8eb4cf0d78',1,0),('6bf4f0f9a6d44d2c8d8dc8ed0340d955',NULL,'2019-04-29 02:02:06','2019-04-29 07:10:58','xqyy','pbkdf2:sha256:50000$qxp7SMn8$b81e2883f8ac1440f2fece848488a00163a085853cee9ee4517930d3e65ae910','xiqing@xingqing.com','12532563','西青医院','2e0945805fcc4c8586a94a8a008f35f6','a91e49a1a3dd4df69c3a8e8eb4cf0d78',1,0),('7450896bb23b4f118040843882dc73a5',NULL,'2019-04-25 08:28:08','2019-04-26 03:50:44','xxp4','pbkdf2:sha256:50000$W1Ryv0ba$43d39c1e678eb4f1513fdb9c774d27f3178eff3d76e26dec55be835250216397','ceshi4@deepcyto.cn','15598658898','测试4',NULL,'6850ef866c8848968c880689b3e5dee7',1,1),('748935051d7b4027b59312a9d83c5ddb',NULL,'2019-04-24 06:25:20','2019-04-25 06:44:10','admin','pbkdf2:sha256:50000$Rkwdf1zS$28f2f336ef0b89a315b77b1fffa846092f45d5f5e48ac5178001862bc8270cf8','admin@deepcyto.cn','15900000000','初始管理员',NULL,'a7885449932f4e3db736e852a722e1f4',1,1),('8b261682158a45fc8d59c380cc866d50',NULL,'2019-04-25 07:11:41','2019-04-26 03:50:28','xxp5','pbkdf2:sha256:50000$tL5a2kql$4c79549da34a4881aed9fdada1bf8a89650be484a25060ec03fd15859893d28c','ceshi5@deepcyto.cn','15332002556','经理测试5',NULL,'148973e55a094efe8f56599e271e76b3',1,0),('bbe1eea4e3324117b6f29d8fee853725','752b978d-1514-4529-b1aa-d48b27eb373e','2019-04-25 08:29:52','2019-04-29 01:59:40','asdad','pbkdf2:sha256:50000$JxDgFmzJ$79bac52378caea7de8aac18a72ecd87c4ce6837e5f3b617ce337ae06f54b25a1','asda','asda','asda','98798c54a91740699c5ff590173fc114','148973e55a094efe8f56599e271e76b3',1,0),('d239266e158643d3a9a1d907b34103a6',NULL,'2019-05-05 08:21:42','2019-05-05 08:21:42','wdsldk','pbkdf2:sha256:50000$FzCIT0rw$ecbb10bda7c031fc66da177f1ab15f3b8ca0ae2241bbc1845e1c2740abfe0928','dfgdgd','dfgdg','dfgdgd',NULL,'6850ef866c8848968c880689b3e5dee7',0,0),('ebe2f127dd1c4155ab076d6ea7b857ee','bdaad7aa-e05b-4639-9370-8312e21b4eb4','2019-04-25 08:13:30','2019-04-26 05:59:43','22223','pbkdf2:sha256:50000$b8vexYcG$2241333bcafbb46746845fffbd36d0a3efdf1f16141a1e1632d8a43188c77373','123131','1313','1231','98798c54a91740699c5ff590173fc114','a7885449932f4e3db736e852a722e1f4',1,0),('f42c5a0b73784338b4ba6514d3cb3084','87851359-0d97-4a74-8743-92524a6bfee0','2019-04-24 06:40:48','2019-04-24 07:35:23','string','pbkdf2:sha256:50000$Fcz1T1Nh$d87e488ad15d6c14d466612a031fa1f5d4c41aa733a592387f98a1906666ca24','string','string','string2',NULL,'a7885449932f4e3db736e852a722e1f4',1,1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-05-06 12:49:50
