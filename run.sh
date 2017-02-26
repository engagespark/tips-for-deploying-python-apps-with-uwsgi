#!/bin/bash

uwsgi \
  -w app \
  --callable app \
  --http :8080 \
  --master \
  --processes 4 \
  --stats=":8001" \
  --py-tracebacker ./pytracebacker.socket \
  --harakiri=65 \
  $*
