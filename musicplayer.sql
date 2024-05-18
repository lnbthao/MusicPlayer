-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 06, 2024 at 05:23 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `musicplayer`
--

-- --------------------------------------------------------

--
-- Table structure for table `music`
--

CREATE TABLE `music` (
  `id` int(11) NOT NULL,
  `song_name` varchar(255) DEFAULT NULL,
  `singer_name` varchar(255) DEFAULT NULL,
  `genre` varchar(100) DEFAULT NULL,
  `mp3` varchar(255) DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `music`
--

INSERT INTO `music` (`id`, `song_name`, `singer_name`, `genre`, `mp3`, `img`) VALUES
(70, 'Nhắn Nhủ', 'Ronboogz', 'Việt', 'Nhắn Nhủ(Ronboogz).mp3', 'NhanNhu.jpg'),
(75, 'Moonlight', 'Dhruv', 'Âu Mỹ', 'Moolight(Dhruv).mp3', 'moonlight.jpg'),
(78, 'Round And Round', 'Heize', 'Hàn', 'Round and round(Heize).mp3', 'Round and round.jpg'),
(80, 'Stay With Me', 'Chanyeol,Punch', 'Hàn', 'Stay with me(Chanyeol,Punch).mp3', 'Stay with me.jpg'),
(81, 'Double Take', 'Dhruv', 'Âu Mỹ', 'double take(Dhruv).mp3', 'double take.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `music`
--
ALTER TABLE `music`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `music`
--
ALTER TABLE `music`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=82;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
