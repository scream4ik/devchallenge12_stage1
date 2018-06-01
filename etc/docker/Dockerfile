FROM python:3.6

RUN printf "deb http://httpredir.debian.org/debian jessie-backports main non-free\ndeb-src http://httpredir.debian.org/debian jessie-backports main non-free" > /etc/apt/sources.list.d/backports.list
RUN apt-get update \
    \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    \
    rsync \
    sshpass \
    libmaxminddb-dev \
    libmaxminddb0 \
    mmdb-bin \
    binutils \
    libproj-dev \
    gdal-bin \
    wget \
    \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /code
ADD etc/requirements.txt /code/
RUN pip3 install -r /code/requirements.txt
ADD . /code/
WORKDIR /code

RUN mkdir /root/geolite2
RUN wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz -O GeoLite2-City.tar.gz && tar -zxvf GeoLite2-City.tar.gz -C /root/geolite2 --strip 1 && rm GeoLite2-City.tar.gz
RUN wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz -O GeoLite2-Country.tar.gz && tar -zxvf GeoLite2-Country.tar.gz -C /root/geolite2 --strip 1 && rm GeoLite2-Country.tar.gz
