CREATE DATABASE IF NOT EXISTS myloginappX;  #reemplace X con un nro del 1 al 20
USE myloginappX;                            #reemplace X con un nro del 1 al 20
CREATE TABLE IF NOT EXISTS appusers (
id int(10) NOT NULL AUTO_INCREMENT,
username varchar(10) NOT NULL,
password varchar(20) NOT NULL,
email varchar(50) NOT NULL,
CONSTRAINT PK_AppUsers PRIMARY KEY(id)
);