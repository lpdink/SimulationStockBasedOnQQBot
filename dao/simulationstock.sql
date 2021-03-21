/*
 Navicat Premium Data Transfer

 Source Server         : linkToMySql
 Source Server Type    : MySQL
 Source Server Version : 80020
 Source Host           : localhost:3306
 Source Schema         : simulationstock

 Target Server Type    : MySQL
 Target Server Version : 80020
 File Encoding         : 65001

 Date: 21/03/2021 22:25:06
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for alive_orders
-- ----------------------------
DROP TABLE IF EXISTS `alive_orders`;
CREATE TABLE `alive_orders`  (
  `user_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `alive_order_index` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `alive_order_time` datetime(0) NULL DEFAULT NULL,
  `buy_or_sell` enum('True','False') CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `stock_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `stock_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `stock_price` decimal(10, 2) NULL DEFAULT NULL,
  `order_money_amount` double(15, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`, `alive_order_index`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for stock_information
-- ----------------------------
DROP TABLE IF EXISTS `stock_information`;
CREATE TABLE `stock_information`  (
  `stock_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stock_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `now_price` decimal(10, 2) NULL DEFAULT NULL,
  `flush_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`stock_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user_holdings
-- ----------------------------
DROP TABLE IF EXISTS `user_holdings`;
CREATE TABLE `user_holdings`  (
  `user_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stock_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stock_amount` int(0) NULL DEFAULT NULL,
  `bought_price` decimal(10, 2) NULL DEFAULT NULL,
  `bought_total_price` double(10, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`, `stock_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user_information
-- ----------------------------
DROP TABLE IF EXISTS `user_information`;
CREATE TABLE `user_information`  (
  `user_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `free_money_amount` double(15, 2) NULL DEFAULT NULL,
  `total_money_amount` double(15, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
