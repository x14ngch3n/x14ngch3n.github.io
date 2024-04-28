#!/usr/bin/env bash

# get map as image from Google Map API
curl "https://maps.googleapis.com/maps/api/staticmap?\
key=${GOOGLE_MAP_API_KEY}&\
center=20,0&\
zoom=1&\
size=500x250&\
scale=2&\
markers=size:tiny|Melbroune|Shenzhen|Lisbon" --output ./assets/img/map.png
