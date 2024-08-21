#!/bin/bash

REPO_URL=$(terraform output api_repository_url)
TAG=$1

if [ -z "${TAG}" ]; then
  echo "TAG is required"
  exit 1
fi

echo "Pushing docker image to ${REPO_URL} with tag ${TAG}"

aws ecr get-login-password | docker login --username AWS --password-stdin "${REPO_URL}"
docker build --platform linux/amd64 -t "${REPO_URL}":"${TAG}" .
docker push "${REPO_URL}":"${TAG}"
