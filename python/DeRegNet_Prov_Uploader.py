#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 04:03:21 2022

@author: ttiede
"""
import os
import json
from pysbml4j import Sbml4j, Configuration

def get_network_uuid(path):
    with open(os.path.join(path, "optimal_uuid"), "r") as f:
        uuid = f.read()    
    return uuid


def write_simple_file(file_path, file_content):
    with open(file_path, "w") as f:
        f.write(file_content)
        

def get_provenance(sbml4j:Sbml4j, uuid:str):
    provenance_json_string = sbml4j.getProvenance(uuid, "deregnet")
    return provenance_json_string


def main(result_path):
    
    network_uuid = get_network_uuid(result_path)
    
    config = Configuration(port=12342, user="deregnet")
    sbml4j = Sbml4j(config)
    
    metadata = {
            "URL": "https://github.com/KohlbacherLab/deregnet",
            "Release": "Gurobi 9.5.x Release"
            }
    
    provenance_json_string= sbml4j.addProvenance(network_uuid, "DeRegNet", metadata)
    provenance_file = os.path.join(result_path, "optimal_prov.json")
    write_simple_file(provenance_file, json.dumps(provenance_json_string,  indent=2))
    
    print(f"The uploaded network has uuid: {network_uuid}")
    print(f"The provenance report is in : {provenance_file}")
    

if __name__ == "__main__":
    
    result_path = "result"
    main(result_path)