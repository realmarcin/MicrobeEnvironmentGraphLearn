# MicrobeEnvironmentGraphLearn

Repository for graph analysis and graph learning on microbial environmental data


The analysis can be replicated as follows:

1. Obtain environmental microbe data graph with file name:
masterG.edgelist.tsv

2. Run:
make

This will generate a set of files and the file:

masterG_edges.tsv

will be formatted to work with Embiggen.

3. To generate input files for SNAP node2vec and the online embedding projector:

a) download MAK.jar

b) run to convert to integer indices and node type file:

tail -n+2 masterG_edges.tsv > masterG_edges_nohead.tsv
java -classpath MAK.jar DataMining.util.EdgestoInts masterG_edges_nohead.tsv

4. Run SNAP node2vec with the following parameters and slurm script:

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

./node2vec -i:../../../../MicrobeEnvironmentGraphLearn/ENIGMA_data/masterG.edgelist_intindex.txt -o:../../../../MicrobeEnvironmentGraphLearn/ENIGMA_data/masterG.edgelist_i
ntindex.emb -l:100 -r:100 -k:10 -e:10 -d:128 -p:1 -q:1

date
 



