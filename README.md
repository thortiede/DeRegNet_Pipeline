# DeRegNet Research Pipeline with SBML4j

Research Pipeline to use DeRegNet with SBML4j.

This pipeline performs the following steps if SBML4j is running and DeRegNet is configured properly.

Data Pipeline to gather a specific public file from TCGA and Preprocesses the data to be used with DeRegNet

Graph Pipeline to prepare a network (after SBML4j is Loaded with the first three steps of the graph pipeline (not in this repository)).

DeRegNet_Pipeline_Component to run DeRegNet on the score and graph produced

Upload the solution to SBML4j and gather the provenance report.

# Usage

### Prerequisits
A SBML4j instance has to run and be loaded with the networks of choice.
I recommend using sbml4j-compose (https://github.com/thortiede/sbml4j-compose).
Then use KPWD (https://github.com/thortiede/KPWD) to download Pathways from KEGG.
Be aware that you need a valid license to use the KEGG pathways.
Please refer to https://kegg.jp on when you need a license and how to get one!
Then use KEGGtranslator (http://www.cogsys.cs.uni-tuebingen.de/software/KEGGtranslator/) to translate the Pathways to the SBML_CORE_AND_QUAL format.
Afterwards you can use the SBML4j intializer (https://github.com/thortiede/S4IWP) to upload the translated pathways and create the desired network mapping.

Make a backup of the database before running any script you find here.

### Before running the Pipeline

The following adjustments to your local environment have to be made:
1. clear.sh: Change the name of the sbml4j backup (deregnet_base_mapping_prov) to the one you made above.
2. DeRegNet_Pipeline_Component/run_deregnet.sh: Change the /absolute/path/to/gurobi/licence to the path of your Gurobi License file.
3. DeRegNet_Pipeline_Component: Replace the folders *output* and *result* with symbolic links to the same folders in the main directory.

### Execute the Pipeline
The Pipeline can be run using the script

	./run_pipeline.sh

### Execute the Pipeline again
To rerun the pipeline and reset the database before the execution you can use

	./rerun_pipeline.sh

# Final words
This software comes as is. No warranties. Run at your own risk.

A special thank you goes out to Sebastian Winkler for his help in adjusting DeRegNet to the new Gurobi Licensing scheme.
You can find DeRegNet at https://github.com/sebwink/deregnet

