from pprint import pprint
import math
import datetime
import time
import praw
import os

#score = {"score": 0, "created": 0, "created_utc": 0, "num_comments": 0, "over_18": 0}

def norm(post):
    sum_of_squares = 0

    for elements in post:
        sum_of_squares += math.pow(post[elements], 2)

    return math.sqrt(sum_of_squares)

def build_semantic_descriptors(posts):
    semantic_descriptors = {}
    word_count = 0;

    for post in posts:
        sorted_words = list(set(post))
        for word in sorted_words:
            if not word in semantic_descriptors:
                semantic_descriptors[word] = {}
            for iterate in sorted_words:
                if not iterate == word:
                    if not iterate in semantic_descriptors[word]:
                        semantic_descriptors[word][iterate] = 1
                    else:
                        semantic_descriptors[word][iterate] += 1

    return semantic_descriptors

def prepare_semantic_descriptors(text):
    build_posts = []

    text = text.replace("!", ".")  \
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

    posts = text.split("|")

    for post in posts:
        words = post.split()
        build_posts.append(words)

    return build_semantic_descriptors(build_posts)

def parse_post(id, author, name, permalink, title, url, score):
    print(id)

if __name__ == "__main__":
    r = praw.Reddit("unorginaility test")
    submissions = r.get_subreddit("all").get_hot(limit=1)
    report_candidates = r.get_subreddit("nsfw").get_hot(limit=1)

    titles = ""

    for submission in submissions:
        titles += submission.title.encode("ascii", "ignore") + "|"

    test = prepare_semantic_descriptors(titles)

    print(test)
