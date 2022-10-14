docker run -it --rm --entrypoint /run/entry.sh -v $(pwd)/run/:/run -v $(pwd)/output:/input -v $(pwd)/result:/output -v /absolute/path/to/gurobi/licence:/gurobi/lic sebwink/deregnet:grb9.5.2
