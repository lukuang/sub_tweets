"""
get tweets from id lists
"""

import os
import json
import sys
import re
import argparse


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

def get_ids(list_dir,day):
    ids = []
    file_name = os.path.join(list_dir,day)
    with open(file_name) as f:
        for line in f:
            line = line.rstrip()
            parts = line.split()
            print "find id",parts[2]
            ids.append(parts[2])
    return ids


def get_tweets(tweet_files,ids):
    tweets = []
    for a_file in tweet_files:
        print "find in file",a_file
        data = json.load(open(a_file))
        for tweet in data:
            if not isinstance(tweet,dict):
                if tweet is None:
                    continue
                tweet = json.loads(tweet)
            if "id" not in tweet:
                continue
            #print type(tweet["id"])
            if str(tweet["id"]) in ids:
                tweets.append(tweet)
                print "found!", tweet["id"]
    return tweets

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("list_dir")
    parser.add_argument("source_dir")
    parser.add_argument("dest_dir")
    args=parser.parse_args()
    daily_files = get_daily_files(args.source_dir)
    for day in daily_files:
        if day!="2015-10-27":
            continue
        ids = get_ids(args.list_dir,day)
        print type(ids[0])
        print "for %s there are %d ids" %(day,len(ids))
        tweets = get_tweets(daily_files[day],ids)
        output = os.path.join(args.dest_dir,day)
        with open(output,"w") as f:
            j_str = json.dumps(tweets)
            f.write(j_str)

if __name__=="__main__":
    main()

