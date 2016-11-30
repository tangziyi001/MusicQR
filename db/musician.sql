/* Create our database */
CREATE DATABASE musician CHARACTER SET utf8;

/* Setup permissions for the server */
CREATE USER 'appserver'@'localhost' IDENTIFIED BY 'foobarzoot';
CREATE USER 'www-data'@'localhost' IDENTIFIED BY 'foobarzoot';
GRANT ALL ON musician.* TO 'appserver'@'localhost';
GRANT ALL ON musician.* TO 'www-data'@'localhost';
