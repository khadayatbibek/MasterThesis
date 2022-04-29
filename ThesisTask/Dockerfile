FROM python:3.8

ADD . /entity_grid

RUN pip install -r /entity_grid/requirements.txt

RUN set -x \
  && apt-get update \
  && apt-get install -y openjdk-17-jre-headless \
  && apt-get clean

WORKDIR /entity_grid

ENTRYPOINT [ "/entity_grid/CalculateCoherence.py" ]