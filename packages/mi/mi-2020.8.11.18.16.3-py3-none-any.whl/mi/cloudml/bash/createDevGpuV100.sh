#!/usr/bin/env bash
if [ -n "$1" ]
then name=$1
else name=v100
fi;

password=xiaomi
cloudml dev create -n $name -p $password \
--priority_class guaranteed \
-hka h_browser@XIAOMI.HADOOP -hkt tql -he hdfs://zjyprc-hadoop \
-d cr.d.xiaomi.net/cloud-ml/tensorflow-gpu:33103tql2dev  \
-cm rw \
-c 32 -M 32G \
-g 1 -gt v100 -gm 32g

