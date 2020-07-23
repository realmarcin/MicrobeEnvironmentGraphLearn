#!/bin/bash

echo "subject	object" > header.tsv
cut -f1,2 masterG.edgelist.tsv > masterG_edges_raw.tsv
cat header.tsv masterG_edges_raw.tsv > masterG_edges.tsv
sed -i '' 's/: /:/g' masterG_edges.tsv
sed -i '' 's/ /\~/g' masterG_edges.tsv
cut -f1 masterG_edges.tsv > masterG_edges_col1.tsv
cut -f2 masterG_edges.tsv > masterG_edges_col2.tsv
cat masterG_edges_col1.tsv masterG_edges_col2.tsv > masterG_nodes_all.tsv
uniq masterG_nodes_all.tsv | sort > masterG_nodes.tsv

curl https://genomics.lbl.gov/~marcin/MAK/MAK.jar > MAK.jar
tail -n+2 masterG_edges.tsv > masterG_edges_nohead.tsv
java -classpath MAK.jar DataMining.util.EdgestoInts masterG_edges_nohead.tsv

#mkdir -p me_data
#cp masterG_nodes.tsv masterG_edges.tsv masterG.edgelist.tsv me_data/
#tar -zcf me_data.tgz me_data


