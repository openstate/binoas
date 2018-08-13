CREATE DATABASE IF NOT EXISTS `binoas`;

CREATE TABLE IF NOT EXISTS `binoas`.`user` (
  `id` INT(11) NOT NULL PRIMARY KEY,
  `external_id` VARCHAR(255),
  `email` VARCHAR(255) NOT NULL,
  index idx_external (external_id),
  index idx_email (email)
);

CREATE TABLE IF NOT EXISTS `binoas`.`user_queries` (
  `user_id` INT(11) NOT NULL,
  `query_id` VARCHAR(255) NOT NULL,
  `frequency` VARCHAR(32),
  PRIMARY KEY (`user_id`, `query_id`),
  index idx_user_id (user_id),
  index idx_query_frequency (query_id, frequency)
);
