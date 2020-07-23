# MicrobeEnvironmentGraphLearn

## Repository for graph analysis and graph learning on microbial environmental data


The analysis can be replicated as follows:

1. Obtain environmental microbe data graph with file name:
```masterG.edgelist.tsv```

2. Assuming in main repository directory, run:
```make```

This will generate a set of files and the file:

``masterG_edges.tsv```

will be formatted to work with the Embiggen package.

3. To generate input files for SNAP node2vec and the online embedding projector:

- download ```MAK.jar```

```curl https://genomics.lbl.gov/~marcin/MAK.jar > MAK.jar```

- run to convert to integer indices and node type file:

tail -n+2 masterG_edges.tsv > masterG_edges_nohead.tsv
java -classpath MAK.jar DataMining.util.EdgestoInts masterG_edges_nohead.tsv

this will generate the following files:
```
masterG.edgelist_intindex.txt
masterG.edgelist_col12_nodes_meta.txt
masterG.edgelist_col12_nodes_intindex.txt
```

4. Run SNAP node2vec with the following parameters and slurm script using ```masterG.edgelist_intindex.txt``` as input:
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



