#!/bin/sh

#--graph /io/test/reg_cancer_topic_no_selfloops.graphml \
# --scores /io/test/data/score_ensembl_sbml4j.csv \
avgdrgnt.py \
--graph /input/deregnet_base_cancer_types_chapter4.graphml \
--scores /input/69a92ea6-7d1e-4cac-a65f-b8afa2380e97_score.csv \
--sep ';' \
--graph-id-attr name \
--output-path /output

