#!/bin/bash

docker ps | grep $(basename $(pwd)) | awk '{print "docker kill " $1 }' | bash
docker ps -a | grep $(basename $(pwd)) | awk '{print "docker rm " $1 }' | bash

