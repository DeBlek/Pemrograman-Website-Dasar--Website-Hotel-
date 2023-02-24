-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 30, 2022 at 05:03 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `uas_website`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `Id_Admin` int(255) NOT NULL,
  `Username_Admin` varchar(255) NOT NULL,
  `Password_Admin` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `checkin`
--

CREATE TABLE `checkin` (
  `Kode_Checkin` int(255) NOT NULL,
  `Id_Sewa` int(255) NOT NULL,
  `Tanggal` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `checkout`
--

CREATE TABLE `checkout` (
  `Kode_Checkout` int(255) NOT NULL,
  `Id_Sewa` int(11) NOT NULL,
  `Tanggal` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `jenis_kamar`
--

CREATE TABLE `jenis_kamar` (
  `Id_JenisKamar` int(255) NOT NULL,
  `Nama_Jenis` varchar(255) NOT NULL,
  `Stock_Kamar` int(255) NOT NULL,
  `Harga_Kamar` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `kamar`
--

CREATE TABLE `kamar` (
  `Kode_Kamar` int(255) NOT NULL,
  `Jenis_Kamar` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `pelanggan`
--

CREATE TABLE `pelanggan` (
  `Id_Pelanggan` int(255) NOT NULL,
  `Nama_Pelanggan` varchar(255) NOT NULL,
  `Jenis_Kelamin` varchar(255) NOT NULL,
  `Alamat_Pelanggan` varchar(255) NOT NULL,
  `No_Tlpn` int(13) NOT NULL,
  `Email_Pelanggan` varchar(255) NOT NULL,
  `Password_Pelanggan` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sewa`
--

CREATE TABLE `sewa` (
  `Id_Sewa` int(255) NOT NULL,
  `Id_Pelanggan` int(255) NOT NULL,
  `Id_Kamar` int(255) NOT NULL,
  `Jmlh_Kamar` int(255) NOT NULL,
  `Check_In` varchar(255) NOT NULL,
  `Check_Out` varchar(255) NOT NULL,
  `Total_Harga` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`Id_Admin`),
  ADD UNIQUE KEY `Username_Admin` (`Username_Admin`);

--
-- Indexes for table `checkin`
--
ALTER TABLE `checkin`
  ADD PRIMARY KEY (`Kode_Checkin`),
  ADD KEY `CHeckin_Id_Sewa` (`Id_Sewa`);

--
-- Indexes for table `checkout`
--
ALTER TABLE `checkout`
  ADD PRIMARY KEY (`Kode_Checkout`),
  ADD KEY `Checkout_Id_sewa` (`Id_Sewa`);

--
-- Indexes for table `jenis_kamar`
--
ALTER TABLE `jenis_kamar`
  ADD PRIMARY KEY (`Id_JenisKamar`);

--
-- Indexes for table `kamar`
--
ALTER TABLE `kamar`
  ADD PRIMARY KEY (`Kode_Kamar`),
  ADD UNIQUE KEY `Jenis_Kamar` (`Jenis_Kamar`),
  ADD UNIQUE KEY `Jenis_Kamar_2` (`Jenis_Kamar`);

--
-- Indexes for table `pelanggan`
--
ALTER TABLE `pelanggan`
  ADD PRIMARY KEY (`Id_Pelanggan`),
  ADD UNIQUE KEY `Email_Pelanggan` (`Email_Pelanggan`);

--
-- Indexes for table `sewa`
--
ALTER TABLE `sewa`
  ADD PRIMARY KEY (`Id_Sewa`),
  ADD KEY `Sewa_Id_Pelanggan` (`Id_Pelanggan`),
  ADD KEY `Sewa_Id_Kamar` (`Id_Kamar`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `Id_Admin` int(255) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `checkin`
--
ALTER TABLE `checkin`
  MODIFY `Kode_Checkin` int(255) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `checkout`
--
ALTER TABLE `checkout`
  MODIFY `Kode_Checkout` int(255) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `jenis_kamar`
--
ALTER TABLE `jenis_kamar`
  MODIFY `Id_JenisKamar` int(255) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `kamar`
--
ALTER TABLE `kamar`
  MODIFY `Kode_Kamar` int(255) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pelanggan`
--
ALTER TABLE `pelanggan`
  MODIFY `Id_Pelanggan` int(255) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sewa`
--
ALTER TABLE `sewa`
  MODIFY `Id_Sewa` int(255) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `checkin`
--
ALTER TABLE `checkin`
  ADD CONSTRAINT `CHeckin_Id_Sewa` FOREIGN KEY (`Id_Sewa`) REFERENCES `sewa` (`Id_Sewa`);

--
-- Constraints for table `checkout`
--
ALTER TABLE `checkout`
  ADD CONSTRAINT `Checkout_Id_sewa` FOREIGN KEY (`Id_Sewa`) REFERENCES `sewa` (`Id_Sewa`);

--
-- Constraints for table `kamar`
--
ALTER TABLE `kamar`
  ADD CONSTRAINT `Kamar_Id_JenisKAmar` FOREIGN KEY (`Jenis_Kamar`) REFERENCES `jenis_kamar` (`Id_JenisKamar`);

--
-- Constraints for table `sewa`
--
ALTER TABLE `sewa`
  ADD CONSTRAINT `Sewa_Id_Kamar` FOREIGN KEY (`Id_Kamar`) REFERENCES `kamar` (`Kode_Kamar`),
  ADD CONSTRAINT `Sewa_Id_Pelanggan` FOREIGN KEY (`Id_Pelanggan`) REFERENCES `pelanggan` (`Id_Pelanggan`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
