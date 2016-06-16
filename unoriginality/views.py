from django.shortcuts import render
from django.http import HttpResponse
import praw
import math

def search(request):
    #sorted(d, key=d.get, reverse=True):
    message = request.GET['subreddit']
    return HttpResponse(message)


def index(request):
    global r, top_submissions

    r = praw.Reddit("unorginaility development -- v1.00")
    top_submissions = r.get_subreddit("all").get_hot(limit=100)

    repost_candidates = r.get_subreddit("funny").get_rising(limit=100)

    reference_titles = ""
    repost_titles = ""

    for submission in top_submissions:
        reference_titles += submission.title.encode("ascii", "ignore") + "|"

    reference = prepare_semantic_descriptors(reference_titles)
    #
    # for submission in repost_candidates:
    #     repost_title = submission.title.encode("ascii", "ignore") + "|"
    #     candidate = prepare_semantic_descriptors(repost_title)
    #
    #     score = similarity_score(candidate, reference)
    #
    return render(request, 'unoriginality/home.html')

    #return HttpResponse(reference_titles)

def norm(post):
    sum_of_squares = 0

    for elements in post:
        sum_of_squares += math.pow(post[elements], 2)

    return math.sqrt(sum_of_squares)

def cosine_similarity(post, reference):
    dot_product = 0

    for keys in post.keys():
        if keys in reference:
            dot_product += post[keys] * reference[keys]

    if (norm(post) * norm(reference)) == 0:
        return 0
    else:
        return dot_product / (norm(post) * norm(reference))

def similarity_score(post, reference):
    similarity_score = {}

    for keys in post.keys():
        if keys in reference:
            similarity_score[keys] = cosine_similarity(post[keys], reference[keys]);

    return norm(similarity_score)

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

    text = text.replace("!", " ")  \
               .replace("?", " ")  \
               .replace(".", " ")  \
               .replace("(", " ")  \
               .replace(")", " ")  \
               .replace("[", " ")  \
               .replace("]", " ")  \
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
