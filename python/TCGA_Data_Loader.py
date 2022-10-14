#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 22:08:45 2022

@author: ttiede
"""

"""
This is the Data Loader Pipeline Component
Run first Data Loader, then TCGA Data Preprocessing, then DeRegNet Graph Preprocessing
"""
import os

import urllib3
import json
import pysbml4j




def main(file_uuid, base_network_name, base_path):
    http = urllib3.PoolManager()


    tcga_metadata = dict()
    tcga_base_url = "https://api.gdc.cancer.gov"
    #file_uuid = "ef7ad432-5692-4e10-8543-984ef08fd3a2"
    #file_uuid = "9f7f4c2e-aa58-4aa3-a904-09343a6c4bda"
    file_uuid="69a92ea6-7d1e-4cac-a65f-b8afa2380e97"

    data_folder = "data"
    download_file_url = '/'.join([tcga_base_url, data_folder, file_uuid])
    
    project_id = "CPTAC-3"
    
    tcga_metadata["file_uuids"] = list()
    
    local_file_path=f"{base_path}{file_uuid}.tsv"


    download_project_metadata(poolmanager=http,
                              tcga_url=tcga_base_url,
                              project_id=project_id, 
                              metadata=tcga_metadata)
    
    download_file(poolmanager=http,
                    fileresource=download_file_url,
                    local_file_path=local_file_path,
                    metadata=tcga_metadata
                    )



    
    match="gene_names"
    base_net_uuid = sbml4j_connector(metadata=tcga_metadata,
                                     base_network_name=base_network_name,
                                     file_uuid=file_uuid,
                                     file_path=local_file_path,
                                     match=match)    
    print(f"The base network with data annotations and provenance information has uuid {base_net_uuid}")
    print(f"The data file can be found at {local_file_path}")
    
    write_simple_file(f"{base_path}network_uuid", base_net_uuid)
    write_simple_file(F"{base_path}file_uuid", file_uuid)
    
def write_simple_file(file_path, file_content):
    with open(file_path, "w") as f:
        f.write(file_content)
        

def download_project_metadata(poolmanager,
                              tcga_url, 
                              project_id, 
                              metadata:dict):
    
    status_url = os.path.join(tcga_url, "status")
    r = poolmanager.request('GET', status_url)
    
    if r.status == 200:
        metadata["status_url"] = status_url
        metadata["status"] = json.loads(r.data.decode())

    projects = "projects"
    project_params = "?expand=summary,summary.experimental_strategies,summary.data_categories&pretty=false"

    cptac3_url = '/'.join([tcga_url, projects, project_id]) + project_params
    print(cptac3_url)

    r = poolmanager.request('GET', cptac3_url)
    if r.status == 200:
        metadata["project_cptac3_url"] = cptac3_url
        metadata["project_cptac3"] = json.loads(r.data.decode())


def download_file(poolmanager, fileresource, local_file_path, metadata:dict):
    file_uuid = fileresource.split('/')[-1]
    r = poolmanager.request('GET', fileresource, preload_content=False)
    chunk_size = 32
    if r.status == 200:
        metadata["file_uuids"].append(file_uuid)
        metadata["download_file_"+file_uuid+"_url"] = fileresource
        metadata["download_file_"+file_uuid+"_filename"] = r.headers["Content-Disposition"].split('=')[-1]
        metadata["download_file_"+file_uuid+"_Date"] = r.headers["Date"]
        metadata["download_file_"+file_uuid+"_Content-Length"] = r.headers["Content-Length"]
        metadata["download_file_"+file_uuid+"_Content-MD5"] = r.headers["Content-MD5"]
        #local_file_path = '_'.join(['/'.join([file_path, file_uuid]), metadata["download_file_"+file_uuid+"_filename"]])
    
    with open(local_file_path, 'wb') as out:
        while True:
            data = r.read(chunk_size)
            if not data:
                break
            out.write(data)
    
    r.release_conn()
    return fileresource


def sbml4j_connector(metadata:dict,
                     base_network_name="DeRegNet_SIG_Base_Cancer_Types_No_Self_Loops", 
                     file_uuid="69a92ea6-7d1e-4cac-a65f-b8afa2380e97",
                     file_path="",
                     match="gene_names",
                     config=pysbml4j.Configuration(port=12342, user="deregnet")):
    
    sbml4j = pysbml4j.Sbml4j(config)
    
    # Get the base network
    base_net = sbml4j.getNetworkByName(base_network_name)
    
    print(f"base net uuid before adding raw data: {base_net.getInfoDict()['uuid']}")
    # Add all matching data points to the network of choice
    networkname = "DeRegNet_Raw_Data_"+file_uuid
    base_net.addCsvData(file_path, file_uuid, networkname=networkname, doPrefixName=False, match=match, doDerive=True)
    
    # Add metadata to network
    raw_data_net_uuid = sbml4j.getNetworkByName(networkname).uuid
    print(f"Network with raw data annotation has uuid {raw_data_net_uuid}")
    sbml4j.addProvenance(raw_data_net_uuid, file_uuid, metadata)
    print(f"base net uuid after adding raw data: {base_net.getInfoDict()['uuid']}")
    return raw_data_net_uuid
    
    # cases.project.project_id in ["CPTAC-3"] and files.access in ["open"] 
    # and files.analysis.workflow_type in ["Seurat - 10x Chromium"] 
    # and files.data_format in ["tsv"] 
    # and files.data_type in ["Differential Gene Expression"]



    

if __name__ == "__main__":
    file_uuid="69a92ea6-7d1e-4cac-a65f-b8afa2380e97"
    #base_network_name="DeRegNet_SIG_Base_KEGG_Cancer_Types_Diss"
    base_network_name="SIGNALLING_cancer_types"
    base_path="data/tcga/"
    main(file_uuid, base_network_name, base_path)
    

def load(file_uuid, base_network_name):
    main(file_uuid, base_network_name)









"""
project_files_params="?expand=files"
cptac3_files_url = '/'.join([tcga_base_url, projects, project_id]) + project_files_params
print(cptac3_files_url)

r = http.request('GET', cptac3_files_url)
if r.status == 200:
    metadata["project_cptac3_files_url"] = cptac3_files_url
    metadata["project_cptac3_files"] = r.data
    print(json.loads(r.data))
"""