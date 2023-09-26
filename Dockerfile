ARG BUILD_TYPE=dev
ARG SSH_HOST
ARG SSH_PATH

FROM python:3.10-slim AS nlp-toolkit-base

WORKDIR /libs
COPY . /libs
COPY ./requirements.txt requirements.txt
ONBUILD COPY scripts/ ./scripts
ONBUILD RUN mkdir ./data

RUN apt-get update --allow-releaseinfo-change && \
    apt-get install --no-install-recommends -y curl jq wget git build-essential openssh-client

RUN pip install -r requirements.txt
RUN python -m nltk.downloader stopwords punkt wordnet omw-1.4
EXPOSE 8080

ENV BUILD_MODE=local
ENV SVC_NAME=nlp_toolkit

CMD /bin/sh -c "python -m pytest ./tests  -s -x"