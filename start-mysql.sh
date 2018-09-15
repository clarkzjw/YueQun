
CREATE DATABASE yuequnbot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
docker run --name yqbot-mysql -p 3306:3306 -v /app/data/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=mysql-pw-secret -d mysql:8.0.12
