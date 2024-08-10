-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 03-12-2023 a las 17:22:00
-- Versión del servidor: 8.0.31
-- Versión de PHP: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `libreriajpva2614986`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `autores`
--

DROP TABLE IF EXISTS `autores`;
CREATE TABLE IF NOT EXISTS `autores` (
  `id_autor` int NOT NULL AUTO_INCREMENT,
  `nombres` varchar(25) NOT NULL,
  `apellidos` varchar(25) NOT NULL,
  `estado` varchar(10) NOT NULL DEFAULT 'ACTIVO',
  PRIMARY KEY (`id_autor`)
) ENGINE=MyISAM AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `autores`
--

INSERT INTO `autores` (`id_autor`, `nombres`, `apellidos`, `estado`) VALUES
(1, 'Marc', 'Cerasini', 'ACTIVO'),
(2, 'Julio', 'Verne', 'ACTIVO'),
(3, 'Edgar', 'Allan Poe', 'ACTIVO'),
(4, 'Mary', 'Wollstonecraft Shelley', 'ACTIVO'),
(5, 'Ben', 'Mezrich', 'ACTIVO'),
(6, 'Bram', 'Stoker', 'ACTIVO'),
(7, 'Bruno', 'Nievas', 'ACTIVO'),
(8, 'César', 'García Muñoz', 'ACTIVO'),
(9, 'Armando', 'Rodera', 'ACTIVO'),
(10, 'Jane', 'Austen', 'ACTIVO'),
(11, 'Emily', 'Bronte', 'ACTIVO'),
(12, 'Alejandro', 'Dumas', 'ACTIVO'),
(13, 'Gabriel', 'García Márquez', 'ACTIVO'),
(14, 'Nikos', 'Kazantzakis', 'ACTIVO'),
(15, 'Raymond', 'Carver', 'ACTIVO'),
(16, 'Umberto', 'Eco', 'ACTIVO'),
(17, 'Ernest', 'Hemingway', 'ACTIVO'),
(18, 'Toni', 'Morrison', 'ACTIVO'),
(19, 'Haruki', 'Murakami', 'ACTIVO'),
(20, 'J.K.', 'Rowling', 'ACTIVO'),
(21, 'George', 'Orwell', 'ACTIVO'),
(22, 'William', 'Shakespeare', 'ACTIVO'),
(23, 'Charlotte', 'Bronte', 'ACTIVO'),
(24, 'Agatha', 'Christie', 'ACTIVO'),
(25, 'Charles', 'Dickens', 'ACTIVO'),
(26, 'Leo', 'Tolstoy', 'ACTIVO'),
(27, 'Jose', 'Saramago', 'ACTIVO'),
(28, 'Jorge Luis', 'Borges', 'ACTIVO'),
(29, 'Albert', 'Camus', 'ACTIVO'),
(30, 'Ernesto', 'Sábato', 'ACTIVO'),
(31, 'Héctor Abad', 'Faciolince', 'ACTIVO'),
(32, 'Julio', 'Cortázar', 'ACTIVO'),
(33, 'Stephen', 'King', 'ACTIVO'),
(34, 'Mario', 'Vargas Llosa', 'ACTIVO'),
(35, 'Carlos', 'Ruiz Zafón', 'ACTIVO'),
(36, 'Juan', 'Velasquez', 'ACTIVO'),
(37, 'Alex', 'Preukschat', 'ACTIVO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

DROP TABLE IF EXISTS `categorias`;
CREATE TABLE IF NOT EXISTS `categorias` (
  `id_categoria` int NOT NULL AUTO_INCREMENT,
  `categoria` varchar(40) NOT NULL,
  `estado` varchar(10) NOT NULL DEFAULT 'ACTIVO',
  PRIMARY KEY (`id_categoria`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id_categoria`, `categoria`, `estado`) VALUES
(1, 'Acción y Aventura', 'ACTIVO'),
(2, 'Terror', 'ACTIVO'),
(3, 'Ficción Moderna', 'ACTIVO'),
(4, 'Suspenso', 'ACTIVO'),
(5, 'Romance', 'ACTIVO'),
(6, 'Narrativa', 'ACTIVO'),
(7, 'Novela', 'ACTIVO'),
(8, 'Poesía', 'ACTIVO'),
(9, 'Fantasía', 'ACTIVO'),
(10, 'Ficción', 'ACTIVO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

DROP TABLE IF EXISTS `clientes`;
CREATE TABLE IF NOT EXISTS `clientes` (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `identificacion` varchar(11) NOT NULL,
  `nombres` varchar(25) NOT NULL,
  `apellidos` varchar(25) NOT NULL,
  `telefono` varchar(12) NOT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `correo_electronico` varchar(100) NOT NULL,
  `estado` varchar(10) NOT NULL DEFAULT 'ACTIVO',
  PRIMARY KEY (`id_cliente`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `identificacion`, `nombres`, `apellidos`, `telefono`, `direccion`, `correo_electronico`, `estado`) VALUES
(1, '1020466894', 'Juan Pablo', 'Velásquez Arboleda', '3003455466', 'Av. Siempre Viva 555', 'juanpv@gmail.com', 'ACTIVO'),
(2, '76743523', 'Silvia Omaira', 'Penagos', '4564403', 'Cl 54 # 54 - 11', 'silvia@gmail.com', 'ACTIVO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libros`
--

DROP TABLE IF EXISTS `libros`;
CREATE TABLE IF NOT EXISTS `libros` (
  `isbn` int NOT NULL,
  `titulo` varchar(125) NOT NULL,
  `fecha_pub` date NOT NULL,
  `categoria` int NOT NULL,
  `precio` int NOT NULL,
  `portada` varchar(128) DEFAULT NULL,
  `cantidad_stock` int NOT NULL,
  `estado` varchar(10) NOT NULL DEFAULT 'ACTIVO',
  PRIMARY KEY (`isbn`),
  KEY `categoria` (`categoria`)
) ;

--
-- Volcado de datos para la tabla `libros`
--

INSERT INTO `libros` (`isbn`, `titulo`, `fecha_pub`, `categoria`, `precio`, `portada`, `cantidad_stock`, `estado`) VALUES
(3725, 'Operation Hell Gate', '2005-09-27', 1, 48000, 'no_portada.png', 97, 'ACTIVO'),
(7515, 'Godzilla 2000', '1997-11-11', 3, 65000, 'no_portada.png', 0, 'INACTIVO'),
(3281, 'Miguel Strogoff', '2001-12-10', 1, 25000, 'no_portada.png', 100, 'ACTIVO'),
(5831, 'Viaje al centro de la Tierra', '1864-11-25', 7, 20000, 'no_portada.png', 1, 'ACTIVO'),
(3277, 'La vuelta al mundo en ochenta dias', '2003-05-22', 1, 32000, 'no_portada.png', 50, 'ACTIVO'),
(4683, 'El Gato Negro', '1997-10-12', 2, 44000, 'no_portada.png', 100, 'ACTIVO'),
(9781, 'Un sueño en un sueño', '1849-03-31', 8, 25000, 'no_portada.png', 5, 'ACTIVO'),
(7269, 'El corazón delator', '1999-08-15', 2, 48000, 'no_portada.png', 35, 'ACTIVO'),
(4986, 'Frankenstein', '1990-03-01', 2, 55500, 'no_portada.png', 100, 'ACTIVO'),
(6186, 'Mathilda', '1959-01-01', 3, 70000, 'no_portada.png', 9, 'ACTIVO'),
(3852, 'Sexo en la Luna', '2011-06-01', 3, 29500, 'no_portada.png', 100, 'ACTIVO'),
(8000, 'The Antisocial Network', '2021-09-07', 6, 85000, 'no_portada.png', 10, 'ACTIVO'),
(4634, 'The midnight ride', '2022-03-22', 4, 35500, 'no_portada.png', 35, 'ACTIVO'),
(4159, 'Drácula', '1999-04-10', 2, 46800, 'no_portada.png', 100, 'ACTIVO'),
(2266, 'La joya de las siete estrellas', '1903-01-01', 2, 50000, 'no_portada.png', 3, 'ACTIVO'),
(8991, 'La dama del sudario', '1995-12-07', 2, 40000, 'no_portada.png', 45, 'ACTIVO'),
(4287, 'Realidad Aumentada', '2001-03-13', 4, 35200, 'no_portada.png', 100, 'ACTIVO'),
(2185, 'Lo que el hielo atrapa', '2015-01-01', 1, 61000, 'no_portada.png', 0, 'INACTIVO'),
(4428, 'Juicio Final, Sangre en el Cielo', '2009-05-30', 4, 40000, 'no_portada.png', 100, 'ACTIVO'),
(2168, 'Herederos del Cielo', '2021-03-19', 3, 20000, 'no_portada.png', 3, 'ACTIVO'),
(4660, 'El Enigma de los Vencidos', '2000-11-25', 4, 38500, 'no_portada.png', 100, 'ACTIVO'),
(1713, 'El Aroma Del Miedo', '2017-09-05', 4, 35000, 'no_portada.png', 4, 'ACTIVO'),
(5784, 'Orgullo y Prejuicio', '2003-09-25', 5, 36100, 'no_portada.png', 100, 'ACTIVO'),
(3069, 'Darcy and Elizabeth', '1813-12-12', 5, 54500, 'no_portada.png', 15, 'ACTIVO'),
(1331, 'Lady Susan', '2000-01-28', 7, 38000, 'no_portada.png', 25, 'ACTIVO'),
(6039, 'Cumbres Borrascosas', '1998-11-25', 5, 60800, 'no_portada.png', 100, 'ACTIVO'),
(6154, 'No coward soul is mine', '1990-10-12', 8, 48000, 'no_portada.png', 22, 'ACTIVO'),
(6182, 'La Dama de las Camelias', '1995-07-28', 5, 57600, 'no_portada.png', 100, 'ACTIVO'),
(6073, 'Black', '1858-12-01', 7, 25000, 'no_portada.png', 13, 'ACTIVO'),
(2190, 'Los tres mosqueteros', '1997-08-04', 1, 66000, 'no_portada.png', 55, 'ACTIVO'),
(7297, 'Cien Años de Soledad', '1990-04-27', 6, 39500, 'no_portada.png', 100, 'ACTIVO'),
(2437, 'Crónica de Una Muerte Anunciada', '2016-07-15', 6, 48000, 'no_portada.png', 100, 'ACTIVO'),
(1280, 'Alexis Zorba, El Griego', '2010-11-25', 6, 38500, 'no_portada.png', 98, 'ACTIVO'),
(7211, 'Libertad o muerte', '1953-12-31', 7, 10000, 'no_portada.png', 20, 'ACTIVO'),
(2875, 'Cathedral', '2004-08-15', 6, 25700, 'no_portada.png', 100, 'ACTIVO'),
(6240, 'De qué hablamos cuando hablamos de amor', '2000-11-18', 10, 37000, 'no_portada.png', 45, 'ACTIVO'),
(9788, 'Si me necesitas, llámame', '2000-01-31', 8, 29000, 'no_portada.png', 10, 'ACTIVO'),
(8807, 'El Nombre de la Rosa', '2011-05-24', 7, 68000, 'no_portada.png', 99, 'ACTIVO'),
(5118, 'El cementerio de Praga', '2010-10-25', 7, 70000, 'no_portada.png', 32, 'ACTIVO'),
(5170, 'Historia de la belleza', '2004-10-06', 5, 85000, 'no_portada.png', 19, 'ACTIVO'),
(5963, 'El viejo y el mar', '1952-12-31', 7, 45000, 'no_portada.png', 0, 'INACTIVO'),
(8900, 'Fiesta', '1926-10-22', 7, 70500, 'no_portada.png', 20, 'ACTIVO'),
(1400, 'Sula', '1973-11-30', 1, 80000, 'no_portada.png', 10, 'ACTIVO'),
(9778, 'Volver', '2012-05-08', 5, 30000, 'no_portada.png', 3, 'ACTIVO'),
(2022, 'After Dark', '2004-09-30', 3, 65000, 'no_portada.png', 8, 'ACTIVO'),
(5264, 'Kafka en la orilla', '2002-09-12', 7, 50000, 'no_portada.png', 0, 'INACTIVO'),
(8468, 'Romeo y Julieta', '1597-12-01', 5, 55500, 'no_portada.png', 30, 'ACTIVO'),
(5335, 'El sueño de una noche de verano', '1605-01-01', 7, 30500, 'no_portada.png', 10, 'ACTIVO'),
(5437, 'El asesinato de Roger Ackroyd', '1926-06-06', 3, 90000, 'no_portada.png', 2, 'ACTIVO'),
(1378, 'El misterioso caso de Styles', '1867-12-31', 6, 10000, 'no_portada.png', 8, 'ACTIVO'),
(2473, 'A Tale of Two Cities', '2007-10-31', 7, 20000, 'no_portada.png', 3, 'ACTIVO'),
(4979, 'Calle sin salida', '1867-12-31', 6, 10000, 'no_portada.png', 5, 'ACTIVO'),
(4812, 'Guerra y paz', '1869-12-12', 7, 100000, 'no_portada.png', 5, 'ACTIVO'),
(7419, 'Las tres preguntas', '1903-01-31', 1, 60000, 'no_portada.png', 22, 'ACTIVO'),
(2511, 'Ensayo sobre la ceguera', '1995-04-20', 7, 50000, 'no_portada.png', 43, 'ACTIVO'),
(5486, 'Intermitencias de la muerte', '2005-06-09', 7, 55000, 'no_portada.png', 25, 'ACTIVO'),
(2478, 'La biblioteca de Babel', '2001-07-19', 10, 35000, 'no_portada.png', 45, 'ACTIVO'),
(2560, 'El inmortal', '2002-09-29', 10, 40000, 'no_portada.png', 55, 'ACTIVO'),
(9784, 'El extanjero', '1995-04-19', 7, 60000, 'no_portada.png', 33, 'ACTIVO'),
(2239, 'La caída', '1998-06-14', 7, 66000, 'no_portada.png', 45, 'ACTIVO'),
(8432, 'El túnel', '2001-01-21', 7, 58000, 'no_portada.png', 30, 'ACTIVO'),
(9286, 'Sobre héroes y tumbas', '2003-04-12', 7, 55000, 'no_portada.png', 35, 'ACTIVO'),
(7357, 'La oculta', '2014-09-16', 10, 45000, 'no_portada.png', 45, 'ACTIVO'),
(4124, 'Angosta', '2003-11-06', 10, 48000, 'no_portada.png', 25, 'ACTIVO'),
(4572, 'Rayuela', '1990-06-28', 7, 40500, 'no_portada.png', 20, 'ACTIVO'),
(6691, 'Final del juego', '1995-09-30', 10, 44500, 'no_portada.png', 53, 'ACTIVO'),
(6439, 'La cúpula', '2009-10-10', 7, 66500, 'no_portada.png', 60, 'ACTIVO'),
(1236, 'Doctor sueño', '2013-09-24', 2, 60500, 'no_portada.png', 36, 'ACTIVO'),
(9959, '1984', '2000-07-27', 10, 57500, 'no_portada.png', 55, 'ACTIVO'),
(8897, 'Subir por aire', '1990-05-07', 10, 43000, 'no_portada.png', 60, 'ACTIVO'),
(8185, 'La fiesta del chivo', '2000-07-17', 7, 35000, 'no_portada.png', 28, 'ACTIVO'),
(5455, 'El héroe discreto', '2013-09-02', 10, 32500, 'no_portada.png', 38, 'ACTIVO'),
(2595, 'La sombra del viento', '2001-05-12', 4, 44000, 'no_portada.png', 22, 'ACTIVO'),
(5552, 'El juego del ángel', '2008-04-17', 7, 28500, 'no_portada.png', 20, 'ACTIVO'),
(6404, 'Blockchain', '2017-05-23', 3, 65000, 'no_portada.png', 5, 'ACTIVO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libro_por_autor`
--

DROP TABLE IF EXISTS `libro_por_autor`;
CREATE TABLE IF NOT EXISTS `libro_por_autor` (
  `id_autor` int NOT NULL,
  `isbn` int NOT NULL,
  `estado` varchar(10) NOT NULL DEFAULT 'ACTIVO',
  PRIMARY KEY (`id_autor`,`isbn`),
  KEY `isbn` (`isbn`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `libro_por_autor`
--

INSERT INTO `libro_por_autor` (`id_autor`, `isbn`, `estado`) VALUES
(2, 3725, 'ACTIVO'),
(4, 7515, 'ACTIVO'),
(2, 3281, 'ACTIVO'),
(2, 5831, 'ACTIVO'),
(2, 3277, 'ACTIVO'),
(6, 4683, 'ACTIVO'),
(6, 9781, 'ACTIVO'),
(6, 7269, 'ACTIVO'),
(6, 4986, 'ACTIVO'),
(4, 6186, 'ACTIVO'),
(5, 3852, 'ACTIVO'),
(5, 8000, 'ACTIVO'),
(5, 4634, 'ACTIVO'),
(6, 4159, 'ACTIVO'),
(6, 2266, 'ACTIVO'),
(6, 8991, 'ACTIVO'),
(4, 4287, 'ACTIVO'),
(7, 2185, 'ACTIVO'),
(4, 4428, 'ACTIVO'),
(4, 2168, 'ACTIVO'),
(6, 4660, 'ACTIVO'),
(6, 1713, 'ACTIVO'),
(10, 5784, 'ACTIVO'),
(10, 3069, 'ACTIVO'),
(10, 1331, 'ACTIVO'),
(11, 6039, 'ACTIVO'),
(11, 6154, 'ACTIVO'),
(11, 6182, 'ACTIVO'),
(11, 6073, 'ACTIVO'),
(12, 2190, 'ACTIVO'),
(37, 6404, 'ACTIVO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tbl_pedido_cliente`
--

DROP TABLE IF EXISTS `tbl_pedido_cliente`;
CREATE TABLE IF NOT EXISTS `tbl_pedido_cliente` (
  `id_pedido` int NOT NULL AUTO_INCREMENT,
  `nro_pedido` int NOT NULL,
  `id_cliente` int NOT NULL,
  `isbn` int NOT NULL,
  `fecha_pedido` date NOT NULL,
  `cantidad` int NOT NULL DEFAULT '1',
  `subtotal` int NOT NULL,
  `estado` varchar(10) NOT NULL DEFAULT 'ACTIVO',
  PRIMARY KEY (`id_pedido`),
  KEY `id_cliente` (`id_cliente`),
  KEY `isbn` (`isbn`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `tbl_pedido_cliente`
--

INSERT INTO `tbl_pedido_cliente` (`id_pedido`, `nro_pedido`, `id_cliente`, `isbn`, `fecha_pedido`, `cantidad`, `subtotal`, `estado`) VALUES
(1, 1, 1, 3725, '2023-11-28', 3, 144000, 'ACTIVO'),
(2, 2, 1, 2022, '2023-11-29', 1, 65000, 'ACTIVO'),
(5, 3, 2, 2875, '2023-12-01', 1, 25700, 'ACTIVO'),
(6, 4, 1, 1280, '2023-12-01', 2, 77000, 'ACTIVO'),
(7, 5, 2, 8807, '2023-12-01', 1, 68000, 'ACTIVO'),
(8, 6, 2, 2473, '2023-12-01', 1, 20000, 'ACTIVO'),
(9, 7, 1, 9959, '2023-12-01', 1, 57500, 'ACTIVO'),
(10, 8, 1, 7515, '2023-12-01', 2, 130000, 'ACTIVO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) NOT NULL,
  `clave` varchar(50) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `usuario`, `clave`, `nombre`) VALUES
(1, 'juanpv', 'juan1234', 'Juan'),
(2, 'admin', 'admin', 'Administrador'),
(3, 'pablov', 'juan1234', 'Pablo'),
(6, 'juanvel', 'juan1234', 'Juan');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
