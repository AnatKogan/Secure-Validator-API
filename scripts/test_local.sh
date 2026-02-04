#!/usr/bin/env bash
set -e

curl -s http://localhost:8080/health | grep -q ok

code=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8080/validate \
  -H "Content-Type: application/json" -d '{"value":"wrong"}')
test "$code" = "401"

code=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8080/validate \
  -H "Content-Type: application/json" -d '{"value":"1234"}')
test "$code" = "200"
