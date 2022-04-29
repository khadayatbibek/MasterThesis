#!/bin/bash

kubectl create namespace thesis-khadayat

mkdir -vp entity-grid-jobs

for topic in $(seq 1 150); do
  sed "s/\$TOPIC/$topic/g" < ./kubernetes-job-template.yaml > ./entity-grid-jobs/topic-$( printf "%03d" ${topic} ).yaml
done