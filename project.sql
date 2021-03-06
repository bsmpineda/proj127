CREATE USER IF NOT EXISTS 'proj127'@'localhost' IDENTIFIED BY 'proj127';
GRANT ALL ON project127.* TO 'proj127'@'localhost';

DROP DATABASE IF EXISTS `project127`; 
CREATE DATABASE IF NOT EXISTS `project127`; 
use project127;

CREATE TABLE category(
	category_id 	INT(5) NOT NULL AUTO_INCREMENT,
	name 			varchar(15),
  	description 	varchar(100),
	CONSTRAINT category_category_id_pk PRIMARY KEY(category_id) 
);

CREATE TABLE task(
	task_id	 	INT(5) NOT NULL AUTO_INCREMENT,
	title 		varchar(15) 	NOT NULL, 
	details 	varchar(50),
	deadline 	date,
	status 		varchar(10),
	category_id INT(5) NULL,
	CONSTRAINT task_task_id_pk PRIMARY KEY(task_id),
	CONSTRAINT task_category_id_fk FOREIGN KEY(category_id) REFERENCES category(category_id)
); 



