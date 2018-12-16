FROM alpine:3.7

RUN adduser socek -u 4242 -g 4242 -D -H
RUN apk update && apk add --no-cache \
        python3 python3-dev nodejs \
        php7 py3-psycopg2 gcc \
        ruby ruby-dev \
        bash \
        musl-dev linux-headers iptables

RUN apk add --no-cache \
        git make bison flex protobuf protobuf-dev \
        g++ pkgconf autoconf libtool \
        bsd-compat-headers \
    && \
    git clone --depth=1 --branch=2.8 https://github.com/google/nsjail.git /nsjail && \
    cd /nsjail && \
    sed -i '1s/^/#define ST_RELATIME 4096\n/' mnt.cc && \
    make && \
    cp /nsjail/nsjail /bin && \
    rm -rf /nsjail

COPY requirements.txt .
RUN pip3 install -r requirements.txt

#security
RUN apk del gcc g++

ENV FLASK_APP=app.py
COPY code /code
RUN chmod 600 /code && chmod 600 -R /code
WORKDIR /code

CMD /bin/sh uwsgi_me.sh
