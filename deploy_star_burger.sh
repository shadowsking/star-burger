#!/bin/bash
cd /opt/star-burger
git status
git pull

#docker-compose -f .\docker-compose-dev.yml up --build
#docker-compose up -d --force-recreate
docker-compose up -d --build

docker exec star-burger-backend python manage.py collectstatic --noinput
docker exec star-burger-backend python manage.py migrate --noinput

sudo systemctl reload nginx

source .env
revision=$(git rev-parse --verify HEAD)

curl --request POST \
     --url "https://api.rollbar.com/api/1/deploy" \
     --header "X-Rollbar-Access-Token: $ROLLBAR_ACCESS_TOKEN" \
     --header "content-type: application/json" \
     --data '
{
  "environment": "'"$ROLLBAR_ENVIRONMENT"'",
  "revision": "'"$revision"'"
}'
