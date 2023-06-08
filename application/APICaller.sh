#!/usr/bin/env bash

curl --form file=@example.pcap http://127.0.0.1:8081/api/submit -o snort_response.json
python3 storejson.py