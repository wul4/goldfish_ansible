#!/bin/bash

set -e

echo "Testing stage 1 calls with curl againtst proxy / LB node ip 192.168.120.7"
echo
echo "------ TEST 1 ------"
set -x
curl -v http://LOADBALANCER_IP:80/api/v1/hello/world/bar \
  | jq '.["message"]' \
  | grep "Hello world! Example setting is:" \
  || { set +x ; echo "TEST 1 [FAIL]" ; exit 1 ; }
set +x
echo "------ TEST 1 [OK] ------"
echo
echo "------ TEST 2 ------"
set -x
curl -v -H "Content-Type: application/json" -X POST \
  http://LOADBALANCER_IP:80/api/v1/hello/world/bar --data '{"bar": "test"}' \
  | jq '.["status"]' \
  | grep "Posted to Hello World!" \
  || { set +x ; echo "TEST 2 [FAIL]" ; exit 1 ; }
set +x
echo "------ TEST 2 [OK] ------"
echo
echo "Stage 1 tests [OK]"
