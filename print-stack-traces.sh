#!/bin/bash

for i in 1 2 3 4; do
  echo "Stack trace for worker $i"
  uwsgi --connect-and-read pytracebacker.socket$i
done
