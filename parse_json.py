"""
parse json file to xml
"""

import os
import json
import sys
import re
from string import Template
import argparse

doc_template = Template("""
<DOC>
<DOCNO>$docid</DOCNO>
<TEXT>
$text
</TEXT>
</DOC>
""")

def parse_tweet_json(json_file):
    content = ""
    data = json.load(open(json_file))
    for tweet in data:
        content += doc_template.substitute(docid=tweet["id"],text=tweet["text"])
    return content


def write_to_xml(dest_file,content):
    with open(dest_dir,"w") as f:
        f.write(content)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file")
    parser.add_argument("dest_dir")
    args=parser.parse_args()
    content = parse_tweet_json(args.json_file)
    dest_file = os.path.join(dest_dir, os.path.basename(args.json_file))
    write_to_xml(dest_file,content)

if __name__=="__main__":
    main()

