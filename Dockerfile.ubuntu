FROM ubuntu:18.04

RUN groupadd socek --gid 4242
RUN useradd socek \
    --uid 4242 --gid 4242 \
    --no-create-home \
    --shell /bin/false
RUN apt-get -y update && apt-get install -y \
    autoconf \
    bison \
    flex \
    gcc \
    g++ \
    git \
    libprotobuf-dev \
    libtool \
    make \
    pkg-config \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth=1 --branch=2.8 https://github.com/google/nsjail.git /nsjail && \
    cd /nsjail && \
    make && \
    cp /nsjail/nsjail /bin && \
    rm -rf /nsjail

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && apt-get install -y \
    python3 python3-dev python3-psycopg2 python3-pip \
    nodejs \
    php \ 
    ruby ruby-dev \
    bash \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install -r requirements.txt

#security!
RUN apt-get purge -y gcc g++ git make

ENV FLASK_APP=app.py
COPY code /code
RUN chmod 600 /code && chmod 600 -R /code
WORKDIR /code

CMD /bin/sh uwsgi_me.sh
