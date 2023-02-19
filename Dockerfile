FROM python:3.6

COPY manage.py gunicorn-cfg.py requirements.txt .env /src/

WORKDIR /src

RUN apt-get update -y
RUN apt-get -y install nano

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# tr_TR.UTF-8 UTF-8/tr_TR.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG tr_TR.UTF-8
ENV LC_ALL tr_TR.UTF-8

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Istanbul
RUN apt-get install -y tzdata

RUN dpkg-reconfigure tzdata

RUN pip install -r requirements.txt

RUN mkdir /root/logs

COPY . /src

EXPOSE 80
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]