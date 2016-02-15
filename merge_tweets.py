"""
merge old tweets into tweets
"""

import os
import json
import sys
import re
import argparse

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old_dir")
    parser.add_argument("tweets_dir")
    args=parser.parse_args()
    old_tweets = os.walk(args.old_dir).next()[2]
    tweets = os.walk(args.tweets_dir).next()[2]
    for old in old_tweets:
        if old not in tweets:
            print old
            



if __name__=="__main__":
    main()

