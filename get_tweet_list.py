"""
get top 1000 tweet list per day
"""

import os
import json
from string import Template
import sys
import re
import argparse
import subprocess


index_para_template = Template("""
<parameters>
       <index>$index</index>
       <memory>2G</memory>
       <corpus>
         <path>$file_path</path>
         <class>trectext</class>
       </corpus>
       <stemmer><name>porter</name></stemmer>
</parameters>
""")

query_para_template = Template("""
<parameters>
    <index>$index</index>
    <count>1000</count>
    <trecFormat>true</trecFormat>
    <runID>test</runID>
    <method>f2exp</method>
    <query>
    <number>1</number>
    <text>
    #combine($query)
    </text>
    </query>
 </parameters>
""")


def create_index_para_file(days,index_dir,data_dir,buildIndex):
    for day in days:
        index_para_file = os.path.join(index_dir,"index_para_"+day)
        index = os.path.join(index_dir,day)
        file_path = os.path.join(data_dir,day)
        with open(index_para_file,"w") as f:
            f.write(index_para_template.substitute(index=index,file_path=file_path))
        p = subprocess.Popen([buildIndex,index_para_file],stdout=subprocess.PIPE)
        print p.communicate()[0]

def create_query_para_file(days,index_dir,result_dir,query,runQuery):
    for day in days:
        query_para_file = os.path.join(result_dir,"query_para_"+day)
        index = os.path.join(index_dir,day)
        output = os.path.join(result_dir,day)
        with open(query_para_file,"w") as f:
            f.write(query_para_template.substitute(index=index,query=query))
        p = subprocess.Popen([runQuery,query_para_file],stdout=subprocess.PIPE)
        with open(output,"w") as f:
            f.write(p.communicate()[0])

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_dir")
    parser.add_argument("index_dir")
    parser.add_argument("result_dir")
    parser.add_argument("--buildIndex","-b",default="/home/1546/peilin_ex/IndriBuildIndex_EX")
    parser.add_argument("--runQuery","-r",default="/home/1546/peilin_ex/IndriRunQuery_EX")
    args=parser.parse_args()
    query = re.sub("_"," ",os.path.basename(args.result_dir))
    days = os.walk(args.data_dir).next()[2]
    create_index_para_file(days,args.index_dir,args.data_dir,args.buildIndex)
    create_query_para_file(days,args.index_dir,args.result_dir,query,args.runQuery)



if __name__=="__main__":
    main()

