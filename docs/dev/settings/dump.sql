# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: account-dev.cbrh124qj1x0.ap-northeast-2.rds.amazonaws.com (MySQL 5.5.5-10.1.31-MariaDB)
# Database: account
# Generation Time: 2018-12-03 07:02:45 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table oauth2_application
# ------------------------------------------------------------

DROP TABLE IF EXISTS `oauth2_application`;

CREATE TABLE `oauth2_application` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `oauth2_user_id` int(10) unsigned NOT NULL,
  `client_id` varchar(100) NOT NULL,
  `redirect_uris` longtext NOT NULL,
  `client_secret` varchar(255) NOT NULL,
  `skip_authorization` tinyint(1) NOT NULL,
  `client_type` varchar(32) NOT NULL,
  `authorization_grant_type` varchar(32) NOT NULL,
  `is_in_house` tinyint(1) NOT NULL,
  `jwt_alg` varchar(6) NOT NULL,
  `jwt_hs_256_secret` varchar(32) NOT NULL,
  `created` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `client_id` (`client_id`),
  KEY `oauth2_application_client_secret_33d565b4` (`client_secret`),
  KEY `oauth2_user_id` (`oauth2_user_id`),
  CONSTRAINT `oauth2_application_ibfk_2` FOREIGN KEY (`oauth2_user_id`) REFERENCES `oauth2_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `oauth2_application` WRITE;
/*!40000 ALTER TABLE `oauth2_application` DISABLE KEYS */;

INSERT INTO `oauth2_application` (`id`, `name`, `oauth2_user_id`, `client_id`, `redirect_uris`, `client_secret`, `skip_authorization`, `client_type`, `authorization_grant_type`, `is_in_house`, `jwt_alg`, `jwt_hs_256_secret`, `created`, `last_modified`)
VALUES
	(1,'Ridibooks',1,'Nkt2Xdc0zMuWmye6MSkYgqCh9q6JjeMCsUiH1kgL','https://account.dev.ridi.io/ridi/callback/ https://dev.ridi.io app://authorizedhttps://view.ridibooks.com/books/ app://authorized https://local.ridi.io https://select.local.ridi.io https://test.ridi.io https://pay.ridi.io\nhttps://pay.local.ridi.io/ https://library.dev.ridi.io/ https://library.local.ridi.io/','TJcf9DgxFCFpgA6k5ESnsK49i0MUwbjkkzznLMfj9KGfTbiwtI3HPlQsc20V5prrrOx7wOn2Mbx7x0ngEp7gWOCQnBJzpXhNVtygAOYV9cxEhFRB5GYhEtg7RvGLnaSt',1,'confidential','authorization-code',1,'HS256','Ad!YB4G,]Gp-cnKO\\|/){}1_4@4ASpjZ','2018-04-03 18:13:35','2018-04-03 18:13:35'),
	(3,'Ridibooks',1,'6CGJqfEDvjC88eFVX2Wd3cQykkh2n6V4jTdFb22J','','Y8KtbgF5rfdVUx5Vr7QGugh3LP5FtCPBPkuDCscNhZFL7rPn3Vd2M28YuC7JVSc6K4YydN38dJMgqWCdDUrRzeyfKW2TAeZfgPKQUuNq4VJCxtQsxcMW7Zg4nwBMDqLW',1,'confidential','password',0,'HS256','Ad!YB4G,]Gp-cnKO\\|/){}1_4@4ASpjZ','2018-04-03 18:13:35','2018-04-03 18:13:35');

/*!40000 ALTER TABLE `oauth2_application` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table oauth2_grant
# ------------------------------------------------------------

DROP TABLE IF EXISTS `oauth2_grant`;

CREATE TABLE `oauth2_grant` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(255) NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `application_id` bigint(20) unsigned NOT NULL,
  `redirect_uri` longtext NOT NULL,
  `scope` longtext NOT NULL,
  `expires` datetime NOT NULL,
  `created` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `user_id` (`user_id`),
  KEY `application_id` (`application_id`),
  CONSTRAINT `oauth2_grant_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`idx`),
  CONSTRAINT `oauth2_grant_ibfk_2` FOREIGN KEY (`application_id`) REFERENCES `oauth2_application` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `oauth2_grant` WRITE;
/*!40000 ALTER TABLE `oauth2_grant` DISABLE KEYS */;

INSERT INTO `oauth2_grant` (`id`, `code`, `user_id`, `application_id`, `redirect_uri`, `scope`, `expires`, `created`, `last_modified`)
VALUES
	(68,'olJs7IPVxt2XmuwLdk9u8As7eHtyHf',9,1,'https://account.dev.ridi.com/ridi/callback/','all','2019-06-20 22:08:43','2018-06-20 21:58:43','2018-06-20 21:58:43');

/*!40000 ALTER TABLE `oauth2_grant` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table oauth2_refreshtoken
# ------------------------------------------------------------

DROP TABLE IF EXISTS `oauth2_refreshtoken`;

CREATE TABLE `oauth2_refreshtoken` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `token` varchar(255) NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `application_id` bigint(20) unsigned NOT NULL,
  `scope` longtext NOT NULL,
  `expires` datetime NOT NULL,
  `created` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  `revoked` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  KEY `application_id` (`application_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `oauth2_refreshtoken_ibfk_1` FOREIGN KEY (`application_id`) REFERENCES `oauth2_application` (`id`),
  CONSTRAINT `oauth2_refreshtoken_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`idx`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `oauth2_refreshtoken` WRITE;
/*!40000 ALTER TABLE `oauth2_refreshtoken` DISABLE KEYS */;

INSERT INTO `oauth2_refreshtoken` (`id`, `token`, `user_id`, `application_id`, `scope`, `expires`, `created`, `last_modified`, `revoked`)
VALUES
	(3721,'PpR41hR2xqBTH5uo6OAYM3RIbwgeIL',2141717,1,'all','2018-12-03 17:23:55','2018-11-03 17:23:55','2018-11-03 17:23:55',NULL);

/*!40000 ALTER TABLE `oauth2_refreshtoken` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table oauth2_user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `oauth2_user`;

CREATE TABLE `oauth2_user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(16) NOT NULL,
  `created` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `oauth2_user` WRITE;
/*!40000 ALTER TABLE `oauth2_user` DISABLE KEYS */;

INSERT INTO `oauth2_user` (`id`, `name`, `created`, `last_modified`)
VALUES
	(1,'Ridibooks','0000-00-00 00:00:00','0000-00-00 00:00:00');

/*!40000 ALTER TABLE `oauth2_user` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `idx` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id` varchar(32) NOT NULL DEFAULT '',
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `created` datetime NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY (`idx`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;

INSERT INTO `user` (`idx`, `id`, `password`, `last_login`, `created`, `last_modified`)
VALUES
	(2,'spinerve','',NULL,'2018-07-04 14:55:09','2018-07-04 14:55:09');

/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
