#!/usr/bin/env bash

sudo docker run  --name mysql -p 33070:3306  -v <path>:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=pass -d mysql:5.7.17
# CREATE DATABASE yuequnbot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
