#! /bin/sh

# clear rabbitmq
docker exec delphiapi_rabbitmq_1 bash -c "rabbitmqctl stop_app && rabbitmqctl reset && rabbitmqctl start_app"

# clear redis
docker exec delphiapi_redis_1 redis-cli FLUSHALL

# clear database
docker-compose down
# docker-compose start
