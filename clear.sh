#!/bin/bash

rm ./data/tcga/*
rm ./result/*
rm ./output/*

cd sbml4j-compose
docker-compose down

./sbml4j.sh -r deregnet_base_mapping_prov

docker-compose up -d
