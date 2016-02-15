"""
parse json file to xml
"""

import os
import json
import sys
import re
from string import Template
import argparse

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

doc_template = Template("""
<DOC>
<DOCNO>$docid</DOCNO>
<TEXT>
$text
</TEXT>
</DOC>
""")

def parse_tweet_json(day,json_files,no_dup):
    content = ""
    if no_dup:
        for f in json_files:
            print f
            data = json.load(open(f))
            for tweet in data:
                if not isinstance(tweet,dict):
                    if tweet is None:
                        continue
                    tweet =json.loads(tweet)
                if "text" not in tweet:
                    continue
                text=tweet["text"]
                text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
                content += doc_template.substitute(docid=tweet["id"],text=text)
    else:
        all_tweets = {}
        for f in json_files:
            print f
            data = json.load(open(f))
            for tweet in data:
                if not isinstance(tweet,dict):
                    if tweet is None:
                        continue
                    tweet =json.loads(tweet)

                if "text" not in tweet:
                    continue
                text=tweet["text"]
                text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
                if text not in all_tweets:
                    all_tweets[text] = 0
                    content += doc_template.substitute(docid=tweet["id"],text=text)


    return content


def write_to_xml(dest_file,content):
    with open(dest_file,"w") as f:
        f.write(content)

def get_daily_files(source_dir):
    daily_files = {}
    files = os.walk(source_dir).next()[2]
    for f in files:
        m = re.search("^(.+?)-\d+$",f)
        if m is None:
            print "file name error"
            print f
            sys.exit(-1)
        else:
            day = m.group(1)
            if day not in daily_files:
                daily_files[day] = []
            daily_files[day].append(os.path.join(source_dir,f))
    return daily_files

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir")
    parser.add_argument("--no_dup","--n",action="store_true")
    parser.add_argument("dest_dir")
    args=parser.parse_args()
    daily_files = get_daily_files(args.source_dir)
    #print daily_files
    #sys.exit(0)
    for day in daily_files:
        content = parse_tweet_json(day,daily_files[day],args.no_dup)
        dest_file = os.path.join(args.dest_dir, day)
        write_to_xml(dest_file,content)

if __name__=="__main__":
    main()

