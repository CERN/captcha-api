#!/bin/bash

set -e

helpFunction()
{
   echo ""
   echo "Usage: $0 -t GITHUB_TAG"
   echo -e "\t-t Git tag or branch to use uppon image creation."
   exit 1
}

while getopts "t:" opt
do
   case "$opt" in
      t ) GITHUB_TAG="$OPTARG" ;;
      ? ) helpFunction ;;
   esac
done

if [ -z "$GITHUB_TAG" ]
then
   echo "Please specify the wanted github tag.";
   helpFunction
fi

REGISTRY_HOST=521201862965.dkr.ecr.eu-west-1.amazonaws.com
REPOSITORY=captcha-api
AWS_REGION="eu-west-1"

aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $REGISTRY_HOST

docker build --file ./Dockerfile --build-arg DOCKER_REGISTRY_HOST=$REGISTRY_HOST --build-arg BUILD_GIT_TAG=$GITHUB_TAG --cache-from $REGISTRY_HOST/$REPOSITORY:latest -t $REGISTRY_HOST/$REPOSITORY:$GITHUB_TAG -t $REGISTRY_HOST/$REPOSITORY:latest .

docker push $REGISTRY_HOST/$REPOSITORY:latest && docker push $REGISTRY_HOST/$REPOSITORY:$GITHUB_TAG
