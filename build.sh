#!/bin/bash
if [ -f .env ]; then
    source .env
fi

if [ -z "$GLOBAL_REGISTRY_ADDR" ] || \
   [ -z "$GROUP_NAME" ] || \
   [ -z "$IMAGE_NAME" ] || \
   [ -z "$IMAGE_TAG" ]; then
    echo "Error: One or more variables are not set."
    exit 1
fi

# Build Docker image with build arguments
docker build -t $GLOBAL_REGISTRY_ADDR/$GROUP_NAME/$IMAGE_NAME:$IMAGE_TAG .

echo "Build complete!"
