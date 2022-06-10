CREATE USER 'user'@%' IDENTIFIED WITH mysql_native_password BY 'password';
GRANT SELECT ON *.* TO user@'%';
FLUSH PRIVILEGES;
