#!/bin/bash

if [ -e pid.stamp ]
then
    echo 'kill old process...'
    kill -9 `cat pid.stamp`;
fi

#nohup gradio webui.py & echo $! > pid.stamp
nohup gradio app.py & echo "pid: $!"
echo 'restarting...'
sleep 5
env_file="./.env"
py_environment=$(grep "^PY_ENVIRONMENT=" "$env_file" | cut -d '=' -f 2)

# Get the TCP port number from the configure file
libai_tcp_port=$(grep "ui_port:" "./config/config-$py_environment.yaml" | head -n 1 | awk '{print $2}')

# Check if the tcp_port variable is set
if [ -z "$libai_tcp_port" ]
then
  echo "Warning: libai_tcp_port environment variable is not set."
#  exit 1
fi

while [ 1 ]; do
  # Find the process ID associated with the specified TCP port
  pid=$(netstat -nap | grep ":$libai_tcp_port " | awk '{print $7}' | head -n 1 | cut -d '/' -f 1)

  # Check if a process ID is found
  if [ -n "$pid" ] && [ "$pid" != "-" ]
  then
    echo "Process ID associated with TCP port $libai_tcp_port: $pid"
    # Dump the process ID to a local file named pid.stamp
    echo "$pid" > pid.stamp
    echo "Process ID dumped to pid.stamp"
    break
  else
    echo "No process found listening on TCP port $libai_tcp_port"
    echo "continue waiting 3 seconds... "
    sleep 3
  fi
done


