# syntax = docker/dockerfile:1.0-experimental
# DOCKER_BUILDKIT=1 docker build . -f recommendations/Dockerfile -t recommendations --secret id=ca.key,src=ca.key

FROM python:3.9-slim as base

RUN mkdir /service
COPY . /service/
WORKDIR "/service/"

RUN apt update
RUN apt install -y git

RUN pip install --upgrade pip
RUN --mount=type=secret,id=PASSPORT_CI_TOKEN \
  export PASSPORT_CI_TOKEN=$(cat /run/secrets/PASSPORT_CI_TOKEN) && \
  pip install --editable ./servicer[dev,test,docs] && \
  pip install -r servicer/requirements.txt

EXPOSE 50051
ENTRYPOINT [ "python", "-m", "src.package_server.__main__" ]

###########START NEW IMAGE : DEBUGGER ###################
FROM base as debug
RUN pip install ptvsd


###########START NEW IMAGE: STAGING ###################
FROM base as staging


###########START NEW IMAGE: PRODUCTION ###################
FROM base as prod
