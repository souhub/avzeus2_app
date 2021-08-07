FROM python:3.8

RUN apt update \
    && apt install -y default-mysql-client \
    && apt install --no-install-recommends -y tzdata \
    && apt clean

WORKDIR /usr/src/app

COPY services/admin_itube ./app
COPY services/database ./database
COPY services/utils ./utils
COPY scripts ./scripts

COPY docker/admin_itube/requirements.txt requirements.txt
RUN pip install -U pip \
    && pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8080

WORKDIR /usr/src/app/app
