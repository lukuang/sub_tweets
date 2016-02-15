"""
merge old tweets into tweets
"""

import os
import json
import sys
import re
import argparse
import shutil

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old_dir")
    parser.add_argument("tweets_dir")
    args=parser.parse_args()
    old_tweets = os.walk(args.old_dir).next()[2]
    tweets = os.walk(args.tweets_dir).next()[2]
    for old in old_tweets:
        if old not in tweets:
            src = os.path.join(args.old_dir,old)
            dest = os.path.join(args.tweets_dir,old)
            shutil.copyfile(src,dest)




if __name__=="__main__":
    main()

