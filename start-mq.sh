#!/usr/bin/env bash

docker run -d --hostname yqbot-rabbit --name yqbot-rabbit -p 5672:5672 -p 8080:15672 rabbitmq:3-management
