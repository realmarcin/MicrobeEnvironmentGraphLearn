# MicrobeEnvironmentGraphLearn

## Repository for graph analysis and graph learning on microbial environmental data


The analysis can be replicated as follows:

1. Obtain environmental microbe data graph with file name:
   ```masterG.edgelist.tsv```

2. Assuming in main repository directory, run:

   ```make```

   This will generate a set of files and the file:

   ```masterG_edges.tsv```

   will be formatted to work with the [Embiggen package](https://github.com/monarch-initiative/embiggen).

   The file:
   
   ```masterG_edges_nodes_intindex.txt```

   will be formatted to work with the [SNAP HPC implementation](https://github.com/snap-stanford/snap/tree/master/examples/node2vec), including node2vec.

   In addition, the file:
   
   ```masterG.edgelist_col12_nodes_meta.txt```
   
   contains node types formatted as metadata for the embedding projector (see below).

3. Run SNAP node2vec with the following parameters and [slurm script](https://github.com/realmarcin/MicrobeEnvironmentGraphLearn/blob/master/run_kgcovid_l100_r100.sl).


4. The resulting embeddings can be visualized:
- Using the [UMAP notebook](https://github.com/realmarcin/MicrobeEnvironmentGraphLearn/blob/master/embedding_umap.ipynb). 
- Using the [embedding projector](https://projector.tensorflow.org/).



