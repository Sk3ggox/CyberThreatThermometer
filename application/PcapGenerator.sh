#!/usr/bin/env bash

while true; do
	sudo tcpdump -G 1 -W 1 -w example.pcap -i ens33 -nn -Z student;
	sleep 1;
done