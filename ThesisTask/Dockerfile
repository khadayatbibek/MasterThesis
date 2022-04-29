FROM python:3.8

ADD . /ThesisTask

RUN pip install -r /ThesisTask/requirements.txt

RUN set -x \
  && apt-get update \
  && apt-get install -y openjdk-17-jre-headless \
  && apt-get clean

WORKDIR /ThesisTask

ENTRYPOINT [ "/ThesisTask/CalculateCoherence.py" ]