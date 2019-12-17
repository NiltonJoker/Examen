-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-12-2019 a las 00:35:41
-- Versión del servidor: 10.1.38-MariaDB
-- Versión de PHP: 7.3.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tienda_ropa`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administrador`
--

CREATE TABLE `administrador` (
  `idadm` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `administrador`
--

INSERT INTO `administrador` (`idadm`, `username`, `password`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito`
--

CREATE TABLE `carrito` (
  `id_carrito` int(11) NOT NULL,
  `idproducto` int(11) NOT NULL,
  `idcliente` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria`
--

CREATE TABLE `categoria` (
  `idcategoria` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `categoria`
--

INSERT INTO `categoria` (`idcategoria`, `nombre`) VALUES
(1, 'Camisetas'),
(2, 'Pantalones'),
(3, 'Gorras'),
(4, 'Shorts'),
(5, 'Sandalias');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `idcliente` int(11) NOT NULL,
  `nombre` varchar(45) DEFAULT NULL,
  `direccion` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `info-pago` varchar(45) DEFAULT NULL,
  `contraseña` varchar(45) DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`idcliente`, `nombre`, `direccion`, `email`, `info-pago`, `contraseña`, `avatar`) VALUES
(3, 'Nilton', 'Edificios de Enace', 'nilton3@hotmail.com', NULL, '123456', '../static/img/banana.png'),
(5, 'Hector', 'DisneyLand Sede-Bolivia', 'elpiernadebebe@gmail.com', NULL, '1234', '../static/img/felcha.png'),
(6, 'Samir', 'Oficina en la que penan', 'samir@gmail.com', NULL, '123', ''),
(7, 'Jose', 'ujcm', 'jose@hotmail.com', NULL, '123456', ''),
(8, 'Tyson', 'Magisterio', 'tysonp@gmail.com', NULL, '1234', ''),
(9, 'Señor Pruebas', NULL, 'prueba@prueba.com', NULL, '12', '../static/img/icono.png'),
(10, 'Pepe', 'Ciudad Nueva', 'pepe@gmail.com', NULL, 'pepe', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comentarios`
--

CREATE TABLE `comentarios` (
  `idcomentario` int(11) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `video` varchar(255) DEFAULT NULL,
  `fecha` date NOT NULL,
  `idcliente` int(11) NOT NULL,
  `idtema` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `comentarios`
--

INSERT INTO `comentarios` (`idcomentario`, `descripcion`, `video`, `fecha`, `idcliente`, `idtema`) VALUES
(1, 'esto es un comentario al comentario', NULL, '2019-12-06', 5, 1),
(2, 'jaaaaaaaaaaaaaaaaa', 'https://www.youtube.com/embed/mJq8xXAfczo?start=', '2019-12-05', 8, 2),
(5, 'repsuesta', '', '2019-12-06', 3, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_pedido`
--

CREATE TABLE `detalle_pedido` (
  `iddetalle` int(11) NOT NULL,
  `idhistorial` int(11) NOT NULL,
  `idproducto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `subtotal` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `detalle_pedido`
--

INSERT INTO `detalle_pedido` (`iddetalle`, `idhistorial`, `idproducto`, `cantidad`, `subtotal`) VALUES
(1, 1, 1, 1, 12),
(2, 2, 3, 1, 13),
(3, 3, 2, 1, 20),
(4, 4, 8, 2, 60),
(5, 4, 1, 1, 12),
(6, 5, 2, 1, 20),
(7, 6, 4, 1, 15),
(8, 7, 1, 2, 24),
(9, 7, 6, 1, 20),
(10, 7, 12, 1, 20),
(11, 8, 7, 2, 84);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `idproducto` int(11) NOT NULL,
  `nombre` varchar(45) DEFAULT NULL,
  `stock` varchar(45) DEFAULT NULL,
  `precio_u` varchar(45) DEFAULT NULL,
  `imagen` varchar(255) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `idcategoria` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`idproducto`, `nombre`, `stock`, `precio_u`, `imagen`, `descripcion`, `idcategoria`) VALUES
(1, 'Camiseta Puma', '5', '12', '../static/img/puma.jpg', 'Camiseta Puma 100% Algodon Original', 1),
(2, 'Camiseta Gucci', '0', '20', '../static/img/gucci.png', 'Camiseta Gucci Modelo 2019 Original', 1),
(3, 'Camiseta LaCoste', '3', '13', '../static/img/lacoste.jpg', 'Camiseta Lacoste 100% Original modelo exclusivo', 1),
(4, 'Camiseta Adidas', '29', '15', '../static/img/adidas.jpg', 'Camiseta Adidas 100% Algodon Modelo 2018', 1),
(5, 'Camiseta Thom Browne', '5', '50', '../static/img/thom.jpg', 'Camiseta Thom Browne Diseño exclusivo', 1),
(6, 'Camiseta Paul Stuart', '41', '20', '../static/img/paul.jpg', 'Camiseta Paul Stuart 100% Original', 1),
(7, 'Pantalon Negro', '12', '42', '../static/img/pantalon.jpg', 'Pantalon negro 100% original', 2),
(8, 'Gorra de resident evil 2', '0', '30', '../static/img/resident.jpg', 'Gorra original del juego Resident Evil 2', 3),
(12, 'Gorra Puma', '9', '20', '../static/img/gorra-puma.jpg', 'Gorra Puma 100% original color negro', 3),
(13, 'pantalon gris 2', '14', '20', '../static/img/pantalon-gris.jpg', 'pantalo de color gris', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tema`
--

CREATE TABLE `tema` (
  `idtema` int(11) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `video` varchar(255) DEFAULT NULL,
  `fecha` date NOT NULL,
  `idcliente` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `tema`
--

INSERT INTO `tema` (`idtema`, `descripcion`, `video`, `fecha`, `idcliente`) VALUES
(1, 'Hola esto es un comentario', 'https://www.youtube.com/embed/oC5wyJ5eAzU', '2019-12-05', 3),
(2, 'Hola', 'https://www.youtube.com/embed/9VAz-UEypxs?start=', '2019-12-05', 3),
(4, 'este es un comentario', '', '2019-12-06', 3),
(5, 'asdadsdsad', '', '2019-12-08', 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `idhistorial` int(11) NOT NULL,
  `fecha` datetime DEFAULT NULL,
  `total` int(11) DEFAULT NULL,
  `idcliente` int(11) NOT NULL,
  `estado` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `ventas`
--

INSERT INTO `ventas` (`idhistorial`, `fecha`, `total`, `idcliente`, `estado`) VALUES
(1, '2019-12-04 13:47:17', 12, 3, 'Entregado'),
(2, '2019-12-08 00:00:00', 13, 3, 'Entregado'),
(3, '2019-12-08 05:38:21', 20, 3, 'Espera'),
(4, '2019-12-08 05:43:37', 72, 3, 'Espera'),
(5, '2019-12-08 06:24:46', 20, 3, 'Espera'),
(6, '2019-12-08 21:57:51', 15, 5, 'Espera'),
(7, '2019-12-08 21:58:15', 64, 5, 'Espera'),
(8, '2019-12-12 18:15:26', 84, 3, 'Pendiente');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administrador`
--
ALTER TABLE `administrador`
  ADD PRIMARY KEY (`idadm`);

--
-- Indices de la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD PRIMARY KEY (`id_carrito`),
  ADD KEY `id_producto` (`idproducto`),
  ADD KEY `id_cliente` (`idcliente`);

--
-- Indices de la tabla `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`idcategoria`);

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`idcliente`);

--
-- Indices de la tabla `comentarios`
--
ALTER TABLE `comentarios`
  ADD PRIMARY KEY (`idcomentario`),
  ADD KEY `idtema` (`idtema`),
  ADD KEY `idcliente` (`idcliente`),
  ADD KEY `idtema_2` (`idtema`);

--
-- Indices de la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD PRIMARY KEY (`iddetalle`),
  ADD KEY `idhistorial` (`idhistorial`),
  ADD KEY `idproducto` (`idproducto`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`idproducto`),
  ADD KEY `idcategoria` (`idcategoria`);

--
-- Indices de la tabla `tema`
--
ALTER TABLE `tema`
  ADD PRIMARY KEY (`idtema`),
  ADD KEY `idcliente` (`idcliente`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`idhistorial`),
  ADD KEY `idcliente` (`idcliente`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administrador`
--
ALTER TABLE `administrador`
  MODIFY `idadm` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `carrito`
--
ALTER TABLE `carrito`
  MODIFY `id_carrito` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `categoria`
--
ALTER TABLE `categoria`
  MODIFY `idcategoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `idcliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `comentarios`
--
ALTER TABLE `comentarios`
  MODIFY `idcomentario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  MODIFY `iddetalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `idproducto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `tema`
--
ALTER TABLE `tema`
  MODIFY `idtema` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `idhistorial` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`idcliente`) REFERENCES `cliente` (`idcliente`),
  ADD CONSTRAINT `carrito_ibfk_2` FOREIGN KEY (`idproducto`) REFERENCES `productos` (`idproducto`);

--
-- Filtros para la tabla `comentarios`
--
ALTER TABLE `comentarios`
  ADD CONSTRAINT `comentarios_ibfk_1` FOREIGN KEY (`idtema`) REFERENCES `tema` (`idtema`),
  ADD CONSTRAINT `comentarios_ibfk_2` FOREIGN KEY (`idcliente`) REFERENCES `cliente` (`idcliente`);

--
-- Filtros para la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD CONSTRAINT `detalle_pedido_ibfk_2` FOREIGN KEY (`idproducto`) REFERENCES `productos` (`idproducto`),
  ADD CONSTRAINT `detalle_pedido_ibfk_3` FOREIGN KEY (`idhistorial`) REFERENCES `ventas` (`idhistorial`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`idcategoria`) REFERENCES `categoria` (`idcategoria`);

--
-- Filtros para la tabla `tema`
--
ALTER TABLE `tema`
  ADD CONSTRAINT `tema_ibfk_1` FOREIGN KEY (`idcliente`) REFERENCES `cliente` (`idcliente`);

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`idcliente`) REFERENCES `cliente` (`idcliente`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
