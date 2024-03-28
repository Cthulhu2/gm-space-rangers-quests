#!/bin/sh

IP=127.0.0.1

echo "[req]
default_bits  = 2048
distinguished_name = req_distinguished_name
req_extensions = req_ext
x509_extensions = v3_req
prompt = no

[req_distinguished_name]
countryName = XX
stateOrProvinceName = N/A
localityName = N/A
organizationName = Cthulhu Fhtagn
commonName = $IP

[req_ext]
subjectAltName = @alt_names

[v3_req]
subjectAltName = @alt_names

[alt_names]
IP.1 = $IP
" > san.cnf

openssl req -x509 -nodes \
  -days 2911970 \
  -newkey rsa:2048 \
  -keyout ./cert/key.pem \
  -out ./cert/cert.pem \
  -config san.cnf
rm san.cnf
