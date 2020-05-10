#!/bin/bash

set -e

echo "Testing stage 2 calls with curl againtst proxy / LB node ip 192.168.120.7"
echo
echo "------ TEST 1 ------"
set -x
curl -v -X DELETE http://LOADBALANCER_IP:80/api/v1/hello/world/bar \
  | jq '.["message"]' \
  | grep "Hello from Bar DELETE" \
  || { set +x ; echo "TEST 1 [FAIL]" ; exit 1 ; }
set +x
echo "------ TEST 1 [OK] ------"
echo
echo "------ TEST 2 ------"
set -x
curl -v http://LOADBALANCER_IP:80/api/v2/newapi/pebble \
  | jq '.["payload"]' \
  | grep "Pebble logo yelling back!" \
  || { set +x ; echo "TEST 2 [FAIL]" ; exit 1 ; }
set +x
echo "------ TEST 2 [OK] ------"
echo
echo "Stage 2 tests [OK]"
