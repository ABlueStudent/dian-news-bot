FROM python:alpine
WORKDIR /app

ADD . .
RUN apk update\ 
&& apk add build-base\ 
&& python -m pip install -r requirements.txt

CMD [ "python", "src/main.py" ]