-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-12-2023 a las 12:18:24
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `florentino`
--
CREATE DATABASE IF NOT EXISTS `florentino` DEFAULT CHARACTER SET utf8 COLLATE utf8_spanish_ci;
USE `florentino`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `aperitivos`
--

DROP TABLE IF EXISTS `aperitivos`;
CREATE TABLE `aperitivos` (
  `id` int(11) NOT NULL,
  `nombre` text NOT NULL,
  `descripcion` text NOT NULL,
  `estado` int(5) NOT NULL,
  `tipo` text NOT NULL,
  `precio` float DEFAULT NULL,
  `img_ruta` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `aperitivos`
--

INSERT INTO `aperitivos` (`id`, `nombre`, `descripcion`, `estado`, `tipo`, `precio`, `img_ruta`) VALUES
(1, 'Empanada carne', 'Empanada rellena de carne picada y tomate.', 1, 'Salado', 2.9, 'static/imgs/aperitivos/empanada_de_carne.webp'),
(2, 'Empanada atún', 'Empanada rellena de atún, cebolla, tomate y huevo cocido.', 0, 'Salado', 2.2, 'static/imgs/aperitivos/empanada_atun.webp'),
(3, 'Pincho de tortilla', 'Pincho de tortilla de patatas con cebolla, mayonesa, queso de cabra, jamón serrano y pan.', 1, 'Salado', 3, 'static/imgs/aperitivos/pincho_tortilla.webp'),
(4, 'Poke bowl', 'Contiene salmón noruego, aguacate, alga wakame, cebolleta china, cebolla roja, huevo de corral poché y aceite de sésamo.', 0, 'Salado', 6.5, 'static/imgs/aperitivos/poke_bowl.webp'),
(5, 'Croquetas', 'Croquetas caseras elaboradas con jamón ibérico.', 1, 'Salado', 3, 'static/imgs/aperitivos/croquetas.webp'),
(6, 'Ensalada César', 'Ensalada de lechuga romana y croûtons con jugo de limón, aceite de oliva, huevo, salsa Worcestershire, anchoas, ajo, mostaza de Dijon, queso parmesano y pimienta negra.', 0, 'Salado', 4.5, 'static/imgs/aperitivos/ensalada_cesar.webp'),
(7, 'Sanwich mixto', 'Sándwich emparedado con jamón y queso amarillo dentro de dos rebanadas de pan de sándwich.', 1, 'Salado', 2.5, 'static/imgs/aperitivos/sandwich_mixto.webp'),
(8, 'Croissant', 'Croissant con mantequilla.', 0, 'Dulce', 1.5, 'static/imgs/aperitivos/croissant.webp'),
(9, 'Caracola', 'Bocado dulce y esponjoso, con una masa aromática.', 1, 'Dulce', 1.8, 'static/imgs/aperitivos/caracola.webp'),
(10, 'Napolitana de crema', 'Crema de vainilla envuelta por masa de hojaldre.', 0, 'Dulce', 2.2, 'static/imgs/aperitivos/napolitanas_crema.webp'),
(11, 'Napolitana chocolate', 'Crema de chocolate envuelta por masa de hojaldre.', 1, 'Dulce', 2.2, 'static/imgs/aperitivos/napolitanas_chocolate.webp'),
(12, 'Pancakes', 'Torta plana, redonda y dulce, cuya masa contiene leche y está levadurizada. Con nata y sirope si se quiere.', 0, 'Dulce', 3.5, 'static/imgs/aperitivos/pancakes.webp'),
(13, 'Crêpe', 'Crêpe rellena de Nutella con trozos de fresas salsa de chocolate, almendra en grano y nata.', 1, 'Dulce', 4, 'static/imgs/aperitivos/crepe.webp'),
(14, 'Porción tarta de manzana', 'Tarta elaborada con harina, levadura, huevos, azúcar, manzana, leche y mantequilla.', 0, 'Dulce', 3, 'static/imgs/aperitivos/porcion_tarta_manzana.webp'),
(15, 'Aperitivo_prueba1', 'Descripción aperitivo_prueba1.', 1, 'Salado', 9.2, 'static/imgs/aperitivos/images.jpeg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bebidas`
--

DROP TABLE IF EXISTS `bebidas`;
CREATE TABLE `bebidas` (
  `id` int(11) NOT NULL,
  `nombre` text NOT NULL,
  `descripcion` text NOT NULL,
  `estado` int(5) NOT NULL,
  `tipo` text NOT NULL,
  `precio` float DEFAULT NULL,
  `img_ruta` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `bebidas`
--

INSERT INTO `bebidas` (`id`, `nombre`, `descripcion`, `estado`, `tipo`, `precio`, `img_ruta`) VALUES
(1, 'Café Espresso', 'Este es un café tipo concentrado servido en pequeñas cantidades, que sirve de base para muchos otros tipos de café.', 1, 'Sólo', 2.5, 'static/imgs/bebidas/cafe_espresso.webp'),
(2, 'Café Americano', 'Este es un café Espresso diluido con agua caliente.', 0, 'Sólo', 2, 'static/imgs/bebidas/cafe_americano.webp'),
(3, 'Café Ristretto', 'Es un «espresso corto» con menos agua para un sabor más fuerte. ', 1, 'Sólo', 2.5, 'static/imgs/bebidas/cafe_ristretto.webp'),
(4, 'Café Negro', 'También conocido como café solo, es café que se sirve sin leche ni crema.', 0, 'Sólo', 2, 'static/imgs/bebidas/cafe_negro.webp'),
(5, 'Café Espresso Romano', 'Este es un espresso servido con una rodaja de limón al lado.', 1, 'Sólo', 3, 'static/imgs/bebidas/cafe_espresso_romano.webp'),
(6, 'Café Latte', 'Un café Espresso combinado con leche caliente y espuma de leche.', 0, 'Con leche', 4, 'static/imgs/bebidas/cafe_latte.webp'),
(7, 'Café Cortado', 'Popular en España y América Latina, es un espresso «cortado» con una pequeña cantidad de leche caliente. ', 1, 'Con leche', 3.5, 'static/imgs/bebidas/cafe_cortado.webp'),
(8, 'Capuchino', 'Es un tercio de espresso, un tercio de leche caliente y un tercio de espuma de leche.', 0, 'Con leche', 4.5, 'static/imgs/bebidas/capuchino.webp'),
(9, 'Café Mocha', 'Un café latte con chocolate.', 1, 'Con leche', 4.5, 'static/imgs/bebidas/cafe_mocha.webp'),
(10, 'Café Macchiato', 'Espresso con una pequeña cantidad de leche espumada.', 0, 'Con leche', 3, 'static/imgs/bebidas/cafe_macchiato.webp'),
(11, 'Café con Leche', 'Es mitad café, mitad leche.', 1, 'Con leche', 3.5, 'static/imgs/bebidas/cafe_con_leche.webp'),
(12, 'Café Irlandés', 'Esta bebida se caracteriza por su sabor suave y cremoso, con un equilibrio entre la dulzura de la crema y la calidez del whisky.', 0, 'Con alcohol', 6, 'static/imgs/bebidas/cafe_irlandes.webp'),
(13, 'Carajillo', 'Es una combinación de café y licor, generalmente brandy o ron.', 1, 'Con alcohol', 5, 'static/imgs/bebidas/carajillo.webp'),
(14, 'Café Helado', 'Café que se sirve frío, generalmente con hielo.', 0, 'Helado', 3.5, 'static/imgs/bebidas/cafe_helado.webp'),
(15, 'Café Affogato', 'Un postre de café que incluye una bola de helado cubierta con un chorro de espresso.', 1, 'Helado', 4, 'static/imgs/bebidas/cafe_affogato.webp'),
(16, 'Café Frappé', 'Un café helado cubierto con crema batida y jarabe.', 0, 'Helado', 4, 'static/imgs/bebidas/cafe_frappe.webp'),
(17, 'Cappuccino Freddo', 'Es la versión fría del cappuccino.', 1, 'Helado', 3.5, 'static/imgs/bebidas/cappuccino_freddo.webp'),
(18, 'Café Eiskaffee', 'Un café alemán que combina helado de vainilla, café frío y crema batida.', 0, 'Helado', 5, 'static/imgs/bebidas/cafe_eiskaffee.webp');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `aperitivos`
--
ALTER TABLE `aperitivos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `bebidas`
--
ALTER TABLE `bebidas`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `aperitivos`
--
ALTER TABLE `aperitivos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `bebidas`
--
ALTER TABLE `bebidas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
