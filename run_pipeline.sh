#!/bin/bash

python python/TCGA_Data_Loader.py
python python/TCGA_Data_Preprocessing.py
echo "====== Data Preprocessig finished ====="

python python/DeRegNet_Graph_Preprocessing.py

echo "====== Graph Preprocessig finished ====="


# The run DeRegnet
cd DeRegNet_Pipeline_Component
./run_deregnet.sh

echo "====== DeRegNet finished ====="

cd ..
python python/DeRegNet_Result_Uploader.py

echo "====== Result uplodaded, Uploading provenance: ====="

python python/DeRegNet_Prov_Uploader.py

echo "====== Done ======"
