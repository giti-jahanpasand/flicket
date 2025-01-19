#!/bin/bash

docker build -t $GLOBAL_REGISTRY_ADDR/$GROUP_NAME/$IMAGE_NAME:$IMAGE_TAG .
echo "Build complete!"
