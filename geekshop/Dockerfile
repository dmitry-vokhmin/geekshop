FROM python:3.8.5-alpine
WORKDIR /usr/src/geekshop
RUN apk --update --no-cache bash gcc
RUN apk update
RUN apk add make posgresql-dev gcc python3-dev posgresql-client
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
