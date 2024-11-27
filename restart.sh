#!/bin/bash

sudo systemctl daemon-reload
sudo systemctl restart nginx
sudo systemctl restart flaskapp

# Wait for the socket file to be created, if necessary
sleep 1

# Check if socket file exists, then change permissions
if [ -e flaskapp.sock ]; then
    sudo chown sergio:www-data flaskapp.sock
    chmod 755 .
    chmod 777 flaskapp.sock
else
    echo "Socket file flaskapp.sock not found."
fi
