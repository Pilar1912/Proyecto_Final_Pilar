#!/bin/bash

#BROKER="200.122.207.134"
BROKER="10.160.41.62:3000"
PORT=1884
TOPIC="iot/data/Grupo7"

# Coordenadas de campus
declare -A LAT
declare -A LON

LAT[robledo]=6.271717
LON[robledo]=-75.582458

LAT[fraternidad]=6.244213
LON[fraternidad]=-75.581452

LAT[castilla]=6.265547
LON[castilla]=-75.610989

LAT[poblado]=6.208520
LON[poblado]=-75.567029

while true; do
  # Robledo → solo temperatura
  TEMP=$(shuf -i 18-35 -n 1)
  mosquitto_pub -h "$BROKER" -p "$PORT" -t "$TOPIC" \
    -u "$MOSQUITTO_USERNAME" -P "$MOSQUITTO_PASSWORD" -m \
    "{\"sede\": \"Robledo\", \"temperature\": $TEMP, \"lat\": ${LAT[robledo]}, \"lon\": ${LON[robledo]}}"
  echo "🌡️ Sede Robledo → temperatura: $TEMP"

  # Espera 3–5 segundos antes del siguiente ciclo
  sleep $(shuf -i 3-5 -n 1)
done