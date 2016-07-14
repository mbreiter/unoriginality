from django.shortcuts import render
from django.http import HttpResponse
from collections import OrderedDict

from datetime import datetime, timedelta
import praw
import math

def search(request):
    r = praw.Reddit("unorginaility development -- candidates -- v1.10")
    subreddit = request.GET["subreddit"]

    reference(request)

    try:
        reposts = r.get_subreddit(subreddit, fetch = True).get_rising(limit=1000)
    except:
        return HttpResponse("bruh")

    repost_candidates = {}

    for submission in reposts:
        reposts = submission.title.encode("ascii", "ignore") + "|"
        repost_descriptor = prepare_semantic_descriptors(reposts)

        score = similarity_score(repost_descriptor, request.session["reference"])
        repost_candidates[submission] = score

    repost_candidates = OrderedDict(sorted(repost_candidates.items(), reverse=True))

    serve = {"repost_candidates" : repost_candidates, "subreddit": subreddit}

    return render(request, "unoriginality/search.html", serve)

def index(request):
    reference(request)
    return render(request, "unoriginality/header.html")

def reference(request):
    r = praw.Reddit("unorginaility development -- refernce -- v1.10")

    try:
        top_submissions = r.get_subreddit(request.GET["curate"], fetch = True)
    except:
        top_submissions = r.get_subreddit("all")

    if request.GET.get("category", None) == "top":
        top_submissions = top_submissions.get_top_from_year(limit = 100)
    elif request.GET.get("category", None) == "controversial":
        top_submissions = top_submissions.get_controversial_form_year(limit = 100)
    elif request.GET.get("category", None) == "new":
        top_submissions = top_submissions.get_new(limit = 100)
    elif request.GET.get("category", None) == "hot":
        top_submissions = top_submissions.get_hot(limit = 100)
    else:
        top_submissions = top_submissions.get_rising(limit = 100)

    reference_titles = ""

    for submission in top_submissions:
        reference_titles += submission.title.encode("ascii", "ignore") + "|"

    reference = prepare_semantic_descriptors(reference_titles)
    request.session["reference"] = reference

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
               .replace(""", " ")  \
               .replace(""", " ")  \
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
