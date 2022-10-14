#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 18:44:56 2022

@author: ttiede
"""

"""
This is the Graph Preprocessing module of the graph pipeline
Run first Data Loader, then TCGA Data Preprocessing, then DeRegNet Graph Preprocessing
"""
import os
import numpy as np
import igraph

from pysbml4j import Sbml4j
from pysbml4j import Configuration


def write_simple_file(file_path, file_content):
    with open(file_path, "w") as f:
        f.write(file_content)
        

def create_igraph_from_sbml4j(graphml):
    graphml_file = write_graphml(graphml, "temp_deregnet_base.graphml")
    i_graph = igraph.read(graphml_file, format="graphml")
    os.remove("temp_deregnet_base.graphml")
    return i_graph


def create_name_to_id(i_graph, id_attribute):
    #print(i_graph)
    name_to_id = dict()
    for v in i_graph.vs:
        name_to_id[v["name"]] = v[id_attribute]
    return name_to_id


def is_self_loop(relationSymbol):
    parts = relationSymbol.split('->')
    target = parts[len(parts)-1]
    end = len(relationSymbol)-len(target)-2
    source_and_type = relationSymbol[0: end]
    relation_name = source_and_type.split("-")[-1]
    # the substring of source_and_type up to this length then is the source node
    source = source_and_type[:len(source_and_type) - len(relation_name) - 1]
    if source == target:
        return True
    else: 
        return False


def filter_self_loop(filter_dict):
    rel_filter = filter_dict['relationSymbols']
    for elem in rel_filter:
        if is_self_loop(elem):
            print(f"Removing relation {elem} from network")
            rel_filter.remove(elem)
    return filter_dict


def filter_node_by_missing_id(filter_dict, graphml_string, id_attribute):
    ig = create_igraph_from_sbml4j(graphml_string)
    name_to_id = create_name_to_id(ig, id_attribute)
    node_filter = filter_dict['nodeSymbols']
    for name in name_to_id:
        if name_to_id[name] == None or name_to_id[name] == "":
            print(f"Removing node {name} from network")
            node_filter.remove(name)
    return filter_dict


def filter_network_for_deregnet(sbml4j, network_uuid, final_networkname):
    rctk = sbml4j.getNetwork(network_uuid)
    filter_dict = rctk.getOptions()["filter"]
    filter_dict = filter_self_loop(filter_dict)
    #filter_dict = filter_node_by_missing_id(filter_dict, rctk.graphML(directed=True), "ensembl")
    rctk.filter(filter_dict, networkname=final_networkname, doPrefixName=False)
    return sbml4j.getNetworkByName(final_networkname)


def write_graphml(graphml, filename):
    print(f"Writing graphml to file {filename}")
    with open(filename, "w") as f:
        f.write(graphml)
    return filename


def get_network_uuid(path):
    with open(os.path.join(path, "network_uuid"), "r") as f:
        uuid = f.read()
        
    return uuid

def main(network_out, graphml_out, data_path):
    host="http://localhost"
    port = "12342"
    app_context = "/sbml4j"
    user = "deregnet"

    conf = Configuration(host, port, app_context, user=user)
    sbml4j = Sbml4j(conf)

    network_uuid = get_network_uuid(data_path)
    filtered_net = filter_network_for_deregnet(sbml4j, network_uuid, network_out)

    write_graphml(filtered_net.graphML(directed=True), graphml_out)
    
    final_network_uuid = filtered_net.getInfoDict()['uuid']
    
    write_simple_file(os.path.join(data_path, 'network_uuid'), final_network_uuid)
    print(f"The deregnet base network is: {network_out} and has uuid: {final_network_uuid}")
   
    
if __name__ == "__main__":
    #network_to_use = "REGULATORY_CANCER_TOPIC_KEGG"

    #network_uuid_in = "SIGNALLING_cancer_types"
    network_out = "DeRegNet_SIG_Base_KEGG_Cancer_Types_chapter4"
    graphml_out = "output/deregnet_base_cancer_types_chapter4.graphml"
    data_path = "data/tcga"
    main(network_out, graphml_out, data_path)
  
   
    


"""
This is the old code stuff
"""
def create_deregnet_base(sbml4j):
    rctk = sbml4j.getNetworkByName("REGULATORY_CANCER_TOPIC_KEGG")
    options = rctk.getOptions()
    annotation_opt = options['annotation']
    
    rel_an = annotation_opt['relationAnnotation']
    
    filter_list = []
    for an in rel_an:
        parts = an.split('->')
        target = parts[len(parts)-1]
        end = len(an)-len(target)-2
        source_and_type = an[0: end]
        #print(source_and_type)
        if target in source_and_type:
            if source_and_type[len(target):].startswith('-') and "-" not in source_and_type[len(target)+1:]:
                # Self Loop!
                #Filter them out
                filter_list.append(an)
        
    # now remove the elements in filter_list from the filter dict
    
    filter_dict = options['filter']
    rel_filter = filter_dict['relationSymbols']
    for elem in filter_list:
        print(elem)
        rel_filter.remove(elem)
        
    # now rel_filter and since it is object by reference the filter_dict only contains 
    # those relation symbols that are not self loops
    
    # we also need to remove those nodes that do not have an ensembl id
    # we plan to use it to map the scores and each node needs to be accounted for
    rctk_graphml = rctk.graphML(directed=True)
    iGraph = create_igraph_from_sbml4j(rctk_graphml)
    name_to_ensembl = create_name_to_id(iGraph, "ensembl")
    
    node_filter = filter_dict['nodeSymbols']
    for name in name_to_ensembl:
        if name_to_ensembl[name] == None or name_to_ensembl[name] == "":
            print(f"Removing node {name} from network")
            node_filter.remove(name)
            
    # now also only nodes that have an ensembl id set are in the network
    
    # use it to filter the network
    
    rctk.filter(filter_dict, networkname="DeRegNet_REG_Base_Cancer_Topic_No_Self_Loops_All_Ensembl", doPrefixName=False)


def is_self_loop2(relationSymbol):
    parts = relationSymbol.split('->')
    target = parts[len(parts)-1]
    end = len(relationSymbol)-len(target)-2
    source_and_type = relationSymbol[0: end]
    #print(source_and_type)
    if target in source_and_type:
        if source_and_type[len(target):].startswith('-') and "-" not in source_and_type[len(target)+1:]:
            # Self Loop!
            #Filter them out
            return True
    return False
    
def write_score_csv(dictionary):
    header = ["id", "score"]
    with open ("score.csv", 'w') as s:
        s.write("id;score\n")
        for elem in dictionary:
           s.write(f'"{elem}";{dictionary[elem]}\n')

    
def create_synthetic_scores(sbml4j, baseNet, name_to_ensembl):
    
    ensembl_score_dict = dict()
    nodeDict = baseNet.getOptions()['annotation']['nodeAnnotation']
    for elem in nodeDict:
        if name_to_ensembl[elem] != None and name_to_ensembl[elem] != "":
            ensembl_score_dict[name_to_ensembl[elem]] = np.random.random()
        nodeDict[elem] = np.random.random()
        
    return ensembl_score_dict
    #return nodeDict
    #write_score_csv(nodeDict)
    
    
def old_main():
    host="http://localhost"
    port = "8080"
    app_context = "/sbml4j"
    user = "deregnet"
    
    conf = Configuration(host, port, app_context, user=user)
    
    sbml4j = Sbml4j(conf)
    
    #sbml4j.listNetworks()
    
    create_deregnet_base(sbml4j)
    
    baseNet = sbml4j.getNetworkByName("DeRegNet_REG_Base_Cancer_Topic_No_Self_Loops_All_Ensembl")
    
    #nodeDict = create_synthetic_scores(sbml4j, baseNet)
    
    # now get the graphml, convert to igraph and map the name to the Ensembl Id
    graphml = baseNet.graphML(directed=True)
    graphml_file = write_graphml(graphml, "temp_deregnet_base.graphml")
    i_graph = igraph.read(graphml_file, format="graphml")
    #print(i_graph)
    name_to_ensembl = dict()
    for v in i_graph.vs:
        name_to_ensembl[v["name"]] = v["ensembl"]
    
    # now use the name_to_ensembl dict  to create the score file from the nodeAnnotation
    score_dict = create_synthetic_scores(sbml4j, baseNet, name_to_ensembl)
    
    write_score_csv(score_dict)
    
    print(score_dict)


