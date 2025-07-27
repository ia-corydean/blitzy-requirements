/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.2-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: claude_db
-- ------------------------------------------------------
-- Server version	11.8.2-MariaDB-ubu2404

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `action`
--

DROP TABLE IF EXISTS `action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `action` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `action_type_id` int(11) NOT NULL COMMENT 'Reference to action_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_action_type` (`action_type_id`),
  KEY `idx_action_status` (`status_id`),
  KEY `idx_action_created` (`created_at`),
  CONSTRAINT `fk_action_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_action_type` FOREIGN KEY (`action_type_id`) REFERENCES `action_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Action management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `action`
--

LOCK TABLES `action` WRITE;
/*!40000 ALTER TABLE `action` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `action` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `action_type`
--

DROP TABLE IF EXISTS `action_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `action_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_action_type_code` (`code`),
  KEY `idx_action_type_status` (`status_id`),
  CONSTRAINT `fk_action_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Action type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `action_type`
--

LOCK TABLES `action_type` WRITE;
/*!40000 ALTER TABLE `action_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `action_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `address`
--

DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `address` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `address_type_id` int(11) NOT NULL COMMENT 'Reference to address_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  `county_id` int(11) DEFAULT NULL COMMENT 'Reference to county table',
  `country_id` int(11) DEFAULT 1 COMMENT 'Reference to country table',
  `is_validated` tinyint(1) DEFAULT 0 COMMENT 'Address validation status',
  `validation_date` timestamp NULL DEFAULT NULL COMMENT 'When address was validated',
  `latitude` decimal(10,8) DEFAULT NULL COMMENT 'GPS latitude',
  `longitude` decimal(11,8) DEFAULT NULL COMMENT 'GPS longitude',
  PRIMARY KEY (`id`),
  KEY `idx_address_type` (`address_type_id`),
  KEY `idx_address_status` (`status_id`),
  KEY `idx_address_created` (`created_at`),
  KEY `idx_address_county` (`county_id`),
  CONSTRAINT `fk_address_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_address_type` FOREIGN KEY (`address_type_id`) REFERENCES `address_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Address management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address`
--

LOCK TABLES `address` WRITE;
/*!40000 ALTER TABLE `address` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `address` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `address_type`
--

DROP TABLE IF EXISTS `address_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `address_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_address_type_code` (`code`),
  KEY `idx_address_type_status` (`status_id`),
  CONSTRAINT `fk_address_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Address type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address_type`
--

LOCK TABLES `address_type` WRITE;
/*!40000 ALTER TABLE `address_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `address_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `alert`
--

DROP TABLE IF EXISTS `alert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `alert` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `alert_type_id` int(11) NOT NULL COMMENT 'Reference to alert_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  `user_id` int(11) DEFAULT NULL COMMENT 'User who receives alert',
  `title` varchar(255) DEFAULT NULL COMMENT 'Alert title',
  `message` text DEFAULT NULL COMMENT 'Alert message body',
  PRIMARY KEY (`id`),
  KEY `idx_alert_type` (`alert_type_id`),
  KEY `idx_alert_status` (`status_id`),
  KEY `idx_alert_created` (`created_at`),
  KEY `idx_alert_user_status` (`user_id`,`status_id`),
  CONSTRAINT `fk_alert_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_alert_type` FOREIGN KEY (`alert_type_id`) REFERENCES `alert_type` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_alert_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Alert management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alert`
--

LOCK TABLES `alert` WRITE;
/*!40000 ALTER TABLE `alert` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `alert` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `alert_type`
--

DROP TABLE IF EXISTS `alert_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `alert_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  `category` varchar(50) DEFAULT NULL COMMENT 'Alert category: license, document, payment, task',
  `priority` int(11) DEFAULT 0 COMMENT 'Higher number = higher priority',
  `auto_resolve` tinyint(1) DEFAULT 0 COMMENT 'Can alert auto-resolve',
  `resolution_route` varchar(255) DEFAULT NULL COMMENT 'Route to resolve the alert',
  `display_order` int(11) DEFAULT 0 COMMENT 'Display ordering',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_alert_type_code` (`code`),
  KEY `idx_alert_type_status` (`status_id`),
  KEY `idx_alert_type_category` (`category`),
  CONSTRAINT `fk_alert_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Alert type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alert_type`
--

LOCK TABLES `alert_type` WRITE;
/*!40000 ALTER TABLE `alert_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `alert_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `audit`
--

DROP TABLE IF EXISTS `audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `audit_type_id` int(11) NOT NULL COMMENT 'Reference to audit_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_audit_type` (`audit_type_id`),
  KEY `idx_audit_status` (`status_id`),
  KEY `idx_audit_created` (`created_at`),
  CONSTRAINT `fk_audit_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_audit_type` FOREIGN KEY (`audit_type_id`) REFERENCES `audit_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Audit trail management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit`
--

LOCK TABLES `audit` WRITE;
/*!40000 ALTER TABLE `audit` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `audit` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `audit_type`
--

DROP TABLE IF EXISTS `audit_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_audit_type_code` (`code`),
  KEY `idx_audit_type_status` (`status_id`),
  CONSTRAINT `fk_audit_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Audit type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_type`
--

LOCK TABLES `audit_type` WRITE;
/*!40000 ALTER TABLE `audit_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `audit_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `calculation`
--

DROP TABLE IF EXISTS `calculation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `calculation` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `calculation_type_id` int(11) NOT NULL COMMENT 'Reference to calculation_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_calculation_type` (`calculation_type_id`),
  KEY `idx_calculation_status` (`status_id`),
  KEY `idx_calculation_created` (`created_at`),
  CONSTRAINT `fk_calculation_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_calculation_type` FOREIGN KEY (`calculation_type_id`) REFERENCES `calculation_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Calculation management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calculation`
--

LOCK TABLES `calculation` WRITE;
/*!40000 ALTER TABLE `calculation` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `calculation` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `calculation_type`
--

DROP TABLE IF EXISTS `calculation_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `calculation_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_calculation_type_code` (`code`),
  KEY `idx_calculation_type_status` (`status_id`),
  CONSTRAINT `fk_calculation_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Calculation type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calculation_type`
--

LOCK TABLES `calculation_type` WRITE;
/*!40000 ALTER TABLE `calculation_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `calculation_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `cancellation`
--

DROP TABLE IF EXISTS `cancellation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `cancellation` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `cancellation_type_id` int(11) NOT NULL COMMENT 'Reference to cancellation_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_cancellation_type` (`cancellation_type_id`),
  KEY `idx_cancellation_status` (`status_id`),
  KEY `idx_cancellation_created` (`created_at`),
  CONSTRAINT `fk_cancellation_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_cancellation_type` FOREIGN KEY (`cancellation_type_id`) REFERENCES `cancellation_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Cancellation management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cancellation`
--

LOCK TABLES `cancellation` WRITE;
/*!40000 ALTER TABLE `cancellation` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `cancellation` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `cancellation_reason`
--

DROP TABLE IF EXISTS `cancellation_reason`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `cancellation_reason` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Reason code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Reason description',
  `category` varchar(50) DEFAULT NULL COMMENT 'Reason category',
  `requires_documentation` tinyint(1) DEFAULT 0 COMMENT 'Needs documentation',
  `display_order` int(11) DEFAULT 0 COMMENT 'Display sequence',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default reason',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_cancel_reason_code` (`code`),
  KEY `idx_cancel_reason_category` (`category`),
  KEY `fk_cancel_reason_status` (`status_id`),
  KEY `fk_cancel_reason_created_by` (`created_by`),
  KEY `fk_cancel_reason_updated_by` (`updated_by`),
  CONSTRAINT `fk_cancel_reason_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_cancel_reason_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_cancel_reason_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Cancellation reason codes';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cancellation_reason`
--

LOCK TABLES `cancellation_reason` WRITE;
/*!40000 ALTER TABLE `cancellation_reason` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `cancellation_reason` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `cancellation_type`
--

DROP TABLE IF EXISTS `cancellation_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `cancellation_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_cancellation_type_code` (`code`),
  KEY `idx_cancellation_type_status` (`status_id`),
  CONSTRAINT `fk_cancellation_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Cancellation type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cancellation_type`
--

LOCK TABLES `cancellation_type` WRITE;
/*!40000 ALTER TABLE `cancellation_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `cancellation_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `city` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `name` varchar(100) NOT NULL COMMENT 'City name',
  `state_id` int(11) NOT NULL COMMENT 'Reference to state',
  `county_id` int(11) DEFAULT NULL COMMENT 'Reference to county',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_city_state` (`state_id`),
  KEY `idx_city_county` (`county_id`),
  CONSTRAINT `fk_city_county` FOREIGN KEY (`county_id`) REFERENCES `county` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_city_state` FOREIGN KEY (`state_id`) REFERENCES `state` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='City reference table';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city`
--

LOCK TABLES `city` WRITE;
/*!40000 ALTER TABLE `city` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `city` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `claimant`
--

DROP TABLE IF EXISTS `claimant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `claimant` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `claimant_type_id` int(11) NOT NULL COMMENT 'Reference to claimant_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_claimant_type` (`claimant_type_id`),
  KEY `idx_claimant_status` (`status_id`),
  KEY `idx_claimant_created` (`created_at`),
  CONSTRAINT `fk_claimant_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_claimant_type` FOREIGN KEY (`claimant_type_id`) REFERENCES `claimant_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Claimant management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `claimant`
--

LOCK TABLES `claimant` WRITE;
/*!40000 ALTER TABLE `claimant` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `claimant` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `claimant_type`
--

DROP TABLE IF EXISTS `claimant_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `claimant_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_claimant_type_code` (`code`),
  KEY `idx_claimant_type_status` (`status_id`),
  CONSTRAINT `fk_claimant_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Claimant type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `claimant_type`
--

LOCK TABLES `claimant_type` WRITE;
/*!40000 ALTER TABLE `claimant_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `claimant_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `commission`
--

DROP TABLE IF EXISTS `commission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `commission` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `commission_type_id` int(11) NOT NULL COMMENT 'Reference to commission_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_commission_type` (`commission_type_id`),
  KEY `idx_commission_status` (`status_id`),
  KEY `idx_commission_created` (`created_at`),
  CONSTRAINT `fk_commission_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_commission_type` FOREIGN KEY (`commission_type_id`) REFERENCES `commission_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Commission management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commission`
--

LOCK TABLES `commission` WRITE;
/*!40000 ALTER TABLE `commission` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `commission` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `commission_type`
--

DROP TABLE IF EXISTS `commission_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `commission_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_commission_type_code` (`code`),
  KEY `idx_commission_type_status` (`status_id`),
  CONSTRAINT `fk_commission_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Commission type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commission_type`
--

LOCK TABLES `commission_type` WRITE;
/*!40000 ALTER TABLE `commission_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `commission_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `communication`
--

DROP TABLE IF EXISTS `communication`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `communication` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `communication_type_id` int(11) NOT NULL COMMENT 'Reference to communication_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_communication_type` (`communication_type_id`),
  KEY `idx_communication_status` (`status_id`),
  KEY `idx_communication_created` (`created_at`),
  CONSTRAINT `fk_communication_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_communication_type` FOREIGN KEY (`communication_type_id`) REFERENCES `communication_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Communication management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `communication`
--

LOCK TABLES `communication` WRITE;
/*!40000 ALTER TABLE `communication` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `communication` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `communication_method`
--

DROP TABLE IF EXISTS `communication_method`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `communication_method` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `communication_method_type_id` int(11) NOT NULL COMMENT 'Reference to communication_method_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_communication_method_type` (`communication_method_type_id`),
  KEY `idx_communication_method_status` (`status_id`),
  KEY `idx_communication_method_created` (`created_at`),
  CONSTRAINT `fk_communication_method_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_communication_method_type` FOREIGN KEY (`communication_method_type_id`) REFERENCES `communication_method_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Communication method management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `communication_method`
--

LOCK TABLES `communication_method` WRITE;
/*!40000 ALTER TABLE `communication_method` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `communication_method` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `communication_method_type`
--

DROP TABLE IF EXISTS `communication_method_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `communication_method_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_communication_method_type_code` (`code`),
  KEY `idx_communication_method_type_status` (`status_id`),
  CONSTRAINT `fk_communication_method_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Communication method type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `communication_method_type`
--

LOCK TABLES `communication_method_type` WRITE;
/*!40000 ALTER TABLE `communication_method_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `communication_method_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `communication_type`
--

DROP TABLE IF EXISTS `communication_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `communication_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_communication_type_code` (`code`),
  KEY `idx_communication_type_status` (`status_id`),
  CONSTRAINT `fk_communication_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Communication type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `communication_type`
--

LOCK TABLES `communication_type` WRITE;
/*!40000 ALTER TABLE `communication_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `communication_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `configuration`
--

DROP TABLE IF EXISTS `configuration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `configuration` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `configuration_type_id` int(11) NOT NULL COMMENT 'Reference to configuration_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_configuration_type` (`configuration_type_id`),
  KEY `idx_configuration_status` (`status_id`),
  KEY `idx_configuration_created` (`created_at`),
  CONSTRAINT `fk_configuration_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_configuration_type` FOREIGN KEY (`configuration_type_id`) REFERENCES `configuration_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Configuration management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configuration`
--

LOCK TABLES `configuration` WRITE;
/*!40000 ALTER TABLE `configuration` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `configuration` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `configuration_type`
--

DROP TABLE IF EXISTS `configuration_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `configuration_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_configuration_type_code` (`code`),
  KEY `idx_configuration_type_status` (`status_id`),
  CONSTRAINT `fk_configuration_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Configuration type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configuration_type`
--

LOCK TABLES `configuration_type` WRITE;
/*!40000 ALTER TABLE `configuration_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `configuration_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `country`
--

DROP TABLE IF EXISTS `country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `country` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(2) NOT NULL COMMENT 'ISO country code',
  `name` varchar(100) NOT NULL COMMENT 'Country name',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_country_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Country reference table';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `country`
--

LOCK TABLES `country` WRITE;
/*!40000 ALTER TABLE `country` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `country` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `county`
--

DROP TABLE IF EXISTS `county`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `county` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `name` varchar(100) NOT NULL COMMENT 'County name',
  `state_id` int(11) NOT NULL COMMENT 'Reference to state',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_county_state` (`state_id`),
  CONSTRAINT `fk_county_state` FOREIGN KEY (`state_id`) REFERENCES `state` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='County reference table';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `county`
--

LOCK TABLES `county` WRITE;
/*!40000 ALTER TABLE `county` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `county` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `coverage`
--

DROP TABLE IF EXISTS `coverage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `coverage` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `coverage_type_id` int(11) NOT NULL COMMENT 'Reference to coverage_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  `limit_id` int(11) DEFAULT NULL COMMENT 'Reference to limit table',
  `deductible_id` int(11) DEFAULT NULL COMMENT 'Reference to deductible table',
  `premium_amount` decimal(10,2) DEFAULT NULL COMMENT 'Coverage premium',
  `is_required` tinyint(1) DEFAULT 0 COMMENT 'State required coverage',
  `is_selected` tinyint(1) DEFAULT 0 COMMENT 'Customer selected',
  PRIMARY KEY (`id`),
  KEY `idx_coverage_type` (`coverage_type_id`),
  KEY `idx_coverage_status` (`status_id`),
  KEY `idx_coverage_created` (`created_at`),
  CONSTRAINT `fk_coverage_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_coverage_type` FOREIGN KEY (`coverage_type_id`) REFERENCES `coverage_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Coverage management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coverage`
--

LOCK TABLES `coverage` WRITE;
/*!40000 ALTER TABLE `coverage` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `coverage` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `coverage_type`
--

DROP TABLE IF EXISTS `coverage_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `coverage_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_coverage_type_code` (`code`),
  KEY `idx_coverage_type_status` (`status_id`),
  CONSTRAINT `fk_coverage_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Coverage type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coverage_type`
--

LOCK TABLES `coverage_type` WRITE;
/*!40000 ALTER TABLE `coverage_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `coverage_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `deductible`
--

DROP TABLE IF EXISTS `deductible`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `deductible` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `deductible_type_id` int(11) NOT NULL COMMENT 'Reference to deductible_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_deductible_type` (`deductible_type_id`),
  KEY `idx_deductible_status` (`status_id`),
  KEY `idx_deductible_created` (`created_at`),
  CONSTRAINT `fk_deductible_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_deductible_type` FOREIGN KEY (`deductible_type_id`) REFERENCES `deductible_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Deductible management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deductible`
--

LOCK TABLES `deductible` WRITE;
/*!40000 ALTER TABLE `deductible` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `deductible` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `deductible_type`
--

DROP TABLE IF EXISTS `deductible_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `deductible_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_deductible_type_code` (`code`),
  KEY `idx_deductible_type_status` (`status_id`),
  CONSTRAINT `fk_deductible_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Deductible type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deductible_type`
--

LOCK TABLES `deductible_type` WRITE;
/*!40000 ALTER TABLE `deductible_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `deductible_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `discount`
--

DROP TABLE IF EXISTS `discount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `discount` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `discount_type_id` int(11) NOT NULL COMMENT 'Reference to discount_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_discount_type` (`discount_type_id`),
  KEY `idx_discount_status` (`status_id`),
  KEY `idx_discount_created` (`created_at`),
  CONSTRAINT `fk_discount_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_discount_type` FOREIGN KEY (`discount_type_id`) REFERENCES `discount_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Discount management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discount`
--

LOCK TABLES `discount` WRITE;
/*!40000 ALTER TABLE `discount` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `discount` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `discount_type`
--

DROP TABLE IF EXISTS `discount_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `discount_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_discount_type_code` (`code`),
  KEY `idx_discount_type_status` (`status_id`),
  CONSTRAINT `fk_discount_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Discount type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discount_type`
--

LOCK TABLES `discount_type` WRITE;
/*!40000 ALTER TABLE `discount_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `discount_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `distribution_channel`
--

DROP TABLE IF EXISTS `distribution_channel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `distribution_channel` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `distribution_channel_type_id` int(11) NOT NULL COMMENT 'Reference to type',
  `code` varchar(50) NOT NULL COMMENT 'Channel code',
  `name` varchar(100) NOT NULL COMMENT 'Channel name',
  `description` text DEFAULT NULL COMMENT 'Channel description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default channel',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_dist_channel_code` (`code`),
  KEY `idx_dist_channel_type` (`distribution_channel_type_id`),
  KEY `fk_dist_channel_status` (`status_id`),
  KEY `fk_dist_channel_created_by` (`created_by`),
  KEY `fk_dist_channel_updated_by` (`updated_by`),
  CONSTRAINT `fk_dist_channel_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_dist_channel_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_dist_channel_type` FOREIGN KEY (`distribution_channel_type_id`) REFERENCES `distribution_channel_type` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_dist_channel_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Distribution channels';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distribution_channel`
--

LOCK TABLES `distribution_channel` WRITE;
/*!40000 ALTER TABLE `distribution_channel` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `distribution_channel` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `distribution_channel_type`
--

DROP TABLE IF EXISTS `distribution_channel_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `distribution_channel_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Channel type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Channel type description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default channel type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_dist_channel_type_code` (`code`),
  KEY `fk_dist_channel_type_status` (`status_id`),
  KEY `fk_dist_channel_type_created_by` (`created_by`),
  KEY `fk_dist_channel_type_updated_by` (`updated_by`),
  CONSTRAINT `fk_dist_channel_type_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_dist_channel_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_dist_channel_type_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Distribution channel types';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distribution_channel_type`
--

LOCK TABLES `distribution_channel_type` WRITE;
/*!40000 ALTER TABLE `distribution_channel_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `distribution_channel_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `document`
--

DROP TABLE IF EXISTS `document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `document` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `document_type_id` int(11) NOT NULL COMMENT 'Reference to document_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  `file_id` int(11) DEFAULT NULL COMMENT 'Reference to file table',
  `is_signed` tinyint(1) DEFAULT 0 COMMENT 'Signature status',
  `signed_at` timestamp NULL DEFAULT NULL COMMENT 'Signature timestamp',
  `expiration_date` date DEFAULT NULL COMMENT 'Document expiration',
  PRIMARY KEY (`id`),
  KEY `idx_document_type` (`document_type_id`),
  KEY `idx_document_status` (`status_id`),
  KEY `idx_document_created` (`created_at`),
  KEY `idx_document_file` (`file_id`),
  CONSTRAINT `fk_document_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_document_type` FOREIGN KEY (`document_type_id`) REFERENCES `document_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Document management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `document`
--

LOCK TABLES `document` WRITE;
/*!40000 ALTER TABLE `document` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `document` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `document_type`
--

DROP TABLE IF EXISTS `document_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `document_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_document_type_code` (`code`),
  KEY `idx_document_type_status` (`status_id`),
  CONSTRAINT `fk_document_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Document type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `document_type`
--

LOCK TABLES `document_type` WRITE;
/*!40000 ALTER TABLE `document_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `document_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `driver`
--

DROP TABLE IF EXISTS `driver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `driver` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `driver_type_id` int(11) NOT NULL COMMENT 'Reference to driver_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  `name_id` int(11) DEFAULT NULL COMMENT 'Reference to name table',
  `license_id` int(11) DEFAULT NULL COMMENT 'Reference to license table',
  `date_of_birth` date DEFAULT NULL COMMENT 'Driver date of birth',
  `gender_id` int(11) DEFAULT NULL COMMENT 'Reference to gender',
  `marital_status_id` int(11) DEFAULT NULL COMMENT 'Reference to marital_status',
  `years_licensed` int(11) DEFAULT NULL COMMENT 'Years with license',
  `relationship_to_insured_id` int(11) DEFAULT NULL COMMENT 'Reference to relationship type',
  `is_named_insured` tinyint(1) DEFAULT 0 COMMENT 'Named insured flag',
  `violations_count` int(11) DEFAULT 0 COMMENT 'Number of violations',
  `accidents_count` int(11) DEFAULT 0 COMMENT 'Number of accidents',
  PRIMARY KEY (`id`),
  KEY `idx_driver_type` (`driver_type_id`),
  KEY `idx_driver_status` (`status_id`),
  KEY `idx_driver_created` (`created_at`),
  KEY `idx_driver_dob` (`date_of_birth`),
  KEY `fk_driver_name` (`name_id`),
  KEY `fk_driver_license` (`license_id`),
  KEY `fk_driver_gender` (`gender_id`),
  KEY `fk_driver_marital_status` (`marital_status_id`),
  CONSTRAINT `fk_driver_gender` FOREIGN KEY (`gender_id`) REFERENCES `gender` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_driver_license` FOREIGN KEY (`license_id`) REFERENCES `license` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_driver_marital_status` FOREIGN KEY (`marital_status_id`) REFERENCES `marital_status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_driver_name` FOREIGN KEY (`name_id`) REFERENCES `name` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_driver_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_driver_type` FOREIGN KEY (`driver_type_id`) REFERENCES `driver_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Driver management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `driver`
--

LOCK TABLES `driver` WRITE;
/*!40000 ALTER TABLE `driver` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `driver` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `driver_type`
--

DROP TABLE IF EXISTS `driver_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `driver_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_driver_type_code` (`code`),
  KEY `idx_driver_type_status` (`status_id`),
  CONSTRAINT `fk_driver_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Driver type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `driver_type`
--

LOCK TABLES `driver_type` WRITE;
/*!40000 ALTER TABLE `driver_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `driver_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `endorsement`
--

DROP TABLE IF EXISTS `endorsement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `endorsement` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `endorsement_type_id` int(11) NOT NULL COMMENT 'Reference to endorsement_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_endorsement_type` (`endorsement_type_id`),
  KEY `idx_endorsement_status` (`status_id`),
  KEY `idx_endorsement_created` (`created_at`),
  CONSTRAINT `fk_endorsement_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_endorsement_type` FOREIGN KEY (`endorsement_type_id`) REFERENCES `endorsement_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Endorsement management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `endorsement`
--

LOCK TABLES `endorsement` WRITE;
/*!40000 ALTER TABLE `endorsement` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `endorsement` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `endorsement_type`
--

DROP TABLE IF EXISTS `endorsement_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `endorsement_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_endorsement_type_code` (`code`),
  KEY `idx_endorsement_type_status` (`status_id`),
  CONSTRAINT `fk_endorsement_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Endorsement type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `endorsement_type`
--

LOCK TABLES `endorsement_type` WRITE;
/*!40000 ALTER TABLE `endorsement_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `endorsement_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `entity`
--

DROP TABLE IF EXISTS `entity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `entity` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `entity_type_id` int(11) NOT NULL COMMENT 'Reference to entity_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_entity_type` (`entity_type_id`),
  KEY `idx_entity_status` (`status_id`),
  KEY `idx_entity_created` (`created_at`),
  CONSTRAINT `fk_entity_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_entity_type` FOREIGN KEY (`entity_type_id`) REFERENCES `entity_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Entity management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entity`
--

LOCK TABLES `entity` WRITE;
/*!40000 ALTER TABLE `entity` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `entity` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `entity_type`
--

DROP TABLE IF EXISTS `entity_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `entity_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_entity_type_code` (`code`),
  KEY `idx_entity_type_status` (`status_id`),
  CONSTRAINT `fk_entity_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Entity type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entity_type`
--

LOCK TABLES `entity_type` WRITE;
/*!40000 ALTER TABLE `entity_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `entity_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `fee`
--

DROP TABLE IF EXISTS `fee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `fee` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `fee_type_id` int(11) NOT NULL COMMENT 'Reference to fee_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_fee_type` (`fee_type_id`),
  KEY `idx_fee_status` (`status_id`),
  KEY `idx_fee_created` (`created_at`),
  CONSTRAINT `fk_fee_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_fee_type` FOREIGN KEY (`fee_type_id`) REFERENCES `fee_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Fee management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fee`
--

LOCK TABLES `fee` WRITE;
/*!40000 ALTER TABLE `fee` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `fee` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `fee_type`
--

DROP TABLE IF EXISTS `fee_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `fee_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_fee_type_code` (`code`),
  KEY `idx_fee_type_status` (`status_id`),
  CONSTRAINT `fk_fee_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Fee type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fee_type`
--

LOCK TABLES `fee_type` WRITE;
/*!40000 ALTER TABLE `fee_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `fee_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `file`
--

DROP TABLE IF EXISTS `file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_type_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL COMMENT 'Original filename',
  `path` varchar(500) DEFAULT NULL COMMENT 'Storage path',
  `size` bigint(20) DEFAULT NULL COMMENT 'File size in bytes',
  `mime_type` varchar(100) DEFAULT NULL COMMENT 'MIME type',
  `hash` varchar(64) DEFAULT NULL COMMENT 'File hash for integrity',
  `metadata` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'Additional file metadata' CHECK (json_valid(`metadata`)),
  `status_id` int(11) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `storage_location` varchar(50) DEFAULT 'local' COMMENT 'Storage location (local, s3, etc.)',
  PRIMARY KEY (`id`),
  KEY `status_id` (`status_id`),
  KEY `created_by` (`created_by`),
  KEY `updated_by` (`updated_by`),
  KEY `idx_name` (`name`),
  KEY `idx_path` (`path`),
  KEY `idx_type` (`file_type_id`),
  CONSTRAINT `file_ibfk_1` FOREIGN KEY (`file_type_id`) REFERENCES `file_type` (`id`),
  CONSTRAINT `file_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
  CONSTRAINT `file_ibfk_3` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
  CONSTRAINT `file_ibfk_4` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `file`
--

LOCK TABLES `file` WRITE;
/*!40000 ALTER TABLE `file` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `file` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `file_type`
--

DROP TABLE IF EXISTS `file_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `file_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `allowed_extensions` varchar(255) DEFAULT NULL COMMENT 'Comma-separated list',
  `max_size_mb` int(11) DEFAULT NULL COMMENT 'Maximum file size in MB',
  `status_id` int(11) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `status_id` (`status_id`),
  KEY `created_by` (`created_by`),
  KEY `updated_by` (`updated_by`),
  KEY `idx_code` (`code`),
  CONSTRAINT `file_type_ibfk_1` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
  CONSTRAINT `file_type_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
  CONSTRAINT `file_type_ibfk_3` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `file_type`
--

LOCK TABLES `file_type` WRITE;
/*!40000 ALTER TABLE `file_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `file_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `gender`
--

DROP TABLE IF EXISTS `gender`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `gender` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gender_type_id` int(11) NOT NULL,
  `code` varchar(10) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` text DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_gender_code` (`code`),
  KEY `idx_gender_type` (`gender_type_id`),
  KEY `idx_gender_status` (`status_id`),
  CONSTRAINT `fk_gender_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_gender_type` FOREIGN KEY (`gender_type_id`) REFERENCES `gender_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gender`
--

LOCK TABLES `gender` WRITE;
/*!40000 ALTER TABLE `gender` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `gender` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `gender_type`
--

DROP TABLE IF EXISTS `gender_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `gender_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gender_type`
--

LOCK TABLES `gender_type` WRITE;
/*!40000 ALTER TABLE `gender_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `gender_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `integration`
--

DROP TABLE IF EXISTS `integration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `integration` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `integration_type_id` int(11) NOT NULL COMMENT 'Reference to integration_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_integration_type` (`integration_type_id`),
  KEY `idx_integration_status` (`status_id`),
  KEY `idx_integration_created` (`created_at`),
  CONSTRAINT `fk_integration_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_integration_type` FOREIGN KEY (`integration_type_id`) REFERENCES `integration_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Integration management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `integration`
--

LOCK TABLES `integration` WRITE;
/*!40000 ALTER TABLE `integration` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `integration` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `integration_type`
--

DROP TABLE IF EXISTS `integration_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `integration_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_integration_type_code` (`code`),
  KEY `idx_integration_type_status` (`status_id`),
  CONSTRAINT `fk_integration_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Integration type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `integration_type`
--

LOCK TABLES `integration_type` WRITE;
/*!40000 ALTER TABLE `integration_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `integration_type` VALUES
(1,'itc','ITC Bridge','Insurance Technology Corporation integration',0,1,1,NULL,'2025-07-21 19:17:31','2025-07-21 19:17:31');
/*!40000 ALTER TABLE `integration_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `language`
--

DROP TABLE IF EXISTS `language`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `language` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `language_type_id` int(11) NOT NULL,
  `code` varchar(10) NOT NULL COMMENT 'ISO language code',
  `name` varchar(100) NOT NULL COMMENT 'English name',
  `native_name` varchar(100) DEFAULT NULL COMMENT 'Name in native language',
  `is_default` tinyint(1) DEFAULT 0,
  `status_id` int(11) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `language_type_id` (`language_type_id`),
  KEY `status_id` (`status_id`),
  KEY `created_by` (`created_by`),
  KEY `updated_by` (`updated_by`),
  KEY `idx_code` (`code`),
  KEY `idx_default` (`is_default`),
  CONSTRAINT `language_ibfk_1` FOREIGN KEY (`language_type_id`) REFERENCES `language_type` (`id`),
  CONSTRAINT `language_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
  CONSTRAINT `language_ibfk_3` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
  CONSTRAINT `language_ibfk_4` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `language`
--

LOCK TABLES `language` WRITE;
/*!40000 ALTER TABLE `language` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `language` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `language_type`
--

DROP TABLE IF EXISTS `language_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `language_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `status_id` int(11) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `status_id` (`status_id`),
  KEY `created_by` (`created_by`),
  KEY `updated_by` (`updated_by`),
  KEY `idx_code` (`code`),
  CONSTRAINT `language_type_ibfk_1` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
  CONSTRAINT `language_type_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
  CONSTRAINT `language_type_ibfk_3` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `language_type`
--

LOCK TABLES `language_type` WRITE;
/*!40000 ALTER TABLE `language_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `language_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `license`
--

DROP TABLE IF EXISTS `license`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `license` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `license_type_id` int(11) NOT NULL COMMENT 'Reference to license_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_license_type` (`license_type_id`),
  KEY `idx_license_status` (`status_id`),
  KEY `idx_license_created` (`created_at`),
  CONSTRAINT `fk_license_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_license_type` FOREIGN KEY (`license_type_id`) REFERENCES `license_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='License management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `license`
--

LOCK TABLES `license` WRITE;
/*!40000 ALTER TABLE `license` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `license` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `license_type`
--

DROP TABLE IF EXISTS `license_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `license_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_license_type_code` (`code`),
  KEY `idx_license_type_status` (`status_id`),
  CONSTRAINT `fk_license_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='License type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `license_type`
--

LOCK TABLES `license_type` WRITE;
/*!40000 ALTER TABLE `license_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `license_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `limit`
--

DROP TABLE IF EXISTS `limit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `limit` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `limit_type_id` int(11) NOT NULL COMMENT 'Reference to limit_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_limit_type` (`limit_type_id`),
  KEY `idx_limit_status` (`status_id`),
  KEY `idx_limit_created` (`created_at`),
  CONSTRAINT `fk_limit_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_limit_type` FOREIGN KEY (`limit_type_id`) REFERENCES `limit_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Limit management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `limit`
--

LOCK TABLES `limit` WRITE;
/*!40000 ALTER TABLE `limit` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `limit` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `limit_type`
--

DROP TABLE IF EXISTS `limit_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `limit_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_limit_type_code` (`code`),
  KEY `idx_limit_type_status` (`status_id`),
  CONSTRAINT `fk_limit_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Limit type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `limit_type`
--

LOCK TABLES `limit_type` WRITE;
/*!40000 ALTER TABLE `limit_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `limit_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `lock`
--

DROP TABLE IF EXISTS `lock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `lock` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `lock_type_id` int(11) NOT NULL COMMENT 'Reference to lock_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_lock_type` (`lock_type_id`),
  KEY `idx_lock_status` (`status_id`),
  KEY `idx_lock_created` (`created_at`),
  CONSTRAINT `fk_lock_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_lock_type` FOREIGN KEY (`lock_type_id`) REFERENCES `lock_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Record locking management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lock`
--

LOCK TABLES `lock` WRITE;
/*!40000 ALTER TABLE `lock` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `lock` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `lock_type`
--

DROP TABLE IF EXISTS `lock_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `lock_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_lock_type_code` (`code`),
  KEY `idx_lock_type_status` (`status_id`),
  CONSTRAINT `fk_lock_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Lock type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lock_type`
--

LOCK TABLES `lock_type` WRITE;
/*!40000 ALTER TABLE `lock_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `lock_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `log_type_id` int(11) NOT NULL COMMENT 'Reference to log_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_log_type` (`log_type_id`),
  KEY `idx_log_status` (`status_id`),
  KEY `idx_log_created` (`created_at`),
  CONSTRAINT `fk_log_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_log_type` FOREIGN KEY (`log_type_id`) REFERENCES `log_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='System logging management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log`
--

LOCK TABLES `log` WRITE;
/*!40000 ALTER TABLE `log` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `log` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `log_type`
--

DROP TABLE IF EXISTS `log_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_log_type_code` (`code`),
  KEY `idx_log_type_status` (`status_id`),
  CONSTRAINT `fk_log_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Log type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_type`
--

LOCK TABLES `log_type` WRITE;
/*!40000 ALTER TABLE `log_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `log_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `loss`
--

DROP TABLE IF EXISTS `loss`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `loss` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `loss_type_id` int(11) NOT NULL COMMENT 'Reference to loss_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_loss_type` (`loss_type_id`),
  KEY `idx_loss_status` (`status_id`),
  KEY `idx_loss_created` (`created_at`),
  CONSTRAINT `fk_loss_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_loss_type` FOREIGN KEY (`loss_type_id`) REFERENCES `loss_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Loss management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loss`
--

LOCK TABLES `loss` WRITE;
/*!40000 ALTER TABLE `loss` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `loss` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `loss_type`
--

DROP TABLE IF EXISTS `loss_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `loss_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_loss_type_code` (`code`),
  KEY `idx_loss_type_status` (`status_id`),
  CONSTRAINT `fk_loss_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Loss type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loss_type`
--

LOCK TABLES `loss_type` WRITE;
/*!40000 ALTER TABLE `loss_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `loss_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_driver_violation`
--

DROP TABLE IF EXISTS `map_driver_violation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_driver_violation` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `driver_id` int(11) NOT NULL COMMENT 'Reference to driver',
  `violation_id` int(11) NOT NULL COMMENT 'Reference to violation',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_driver_violation` (`driver_id`,`violation_id`),
  KEY `idx_violation` (`violation_id`),
  KEY `fk_map_driver_violation_created_by` (`created_by`),
  CONSTRAINT `fk_map_driver_violation_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_map_driver_violation_driver` FOREIGN KEY (`driver_id`) REFERENCES `driver` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_driver_violation_violation` FOREIGN KEY (`violation_id`) REFERENCES `violation` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Driver to violation mapping';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_driver_violation`
--

LOCK TABLES `map_driver_violation` WRITE;
/*!40000 ALTER TABLE `map_driver_violation` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_driver_violation` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_entity_document`
--

DROP TABLE IF EXISTS `map_entity_document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_entity_document` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `entity_id` int(11) NOT NULL COMMENT 'Reference to entity',
  `document_id` int(11) NOT NULL COMMENT 'Reference to document',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_entity_document` (`entity_id`,`document_id`),
  KEY `idx_document_entity` (`document_id`,`entity_id`),
  KEY `idx_map_entity_document_status` (`status_id`),
  CONSTRAINT `fk_map_entity_document_document` FOREIGN KEY (`document_id`) REFERENCES `document` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_entity_document_entity` FOREIGN KEY (`entity_id`) REFERENCES `entity` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_entity_document_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Entity to document mapping following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_entity_document`
--

LOCK TABLES `map_entity_document` WRITE;
/*!40000 ALTER TABLE `map_entity_document` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_entity_document` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_integration_configuration`
--

DROP TABLE IF EXISTS `map_integration_configuration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_integration_configuration` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `program_id` int(11) NOT NULL COMMENT 'Reference to program',
  `integration_type_id` int(11) NOT NULL COMMENT 'Reference to integration type',
  `configuration_id` int(11) NOT NULL COMMENT 'Reference to configuration',
  `is_active` tinyint(1) DEFAULT 1 COMMENT 'Configuration active flag',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_program_integration_config` (`program_id`,`integration_type_id`,`configuration_id`),
  KEY `idx_program` (`program_id`),
  KEY `fk_map_int_config_integration` (`integration_type_id`),
  KEY `fk_map_int_config_configuration` (`configuration_id`),
  KEY `fk_map_int_config_created_by` (`created_by`),
  KEY `fk_map_int_config_updated_by` (`updated_by`),
  CONSTRAINT `fk_map_int_config_configuration` FOREIGN KEY (`configuration_id`) REFERENCES `configuration` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_int_config_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_map_int_config_integration` FOREIGN KEY (`integration_type_id`) REFERENCES `integration_type` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_int_config_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_int_config_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Integration configuration mapping';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_integration_configuration`
--

LOCK TABLES `map_integration_configuration` WRITE;
/*!40000 ALTER TABLE `map_integration_configuration` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_integration_configuration` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_policy_coverage`
--

DROP TABLE IF EXISTS `map_policy_coverage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_policy_coverage` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `policy_id` int(11) NOT NULL COMMENT 'Reference to policy',
  `coverage_id` int(11) NOT NULL COMMENT 'Reference to coverage',
  `premium_amount` decimal(10,2) DEFAULT NULL COMMENT 'Coverage premium',
  `effective_date` date DEFAULT NULL COMMENT 'Coverage start date',
  `expiration_date` date DEFAULT NULL COMMENT 'Coverage end date',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_policy_coverage_unique` (`policy_id`,`coverage_id`),
  KEY `idx_policy_coverage_policy` (`policy_id`),
  KEY `fk_map_policy_cov_coverage` (`coverage_id`),
  KEY `fk_map_policy_cov_status` (`status_id`),
  KEY `fk_map_policy_cov_created_by` (`created_by`),
  KEY `fk_map_policy_cov_updated_by` (`updated_by`),
  CONSTRAINT `fk_map_policy_cov_coverage` FOREIGN KEY (`coverage_id`) REFERENCES `coverage` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_policy_cov_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_map_policy_cov_policy` FOREIGN KEY (`policy_id`) REFERENCES `policy` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_policy_cov_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_map_policy_cov_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Coverage on policies';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_policy_coverage`
--

LOCK TABLES `map_policy_coverage` WRITE;
/*!40000 ALTER TABLE `map_policy_coverage` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_policy_coverage` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_policy_document`
--

DROP TABLE IF EXISTS `map_policy_document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_policy_document` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `policy_id` int(11) NOT NULL COMMENT 'Reference to policy',
  `document_id` int(11) NOT NULL COMMENT 'Reference to document',
  `document_category` varchar(50) NOT NULL COMMENT 'dec_page, policy_form, etc',
  `is_primary` tinyint(1) DEFAULT 0 COMMENT 'Primary document flag',
  `sequence_number` int(11) DEFAULT 0 COMMENT 'Display order',
  `generated_date` timestamp NULL DEFAULT current_timestamp() COMMENT 'Generation date',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_policy_doc_unique` (`policy_id`,`document_id`),
  KEY `idx_policy_doc_policy` (`policy_id`),
  KEY `idx_policy_doc_category` (`document_category`),
  KEY `fk_map_policy_doc_document` (`document_id`),
  KEY `fk_map_policy_doc_status` (`status_id`),
  KEY `fk_map_policy_doc_created_by` (`created_by`),
  CONSTRAINT `fk_map_policy_doc_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_map_policy_doc_document` FOREIGN KEY (`document_id`) REFERENCES `document` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_policy_doc_policy` FOREIGN KEY (`policy_id`) REFERENCES `policy` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_policy_doc_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Documents associated with policies';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_policy_document`
--

LOCK TABLES `map_policy_document` WRITE;
/*!40000 ALTER TABLE `map_policy_document` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_policy_document` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_policy_driver`
--

DROP TABLE IF EXISTS `map_policy_driver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_policy_driver` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `policy_id` int(11) NOT NULL COMMENT 'Reference to policy',
  `driver_id` int(11) NOT NULL COMMENT 'Reference to driver',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_policy_driver` (`policy_id`,`driver_id`),
  KEY `idx_driver_policy` (`driver_id`,`policy_id`),
  KEY `idx_map_policy_driver_status` (`status_id`),
  CONSTRAINT `fk_map_policy_driver_driver` FOREIGN KEY (`driver_id`) REFERENCES `driver` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_policy_driver_policy` FOREIGN KEY (`policy_id`) REFERENCES `policy` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_policy_driver_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Policy to driver mapping following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_policy_driver`
--

LOCK TABLES `map_policy_driver` WRITE;
/*!40000 ALTER TABLE `map_policy_driver` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_policy_driver` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_policy_installment`
--

DROP TABLE IF EXISTS `map_policy_installment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_policy_installment` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `policy_id` int(11) NOT NULL COMMENT 'Reference to policy',
  `installment_number` int(11) NOT NULL COMMENT 'Installment sequence',
  `due_date` date NOT NULL COMMENT 'Payment due date',
  `amount` decimal(10,2) NOT NULL COMMENT 'Installment amount',
  `paid_date` date DEFAULT NULL COMMENT 'Date paid',
  `paid_amount` decimal(10,2) DEFAULT NULL COMMENT 'Amount paid',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_policy_installment` (`policy_id`,`installment_number`),
  KEY `idx_due_date` (`due_date`),
  KEY `fk_map_policy_inst_status` (`status_id`),
  KEY `fk_map_policy_inst_created_by` (`created_by`),
  KEY `fk_map_policy_inst_updated_by` (`updated_by`),
  CONSTRAINT `fk_map_policy_inst_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_map_policy_inst_policy` FOREIGN KEY (`policy_id`) REFERENCES `policy` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_policy_inst_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_map_policy_inst_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Policy payment installments';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_policy_installment`
--

LOCK TABLES `map_policy_installment` WRITE;
/*!40000 ALTER TABLE `map_policy_installment` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_policy_installment` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_policy_vehicle`
--

DROP TABLE IF EXISTS `map_policy_vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_policy_vehicle` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `policy_id` int(11) NOT NULL COMMENT 'Reference to policy',
  `vehicle_id` int(11) NOT NULL COMMENT 'Reference to vehicle',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_policy_vehicle` (`policy_id`,`vehicle_id`),
  KEY `idx_vehicle_policy` (`vehicle_id`,`policy_id`),
  KEY `idx_map_policy_vehicle_status` (`status_id`),
  CONSTRAINT `fk_map_policy_vehicle_policy` FOREIGN KEY (`policy_id`) REFERENCES `policy` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_policy_vehicle_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_map_policy_vehicle_vehicle` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Policy to vehicle mapping following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_policy_vehicle`
--

LOCK TABLES `map_policy_vehicle` WRITE;
/*!40000 ALTER TABLE `map_policy_vehicle` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_policy_vehicle` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_producer_policy_commission`
--

DROP TABLE IF EXISTS `map_producer_policy_commission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_producer_policy_commission` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `producer_id` int(11) NOT NULL COMMENT 'Reference to producer',
  `policy_id` int(11) NOT NULL COMMENT 'Reference to policy',
  `commission_amount` decimal(10,2) DEFAULT NULL COMMENT 'Commission amount',
  `paid_date` date DEFAULT NULL COMMENT 'Date commission paid',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_producer_policy` (`producer_id`,`policy_id`),
  KEY `idx_producer` (`producer_id`),
  KEY `idx_policy` (`policy_id`),
  KEY `fk_map_prod_policy_comm_status` (`status_id`),
  KEY `fk_map_prod_policy_comm_created_by` (`created_by`),
  KEY `fk_map_prod_policy_comm_updated_by` (`updated_by`),
  CONSTRAINT `fk_map_prod_policy_comm_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_map_prod_policy_comm_policy` FOREIGN KEY (`policy_id`) REFERENCES `policy` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_prod_policy_comm_producer` FOREIGN KEY (`producer_id`) REFERENCES `producer` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_prod_policy_comm_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_map_prod_policy_comm_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Producer commission tracking per policy';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_producer_policy_commission`
--

LOCK TABLES `map_producer_policy_commission` WRITE;
/*!40000 ALTER TABLE `map_producer_policy_commission` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_producer_policy_commission` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_producer_suspense`
--

DROP TABLE IF EXISTS `map_producer_suspense`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_producer_suspense` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `producer_id` int(11) NOT NULL COMMENT 'Reference to producer',
  `suspense_id` int(11) NOT NULL COMMENT 'Reference to suspense record',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_producer_suspense` (`producer_id`,`suspense_id`),
  KEY `fk_prod_susp_suspense` (`suspense_id`),
  KEY `fk_prod_susp_created_by` (`created_by`),
  KEY `fk_prod_susp_updated_by` (`updated_by`),
  CONSTRAINT `fk_prod_susp_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_prod_susp_producer` FOREIGN KEY (`producer_id`) REFERENCES `producer` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_prod_susp_suspense` FOREIGN KEY (`suspense_id`) REFERENCES `suspense` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_prod_susp_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Producer task tracking';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_producer_suspense`
--

LOCK TABLES `map_producer_suspense` WRITE;
/*!40000 ALTER TABLE `map_producer_suspense` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_producer_suspense` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_program_coverage`
--

DROP TABLE IF EXISTS `map_program_coverage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_program_coverage` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `program_id` int(11) NOT NULL COMMENT 'Reference to program',
  `coverage_id` int(11) NOT NULL COMMENT 'Reference to coverage',
  `is_required` tinyint(1) DEFAULT 0 COMMENT 'Required coverage for program',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_program_coverage` (`program_id`,`coverage_id`),
  KEY `idx_program` (`program_id`),
  KEY `fk_map_prog_cov_coverage` (`coverage_id`),
  KEY `fk_map_prog_cov_created_by` (`created_by`),
  CONSTRAINT `fk_map_prog_cov_coverage` FOREIGN KEY (`coverage_id`) REFERENCES `coverage` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_prog_cov_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_map_prog_cov_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Program coverage mapping';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_program_coverage`
--

LOCK TABLES `map_program_coverage` WRITE;
/*!40000 ALTER TABLE `map_program_coverage` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_program_coverage` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_program_deductible`
--

DROP TABLE IF EXISTS `map_program_deductible`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_program_deductible` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `program_id` int(11) NOT NULL COMMENT 'Reference to program',
  `deductible_id` int(11) NOT NULL COMMENT 'Reference to deductible',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default deductible for this program',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_program_deductible` (`program_id`,`deductible_id`),
  KEY `idx_program` (`program_id`),
  KEY `fk_map_prog_ded_deductible` (`deductible_id`),
  KEY `fk_map_prog_ded_created_by` (`created_by`),
  CONSTRAINT `fk_map_prog_ded_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_map_prog_ded_deductible` FOREIGN KEY (`deductible_id`) REFERENCES `deductible` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_prog_ded_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Program deductible options';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_program_deductible`
--

LOCK TABLES `map_program_deductible` WRITE;
/*!40000 ALTER TABLE `map_program_deductible` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_program_deductible` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_program_limit`
--

DROP TABLE IF EXISTS `map_program_limit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_program_limit` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `program_id` int(11) NOT NULL COMMENT 'Reference to program',
  `limit_id` int(11) NOT NULL COMMENT 'Reference to limit',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default limit for this program',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_program_limit` (`program_id`,`limit_id`),
  KEY `idx_program` (`program_id`),
  KEY `fk_map_prog_limit_limit` (`limit_id`),
  KEY `fk_map_prog_limit_created_by` (`created_by`),
  CONSTRAINT `fk_map_prog_limit_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_map_prog_limit_limit` FOREIGN KEY (`limit_id`) REFERENCES `limit` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_prog_limit_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Program limit options';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_program_limit`
--

LOCK TABLES `map_program_limit` WRITE;
/*!40000 ALTER TABLE `map_program_limit` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_program_limit` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_program_news`
--

DROP TABLE IF EXISTS `map_program_news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_program_news` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `program_id` int(11) NOT NULL COMMENT 'Reference to program',
  `news_id` int(11) NOT NULL COMMENT 'Reference to news',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_program_news` (`program_id`,`news_id`),
  KEY `idx_news` (`news_id`),
  KEY `fk_map_program_news_created_by` (`created_by`),
  CONSTRAINT `fk_map_program_news_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_map_program_news_news` FOREIGN KEY (`news_id`) REFERENCES `news` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_program_news_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Program-specific news';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_program_news`
--

LOCK TABLES `map_program_news` WRITE;
/*!40000 ALTER TABLE `map_program_news` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_program_news` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_program_producer`
--

DROP TABLE IF EXISTS `map_program_producer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_program_producer` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `program_id` int(11) NOT NULL COMMENT 'Reference to program',
  `producer_id` int(11) NOT NULL COMMENT 'Reference to producer',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_program_producer` (`program_id`,`producer_id`),
  KEY `idx_producer_program` (`producer_id`,`program_id`),
  KEY `idx_map_program_producer_status` (`status_id`),
  CONSTRAINT `fk_map_program_producer_producer` FOREIGN KEY (`producer_id`) REFERENCES `producer` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_program_producer_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_program_producer_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Program to producer mapping following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_program_producer`
--

LOCK TABLES `map_program_producer` WRITE;
/*!40000 ALTER TABLE `map_program_producer` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_program_producer` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_program_underwriting_question`
--

DROP TABLE IF EXISTS `map_program_underwriting_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_program_underwriting_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `program_id` int(11) NOT NULL COMMENT 'Reference to program',
  `underwriting_question_id` int(11) NOT NULL COMMENT 'Reference to question',
  `is_required` tinyint(1) DEFAULT 1 COMMENT 'Required for this program',
  `display_order` int(11) DEFAULT 0 COMMENT 'Display sequence',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_program_question` (`program_id`,`underwriting_question_id`),
  KEY `idx_program` (`program_id`),
  KEY `fk_map_prog_uw_question` (`underwriting_question_id`),
  KEY `fk_map_prog_uw_created_by` (`created_by`),
  CONSTRAINT `fk_map_prog_uw_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_map_prog_uw_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_prog_uw_question` FOREIGN KEY (`underwriting_question_id`) REFERENCES `underwriting_question` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Program underwriting question mapping';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_program_underwriting_question`
--

LOCK TABLES `map_program_underwriting_question` WRITE;
/*!40000 ALTER TABLE `map_program_underwriting_question` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_program_underwriting_question` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_quote_coverage`
--

DROP TABLE IF EXISTS `map_quote_coverage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_quote_coverage` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `quote_id` int(11) NOT NULL COMMENT 'Reference to quote',
  `coverage_id` int(11) NOT NULL COMMENT 'Reference to coverage',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_quote_coverage_unique` (`quote_id`,`coverage_id`),
  KEY `idx_quote` (`quote_id`),
  KEY `fk_map_quote_cov_coverage` (`coverage_id`),
  KEY `fk_map_quote_cov_status` (`status_id`),
  KEY `fk_map_quote_cov_created_by` (`created_by`),
  KEY `fk_map_quote_cov_updated_by` (`updated_by`),
  CONSTRAINT `fk_map_quote_cov_coverage` FOREIGN KEY (`coverage_id`) REFERENCES `coverage` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_quote_cov_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_map_quote_cov_quote` FOREIGN KEY (`quote_id`) REFERENCES `quote` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_quote_cov_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_map_quote_cov_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Quote coverage selections';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_quote_coverage`
--

LOCK TABLES `map_quote_coverage` WRITE;
/*!40000 ALTER TABLE `map_quote_coverage` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_quote_coverage` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_quote_driver`
--

DROP TABLE IF EXISTS `map_quote_driver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_quote_driver` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `quote_id` int(11) NOT NULL COMMENT 'Reference to quote',
  `driver_id` int(11) NOT NULL COMMENT 'Reference to driver',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_quote_driver` (`quote_id`,`driver_id`),
  KEY `idx_driver_quote` (`driver_id`,`quote_id`),
  KEY `idx_map_quote_driver_status` (`status_id`),
  CONSTRAINT `fk_map_quote_driver_driver` FOREIGN KEY (`driver_id`) REFERENCES `driver` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_quote_driver_quote` FOREIGN KEY (`quote_id`) REFERENCES `quote` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_quote_driver_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Quote to driver mapping following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_quote_driver`
--

LOCK TABLES `map_quote_driver` WRITE;
/*!40000 ALTER TABLE `map_quote_driver` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_quote_driver` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_quote_underwriting_question`
--

DROP TABLE IF EXISTS `map_quote_underwriting_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_quote_underwriting_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `quote_id` int(11) NOT NULL COMMENT 'Reference to quote',
  `underwriting_question_id` int(11) NOT NULL COMMENT 'Reference to question',
  `underwriting_answer_id` int(11) NOT NULL COMMENT 'Reference to selected answer',
  `answered_date` timestamp NULL DEFAULT current_timestamp() COMMENT 'When answer was provided',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_quote_question_unique` (`quote_id`,`underwriting_question_id`),
  KEY `idx_map_quote` (`quote_id`),
  KEY `idx_map_question` (`underwriting_question_id`),
  KEY `idx_map_answer` (`underwriting_answer_id`),
  KEY `fk_map_quote_uw_created_by` (`created_by`),
  KEY `fk_map_quote_uw_updated_by` (`updated_by`),
  CONSTRAINT `fk_map_quote` FOREIGN KEY (`quote_id`) REFERENCES `quote` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_map_quote_uw_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_map_quote_uw_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_map_underwriting_answer` FOREIGN KEY (`underwriting_answer_id`) REFERENCES `underwriting_answer` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_map_underwriting_question` FOREIGN KEY (`underwriting_question_id`) REFERENCES `underwriting_question` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Links quotes to specific question/answer pairs';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_quote_underwriting_question`
--

LOCK TABLES `map_quote_underwriting_question` WRITE;
/*!40000 ALTER TABLE `map_quote_underwriting_question` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_quote_underwriting_question` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_quote_vehicle`
--

DROP TABLE IF EXISTS `map_quote_vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_quote_vehicle` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `quote_id` int(11) NOT NULL COMMENT 'Reference to quote',
  `vehicle_id` int(11) NOT NULL COMMENT 'Reference to vehicle',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_quote_vehicle` (`quote_id`,`vehicle_id`),
  KEY `idx_vehicle_quote` (`vehicle_id`,`quote_id`),
  KEY `idx_map_quote_vehicle_status` (`status_id`),
  CONSTRAINT `fk_map_quote_vehicle_quote` FOREIGN KEY (`quote_id`) REFERENCES `quote` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_quote_vehicle_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_map_quote_vehicle_vehicle` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Quote to vehicle mapping following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_quote_vehicle`
--

LOCK TABLES `map_quote_vehicle` WRITE;
/*!40000 ALTER TABLE `map_quote_vehicle` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_quote_vehicle` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_resource_group`
--

DROP TABLE IF EXISTS `map_resource_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_resource_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `resource_id` int(11) NOT NULL COMMENT 'Reference to resource',
  `resource_group_id` int(11) NOT NULL COMMENT 'Reference to resource_group',
  `display_order` int(11) DEFAULT 0 COMMENT 'Sort order within group',
  `status_id` int(11) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_resource_group` (`resource_id`,`resource_group_id`),
  KEY `created_by` (`created_by`),
  KEY `updated_by` (`updated_by`),
  KEY `idx_group_order` (`resource_group_id`,`display_order`),
  KEY `idx_resource` (`resource_id`),
  KEY `idx_status` (`status_id`),
  CONSTRAINT `map_resource_group_ibfk_1` FOREIGN KEY (`resource_id`) REFERENCES `resource` (`id`) ON DELETE CASCADE,
  CONSTRAINT `map_resource_group_ibfk_2` FOREIGN KEY (`resource_group_id`) REFERENCES `resource_group` (`id`) ON DELETE CASCADE,
  CONSTRAINT `map_resource_group_ibfk_3` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
  CONSTRAINT `map_resource_group_ibfk_4` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
  CONSTRAINT `map_resource_group_ibfk_5` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_resource_group`
--

LOCK TABLES `map_resource_group` WRITE;
/*!40000 ALTER TABLE `map_resource_group` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_resource_group` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_role_permission`
--

DROP TABLE IF EXISTS `map_role_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_role_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `role_id` int(11) NOT NULL COMMENT 'Reference to role',
  `permission_id` int(11) NOT NULL COMMENT 'Reference to permission',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_role_permission` (`role_id`,`permission_id`),
  KEY `idx_permission_role` (`permission_id`,`role_id`),
  KEY `idx_map_role_permission_status` (`status_id`),
  CONSTRAINT `fk_map_role_permission_permission` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_role_permission_role` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_role_permission_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Role to permission mapping following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_role_permission`
--

LOCK TABLES `map_role_permission` WRITE;
/*!40000 ALTER TABLE `map_role_permission` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_role_permission` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_user_role`
--

DROP TABLE IF EXISTS `map_user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_user_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `user_id` int(11) NOT NULL COMMENT 'Reference to user',
  `role_id` int(11) NOT NULL COMMENT 'Reference to role',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_user_role` (`user_id`,`role_id`),
  KEY `idx_role_user` (`role_id`,`user_id`),
  KEY `idx_map_user_role_status` (`status_id`),
  CONSTRAINT `fk_map_user_role_role` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_map_user_role_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_map_user_role_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='User to role mapping following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_user_role`
--

LOCK TABLES `map_user_role` WRITE;
/*!40000 ALTER TABLE `map_user_role` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_user_role` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `map_vehicle_coverage`
--

DROP TABLE IF EXISTS `map_vehicle_coverage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_vehicle_coverage` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `vehicle_id` int(11) NOT NULL COMMENT 'Reference to vehicle',
  `coverage_id` int(11) NOT NULL COMMENT 'Reference to coverage',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_vehicle_coverage_unique` (`vehicle_id`,`coverage_id`),
  KEY `idx_map_vehicle` (`vehicle_id`),
  KEY `idx_map_coverage` (`coverage_id`),
  KEY `fk_map_vehicle_coverage_created_by` (`created_by`),
  KEY `fk_map_vehicle_coverage_updated_by` (`updated_by`),
  CONSTRAINT `fk_map_vehicle_coverage_coverage` FOREIGN KEY (`coverage_id`) REFERENCES `coverage` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_map_vehicle_coverage_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_map_vehicle_coverage_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_map_vehicle_coverage_vehicle` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Links coverages to vehicles for consistency';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_vehicle_coverage`
--

LOCK TABLES `map_vehicle_coverage` WRITE;
/*!40000 ALTER TABLE `map_vehicle_coverage` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `map_vehicle_coverage` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `marital_status`
--

DROP TABLE IF EXISTS `marital_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `marital_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `marital_status_type_id` int(11) NOT NULL,
  `code` varchar(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` text DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_marital_status_code` (`code`),
  KEY `idx_marital_status_type` (`marital_status_type_id`),
  KEY `idx_marital_status_status` (`status_id`),
  CONSTRAINT `fk_marital_status_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_marital_status_type` FOREIGN KEY (`marital_status_type_id`) REFERENCES `marital_status_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marital_status`
--

LOCK TABLES `marital_status` WRITE;
/*!40000 ALTER TABLE `marital_status` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `marital_status` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `marital_status_type`
--

DROP TABLE IF EXISTS `marital_status_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `marital_status_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `is_default` tinyint(1) DEFAULT 0,
  `status_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_marital_status_type_code` (`code`),
  KEY `idx_marital_status_type_status` (`status_id`),
  CONSTRAINT `fk_marital_status_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marital_status_type`
--

LOCK TABLES `marital_status_type` WRITE;
/*!40000 ALTER TABLE `marital_status_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `marital_status_type` VALUES
(1,'STANDARD','Standard Marital Status','Common marital status options',1,1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(2,'LEGAL','Legal Marital Status','Legal relationship status options',0,1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(3,'INSURANCE','Insurance Marital Status','Status options for insurance rating',0,1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10');
/*!40000 ALTER TABLE `marital_status_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `name`
--

DROP TABLE IF EXISTS `name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `name` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `name_type_id` int(11) NOT NULL COMMENT 'Reference to name_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  `suffix` varchar(10) DEFAULT NULL COMMENT 'Name suffix (Jr, Sr, etc)',
  `business_name` varchar(255) DEFAULT NULL COMMENT 'Business/DBA name',
  `is_business` tinyint(1) DEFAULT 0 COMMENT 'Business vs individual',
  `first_name` varchar(100) DEFAULT NULL COMMENT 'First name',
  `last_name` varchar(100) DEFAULT NULL COMMENT 'Last name',
  `middle_name` varchar(100) DEFAULT NULL COMMENT 'Middle name',
  PRIMARY KEY (`id`),
  KEY `idx_name_type` (`name_type_id`),
  KEY `idx_name_status` (`status_id`),
  KEY `idx_name_created` (`created_at`),
  KEY `idx_name_business` (`business_name`),
  CONSTRAINT `fk_name_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_name_type` FOREIGN KEY (`name_type_id`) REFERENCES `name_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Name management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `name`
--

LOCK TABLES `name` WRITE;
/*!40000 ALTER TABLE `name` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `name` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `name_type`
--

DROP TABLE IF EXISTS `name_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `name_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_name_type_code` (`code`),
  KEY `idx_name_type_status` (`status_id`),
  CONSTRAINT `fk_name_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Name type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `name_type`
--

LOCK TABLES `name_type` WRITE;
/*!40000 ALTER TABLE `name_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `name_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `news`
--

DROP TABLE IF EXISTS `news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `news` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `title` varchar(255) NOT NULL COMMENT 'News title',
  `content` text NOT NULL COMMENT 'Full news content',
  `summary` varchar(500) DEFAULT NULL COMMENT 'Brief summary for list view',
  `news_type_id` int(11) NOT NULL COMMENT 'Reference to news_type',
  `publication_date` timestamp NOT NULL COMMENT 'When to publish',
  `expiration_date` timestamp NULL DEFAULT NULL COMMENT 'When to expire',
  `priority` int(11) DEFAULT 0 COMMENT 'Higher number = higher priority',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `fk_news_type` (`news_type_id`),
  KEY `fk_news_status` (`status_id`),
  KEY `fk_news_created_by` (`created_by`),
  KEY `fk_news_updated_by` (`updated_by`),
  KEY `idx_news_publication` (`publication_date`,`status_id`),
  KEY `idx_news_expiration` (`expiration_date`),
  CONSTRAINT `fk_news_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_news_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_news_type` FOREIGN KEY (`news_type_id`) REFERENCES `news_type` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_news_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Dashboard news items';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news`
--

LOCK TABLES `news` WRITE;
/*!40000 ALTER TABLE `news` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `news` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `news_type`
--

DROP TABLE IF EXISTS `news_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `news_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Type description',
  `icon` varchar(50) DEFAULT NULL COMMENT 'Icon class for UI',
  `color` varchar(20) DEFAULT NULL COMMENT 'Color scheme',
  `display_order` int(11) DEFAULT 0 COMMENT 'Display ordering',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_news_type_code` (`code`),
  KEY `fk_news_type_status` (`status_id`),
  KEY `fk_news_type_created_by` (`created_by`),
  KEY `fk_news_type_updated_by` (`updated_by`),
  CONSTRAINT `fk_news_type_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_news_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_news_type_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='News categorization';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news_type`
--

LOCK TABLES `news_type` WRITE;
/*!40000 ALTER TABLE `news_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `news_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `non_renewal`
--

DROP TABLE IF EXISTS `non_renewal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `non_renewal` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `non_renewal_type_id` int(11) NOT NULL COMMENT 'Reference to non_renewal_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_non_renewal_type` (`non_renewal_type_id`),
  KEY `idx_non_renewal_status` (`status_id`),
  KEY `idx_non_renewal_created` (`created_at`),
  CONSTRAINT `fk_non_renewal_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_non_renewal_type` FOREIGN KEY (`non_renewal_type_id`) REFERENCES `non_renewal_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Non-renewal management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `non_renewal`
--

LOCK TABLES `non_renewal` WRITE;
/*!40000 ALTER TABLE `non_renewal` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `non_renewal` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `non_renewal_type`
--

DROP TABLE IF EXISTS `non_renewal_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `non_renewal_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_non_renewal_type_code` (`code`),
  KEY `idx_non_renewal_type_status` (`status_id`),
  CONSTRAINT `fk_non_renewal_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Non-renewal type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `non_renewal_type`
--

LOCK TABLES `non_renewal_type` WRITE;
/*!40000 ALTER TABLE `non_renewal_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `non_renewal_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `note`
--

DROP TABLE IF EXISTS `note`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `note` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `note_type_id` int(11) NOT NULL COMMENT 'Reference to note_type',
  `note_text` text NOT NULL COMMENT 'Note content',
  `entity_type` varchar(50) DEFAULT NULL COMMENT 'Type of entity (quote, policy, claim, etc.)',
  `entity_id` int(11) DEFAULT NULL COMMENT 'ID of related entity',
  `is_internal` tinyint(1) DEFAULT 1 COMMENT 'Internal vs customer-visible',
  `priority` varchar(20) DEFAULT 'NORMAL' COMMENT 'Note priority level',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_note_type` (`note_type_id`),
  KEY `idx_note_entity` (`entity_type`,`entity_id`),
  KEY `idx_note_status` (`status_id`),
  KEY `idx_note_created` (`created_at`),
  KEY `fk_note_created_by` (`created_by`),
  KEY `fk_note_updated_by` (`updated_by`),
  CONSTRAINT `fk_note_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_note_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_note_type` FOREIGN KEY (`note_type_id`) REFERENCES `note_type` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_note_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Note management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `note`
--

LOCK TABLES `note` WRITE;
/*!40000 ALTER TABLE `note` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `note` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `note_type`
--

DROP TABLE IF EXISTS `note_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `note_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_note_type_code` (`code`),
  KEY `idx_note_type_status` (`status_id`),
  CONSTRAINT `fk_note_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Note type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `note_type`
--

LOCK TABLES `note_type` WRITE;
/*!40000 ALTER TABLE `note_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `note_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `passenger`
--

DROP TABLE IF EXISTS `passenger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `passenger` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `passenger_type_id` int(11) NOT NULL COMMENT 'Reference to passenger_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_passenger_type` (`passenger_type_id`),
  KEY `idx_passenger_status` (`status_id`),
  KEY `idx_passenger_created` (`created_at`),
  CONSTRAINT `fk_passenger_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_passenger_type` FOREIGN KEY (`passenger_type_id`) REFERENCES `passenger_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Passenger management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passenger`
--

LOCK TABLES `passenger` WRITE;
/*!40000 ALTER TABLE `passenger` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `passenger` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `passenger_type`
--

DROP TABLE IF EXISTS `passenger_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `passenger_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_passenger_type_code` (`code`),
  KEY `idx_passenger_type_status` (`status_id`),
  CONSTRAINT `fk_passenger_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Passenger type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passenger_type`
--

LOCK TABLES `passenger_type` WRITE;
/*!40000 ALTER TABLE `passenger_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `passenger_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `payment_method`
--

DROP TABLE IF EXISTS `payment_method`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_method` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `payment_method_type_id` int(11) NOT NULL COMMENT 'Reference to payment_method_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_payment_method_type` (`payment_method_type_id`),
  KEY `idx_payment_method_status` (`status_id`),
  KEY `idx_payment_method_created` (`created_at`),
  CONSTRAINT `fk_payment_method_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_payment_method_type` FOREIGN KEY (`payment_method_type_id`) REFERENCES `payment_method_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Payment method management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_method`
--

LOCK TABLES `payment_method` WRITE;
/*!40000 ALTER TABLE `payment_method` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `payment_method` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `payment_method_type`
--

DROP TABLE IF EXISTS `payment_method_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_method_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_payment_method_type_code` (`code`),
  KEY `idx_payment_method_type_status` (`status_id`),
  CONSTRAINT `fk_payment_method_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Payment method type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_method_type`
--

LOCK TABLES `payment_method_type` WRITE;
/*!40000 ALTER TABLE `payment_method_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `payment_method_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `payment_plan`
--

DROP TABLE IF EXISTS `payment_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_plan` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `payment_plan_type_id` int(11) NOT NULL COMMENT 'Reference to payment_plan_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_payment_plan_type` (`payment_plan_type_id`),
  KEY `idx_payment_plan_status` (`status_id`),
  KEY `idx_payment_plan_created` (`created_at`),
  CONSTRAINT `fk_payment_plan_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_payment_plan_type` FOREIGN KEY (`payment_plan_type_id`) REFERENCES `payment_plan_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Payment plan management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_plan`
--

LOCK TABLES `payment_plan` WRITE;
/*!40000 ALTER TABLE `payment_plan` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `payment_plan` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `payment_plan_type`
--

DROP TABLE IF EXISTS `payment_plan_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_plan_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_payment_plan_type_code` (`code`),
  KEY `idx_payment_plan_type_status` (`status_id`),
  CONSTRAINT `fk_payment_plan_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Payment plan type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_plan_type`
--

LOCK TABLES `payment_plan_type` WRITE;
/*!40000 ALTER TABLE `payment_plan_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `payment_plan_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `permission_type_id` int(11) NOT NULL COMMENT 'Reference to permission_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  `code` varchar(50) DEFAULT NULL COMMENT 'Permission code',
  `name` varchar(100) DEFAULT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Permission description',
  `category` varchar(50) DEFAULT NULL COMMENT 'Permission category',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_code` (`code`),
  KEY `idx_permission_type` (`permission_type_id`),
  KEY `idx_permission_status` (`status_id`),
  KEY `idx_permission_created` (`created_at`),
  CONSTRAINT `fk_permission_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_permission_type` FOREIGN KEY (`permission_type_id`) REFERENCES `permission_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Permission management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `permission` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `permission_type`
--

DROP TABLE IF EXISTS `permission_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `permission_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_permission_type_code` (`code`),
  KEY `idx_permission_type_status` (`status_id`),
  CONSTRAINT `fk_permission_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Permission type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission_type`
--

LOCK TABLES `permission_type` WRITE;
/*!40000 ALTER TABLE `permission_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `permission_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `policy`
--

DROP TABLE IF EXISTS `policy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `policy` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `policy_type_id` int(11) NOT NULL COMMENT 'Reference to policy_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  `policy_number` varchar(50) DEFAULT NULL COMMENT 'Policy number',
  `program_id` int(11) DEFAULT NULL COMMENT 'Reference to program',
  `quote_id` int(11) DEFAULT NULL COMMENT 'Reference to originating quote',
  `producer_id` int(11) DEFAULT NULL COMMENT 'Reference to producer',
  `effective_date` date DEFAULT NULL COMMENT 'Policy effective date',
  `expiration_date` date DEFAULT NULL COMMENT 'Policy expiration date',
  `premium` decimal(10,2) DEFAULT NULL COMMENT 'Total premium amount',
  `bound_date` timestamp NULL DEFAULT NULL COMMENT 'When policy was bound',
  `cancellation_date` date DEFAULT NULL COMMENT 'Cancellation effective date',
  `cancellation_reason_id` int(11) DEFAULT NULL COMMENT 'Reason for cancellation',
  `reinstatement_date` date DEFAULT NULL COMMENT 'Reinstatement date',
  `non_renewal_date` date DEFAULT NULL COMMENT 'Non-renewal date',
  `non_renewal_reason_id` int(11) DEFAULT NULL COMMENT 'Non-renewal reason',
  `total_vehicles` int(11) DEFAULT 0 COMMENT 'Number of vehicles',
  `total_drivers` int(11) DEFAULT 0 COMMENT 'Number of drivers',
  `payment_plan_id` int(11) DEFAULT NULL COMMENT 'Selected payment plan',
  `down_payment` decimal(10,2) DEFAULT NULL COMMENT 'Down payment amount',
  `paid_to_date` date DEFAULT NULL COMMENT 'Paid through date',
  `total_paid` decimal(10,2) DEFAULT 0.00 COMMENT 'Total amount paid',
  `balance_due` decimal(10,2) DEFAULT 0.00 COMMENT 'Outstanding balance',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_policy_number_unique` (`policy_number`),
  KEY `idx_policy_type` (`policy_type_id`),
  KEY `idx_policy_status` (`status_id`),
  KEY `idx_policy_created` (`created_at`),
  KEY `idx_policy_dates` (`effective_date`,`expiration_date`),
  KEY `idx_policy_producer` (`producer_id`),
  KEY `fk_policy_program` (`program_id`),
  KEY `fk_policy_quote` (`quote_id`),
  KEY `idx_policy_cancellation` (`cancellation_date`),
  KEY `idx_policy_paid_to` (`paid_to_date`),
  CONSTRAINT `fk_policy_producer` FOREIGN KEY (`producer_id`) REFERENCES `producer` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_policy_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_policy_quote` FOREIGN KEY (`quote_id`) REFERENCES `quote` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_policy_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_policy_type` FOREIGN KEY (`policy_type_id`) REFERENCES `policy_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Policy management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `policy`
--

LOCK TABLES `policy` WRITE;
/*!40000 ALTER TABLE `policy` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `policy` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `policy_number_prefix`
--

DROP TABLE IF EXISTS `policy_number_prefix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `policy_number_prefix` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `policy_number_prefix_type_id` int(11) NOT NULL,
  `prefix` varchar(20) NOT NULL,
  `description` text DEFAULT NULL,
  `sequence_start` int(11) DEFAULT 1,
  `status_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_policy_number_prefix` (`prefix`),
  KEY `idx_policy_number_prefix_type` (`policy_number_prefix_type_id`),
  KEY `idx_policy_number_prefix_status` (`status_id`),
  CONSTRAINT `fk_policy_number_prefix_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_policy_number_prefix_type` FOREIGN KEY (`policy_number_prefix_type_id`) REFERENCES `policy_number_prefix_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `policy_number_prefix`
--

LOCK TABLES `policy_number_prefix` WRITE;
/*!40000 ALTER TABLE `policy_number_prefix` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `policy_number_prefix` VALUES
(1,1,'AUTO','Standard auto insurance policies',1000000,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11'),
(2,1,'HOME','Homeowners insurance policies',2000000,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11'),
(3,1,'LIFE','Life insurance policies',3000000,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11'),
(4,1,'COMM','Commercial insurance policies',4000000,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11'),
(5,2,'CA','California policies',5000000,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11'),
(6,2,'TX','Texas policies',6000000,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11'),
(7,2,'FL','Florida policies',7000000,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11'),
(8,2,'NY','New York policies',8000000,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11'),
(9,3,'SR22','SR-22 policies',9000000,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11'),
(10,3,'SR26','SR-26 policies',9500000,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11'),
(11,3,'NON','Non-standard policies',10000000,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11'),
(12,4,'WEB','Online direct policies',11000000,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11'),
(13,4,'AGT','Agent-sold policies',12000000,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11'),
(14,4,'BRK','Broker-sold policies',13000000,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11');
/*!40000 ALTER TABLE `policy_number_prefix` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `policy_number_prefix_type`
--

DROP TABLE IF EXISTS `policy_number_prefix_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `policy_number_prefix_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `is_default` tinyint(1) DEFAULT 0,
  `status_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_policy_number_prefix_type_code` (`code`),
  KEY `idx_policy_number_prefix_type_status` (`status_id`),
  CONSTRAINT `fk_policy_number_prefix_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `policy_number_prefix_type`
--

LOCK TABLES `policy_number_prefix_type` WRITE;
/*!40000 ALTER TABLE `policy_number_prefix_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `policy_number_prefix_type` VALUES
(1,'PROGRAM','Program Prefix','Prefixes for different insurance programs',1,1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(2,'STATE','State Prefix','State-specific policy prefixes',0,1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(3,'PRODUCT','Product Prefix','Product line specific prefixes',0,1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(4,'CHANNEL','Channel Prefix','Distribution channel prefixes',0,1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10');
/*!40000 ALTER TABLE `policy_number_prefix_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `policy_type`
--

DROP TABLE IF EXISTS `policy_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `policy_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_policy_type_code` (`code`),
  KEY `idx_policy_type_status` (`status_id`),
  CONSTRAINT `fk_policy_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Policy type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `policy_type`
--

LOCK TABLES `policy_type` WRITE;
/*!40000 ALTER TABLE `policy_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `policy_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `producer`
--

DROP TABLE IF EXISTS `producer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `producer` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `producer_type_id` int(11) NOT NULL COMMENT 'Reference to producer_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  `producer_code` varchar(50) DEFAULT NULL COMMENT 'Producer identifier code',
  `name_id` int(11) DEFAULT NULL COMMENT 'Reference to name table',
  `license_id` int(11) DEFAULT NULL COMMENT 'Reference to license table',
  `commission_id` int(11) DEFAULT NULL COMMENT 'Reference to commission table',
  `tax_identification_id` int(11) DEFAULT NULL COMMENT 'Reference to tax_identification',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_producer_code_unique` (`producer_code`),
  KEY `idx_producer_type` (`producer_type_id`),
  KEY `idx_producer_status` (`status_id`),
  KEY `idx_producer_created` (`created_at`),
  KEY `fk_producer_name` (`name_id`),
  KEY `fk_producer_license` (`license_id`),
  KEY `fk_producer_commission` (`commission_id`),
  KEY `fk_producer_tax_id` (`tax_identification_id`),
  CONSTRAINT `fk_producer_commission` FOREIGN KEY (`commission_id`) REFERENCES `commission` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_producer_license` FOREIGN KEY (`license_id`) REFERENCES `license` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_producer_name` FOREIGN KEY (`name_id`) REFERENCES `name` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_producer_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_producer_tax_id` FOREIGN KEY (`tax_identification_id`) REFERENCES `tax_identification` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_producer_type` FOREIGN KEY (`producer_type_id`) REFERENCES `producer_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Producer management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producer`
--

LOCK TABLES `producer` WRITE;
/*!40000 ALTER TABLE `producer` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `producer` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `producer_type`
--

DROP TABLE IF EXISTS `producer_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `producer_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_producer_type_code` (`code`),
  KEY `idx_producer_type_status` (`status_id`),
  CONSTRAINT `fk_producer_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Producer type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producer_type`
--

LOCK TABLES `producer_type` WRITE;
/*!40000 ALTER TABLE `producer_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `producer_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `program`
--

DROP TABLE IF EXISTS `program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `program` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `program_type_id` int(11) NOT NULL COMMENT 'Reference to program_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  `policy_number_prefix_id` int(11) DEFAULT NULL COMMENT 'Reference to policy_number_prefix',
  `name` varchar(100) DEFAULT NULL COMMENT 'Program name',
  `description` text DEFAULT NULL COMMENT 'Program description',
  `effective_date` date DEFAULT NULL COMMENT 'Program start date',
  `expiration_date` date DEFAULT NULL COMMENT 'Program end date',
  PRIMARY KEY (`id`),
  KEY `idx_program_type` (`program_type_id`),
  KEY `idx_program_status` (`status_id`),
  KEY `idx_program_created` (`created_at`),
  KEY `idx_program_dates` (`effective_date`,`expiration_date`),
  KEY `fk_program_prefix` (`policy_number_prefix_id`),
  CONSTRAINT `fk_program_prefix` FOREIGN KEY (`policy_number_prefix_id`) REFERENCES `policy_number_prefix` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_program_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_program_type` FOREIGN KEY (`program_type_id`) REFERENCES `program_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Program management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program`
--

LOCK TABLES `program` WRITE;
/*!40000 ALTER TABLE `program` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `program` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `program_type`
--

DROP TABLE IF EXISTS `program_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `program_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_program_type_code` (`code`),
  KEY `idx_program_type_status` (`status_id`),
  CONSTRAINT `fk_program_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Program type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program_type`
--

LOCK TABLES `program_type` WRITE;
/*!40000 ALTER TABLE `program_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `program_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `quote`
--

DROP TABLE IF EXISTS `quote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `quote` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `quote_type_id` int(11) NOT NULL COMMENT 'Reference to quote_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  `quote_number` varchar(50) DEFAULT NULL COMMENT 'Quote number',
  `program_id` int(11) DEFAULT NULL COMMENT 'Reference to program',
  `producer_id` int(11) DEFAULT NULL COMMENT 'Reference to producer',
  `policy_id` int(11) DEFAULT NULL COMMENT 'Reference to bound policy',
  `effective_date` date DEFAULT NULL COMMENT 'Quote effective date',
  `expiration_date` date DEFAULT NULL COMMENT 'Quote expiration date',
  `premium` decimal(10,2) DEFAULT NULL COMMENT 'Quoted premium amount',
  `bound_date` timestamp NULL DEFAULT NULL COMMENT 'When quote was bound',
  `version_number` int(11) DEFAULT 1 COMMENT 'Quote version number',
  `is_renewal` tinyint(1) DEFAULT 0 COMMENT 'Is this a renewal quote',
  `renewal_policy_id` int(11) DEFAULT NULL COMMENT 'Reference to policy being renewed',
  `distribution_channel_id` int(11) DEFAULT NULL COMMENT 'Source channel for quote creation',
  `external_reference` varchar(100) DEFAULT NULL COMMENT 'External system reference',
  `total_vehicles` int(11) DEFAULT 0 COMMENT 'Number of vehicles',
  `total_drivers` int(11) DEFAULT 0 COMMENT 'Number of drivers',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_quote_number_unique` (`quote_number`),
  KEY `idx_quote_type` (`quote_type_id`),
  KEY `idx_quote_status` (`status_id`),
  KEY `idx_quote_created` (`created_at`),
  KEY `idx_quote_dates` (`effective_date`,`expiration_date`),
  KEY `idx_quote_producer` (`producer_id`),
  KEY `fk_quote_program` (`program_id`),
  KEY `fk_quote_policy` (`policy_id`),
  CONSTRAINT `fk_quote_policy` FOREIGN KEY (`policy_id`) REFERENCES `policy` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_quote_producer` FOREIGN KEY (`producer_id`) REFERENCES `producer` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_quote_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_quote_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_quote_type` FOREIGN KEY (`quote_type_id`) REFERENCES `quote_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Quote management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quote`
--

LOCK TABLES `quote` WRITE;
/*!40000 ALTER TABLE `quote` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `quote` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `quote_type`
--

DROP TABLE IF EXISTS `quote_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `quote_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_quote_type_code` (`code`),
  KEY `idx_quote_type_status` (`status_id`),
  CONSTRAINT `fk_quote_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Quote type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quote_type`
--

LOCK TABLES `quote_type` WRITE;
/*!40000 ALTER TABLE `quote_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `quote_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `rate`
--

DROP TABLE IF EXISTS `rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `rate` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `rate_type_id` int(11) NOT NULL COMMENT 'Reference to rate_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_rate_type` (`rate_type_id`),
  KEY `idx_rate_status` (`status_id`),
  KEY `idx_rate_created` (`created_at`),
  CONSTRAINT `fk_rate_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_rate_type` FOREIGN KEY (`rate_type_id`) REFERENCES `rate_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Rate management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rate`
--

LOCK TABLES `rate` WRITE;
/*!40000 ALTER TABLE `rate` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `rate` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `rate_type`
--

DROP TABLE IF EXISTS `rate_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `rate_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_rate_type_code` (`code`),
  KEY `idx_rate_type_status` (`status_id`),
  CONSTRAINT `fk_rate_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Rate type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rate_type`
--

LOCK TABLES `rate_type` WRITE;
/*!40000 ALTER TABLE `rate_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `rate_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `refund`
--

DROP TABLE IF EXISTS `refund`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `refund` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `refund_type_id` int(11) NOT NULL COMMENT 'Reference to refund_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_refund_type` (`refund_type_id`),
  KEY `idx_refund_status` (`status_id`),
  KEY `idx_refund_created` (`created_at`),
  CONSTRAINT `fk_refund_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_refund_type` FOREIGN KEY (`refund_type_id`) REFERENCES `refund_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Refund management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `refund`
--

LOCK TABLES `refund` WRITE;
/*!40000 ALTER TABLE `refund` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `refund` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `refund_type`
--

DROP TABLE IF EXISTS `refund_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `refund_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_refund_type_code` (`code`),
  KEY `idx_refund_type_status` (`status_id`),
  CONSTRAINT `fk_refund_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Refund type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `refund_type`
--

LOCK TABLES `refund_type` WRITE;
/*!40000 ALTER TABLE `refund_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `refund_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `reinstatement`
--

DROP TABLE IF EXISTS `reinstatement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `reinstatement` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `reinstatement_type_id` int(11) NOT NULL COMMENT 'Reference to reinstatement_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_reinstatement_type` (`reinstatement_type_id`),
  KEY `idx_reinstatement_status` (`status_id`),
  KEY `idx_reinstatement_created` (`created_at`),
  CONSTRAINT `fk_reinstatement_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_reinstatement_type` FOREIGN KEY (`reinstatement_type_id`) REFERENCES `reinstatement_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Reinstatement management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reinstatement`
--

LOCK TABLES `reinstatement` WRITE;
/*!40000 ALTER TABLE `reinstatement` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `reinstatement` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `reinstatement_type`
--

DROP TABLE IF EXISTS `reinstatement_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `reinstatement_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_reinstatement_type_code` (`code`),
  KEY `idx_reinstatement_type_status` (`status_id`),
  CONSTRAINT `fk_reinstatement_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Reinstatement type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reinstatement_type`
--

LOCK TABLES `reinstatement_type` WRITE;
/*!40000 ALTER TABLE `reinstatement_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `reinstatement_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `relationship_to_insured`
--

DROP TABLE IF EXISTS `relationship_to_insured`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `relationship_to_insured` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `relationship_to_insured_type_id` int(11) NOT NULL COMMENT 'Reference to relationship_to_insured_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_relationship_to_insured_type` (`relationship_to_insured_type_id`),
  KEY `idx_relationship_to_insured_status` (`status_id`),
  KEY `idx_relationship_to_insured_created` (`created_at`),
  CONSTRAINT `fk_relationship_to_insured_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_relationship_to_insured_type` FOREIGN KEY (`relationship_to_insured_type_id`) REFERENCES `relationship_to_insured_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Relationship to insured management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relationship_to_insured`
--

LOCK TABLES `relationship_to_insured` WRITE;
/*!40000 ALTER TABLE `relationship_to_insured` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `relationship_to_insured` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `relationship_to_insured_type`
--

DROP TABLE IF EXISTS `relationship_to_insured_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `relationship_to_insured_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_relationship_to_insured_type_code` (`code`),
  KEY `idx_relationship_to_insured_type_status` (`status_id`),
  CONSTRAINT `fk_relationship_to_insured_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Relationship to insured type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relationship_to_insured_type`
--

LOCK TABLES `relationship_to_insured_type` WRITE;
/*!40000 ALTER TABLE `relationship_to_insured_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `relationship_to_insured_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `renewal`
--

DROP TABLE IF EXISTS `renewal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `renewal` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `renewal_type_id` int(11) NOT NULL COMMENT 'Reference to renewal_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_renewal_type` (`renewal_type_id`),
  KEY `idx_renewal_status` (`status_id`),
  KEY `idx_renewal_created` (`created_at`),
  CONSTRAINT `fk_renewal_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_renewal_type` FOREIGN KEY (`renewal_type_id`) REFERENCES `renewal_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Renewal management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `renewal`
--

LOCK TABLES `renewal` WRITE;
/*!40000 ALTER TABLE `renewal` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `renewal` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `renewal_offer`
--

DROP TABLE IF EXISTS `renewal_offer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `renewal_offer` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `policy_id` int(11) NOT NULL COMMENT 'Reference to policy',
  `quote_id` int(11) NOT NULL COMMENT 'Reference to renewal quote',
  `offer_date` timestamp NULL DEFAULT current_timestamp() COMMENT 'Offer generation date',
  `expiration_date` date NOT NULL COMMENT 'Offer expiration',
  `current_premium` decimal(10,2) DEFAULT NULL COMMENT 'Current policy premium',
  `renewal_premium` decimal(10,2) DEFAULT NULL COMMENT 'Proposed renewal premium',
  `premium_change` decimal(10,2) DEFAULT NULL COMMENT 'Premium difference',
  `change_percentage` decimal(5,2) DEFAULT NULL COMMENT 'Percentage change',
  `is_auto_renewal` tinyint(1) DEFAULT 0 COMMENT 'Auto-renewal flag',
  `customer_notified` tinyint(1) DEFAULT 0 COMMENT 'Notification sent',
  `notification_date` timestamp NULL DEFAULT NULL COMMENT 'When notified',
  `response_required_by` date DEFAULT NULL COMMENT 'Response deadline',
  `customer_response` varchar(50) DEFAULT NULL COMMENT 'accept, decline, modify',
  `response_date` timestamp NULL DEFAULT NULL COMMENT 'Response date',
  `decline_reason` text DEFAULT NULL COMMENT 'Reason if declined',
  `new_policy_id` int(11) DEFAULT NULL COMMENT 'New policy if renewed',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Policy renewal offers';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `renewal_offer`
--

LOCK TABLES `renewal_offer` WRITE;
/*!40000 ALTER TABLE `renewal_offer` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `renewal_offer` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `renewal_type`
--

DROP TABLE IF EXISTS `renewal_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `renewal_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_renewal_type_code` (`code`),
  KEY `idx_renewal_type_status` (`status_id`),
  CONSTRAINT `fk_renewal_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Renewal type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `renewal_type`
--

LOCK TABLES `renewal_type` WRITE;
/*!40000 ALTER TABLE `renewal_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `renewal_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `resource`
--

DROP TABLE IF EXISTS `resource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `resource` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `resource_type_id` int(11) NOT NULL,
  `code` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `url` varchar(500) NOT NULL,
  `description` text DEFAULT NULL,
  `display_order` int(11) DEFAULT 0,
  `status_id` int(11) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `status_id` (`status_id`),
  KEY `created_by` (`created_by`),
  KEY `updated_by` (`updated_by`),
  KEY `idx_code` (`code`),
  KEY `idx_type` (`resource_type_id`),
  CONSTRAINT `resource_ibfk_1` FOREIGN KEY (`resource_type_id`) REFERENCES `resource_type` (`id`),
  CONSTRAINT `resource_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
  CONSTRAINT `resource_ibfk_3` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
  CONSTRAINT `resource_ibfk_4` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resource`
--

LOCK TABLES `resource` WRITE;
/*!40000 ALTER TABLE `resource` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `resource` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `resource_group`
--

DROP TABLE IF EXISTS `resource_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `resource_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL COMMENT 'Unique identifier code',
  `name` varchar(100) NOT NULL COMMENT 'Display name for category',
  `description` text DEFAULT NULL COMMENT 'Optional description',
  `display_order` int(11) DEFAULT 0 COMMENT 'Sort order for display',
  `status_id` int(11) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `created_by` (`created_by`),
  KEY `updated_by` (`updated_by`),
  KEY `idx_display_order` (`display_order`),
  KEY `idx_status` (`status_id`),
  KEY `idx_code` (`code`),
  CONSTRAINT `resource_group_ibfk_1` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
  CONSTRAINT `resource_group_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
  CONSTRAINT `resource_group_ibfk_3` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resource_group`
--

LOCK TABLES `resource_group` WRITE;
/*!40000 ALTER TABLE `resource_group` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `resource_group` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `resource_type`
--

DROP TABLE IF EXISTS `resource_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `resource_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `is_default` tinyint(1) DEFAULT 0,
  `status_id` int(11) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `status_id` (`status_id`),
  KEY `created_by` (`created_by`),
  KEY `updated_by` (`updated_by`),
  KEY `idx_code` (`code`),
  CONSTRAINT `resource_type_ibfk_1` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
  CONSTRAINT `resource_type_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
  CONSTRAINT `resource_type_ibfk_3` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resource_type`
--

LOCK TABLES `resource_type` WRITE;
/*!40000 ALTER TABLE `resource_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `resource_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `role_type_id` int(11) NOT NULL COMMENT 'Reference to role_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  `code` varchar(50) DEFAULT NULL COMMENT 'Role code',
  `name` varchar(100) DEFAULT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Role description',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_code` (`code`),
  KEY `idx_role_type` (`role_type_id`),
  KEY `idx_role_status` (`status_id`),
  KEY `idx_role_created` (`created_at`),
  CONSTRAINT `fk_role_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_role_type` FOREIGN KEY (`role_type_id`) REFERENCES `role_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Role management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `role_type`
--

DROP TABLE IF EXISTS `role_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_role_type_code` (`code`),
  KEY `idx_role_type_status` (`status_id`),
  CONSTRAINT `fk_role_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Role type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_type`
--

LOCK TABLES `role_type` WRITE;
/*!40000 ALTER TABLE `role_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `role_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `search_history`
--

DROP TABLE IF EXISTS `search_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `search_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `user_id` int(11) NOT NULL COMMENT 'User who performed search',
  `search_query` varchar(255) NOT NULL COMMENT 'Search query text',
  `search_type` varchar(50) DEFAULT NULL COMMENT 'Type of search: global, policy, quote',
  `result_count` int(11) DEFAULT 0 COMMENT 'Number of results returned',
  `selected_result_type` varchar(50) DEFAULT NULL COMMENT 'Type of result selected',
  `selected_result_id` int(11) DEFAULT NULL COMMENT 'ID of selected result',
  `search_duration_ms` int(11) DEFAULT NULL COMMENT 'Search duration in milliseconds',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_user_created` (`user_id`,`created_at`),
  KEY `idx_query` (`search_query`),
  CONSTRAINT `fk_search_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Search query history for analytics';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search_history`
--

LOCK TABLES `search_history` WRITE;
/*!40000 ALTER TABLE `search_history` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `search_history` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `session`
--

DROP TABLE IF EXISTS `session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `session` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `session_type_id` int(11) NOT NULL COMMENT 'Reference to session_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_session_type` (`session_type_id`),
  KEY `idx_session_status` (`status_id`),
  KEY `idx_session_created` (`created_at`),
  CONSTRAINT `fk_session_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_session_type` FOREIGN KEY (`session_type_id`) REFERENCES `session_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Session management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `session`
--

LOCK TABLES `session` WRITE;
/*!40000 ALTER TABLE `session` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `session` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `session_type`
--

DROP TABLE IF EXISTS `session_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `session_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_session_type_code` (`code`),
  KEY `idx_session_type_status` (`status_id`),
  CONSTRAINT `fk_session_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Session type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `session_type`
--

LOCK TABLES `session_type` WRITE;
/*!40000 ALTER TABLE `session_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `session_type` VALUES
(1,'user','User Session','User login sessions',1,1,1,NULL,'2025-07-21 19:17:31','2025-07-21 19:17:31');
/*!40000 ALTER TABLE `session_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `signature`
--

DROP TABLE IF EXISTS `signature`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `signature` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `signature_data` text DEFAULT NULL COMMENT 'Digital signature image/data',
  `initials_data` text DEFAULT NULL COMMENT 'Digital initials image/data',
  `signature_adopted_name` varchar(255) DEFAULT NULL COMMENT 'Name used when adopting signature',
  `signature_adopted_at` timestamp NULL DEFAULT NULL COMMENT 'When signature was adopted',
  `status_id` int(11) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `status_id` (`status_id`),
  KEY `created_by` (`created_by`),
  KEY `updated_by` (`updated_by`),
  KEY `idx_user` (`user_id`),
  CONSTRAINT `signature_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `signature_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
  CONSTRAINT `signature_ibfk_3` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
  CONSTRAINT `signature_ibfk_4` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `signature`
--

LOCK TABLES `signature` WRITE;
/*!40000 ALTER TABLE `signature` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `signature` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `sr22`
--

DROP TABLE IF EXISTS `sr22`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sr22` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `sr22_type_id` int(11) NOT NULL COMMENT 'Reference to sr22_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_sr22_type` (`sr22_type_id`),
  KEY `idx_sr22_status` (`status_id`),
  KEY `idx_sr22_created` (`created_at`),
  CONSTRAINT `fk_sr22_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_sr22_type` FOREIGN KEY (`sr22_type_id`) REFERENCES `sr22_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='SR22 filing management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sr22`
--

LOCK TABLES `sr22` WRITE;
/*!40000 ALTER TABLE `sr22` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `sr22` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `sr22_reason`
--

DROP TABLE IF EXISTS `sr22_reason`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sr22_reason` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Reason code',
  `name` varchar(100) NOT NULL COMMENT 'Reason name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_sr22_reason_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='SR22 reason codes';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sr22_reason`
--

LOCK TABLES `sr22_reason` WRITE;
/*!40000 ALTER TABLE `sr22_reason` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `sr22_reason` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `sr22_type`
--

DROP TABLE IF EXISTS `sr22_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sr22_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_sr22_type_code` (`code`),
  KEY `idx_sr22_type_status` (`status_id`),
  CONSTRAINT `fk_sr22_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='SR22 type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sr22_type`
--

LOCK TABLES `sr22_type` WRITE;
/*!40000 ALTER TABLE `sr22_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `sr22_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `sr26`
--

DROP TABLE IF EXISTS `sr26`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sr26` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `sr26_type_id` int(11) NOT NULL COMMENT 'Reference to sr26_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_sr26_type` (`sr26_type_id`),
  KEY `idx_sr26_status` (`status_id`),
  KEY `idx_sr26_created` (`created_at`),
  CONSTRAINT `fk_sr26_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_sr26_type` FOREIGN KEY (`sr26_type_id`) REFERENCES `sr26_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='SR26 filing management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sr26`
--

LOCK TABLES `sr26` WRITE;
/*!40000 ALTER TABLE `sr26` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `sr26` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `sr26_reason`
--

DROP TABLE IF EXISTS `sr26_reason`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sr26_reason` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Reason code',
  `name` varchar(100) NOT NULL COMMENT 'Reason name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_sr26_reason_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='SR26 reason codes';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sr26_reason`
--

LOCK TABLES `sr26_reason` WRITE;
/*!40000 ALTER TABLE `sr26_reason` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `sr26_reason` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `sr26_type`
--

DROP TABLE IF EXISTS `sr26_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sr26_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_sr26_type_code` (`code`),
  KEY `idx_sr26_type_status` (`status_id`),
  CONSTRAINT `fk_sr26_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='SR26 type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sr26_type`
--

LOCK TABLES `sr26_type` WRITE;
/*!40000 ALTER TABLE `sr26_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `sr26_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `state`
--

DROP TABLE IF EXISTS `state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `state` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(2) NOT NULL COMMENT 'State abbreviation',
  `name` varchar(100) NOT NULL COMMENT 'State name',
  `country_id` int(11) NOT NULL COMMENT 'Reference to country',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_state_code` (`code`),
  KEY `idx_state_country` (`country_id`),
  CONSTRAINT `fk_state_country` FOREIGN KEY (`country_id`) REFERENCES `country` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='State/province reference table';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `state`
--

LOCK TABLES `state` WRITE;
/*!40000 ALTER TABLE `state` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `state` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `status` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `status_type_id` int(11) NOT NULL COMMENT 'Reference to status_type',
  `code` varchar(50) NOT NULL COMMENT 'Unique status code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_status_code` (`code`),
  KEY `idx_status_type` (`status_type_id`),
  CONSTRAINT `fk_status_type` FOREIGN KEY (`status_type_id`) REFERENCES `status_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Universal status management - foundation table';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status`
--

LOCK TABLES `status` WRITE;
/*!40000 ALTER TABLE `status` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `status` VALUES
(1,1,'ACTIVE','Active','Record is active and available',NULL,NULL,'2025-07-18 23:50:34','2025-07-18 23:50:34');
/*!40000 ALTER TABLE `status` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `status_type`
--

DROP TABLE IF EXISTS `status_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_status_type_code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Status type categorization - foundation table';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_type`
--

LOCK TABLES `status_type` WRITE;
/*!40000 ALTER TABLE `status_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `status_type` VALUES
(1,'RECORD','Record Status','General record lifecycle statuses',0,NULL,NULL,'2025-07-18 23:50:34','2025-07-18 23:50:34');
/*!40000 ALTER TABLE `status_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `surcharge`
--

DROP TABLE IF EXISTS `surcharge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `surcharge` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `surcharge_type_id` int(11) NOT NULL COMMENT 'Reference to surcharge_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_surcharge_type` (`surcharge_type_id`),
  KEY `idx_surcharge_status` (`status_id`),
  KEY `idx_surcharge_created` (`created_at`),
  CONSTRAINT `fk_surcharge_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_surcharge_type` FOREIGN KEY (`surcharge_type_id`) REFERENCES `surcharge_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Surcharge management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `surcharge`
--

LOCK TABLES `surcharge` WRITE;
/*!40000 ALTER TABLE `surcharge` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `surcharge` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `surcharge_type`
--

DROP TABLE IF EXISTS `surcharge_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `surcharge_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_surcharge_type_code` (`code`),
  KEY `idx_surcharge_type_status` (`status_id`),
  CONSTRAINT `fk_surcharge_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Surcharge type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `surcharge_type`
--

LOCK TABLES `surcharge_type` WRITE;
/*!40000 ALTER TABLE `surcharge_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `surcharge_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `suspense`
--

DROP TABLE IF EXISTS `suspense`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `suspense` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `suspense_type_id` int(11) NOT NULL COMMENT 'Reference to suspense_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  `route_path` varchar(255) DEFAULT NULL COMMENT 'Navigation path for task',
  `description` text DEFAULT NULL COMMENT 'Detailed description of suspense item',
  `entity_type` varchar(50) DEFAULT NULL COMMENT 'Type of entity (quote, policy, etc.)',
  `entity_id` int(11) DEFAULT NULL COMMENT 'ID of related entity',
  `due_date` date DEFAULT NULL COMMENT 'Due date for resolution',
  PRIMARY KEY (`id`),
  KEY `idx_suspense_type` (`suspense_type_id`),
  KEY `idx_suspense_status` (`status_id`),
  KEY `idx_suspense_created` (`created_at`),
  KEY `idx_suspense_route` (`route_path`),
  KEY `idx_suspense_entity` (`entity_type`,`entity_id`),
  CONSTRAINT `fk_suspense_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_suspense_type` FOREIGN KEY (`suspense_type_id`) REFERENCES `suspense_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Suspense management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suspense`
--

LOCK TABLES `suspense` WRITE;
/*!40000 ALTER TABLE `suspense` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `suspense` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `suspense_type`
--

DROP TABLE IF EXISTS `suspense_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `suspense_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  `category` varchar(50) DEFAULT NULL COMMENT 'Task category for grouping',
  `priority` int(11) DEFAULT 0 COMMENT 'Task priority',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_suspense_type_code` (`code`),
  KEY `idx_suspense_type_status` (`status_id`),
  KEY `idx_suspense_type_category` (`category`),
  CONSTRAINT `fk_suspense_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Suspense type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suspense_type`
--

LOCK TABLES `suspense_type` WRITE;
/*!40000 ALTER TABLE `suspense_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `suspense_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `tax_identification`
--

DROP TABLE IF EXISTS `tax_identification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tax_identification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tax_identification_type_id` int(11) NOT NULL,
  `tax_identification_number` varchar(50) NOT NULL,
  `issuing_country_id` int(11) NOT NULL,
  `issuing_state_id` int(11) DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_tax_identification_number` (`tax_identification_number`),
  KEY `idx_tax_identification_type` (`tax_identification_type_id`),
  KEY `idx_tax_identification_country` (`issuing_country_id`),
  KEY `idx_tax_identification_state` (`issuing_state_id`),
  KEY `idx_tax_identification_status` (`status_id`),
  CONSTRAINT `fk_tax_identification_country` FOREIGN KEY (`issuing_country_id`) REFERENCES `country` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_tax_identification_state` FOREIGN KEY (`issuing_state_id`) REFERENCES `state` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_tax_identification_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_tax_identification_type` FOREIGN KEY (`tax_identification_type_id`) REFERENCES `tax_identification_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tax_identification`
--

LOCK TABLES `tax_identification` WRITE;
/*!40000 ALTER TABLE `tax_identification` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `tax_identification` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `tax_identification_type`
--

DROP TABLE IF EXISTS `tax_identification_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tax_identification_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `is_default` tinyint(1) DEFAULT 0,
  `status_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_tax_identification_type_code` (`code`),
  KEY `idx_tax_identification_type_status` (`status_id`),
  CONSTRAINT `fk_tax_identification_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tax_identification_type`
--

LOCK TABLES `tax_identification_type` WRITE;
/*!40000 ALTER TABLE `tax_identification_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `tax_identification_type` VALUES
(1,'EIN','Employer Identification Number','Federal EIN for businesses',1,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11'),
(2,'SSN','Social Security Number','Individual taxpayer identification',0,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11'),
(3,'ITIN','Individual Taxpayer ID Number','Tax ID for non-resident aliens',0,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11'),
(4,'STATE','State Tax ID','State-issued tax identification',0,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11'),
(5,'FOREIGN','Foreign Tax ID','Non-US tax identification',0,1,1,1,'2025-07-21 16:03:11','2025-07-21 16:03:11');
/*!40000 ALTER TABLE `tax_identification_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `template`
--

DROP TABLE IF EXISTS `template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `template` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `template_type_id` int(11) NOT NULL COMMENT 'Reference to template_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_template_type` (`template_type_id`),
  KEY `idx_template_status` (`status_id`),
  KEY `idx_template_created` (`created_at`),
  CONSTRAINT `fk_template_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_template_type` FOREIGN KEY (`template_type_id`) REFERENCES `template_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Template management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `template`
--

LOCK TABLES `template` WRITE;
/*!40000 ALTER TABLE `template` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `template` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `template_type`
--

DROP TABLE IF EXISTS `template_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `template_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_template_type_code` (`code`),
  KEY `idx_template_type_status` (`status_id`),
  CONSTRAINT `fk_template_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Template type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `template_type`
--

LOCK TABLES `template_type` WRITE;
/*!40000 ALTER TABLE `template_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `template_type` VALUES
(1,'report','Report Template','Templates for generating reports',0,1,1,NULL,'2025-07-21 19:17:31','2025-07-21 19:17:31');
/*!40000 ALTER TABLE `template_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `territory`
--

DROP TABLE IF EXISTS `territory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `territory` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Territory code',
  `name` varchar(100) NOT NULL COMMENT 'Territory name',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_territory_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Rating territory reference table';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `territory`
--

LOCK TABLES `territory` WRITE;
/*!40000 ALTER TABLE `territory` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `territory` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `test_table`
--

DROP TABLE IF EXISTS `test_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_table` (
  `id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_table`
--

LOCK TABLES `test_table` WRITE;
/*!40000 ALTER TABLE `test_table` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `test_table` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `transaction_type_id` int(11) NOT NULL COMMENT 'Reference to transaction_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_transaction_type` (`transaction_type_id`),
  KEY `idx_transaction_status` (`status_id`),
  KEY `idx_transaction_created` (`created_at`),
  CONSTRAINT `fk_transaction_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_transaction_type` FOREIGN KEY (`transaction_type_id`) REFERENCES `transaction_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Transaction management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction`
--

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `transaction_line`
--

DROP TABLE IF EXISTS `transaction_line`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction_line` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `transaction_line_type_id` int(11) NOT NULL COMMENT 'Reference to transaction_line_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_transaction_line_type` (`transaction_line_type_id`),
  KEY `idx_transaction_line_status` (`status_id`),
  KEY `idx_transaction_line_created` (`created_at`),
  CONSTRAINT `fk_transaction_line_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_transaction_line_type` FOREIGN KEY (`transaction_line_type_id`) REFERENCES `transaction_line_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Transaction line management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_line`
--

LOCK TABLES `transaction_line` WRITE;
/*!40000 ALTER TABLE `transaction_line` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `transaction_line` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `transaction_line_type`
--

DROP TABLE IF EXISTS `transaction_line_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction_line_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_transaction_line_type_code` (`code`),
  KEY `idx_transaction_line_type_status` (`status_id`),
  CONSTRAINT `fk_transaction_line_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Transaction line type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_line_type`
--

LOCK TABLES `transaction_line_type` WRITE;
/*!40000 ALTER TABLE `transaction_line_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `transaction_line_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `transaction_type`
--

DROP TABLE IF EXISTS `transaction_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_transaction_type_code` (`code`),
  KEY `idx_transaction_type_status` (`status_id`),
  CONSTRAINT `fk_transaction_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Transaction type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_type`
--

LOCK TABLES `transaction_type` WRITE;
/*!40000 ALTER TABLE `transaction_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `transaction_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `underwriting_answer`
--

DROP TABLE IF EXISTS `underwriting_answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `underwriting_answer` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `underwriting_question_id` int(11) NOT NULL COMMENT 'Reference to question',
  `answer_text` varchar(255) NOT NULL COMMENT 'Display text for answer',
  `answer_value` varchar(100) NOT NULL COMMENT 'Internal value for answer',
  `validation_rules` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'Answer-specific validation rules' CHECK (json_valid(`validation_rules`)),
  `display_order` int(11) DEFAULT 0 COMMENT 'Answer sequence',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_answer_question` (`underwriting_question_id`),
  KEY `idx_answer_value` (`answer_value`),
  KEY `idx_answer_status` (`status_id`),
  KEY `fk_answer_created_by` (`created_by`),
  KEY `fk_answer_updated_by` (`updated_by`),
  CONSTRAINT `fk_answer_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_answer_question` FOREIGN KEY (`underwriting_question_id`) REFERENCES `underwriting_question` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_answer_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_answer_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Answer options for underwriting questions';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `underwriting_answer`
--

LOCK TABLES `underwriting_answer` WRITE;
/*!40000 ALTER TABLE `underwriting_answer` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `underwriting_answer` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `underwriting_question`
--

DROP TABLE IF EXISTS `underwriting_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `underwriting_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `question_code` varchar(50) NOT NULL COMMENT 'Question identifier',
  `question_text` text NOT NULL COMMENT 'Question display text',
  `question_type` varchar(20) NOT NULL COMMENT 'yes_no, text, number, date',
  `is_required` tinyint(1) DEFAULT 1 COMMENT 'Required question',
  `display_order` int(11) DEFAULT 0 COMMENT 'Display sequence',
  `parent_question_id` int(11) DEFAULT NULL COMMENT 'Conditional parent question',
  `parent_answer` varchar(100) DEFAULT NULL COMMENT 'Parent answer to show this',
  `validation_rules` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'Validation configuration' CHECK (json_valid(`validation_rules`)),
  `help_text` text DEFAULT NULL COMMENT 'Help information',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_uw_question_code` (`question_code`),
  KEY `idx_uw_question_parent` (`parent_question_id`),
  KEY `fk_uw_question_status` (`status_id`),
  KEY `fk_uw_question_created_by` (`created_by`),
  KEY `fk_uw_question_updated_by` (`updated_by`),
  CONSTRAINT `fk_uw_question_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_uw_question_parent` FOREIGN KEY (`parent_question_id`) REFERENCES `underwriting_question` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_uw_question_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_uw_question_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Underwriting questions and answers per quote';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `underwriting_question`
--

LOCK TABLES `underwriting_question` WRITE;
/*!40000 ALTER TABLE `underwriting_question` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `underwriting_question` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `user_type_id` int(11) NOT NULL COMMENT 'Reference to user_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  `name_id` int(11) DEFAULT NULL COMMENT 'Reference to name table for user name',
  `role_id` int(11) DEFAULT NULL COMMENT 'Primary user role',
  `email` varchar(255) DEFAULT NULL COMMENT 'User email address',
  `phone` varchar(20) DEFAULT NULL COMMENT 'User phone number',
  `mfa_enabled` tinyint(1) DEFAULT 0 COMMENT 'Multi-factor auth enabled',
  `mfa_secret` varchar(255) DEFAULT NULL COMMENT 'MFA secret key',
  `email_verified` tinyint(1) DEFAULT 0 COMMENT 'Email verification status',
  `phone_verified` tinyint(1) DEFAULT 0 COMMENT 'Phone verification status',
  `last_login_at` timestamp NULL DEFAULT NULL COMMENT 'Last successful login',
  `failed_login_attempts` int(11) DEFAULT 0 COMMENT 'Failed login counter',
  `locked_until` timestamp NULL DEFAULT NULL COMMENT 'Account lock expiration',
  `password_changed_at` timestamp NULL DEFAULT NULL COMMENT 'Last password change',
  `signature_id` int(11) DEFAULT NULL COMMENT 'Reference to signature table',
  `language_preference_id` int(11) DEFAULT NULL COMMENT 'Preferred language',
  `password_reset_token` varchar(255) DEFAULT NULL COMMENT 'Password reset token',
  `password_reset_expires` timestamp NULL DEFAULT NULL COMMENT 'Password reset token expiration',
  `username` varchar(100) DEFAULT NULL COMMENT 'Login username',
  `password` varchar(255) DEFAULT NULL COMMENT 'Hashed password',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_user_email_unique` (`email`),
  UNIQUE KEY `unique_username` (`username`),
  KEY `idx_user_type` (`user_type_id`),
  KEY `idx_user_status` (`status_id`),
  KEY `idx_user_created` (`created_at`),
  KEY `idx_user_role` (`role_id`),
  KEY `fk_user_name` (`name_id`),
  KEY `fk_user_signature` (`signature_id`),
  KEY `fk_user_language` (`language_preference_id`),
  CONSTRAINT `fk_user_language` FOREIGN KEY (`language_preference_id`) REFERENCES `language` (`id`),
  CONSTRAINT `fk_user_name` FOREIGN KEY (`name_id`) REFERENCES `name` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_user_role` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_user_signature` FOREIGN KEY (`signature_id`) REFERENCES `signature` (`id`),
  CONSTRAINT `fk_user_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_user_type` FOREIGN KEY (`user_type_id`) REFERENCES `user_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='User management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `user_type`
--

DROP TABLE IF EXISTS `user_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_user_type_code` (`code`),
  KEY `idx_user_type_status` (`status_id`),
  CONSTRAINT `fk_user_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='User type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_type`
--

LOCK TABLES `user_type` WRITE;
/*!40000 ALTER TABLE `user_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `user_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `vehicle`
--

DROP TABLE IF EXISTS `vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `vehicle_type_id` int(11) NOT NULL COMMENT 'Reference to vehicle_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  `vin` varchar(17) DEFAULT NULL COMMENT 'Vehicle identification number',
  `year` int(11) DEFAULT NULL COMMENT 'Vehicle year',
  `make` varchar(50) DEFAULT NULL COMMENT 'Vehicle make',
  `model` varchar(50) DEFAULT NULL COMMENT 'Vehicle model',
  `vehicle_use_id` int(11) DEFAULT NULL COMMENT 'Reference to vehicle_use',
  `garaging_address_id` int(11) DEFAULT NULL COMMENT 'Reference to address',
  `body_style` varchar(50) DEFAULT NULL COMMENT 'Sedan, SUV, etc',
  `fuel_type` varchar(20) DEFAULT NULL COMMENT 'Gas, electric, hybrid',
  `annual_mileage` int(11) DEFAULT NULL COMMENT 'Estimated annual miles',
  `vehicle_ownership_type_id` int(11) DEFAULT NULL COMMENT 'Reference to ownership type',
  `primary_driver_id` int(11) DEFAULT NULL COMMENT 'Primary driver assignment',
  `vin_verified` tinyint(1) DEFAULT 0 COMMENT 'VIN verification status',
  PRIMARY KEY (`id`),
  KEY `idx_vehicle_type` (`vehicle_type_id`),
  KEY `idx_vehicle_status` (`status_id`),
  KEY `idx_vehicle_created` (`created_at`),
  KEY `idx_vehicle_vin` (`vin`),
  KEY `idx_vehicle_year_make_model` (`year`,`make`,`model`),
  KEY `fk_vehicle_use` (`vehicle_use_id`),
  KEY `fk_vehicle_address` (`garaging_address_id`),
  CONSTRAINT `fk_vehicle_address` FOREIGN KEY (`garaging_address_id`) REFERENCES `address` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_vehicle_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_vehicle_type` FOREIGN KEY (`vehicle_type_id`) REFERENCES `vehicle_type` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_vehicle_use` FOREIGN KEY (`vehicle_use_id`) REFERENCES `vehicle_use` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Vehicle management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle`
--

LOCK TABLES `vehicle` WRITE;
/*!40000 ALTER TABLE `vehicle` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `vehicle` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `vehicle_ownership_type`
--

DROP TABLE IF EXISTS `vehicle_ownership_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle_ownership_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(20) NOT NULL COMMENT 'Ownership type code',
  `name` varchar(50) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Ownership type description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default ownership type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_vehicle_ownership_code` (`code`),
  KEY `fk_vehicle_ownership_status` (`status_id`),
  KEY `fk_vehicle_ownership_created_by` (`created_by`),
  KEY `fk_vehicle_ownership_updated_by` (`updated_by`),
  CONSTRAINT `fk_vehicle_ownership_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_vehicle_ownership_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_vehicle_ownership_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Vehicle ownership types';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle_ownership_type`
--

LOCK TABLES `vehicle_ownership_type` WRITE;
/*!40000 ALTER TABLE `vehicle_ownership_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `vehicle_ownership_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `vehicle_type`
--

DROP TABLE IF EXISTS `vehicle_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_vehicle_type_code` (`code`),
  KEY `idx_vehicle_type_status` (`status_id`),
  CONSTRAINT `fk_vehicle_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Vehicle type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle_type`
--

LOCK TABLES `vehicle_type` WRITE;
/*!40000 ALTER TABLE `vehicle_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `vehicle_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `vehicle_use`
--

DROP TABLE IF EXISTS `vehicle_use`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle_use` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vehicle_use_type_id` int(11) NOT NULL,
  `code` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_vehicle_use_code` (`code`),
  KEY `idx_vehicle_use_type` (`vehicle_use_type_id`),
  KEY `idx_vehicle_use_status` (`status_id`),
  CONSTRAINT `fk_vehicle_use_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_vehicle_use_type` FOREIGN KEY (`vehicle_use_type_id`) REFERENCES `vehicle_use_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle_use`
--

LOCK TABLES `vehicle_use` WRITE;
/*!40000 ALTER TABLE `vehicle_use` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `vehicle_use` VALUES
(1,1,'PLEASURE','Pleasure','Personal pleasure driving only',1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(2,1,'COMMUTE','Commute to Work','Daily commute to work/school',1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(3,1,'BUSINESS','Business','Business use excluding commercial',1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(4,1,'FARM','Farm Use','Personal farm use',1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(5,2,'DELIVERY','Delivery','Commercial delivery service',1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(6,2,'SERVICE','Service Calls','Service or repair calls',1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(7,2,'SALES','Sales','Sales visits and demonstrations',1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(8,2,'TRANSPORT','Transportation','Passenger or goods transport',1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(9,2,'CONSTRUCTION','Construction','Construction site vehicle',1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(10,3,'RIDESHARE_PART','Part-time Rideshare','Part-time rideshare driver',1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(11,3,'RIDESHARE_FULL','Full-time Rideshare','Full-time rideshare driver',1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(12,3,'FOOD_DELIVERY','Food Delivery','Food delivery service',1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(13,3,'PACKAGE_DELIVERY','Package Delivery','Package delivery service',1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(14,4,'EMERGENCY','Emergency Vehicle','Emergency response vehicle',1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(15,4,'GOVERNMENT','Government','Government vehicle',1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(16,4,'EXHIBITION','Exhibition','Show or exhibition vehicle',1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(17,4,'RACING','Racing','Racing or track use',1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10');
/*!40000 ALTER TABLE `vehicle_use` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `vehicle_use_type`
--

DROP TABLE IF EXISTS `vehicle_use_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle_use_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `is_default` tinyint(1) DEFAULT 0,
  `status_id` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_vehicle_use_type_code` (`code`),
  KEY `idx_vehicle_use_type_status` (`status_id`),
  CONSTRAINT `fk_vehicle_use_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle_use_type`
--

LOCK TABLES `vehicle_use_type` WRITE;
/*!40000 ALTER TABLE `vehicle_use_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `vehicle_use_type` VALUES
(1,'PERSONAL','Personal Use','Personal vehicle use categories',1,1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(2,'COMMERCIAL','Commercial Use','Commercial vehicle use categories',0,1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(3,'RIDESHARE','Rideshare Use','Rideshare and delivery use categories',0,1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10'),
(4,'SPECIALTY','Specialty Use','Special purpose vehicle uses',0,1,1,1,'2025-07-21 16:03:10','2025-07-21 16:03:10');
/*!40000 ALTER TABLE `vehicle_use_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `verification`
--

DROP TABLE IF EXISTS `verification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `verification` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `verification_type_id` int(11) NOT NULL COMMENT 'Reference to verification_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_verification_type` (`verification_type_id`),
  KEY `idx_verification_status` (`status_id`),
  KEY `idx_verification_created` (`created_at`),
  CONSTRAINT `fk_verification_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_verification_type` FOREIGN KEY (`verification_type_id`) REFERENCES `verification_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Verification management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `verification`
--

LOCK TABLES `verification` WRITE;
/*!40000 ALTER TABLE `verification` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `verification` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `verification_type`
--

DROP TABLE IF EXISTS `verification_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `verification_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_verification_type_code` (`code`),
  KEY `idx_verification_type_status` (`status_id`),
  CONSTRAINT `fk_verification_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Verification type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `verification_type`
--

LOCK TABLES `verification_type` WRITE;
/*!40000 ALTER TABLE `verification_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `verification_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `violation`
--

DROP TABLE IF EXISTS `violation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `violation` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `violation_type_id` int(11) NOT NULL COMMENT 'Reference to violation type',
  `violation_date` date NOT NULL COMMENT 'Date of violation',
  `description` text DEFAULT NULL COMMENT 'Violation description',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_violation_type` (`violation_type_id`),
  KEY `idx_violation_date` (`violation_date`),
  KEY `fk_violation_status` (`status_id`),
  KEY `fk_violation_created_by` (`created_by`),
  KEY `fk_violation_updated_by` (`updated_by`),
  CONSTRAINT `fk_violation_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_violation_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_violation_type` FOREIGN KEY (`violation_type_id`) REFERENCES `violation_type` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_violation_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Driver violations';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `violation`
--

LOCK TABLES `violation` WRITE;
/*!40000 ALTER TABLE `violation` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `violation` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `violation_type`
--

DROP TABLE IF EXISTS `violation_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `violation_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(20) NOT NULL COMMENT 'Violation type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Violation description',
  `severity_level` int(11) DEFAULT 1 COMMENT 'Severity level 1-5',
  `points` int(11) DEFAULT 0 COMMENT 'Points assigned',
  `is_major` tinyint(1) DEFAULT 0 COMMENT 'Major violation flag',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default violation type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_violation_type_code` (`code`),
  KEY `fk_violation_type_status` (`status_id`),
  KEY `fk_violation_type_created_by` (`created_by`),
  KEY `fk_violation_type_updated_by` (`updated_by`),
  CONSTRAINT `fk_violation_type_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_violation_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_violation_type_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Violation type reference';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `violation_type`
--

LOCK TABLES `violation_type` WRITE;
/*!40000 ALTER TABLE `violation_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `violation_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `witness`
--

DROP TABLE IF EXISTS `witness`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `witness` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `witness_type_id` int(11) NOT NULL COMMENT 'Reference to witness_type',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  KEY `idx_witness_type` (`witness_type_id`),
  KEY `idx_witness_status` (`status_id`),
  KEY `idx_witness_created` (`created_at`),
  CONSTRAINT `fk_witness_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_witness_type` FOREIGN KEY (`witness_type_id`) REFERENCES `witness_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Witness management following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `witness`
--

LOCK TABLES `witness` WRITE;
/*!40000 ALTER TABLE `witness` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `witness` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `witness_type`
--

DROP TABLE IF EXISTS `witness_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `witness_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(50) NOT NULL COMMENT 'Unique type code',
  `name` varchar(100) NOT NULL COMMENT 'Display name',
  `description` text DEFAULT NULL COMMENT 'Detailed description',
  `is_default` tinyint(1) DEFAULT 0 COMMENT 'Default selection flag',
  `status_id` int(11) DEFAULT NULL COMMENT 'Reference to status table',
  `created_by` int(11) DEFAULT NULL COMMENT 'User who created record',
  `updated_by` int(11) DEFAULT NULL COMMENT 'User who last updated record',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_witness_type_code` (`code`),
  KEY `idx_witness_type_status` (`status_id`),
  CONSTRAINT `fk_witness_type_status` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Witness type categorization following GR-41 standards';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `witness_type`
--

LOCK TABLES `witness_type` WRITE;
/*!40000 ALTER TABLE `witness_type` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `witness_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `zip_code`
--

DROP TABLE IF EXISTS `zip_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `zip_code` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier',
  `code` varchar(10) NOT NULL COMMENT 'ZIP code',
  `city_id` int(11) NOT NULL COMMENT 'Reference to city',
  `created_at` timestamp NULL DEFAULT current_timestamp() COMMENT 'Creation timestamp',
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last update timestamp',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_zip_code` (`code`),
  KEY `idx_zip_city` (`city_id`),
  CONSTRAINT `fk_zip_city` FOREIGN KEY (`city_id`) REFERENCES `city` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ZIP code reference table';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zip_code`
--

LOCK TABLES `zip_code` WRITE;
/*!40000 ALTER TABLE `zip_code` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `zip_code` ENABLE KEYS */;
UNLOCK TABLES;
commit;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-07-27 16:35:44
