#!/bin/bash
cd /opt/star-burger
git status
git pull

npm ci --dev
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

if [ ! -d "venv" ]; then
    python -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput

sudo systemctl restart star-burger
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
