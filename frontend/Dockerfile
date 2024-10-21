FROM node:16.16.0

WORKDIR /opt/app

COPY frontend .

RUN npm ci --dev

RUN ./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles_dst --public-url="./"

CMD ["bash", "-c", "cp bundles_dst/* bundles"]
