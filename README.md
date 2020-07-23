# MicrobeEnvironmentGraphLearn

## Repository for graph analysis and graph learning on microbial environmental data


The analysis can be replicated as follows:

1. Obtain environmental microbe data graph with file name:
   ```masterG.edgelist.tsv```

2. Assuming in main repository directory, run:
   ```make```

   This will generate a set of files and the file:

   ```masterG_edges.tsv```

   will be formatted to work with the Embiggen package.

   The file:
   ```masterG_edges_nodes_intindex.txt```

   will be formatted to work with the SNAP framework algorithms, including node2vec.

   In addition, the file:
   ```masterG.edgelist_col12_nodes_meta.txt```
   contains node types formatted as metadata for the [embedding projector](https://projector.tensorflow.org/).

3. Run SNAP node2vec with the following parameters and slurm script using ```masterG.edgelist_intindex.txt``` as input:
```
#!/bin/bash
#SBATCH --qos=lr_normal
#SBATCH --partition=lr_bigmem
#SBATCH --account=ac_mak
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1024G
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --error=%x-%j.err
#SBATCH --output=%x-%j.out


date

./node2vec -i:masterG.edgelist_intindex.txt -o:masterG.edgelist_intindex.emb -l:100 -r:100 -k:10 -e:10 -d:128 -p:1 -q:1

date
```

4. The resulting embeddings can be visualized using the UMAP notebook in [this repository](https://github.com/realmarcin/MicrobeEnvironmentGraphLearn/blob/master/embedding_umap.ipynb). 



