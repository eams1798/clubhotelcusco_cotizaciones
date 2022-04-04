-- MySQL dump 10.13  Distrib 5.7.37, for Linux (x86_64)
--
-- Host: localhost    Database: clubhotelcusco_db
-- ------------------------------------------------------
-- Server version	5.7.37

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
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cliente` (
  `id` varchar(60) NOT NULL,
  `creado` datetime DEFAULT NULL,
  `actualizado` datetime DEFAULT NULL,
  `nombre` varchar(128) NOT NULL,
  `apellido` varchar(128) NOT NULL,
  `dni` int(11) DEFAULT NULL,
  `direccion` varchar(256) DEFAULT NULL,
  `telefono` int(11) DEFAULT NULL,
  `correo` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES ('10f59b5f-193a-4d00-89f7-73f3945488f8','2022-04-02 21:43:22','2022-04-02 21:43:22','Emilia','Mayta Ramírez',57829463,'Av. de Prueba N°0000 - Pueblo Mágico',963852741,NULL),('82365ebb-73e4-4bbc-9311-0970acc70111','2022-04-02 21:43:10','2022-04-02 21:43:10','Willy','Quispe',95453789,'Mz. 99 - Lt. ZE999 - Urb. Ficticia de Prueba - Pueblo Mágico',999555111,NULL);
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cotizacion`
--

DROP TABLE IF EXISTS `cotizacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cotizacion` (
  `id` varchar(60) NOT NULL,
  `creado` datetime DEFAULT NULL,
  `actualizado` datetime DEFAULT NULL,
  `clienteId` varchar(60) NOT NULL,
  `numAdultos` int(11) DEFAULT NULL,
  `numJovenes` int(11) DEFAULT NULL,
  `numNinos` int(11) DEFAULT NULL,
  `fechaEvento` datetime NOT NULL,
  `tipoEvento` varchar(128) NOT NULL,
  `estadoSolicitud` varchar(50) NOT NULL,
  `descuento` float DEFAULT NULL,
  `cantidadProductos` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `clienteId` (`clienteId`),
  CONSTRAINT `cotizacion_ibfk_1` FOREIGN KEY (`clienteId`) REFERENCES `cliente` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cotizacion`
--

LOCK TABLES `cotizacion` WRITE;
/*!40000 ALTER TABLE `cotizacion` DISABLE KEYS */;
INSERT INTO `cotizacion` VALUES ('5c6b84fa-8c5c-4f17-9f20-76cec4651dd7','2022-04-02 22:20:11','2022-04-02 22:20:11','82365ebb-73e4-4bbc-9311-0970acc70111',12,56,0,'2021-01-11 18:00:00','Quinceañera','Aprobado',0.1,'{\"ae97d225-6453-46dc-adf2-37a2fba3cf74\": 4, \"c94153cb-b825-44ce-994a-5d6f52282b2a\": 5, \"d06552fe-4e85-4a40-877f-e524b93fbe27\": 6, \"f60ca44c-e1da-4691-a7c7-be56fac3430a\": 7}'),('97b0c088-6171-4c2e-8372-d2ead824f4e3','2022-04-02 22:07:38','2022-04-02 22:07:38','10f59b5f-193a-4d00-89f7-73f3945488f8',108,45,18,'2019-07-25 22:30:00','Boda','Pendiente',0,'{\"2419352a-3add-4c51-ae50-444c9ab559a8\": 1, \"498baf8b-d6a9-4bc5-9659-fa6a418608da\": 2, \"ae97d225-6453-46dc-adf2-37a2fba3cf74\": 3}');
/*!40000 ALTER TABLE `cotizacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plantilla`
--

DROP TABLE IF EXISTS `plantilla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `plantilla` (
  `id` varchar(60) NOT NULL,
  `creado` datetime DEFAULT NULL,
  `actualizado` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plantilla`
--

LOCK TABLES `plantilla` WRITE;
/*!40000 ALTER TABLE `plantilla` DISABLE KEYS */;
/*!40000 ALTER TABLE `plantilla` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `producto` (
  `id` varchar(60) NOT NULL,
  `creado` datetime DEFAULT NULL,
  `actualizado` datetime DEFAULT NULL,
  `codigo` varchar(16) NOT NULL,
  `nombre` varchar(128) NOT NULL,
  `proveedor` varchar(128) DEFAULT NULL,
  `precioPorUnidad` float DEFAULT NULL,
  `tipoUnidad` varchar(20) NOT NULL,
  `capacidadPorUnidad` float DEFAULT NULL,
  `publicoObjetivo` varchar(20) NOT NULL,
  `productoOservicio` varchar(10) NOT NULL,
  `categoria` varchar(32) NOT NULL,
  `descripcion1` varchar(512) DEFAULT NULL,
  `descripcion2` varchar(512) DEFAULT NULL,
  `enStock` float DEFAULT NULL,
  `enOrden` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES ('2419352a-3add-4c51-ae50-444c9ab559a8','2022-04-02 21:42:38','2022-04-02 21:42:38','GMU','grupo musical','Ritmo Corazón',1950.79,'unidad',1,'todos','Servicio','Personal externo','lorem ipsum','dolor sit amet',25,17),('498baf8b-d6a9-4bc5-9659-fa6a418608da','2022-04-02 21:41:50','2022-04-02 21:41:50','PAN','papas andinas','Hotel Cusco',96.5,'kilo',10,'jovenes','Producto','Entradas','lorem ipsum','dolor sit amet',25,17),('ae97d225-6453-46dc-adf2-37a2fba3cf74','2022-04-02 21:42:09','2022-04-02 21:42:09','BOC','bocaditos de boda','No especificado',198,'unidad',160,'niños','Producto','Entremeses','lorem ipsum','dolor sit amet',12,12),('c94153cb-b825-44ce-994a-5d6f52282b2a','2022-04-02 21:42:52','2022-04-02 21:42:52','EQS','equipo de sonido','No especificado',1024,'unidad',1,'todos','Servicio','Música','lorem ipsum','dolor sit amet',25,17),('d06552fe-4e85-4a40-877f-e524b93fbe27','2022-04-02 21:42:25','2022-04-02 21:42:25','EST','estacionamiento','Hotel Cusco',0,'unidad',16,'adultos','Servicio','Alquiler de zonas','lorem ipsum','dolor sit amet',32,1),('f60ca44c-e1da-4691-a7c7-be56fac3430a','2022-04-02 21:27:55','2022-04-02 21:40:19','VCQ','vino Colqui','Hotel Cusco',108.5,'copas',4,'adultos','Producto','Bebidas','lorem ipsum','dolor sit amet',25,17);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto_cotizacion`
--

DROP TABLE IF EXISTS `producto_cotizacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `producto_cotizacion` (
  `productoId` varchar(60) NOT NULL,
  `cotizacionId` varchar(60) NOT NULL,
  PRIMARY KEY (`productoId`,`cotizacionId`),
  KEY `cotizacionId` (`cotizacionId`),
  CONSTRAINT `producto_cotizacion_ibfk_1` FOREIGN KEY (`productoId`) REFERENCES `producto` (`id`),
  CONSTRAINT `producto_cotizacion_ibfk_2` FOREIGN KEY (`cotizacionId`) REFERENCES `cotizacion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto_cotizacion`
--

LOCK TABLES `producto_cotizacion` WRITE;
/*!40000 ALTER TABLE `producto_cotizacion` DISABLE KEYS */;
INSERT INTO `producto_cotizacion` VALUES ('ae97d225-6453-46dc-adf2-37a2fba3cf74','5c6b84fa-8c5c-4f17-9f20-76cec4651dd7'),('c94153cb-b825-44ce-994a-5d6f52282b2a','5c6b84fa-8c5c-4f17-9f20-76cec4651dd7'),('d06552fe-4e85-4a40-877f-e524b93fbe27','5c6b84fa-8c5c-4f17-9f20-76cec4651dd7'),('f60ca44c-e1da-4691-a7c7-be56fac3430a','5c6b84fa-8c5c-4f17-9f20-76cec4651dd7'),('2419352a-3add-4c51-ae50-444c9ab559a8','97b0c088-6171-4c2e-8372-d2ead824f4e3'),('498baf8b-d6a9-4bc5-9659-fa6a418608da','97b0c088-6171-4c2e-8372-d2ead824f4e3'),('ae97d225-6453-46dc-adf2-37a2fba3cf74','97b0c088-6171-4c2e-8372-d2ead824f4e3');
/*!40000 ALTER TABLE `producto_cotizacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedor`
--

DROP TABLE IF EXISTS `proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proveedor` (
  `id` varchar(60) NOT NULL,
  `creado` datetime DEFAULT NULL,
  `actualizado` datetime DEFAULT NULL,
  `nombreEmpresa` varchar(128) NOT NULL,
  `ruc` bigint(20) DEFAULT NULL,
  `nombreContacto` varchar(128) DEFAULT NULL,
  `direccion` varchar(128) DEFAULT NULL,
  `telefono` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedor`
--

LOCK TABLES `proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor` DISABLE KEYS */;
/*!40000 ALTER TABLE `proveedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuario` (
  `id` varchar(60) NOT NULL,
  `creado` datetime DEFAULT NULL,
  `actualizado` datetime DEFAULT NULL,
  `nombre` varchar(128) NOT NULL,
  `apellido` varchar(128) NOT NULL,
  `dni` int(11) DEFAULT NULL,
  `direccion` varchar(256) DEFAULT NULL,
  `telefono` int(11) DEFAULT NULL,
  `correo` varchar(128) NOT NULL,
  `contrasenia` varchar(128) NOT NULL,
  `rol` varchar(128) NOT NULL,
  `estado` varchar(32) NOT NULL,
  `loggedIn` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES ('5733c055-51c6-47b1-b83c-a7734d797294','2022-04-02 21:43:49','2022-04-02 22:25:18','Alex Armando','Juárez De la Vega',88442211,'Calle de Prueba N°9999 - Pueblo Mágico',986753421,'alexalv@gmail.com','a4075d561b723f7b8979d59a467c2fe6','gerente','activo',0),('a26e1510-5538-4012-b99c-cc27ac9a9890','2022-04-02 21:44:22','2022-04-02 21:44:22','Melany','Vargas',96857430,'Av. Tomasa Tito Condemayta Nro. 903',999000115,'melabc@clubhotelcusco.com','135082d54241877a0cdfe97f67a6b862','dueña','activo',0),('cda4a425-a20c-4868-9c3e-7813569da6ff','2022-04-02 21:44:06','2022-04-02 21:44:06','Camilo','Guairá',74968502,'remoto',999000115,'camg123@yahoo.net','11ffc823672a780dc7d9c42eea4561d7','empleado','en recuperación',0);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-03 18:36:47
