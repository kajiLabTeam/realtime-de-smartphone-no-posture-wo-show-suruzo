#!/bin/sh

cd /home/tada/realtime-zou
/home/tada/.local/bin/uvicorn main:app --host 0.0.0.0

