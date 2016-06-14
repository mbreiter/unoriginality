from pprint import pprint

import math
import datetime
import time
#import praw
import os

score = {"score": 0, "created": 0, "created_utc": 0, "num_comments": 0, "over_18": 0}

def norm(post):
    sum_of_squares = 0

    for elements in post:
        sum_of_squares += math.pow(post[elements], 2)

    return math.sqrt(sum_of_squares)

def build_semantic_descriptors(sentences):
    semantic_descriptors = {}
    word_count = 0;

    for sentence in sentences:
        sorted_sentence = list(set(sentence))
        for word in sorted_sentence:
            if not word in semantic_descriptors:
                semantic_descriptors[word] = {}
            for iterate in sorted_sentence:
                if not iterate == word:
                    if not iterate in semantic_descriptors[word]:
                        semantic_descriptors[word][iterate] = 1
                    else:
                        semantic_descriptors[word][iterate] += 1

    return semantic_descriptors

def prepare_semantic_descriptors(submissions):
    build_sentences = []

    for posts in submissions:
        file = open("RedditTitles.txt")
        text = file.read()

        text = text.replace("!", ".")
                   .replace("?", ".")  \
                   .replace(",", " ")  \
                   .replace("-", " ")  \
                   .replace("'", " ")  \
                   .replace('"', " ")  \
                   .replace(":", " ")  \
                   .replace(";", " ")  \
                   .replace("/", " ")  \
                   .replace("\n", " ") \
                   .lower()

        sentences = text.split(".")

    for sentence in sentences:
        words = sentence.split()
        build_sentences.append(words)

    return build_semantic_descriptors(build_sentences)

def parse_post(id, author, name, permalink, title, url, score):
    print(id)

if __name__ == "__main__":
    os.chdir("/Users/mreiter/Documents")


    # r = praw.Reddit("unorginaility test")
    # submissions = r.get_subreddit("all").get_hot(limit=1000)

    # for s in submissions:
    #     score = {"score": s.score, "num_comments": s.num_comments}
    #
    #     print(s.title.encode("ascii","ignore"))
