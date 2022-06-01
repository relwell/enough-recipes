#!/bin/bash

helm install -n enough-recipes\
             broker bitnami/kafka \
              --set=persistence.storageClass=vultr-block-storage \
              --set=persistence.size=10Gi \
              --set=zookeeper.persistence.storageClass=vultr-block-storage \
              --set=zookeeper.persistence.size=10Gi
