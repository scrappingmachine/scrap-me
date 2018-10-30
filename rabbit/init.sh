#!/bin/sh

# rabbitmq-server &
rabbitmq-server </dev/null >/dev/null 2>&1 &

while true
do
  sleep 2
  rabbitmqctl -q node_health_check  > /dev/null 2>&1
  if [ $? -eq 0 ] ; then
    echo "$0 `date` rabbitmq is now running"
    break
  else
    echo "$0 `date` waiting for rabbitmq startup"
  fi
done

# Create Rabbitmq user
rabbitmqctl add_vhost / 2>/dev/null
rabbitmqctl add_user $RABBITMQ_USER $RABBITMQ_PASSWORD 2>/dev/null
rabbitmqctl set_user_tags $RABBITMQ_USER administrator
rabbitmqctl set_permissions -p / $RABBITMQ_USER  ".*" ".*" ".*"
echo "*** User '$RABBITMQ_USER' with password '$RABBITMQ_PASSWORD' completed. ***"
echo "*** Log in the WebUI at port 15672 (example: http:/localhost:15672) ***"

wget http://localhost:15672/cli/rabbitmqadmin
chmod a+x rabbitmqadmin
./rabbitmqadmin declare queue name=scrap_task durable=false -u $RABBITMQ_USER -p $RABBITMQ_PASSWORD
./rabbitmqadmin declare queue name=scrap_result durable=false -u $RABBITMQ_USER -p $RABBITMQ_PASSWORD
wait
