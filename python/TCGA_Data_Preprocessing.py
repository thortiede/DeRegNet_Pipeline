#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 18:44:56 2022

@author: ttiede
@version: 1.0
"""

"""
This is the Data Preprocessing module of the data pipeline
Run first Data Loader, then TCGA Data Preprocessing, then DeRegNet Graph Preprocessing
"""

import os
import pandas as pd

from pysbml4j import Sbml4j, Configuration


def get_network_uuid(path):
    with open(os.path.join(path, "network_uuid"), "r") as f:
        uuid = f.read()
        
    return uuid

def get_file_uuid(path):
    with open(os.path.join(path, "file_uuid"), "r") as f:
        uuid = f.read()
        
    return uuid


def send_metadata(config, network_uuid, input_file):
    # build a provenance dict for this step
    prov_dict = dict()
    prov_dict["script"] = "TCGA_Data_Preprocessing.py"
    prov_dict["version"] = 1.0
    prov_dict["match_id"] = "name"
    prov_dict["score_column"] = "avg_log2FC"
    prov_dict["input_file"] = input_file

    # Add provenance to the network
    sbml4j = Sbml4j(config)
    sbml4j.addProvenance(network_uuid, "data_preprocessing", prov_dict)
    
    
def preprocess_data(local_file_path, id_col_name, output_path, file_uuid):
    df = pd.read_csv(local_file_path, sep='\t', header=0)
    
    output_header = ["id","score"]
    out_df = df[[id_col_name, "avg_log2FC"]]
    out_df.to_csv(os.path.join(output_path, f"{file_uuid}_score.csv"),
                  sep = ';',
                  header=output_header, 
                  index=False)
    
def main(base_path, output_path):
    
    network_uuid = get_network_uuid(base_path)
    file_uuid = get_file_uuid(base_path)
    local_file_path=f"{base_path}{file_uuid}.tsv"

    id_col_name = "gene_names"
    # incase of id_col = ensembl, and it contains the version, uncomment the following line
    #df["ensembl"] = df["gene"].str.split(pat='.').str[0]
    
    preprocess_data(local_file_path, id_col_name, output_path, file_uuid)
    
    config = Configuration(port=12342, user="deregnet")
    
    send_metadata(config, network_uuid, local_file_path)
    
    print(F"The score file is at {os.path.join(output_path, f'{file_uuid}_score.csv')}")
    
if __name__ == "__main__":
    input_path = "data/tcga/"
    output_path = "output"
    main(input_path, output_path)
    
    
def run(input_path, output_path):
    main(input_path, output_path)