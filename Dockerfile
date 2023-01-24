FROM python:3

RUN apt-get -y -qq update && \
    apt-get install -y -qq curl && \
    apt-get clean

COPY . /usr/app

WORKDIR /usr/app

RUN pip install --upgrade pip -r requirements.txt

ENTRYPOINT [ "python", "./main.py"]