#!/bin/bash

BROKER=localhost
PORT=1884
TOPIC="iot/data"

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
    "{\"sede\": \"a\", \"temperature\": $TEMP, \"lat\": ${LAT[robledo]}, \"lon\": ${LON[robledo]}}"
  echo "🌡️ Sede a → temperatura: $TEMP"

  # Fraternidad → solo humedad
  HUM=$(shuf -i 40-100 -n 1)
  mosquitto_pub -h "$BROKER" -p "$PORT" -t "$TOPIC" \
    -u "$MOSQUITTO_USERNAME" -P "$MOSQUITTO_PASSWORD" -m \
    "{\"sede\": \"b\", \"humidity\": $HUM, \"lat\": ${LAT[fraternidad]}, \"lon\": ${LON[fraternidad]}}"
  echo "💧 Sede B → humedad: $HUM"

  # Castilla → solo velocidad del viento
  WIND=$(shuf -i 0-40 -n 1)
  mosquitto_pub -h "$BROKER" -p "$PORT" -t "$TOPIC" \
    -u "$MOSQUITTO_USERNAME" -P "$MOSQUITTO_PASSWORD" -m \
    "{\"sede\": \"c\", \"wind_speed\": $WIND, \"lat\": ${LAT[castilla]}, \"lon\": ${LON[castilla]}}"
  echo "🍃 Sede C → viento: $WIND"

  # Poblado → solo PM2.5
  PM25=$(shuf -i 5-120 -n 1)
  mosquitto_pub -h "$BROKER" -p "$PORT" -t "$TOPIC" \
    -u "$MOSQUITTO_USERNAME" -P "$MOSQUITTO_PASSWORD" -m \
    "{\"sede\": \"d\", \"pm25\": $PM25, \"lat\": ${LAT[poblado]}, \"lon\": ${LON[poblado]}}"
  echo "🫧 Sede D → PM2.5: $PM25"

  # Espera 3–5 segundos antes del siguiente ciclo
  sleep $(shuf -i 3-5 -n 1)
done
