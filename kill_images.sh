#!/bin/bash

docker images | grep $(basename $(pwd)) | awk '{print "docker rmi -f " $3 }' | bash
docker images | grep \<none\> | awk '{print "docker rmi -f " $3 }' | bash

