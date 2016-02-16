"""
delete retweets in json files
"""

import os
import json
import sys
import re
import argparse






def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir")
    parser.add_argument("dest_dir")
    args=parser.parse_args()

    for json_file in os.walk(args.source_dir).next()[2]:
        content = []
        dest_file = os.path.join(args.dest_dir,json_file)
        data = json.load(open(os.path.join(args.source_dir,json_file)))
        for tweet in data:
            if not isinstance(tweet,dict):
                if tweet is None:
                    continue
                tweet =json.loads(tweet)
            if "text" not in tweet:
                continue
            text=tweet["text"]
            m = re.search("^RT",text)
            if m is not None:
                continue
            else:
                content.append(tweet)
        with open(dest_file,"w") as f:
            j_str = json.dumps(content)
            f.write(j_str)



if __name__=="__main__":
    main()

