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

./node2vec -i:../../../../MicrobeEnvironmentGraphLearn/ENIGMA_data/masterG.edgelist_intindex.txt -o:../../../../MicrobeEnvironmentGraphLearn/ENIGMA_data/masterG.edgelist_intindex.emb -l:100 -r:100 -k:10 -e:10 -d:128 -p:1 -q:1

date
 
