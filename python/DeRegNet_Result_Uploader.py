#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 04:03:21 2022

@author: ttiede
"""
import os
from pysbml4j import Sbml4j, Configuration


def get_network_uuid(path):
    with open(os.path.join(path, "network_uuid"), "r") as f:
        uuid = f.read()
    return uuid


def get_file_uuid(path):
    with open(os.path.join(path, "file_uuid"), "r") as f:
        uuid = f.read()
    return uuid


def read_graphml(file_path):
    file = os.path.join(file_path, "optimal.graphml")
    with open (file, "r") as f:
        graphml = f.read()
    return graphml


def write_simple_file(file_path, file_content):
    with open(file_path, "w") as f:
        f.write(file_content)
        
        
def upload_graphml(graphml, parent_uuid, sbml4j, file_uuid):
    network_name =f"optimal_{file_uuid}"
    network_inv = sbml4j.uploadGraphML(graphml, parentUUID=parent_uuid, networkname=network_name, doPrefixName=False, doSuffixName=False)
    return network_inv[0]["uuid"]


def get_provenance(sbml4j:Sbml4j, uuid:str):
    provenance_json_string = sbml4j.getProvenance(uuid, "deregnet")
    return provenance_json_string


def main(data_path, result_path):
    
    network_uuid = get_network_uuid(data_path)
    file_uuid = get_file_uuid(data_path)
    
    config = Configuration(port=12342, user="deregnet")
    sbml4j = Sbml4j(config)
    result_network_uuid = upload_graphml(os.path.join(result_path, "optimal.graphml"), network_uuid, sbml4j, file_uuid)
    write_simple_file(os.path.join(result_path, "optimal_uuid"), result_network_uuid)
    
    print(f"The uploaded network has uuid: {result_network_uuid}")
    

if __name__ == "__main__":
    
    result_path = "result"
    data_path = "data/tcga"
    main(data_path, result_path)