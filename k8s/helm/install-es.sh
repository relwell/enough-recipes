#!/bin/bash -e

helm install -n enough-recipes \
             es bitnami/elasticsearch \
              --set=master.persistence.storageClass=vultr-block-storage \
              --set=master.persistence.size=10Gi \
              --set=data.persistence.storageClass=vultr-block-storage \
              --set=data.persistence.size=10Gi
