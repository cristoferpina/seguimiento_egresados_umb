-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 06, 2026 at 07:38 PM
-- Server version: 8.4.3
-- PHP Version: 8.3.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `seguimiento_egresados_umb`
--

-- --------------------------------------------------------

--
-- Table structure for table `carreras`
--

CREATE TABLE `carreras` (
  `id_carrera` int NOT NULL,
  `nombre_carrera` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `fecha_registro` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `id_ues` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `carreras`
--

INSERT INTO `carreras` (`id_carrera`, `nombre_carrera`, `fecha_registro`, `id_ues`) VALUES
(1, 'Ingenieria en Sistemas Computacionales', '13-10-2004', 1),
(2, 'Ingenieria en Innovacion Agricola Sustentable', '13-10-2004', 1),
(3, 'Licenciatura en Contaduria', '13-10-2004', 1);

-- --------------------------------------------------------

--
-- Table structure for table `control_escolar`
--

CREATE TABLE `control_escolar` (
  `id_control` int NOT NULL,
  `nombre_control` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `apellido_paterno` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `apellido_materno` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `numero_empleado` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `id_ues` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `control_escolar`
--

INSERT INTO `control_escolar` (`id_control`, `nombre_control`, `apellido_paterno`, `apellido_materno`, `numero_empleado`, `password`, `id_ues`) VALUES
(1, 'Estefania', 'Ytezen', 'Nava', '130002', '1234', 1);

-- --------------------------------------------------------

--
-- Table structure for table `coordinador`
--

CREATE TABLE `coordinador` (
  `id_coordinador` int NOT NULL,
  `nombre_coordinador` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `apellido_paterno` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `apellido_materno` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `numero_empleado` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `id_ues` int DEFAULT NULL,
  `fotografia` varchar(500) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `coordinador`
--

INSERT INTO `coordinador` (`id_coordinador`, `nombre_coordinador`, `apellido_paterno`, `apellido_materno`, `numero_empleado`, `password`, `id_ues`, `fotografia`) VALUES
(1, 'Luis Ramón', 'Vega', 'Ramirez', '130001', '1234', 1, '');

-- --------------------------------------------------------

--
-- Table structure for table `egresados`
--

CREATE TABLE `egresados` (
  `id_egresado` int NOT NULL,
  `nombre_encargado` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `apellido_paterno` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `apellido_materno` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `id_bot` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `telefono` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `correo` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `ni` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `ne` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `generacion` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `modalidad` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `documentos` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `estatus_laboral` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `matricula` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `fotografia` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `estatus_titulacion` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `perfil` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `id_carrera` int DEFAULT NULL,
  `id_ues` int DEFAULT NULL,
  `id_municipio` int DEFAULT NULL,
  `id_localidad` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `egresados`
--

INSERT INTO `egresados` (`id_egresado`, `nombre_encargado`, `apellido_paterno`, `apellido_materno`, `id_bot`, `telefono`, `correo`, `ni`, `ne`, `generacion`, `modalidad`, `documentos`, `estatus_laboral`, `matricula`, `fotografia`, `estatus_titulacion`, `password`, `perfil`, `id_carrera`, `id_ues`, `id_municipio`, `id_localidad`) VALUES
(1, 'Rosalia', 'Vila', 'Tobella', '', '7121948875', 'rosalia@gmail.com', '0000', '0000', '2012', 'I', 'Constancia', 'Desempleado', '13120006', 'uploads/egresados/13220031.jpeg', 'Titulado', '1234', 'Ingeniero', 1, 1, 1, NULL),
(2, 'Juan', 'Lopez', 'Gonzalez', '', '55555555', 'cristoferpil324@gmail.com', '0000', '0000', '2022-2026', 'II', 'uploads\\modalidades\\13220031.pdf', 'Empleado', '13220031', 'uploads/egresados/1.jpg', 'Pendiente', '1234', 'Ingeniero', 1, 2, 2, 2),
(3, 'Cristofer', 'Piña', 'Rodriguez', '', '5633470252', 'cristoferpil324@gmail.com', '0000', '0000', '2022-2026', 'III', 'uploads\\modalidades\\13220030.pdf', 'Desempleado', '13220030', 'uploads/egresados/13220030.jpeg', 'Titulado', '1234', 'Ingeniero', 1, 1, 1, 1),
(4, 'Jesús Andrés', 'Mondragón', 'Tenorio', '', '7121002222', 'andres@gmail.com', '0000', '0000', '2022-2026', 'I', 'uploads\\modalidades\\13220010.pdf', 'Desempleado', '13220010', 'uploads/egresados/13220010.jpg', 'Titulado', 'scrypt:32768:8:1$QXT', 'Igeniero', 1, 1, 1, 1),
(5, 'Jesús ', 'Martinez', 'Narciso', '', '7121002222', 'narciso@gmail.com', '0000', '0000', '2022-2026', 'III', 'uploads\\modalidades\\13220010.pdf', 'Empleado', '13220010', 'uploads/egresados/13220010.jpg', 'Titulado', 'scrypt:32768:8:1$J0H', 'Igeniero', 1, 1, 2, 2),
(6, 'Alejendro', 'Sanchez', 'Garcia', '', '7121002222', 'alex@gmail.com', '0000', '0000', '2022-2026', '', '', 'Empleado', '13220010', 'uploads/egresados/13220010.jpg', 'No titulado', 'scrypt:32768:8:1$sui', 'Igeniero', 1, 1, 3, 3),
(7, 'Lizeth', 'Moreno', 'Piña', '', '7121002222', 'Lizeth@gmail.com', '0000', '0000', '2022-2026', 'IX', '', 'Empleado', '13220099', 'uploads/egresados/13220099.jpg', 'Titulado', 'scrypt:32768:8:1$T5H', 'Igeniero', 1, 1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `encargado_hct`
--

CREATE TABLE `encargado_hct` (
  `id_encargado` int NOT NULL,
  `nombre_encargado` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `apellido_paterno` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `apellido_materno` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `numero_empleado` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `perfil` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `id_carrera` int DEFAULT NULL,
  `id_ues` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `encargado_hct`
--

INSERT INTO `encargado_hct` (`id_encargado`, `nombre_encargado`, `apellido_paterno`, `apellido_materno`, `numero_empleado`, `password`, `perfil`, `id_carrera`, `id_ues`) VALUES
(1, 'Gerardo', 'Moreno', 'de Jesús', '130003', '1234', 'Ingeniero en Sistemas', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `localidades`
--

CREATE TABLE `localidades` (
  `id_localidad` int NOT NULL,
  `nombre_localidad` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `id_municipio` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `localidades`
--

INSERT INTO `localidades` (`id_localidad`, `nombre_localidad`, `id_municipio`) VALUES
(1, 'San Joaquín la Millas', 1),
(2, 'Palizada', 2),
(3, 'Santa Ana Nichi', 3);

-- --------------------------------------------------------

--
-- Table structure for table `municipios`
--

CREATE TABLE `municipios` (
  `id_municipio` int NOT NULL,
  `nombre_municipio` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `estado` varchar(100) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `municipios`
--

INSERT INTO `municipios` (`id_municipio`, `nombre_municipio`, `estado`) VALUES
(1, 'San José del Rincón', 'Estado de Mexico'),
(2, 'Villa victoria', 'Estado de México'),
(3, 'San Felipe del Progreso', 'Estado de México');

-- --------------------------------------------------------

--
-- Table structure for table `ues`
--

CREATE TABLE `ues` (
  `id_ues` int NOT NULL,
  `nombre_ues` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `cct` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `fecha_registro` varchar(10) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ues`
--

INSERT INTO `ues` (`id_ues`, `nombre_ues`, `cct`, `fecha_registro`) VALUES
(1, 'UES San Jose del Rincon', '15ESU0018H', '13-10-2009'),
(2, 'UES Villa Victoria', '15ESU0018R', '13-10-2009'),
(3, 'UES El Oro', '15ESU0018J', '13-10-2009');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `carreras`
--
ALTER TABLE `carreras`
  ADD PRIMARY KEY (`id_carrera`),
  ADD KEY `id_ues` (`id_ues`);

--
-- Indexes for table `control_escolar`
--
ALTER TABLE `control_escolar`
  ADD PRIMARY KEY (`id_control`),
  ADD KEY `id_ues` (`id_ues`);

--
-- Indexes for table `coordinador`
--
ALTER TABLE `coordinador`
  ADD PRIMARY KEY (`id_coordinador`),
  ADD KEY `id_ues` (`id_ues`);

--
-- Indexes for table `egresados`
--
ALTER TABLE `egresados`
  ADD PRIMARY KEY (`id_egresado`),
  ADD KEY `id_ues` (`id_ues`),
  ADD KEY `id_carrera` (`id_carrera`),
  ADD KEY `id_municipio` (`id_municipio`),
  ADD KEY `id_localidad` (`id_localidad`);

--
-- Indexes for table `encargado_hct`
--
ALTER TABLE `encargado_hct`
  ADD PRIMARY KEY (`id_encargado`),
  ADD KEY `id_ues` (`id_ues`),
  ADD KEY `id_carrera` (`id_carrera`);

--
-- Indexes for table `localidades`
--
ALTER TABLE `localidades`
  ADD PRIMARY KEY (`id_localidad`),
  ADD KEY `id_municipio` (`id_municipio`);

--
-- Indexes for table `municipios`
--
ALTER TABLE `municipios`
  ADD PRIMARY KEY (`id_municipio`);

--
-- Indexes for table `ues`
--
ALTER TABLE `ues`
  ADD PRIMARY KEY (`id_ues`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `carreras`
--
ALTER TABLE `carreras`
  MODIFY `id_carrera` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `control_escolar`
--
ALTER TABLE `control_escolar`
  MODIFY `id_control` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `coordinador`
--
ALTER TABLE `coordinador`
  MODIFY `id_coordinador` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `egresados`
--
ALTER TABLE `egresados`
  MODIFY `id_egresado` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `encargado_hct`
--
ALTER TABLE `encargado_hct`
  MODIFY `id_encargado` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `localidades`
--
ALTER TABLE `localidades`
  MODIFY `id_localidad` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `municipios`
--
ALTER TABLE `municipios`
  MODIFY `id_municipio` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `ues`
--
ALTER TABLE `ues`
  MODIFY `id_ues` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `carreras`
--
ALTER TABLE `carreras`
  ADD CONSTRAINT `carreras_ibfk_1` FOREIGN KEY (`id_ues`) REFERENCES `ues` (`id_ues`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `control_escolar`
--
ALTER TABLE `control_escolar`
  ADD CONSTRAINT `control_escolar_ibfk_1` FOREIGN KEY (`id_ues`) REFERENCES `ues` (`id_ues`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `coordinador`
--
ALTER TABLE `coordinador`
  ADD CONSTRAINT `coordinador_ibfk_1` FOREIGN KEY (`id_ues`) REFERENCES `ues` (`id_ues`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `egresados`
--
ALTER TABLE `egresados`
  ADD CONSTRAINT `egresados_ibfk_1` FOREIGN KEY (`id_ues`) REFERENCES `ues` (`id_ues`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `egresados_ibfk_2` FOREIGN KEY (`id_carrera`) REFERENCES `carreras` (`id_carrera`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `egresados_ibfk_3` FOREIGN KEY (`id_municipio`) REFERENCES `municipios` (`id_municipio`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `egresados_ibfk_4` FOREIGN KEY (`id_localidad`) REFERENCES `localidades` (`id_localidad`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `encargado_hct`
--
ALTER TABLE `encargado_hct`
  ADD CONSTRAINT `encargado_hct_ibfk_1` FOREIGN KEY (`id_ues`) REFERENCES `ues` (`id_ues`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `encargado_hct_ibfk_2` FOREIGN KEY (`id_carrera`) REFERENCES `carreras` (`id_carrera`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `localidades`
--
ALTER TABLE `localidades`
  ADD CONSTRAINT `localidades_ibfk_1` FOREIGN KEY (`id_municipio`) REFERENCES `municipios` (`id_municipio`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
