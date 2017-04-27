"""
Dependencies: NLTK, NetworkX- https://networkx.github.io/documentation/networkx-1.10/tutorial/tutorial.html

"""
from nltk import tokenize
import networkx as nx
import itertools
import os
import io

def levenshtein_dist(sentence_one, sentence_two):
    if len(sentence_one) > len(sentence_two):
        sentence_one, sentence_two = sentence_two, sentence_one
    distance = range(len(sentence_one) + 1)
    for index, character in enumerate(sentence_two):
        new_distance = [index + 1]
        for index1, character1 in enumerate(sentence_one):
            if character1 == character:
                new_distance.append(distance[index1])
            else:
                min_distance = min((distance[index1], distance[index1+1], new_distance[-1]))
                new_distance.append(1 + min_distance)
        distance = new_distance
    return distance[-1]

def model_graph(vertices):

    graph = nx.Graph()
    graph.add_nodes_from(vertices)
    combinations = itertools.combinations(vertices, 2)
    vertex_pairs = list(combinations)

    for pair in vertex_pairs:
        sentence_one = pair[0]
        sentence_two = pair[1]
        similarity = levenshtein_dist(sentence_one, sentence_two)
        graph.add_edge(sentence_one, sentence_two, weight=similarity)

    return graph

def get_summary(text):
    sentence_tokens = tokenize.sent_tokenize(text)
    graph = model_graph(sentence_tokens)

    page_ranks = nx.pagerank(graph, weight='weight')
    sorted_page_ranks = sorted(page_ranks, key=page_ranks.get, reverse=True)

    final_summary = ' '.join((' '.join(sorted_page_ranks).split())[0:101])
    return final_summary

def write_files(summary, text_file):
    print '\nGenerating summary to ' + 'summaries/' + text_file
    summary_file = io.open('summaries/' + text_file, 'w')
    summary_file.write(summary)
    summary_file.close()

    print '\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-'


documents = []
for text_files in os.listdir("documents"):
    if text_files.endswith(".txt"):
        documents.append(text_files)
for text_file in documents:
    print '\nSummarizing text from documents/' + text_file
    doc_file = io.open('documents/' + text_file, 'r')
    text = doc_file.read()
    summary = get_summary(text)
    print '\nSummary for document: '+ text_file + "\n" + summary
    write_files(summary, text_file)
