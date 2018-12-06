FROM alpine:3.7

RUN apk update && apk add --no-cache python3 python3-dev nodejs php5 py3-psycopg2 gcc musl-dev linux-headers iptables
RUN adduser socek -u 4242 -g 4242 -D -H

COPY requirements.txt .
RUN pip3 install -r requirements.txt

#security
RUN apk del gcc 

ENV FLASK_APP=app.py
COPY code /code
RUN chmod 600 -R /code
WORKDIR /code

CMD /bin/sh uwsgi_me.sh
