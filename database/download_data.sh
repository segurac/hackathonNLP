#!/bin/bash

for url in $(python3 create_links_download.py); 
    do 
        wget $url 
done
