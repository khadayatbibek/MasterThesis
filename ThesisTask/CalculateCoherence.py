#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 09:50:53 2021

@author: Bibek77
"""

from bs4 import BeautifulSoup
from tqdm import tqdm
import argparse
import atexit
import glob
import html2text
import json
import os
import pathlib
import socket
import subprocess
import sys

from coherence_probability import CoherenceProbability
from normalization1 import cleanText1

def port_is_open(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0
#automate corenlp server
def start_corenlp_server(pidfile='/tmp/corenlp.pid'):
    if port_is_open('127.0.0.1', 9000):
        # do nothing: corenlp server is already listening
        return
    if os.path.isfile(pidfile):
        pid = int(open(pidfile).read())
        try:
            os.kill(pid, 0)
        except OSError:
            pass
        else:
            # do nothing: corenlp server is already starting / running
            return
    corenlp_dir = pathlib.Path(__file__).parent / 'stanford-corenlp-4.2.1'
    corenlp_jars = [
        str(corenlp_dir / jf) for jf in
        ['stanford-corenlp-4.2.1.jar', 'stanford-corenlp-4.2.1-models.jar']]
    corenlp_cmdline = ["java", "-mx8g", "-cp", ":".join(corenlp_jars),
                       "edu.stanford.nlp.pipeline.StanfordCoreNLPServer",
                       "-quiet", "true",
                       "-port", "9000"]
    corenlp = subprocess.Popen(corenlp_cmdline, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    with open(pidfile, 'w') as f:
        f.write(f'{corenlp.pid}')
        f.close()
    def finalize():
        corenlp.terminate()
        os.unlink(pidfile)
    atexit.register(finalize)
    while b"listening at" not in corenlp.stderr.readline():
        # wait for server to start up
        pass


def get_html_path(topic_numbers, topics_path):
    essays_files=[]
    for n in topic_numbers:
        essays_files.append(list(sorted(
            (topics_path / f'topic{n:03}').glob('*.html'))))
    return essays_files

def read_html(filename):
    with open(filename, 'rb') as f:
        html = f.read().decode('utf8', errors='ignore')

    # Get html string
    soup = BeautifulSoup(html, "lxml")
    
    for item in soup.find_all('img'):
        item.decompose()
    for item in soup.find_all('a'):
        item.decompose()
        
    htmltext = soup.encode('utf-8').decode('utf-8','ignore')
    
    text=html2text.html2text(htmltext)
    return text
        
def preprossing_text(txt):
    res_str = txt.replace('\n', ' \n')
    par = res_str.split('\n ')
    paragraphs = [x.replace('\n', '') for x in par ]
    filtered_paragraphs = [x for x in paragraphs if len(x.strip()) > 0]   
    corpus = cleanText1(filtered_paragraphs)   
    text_corpus_list =[' '.join(text) for text in corpus]
    text_corpus_list =list(filter(None, text_corpus_list))
        
    return text_corpus_list

def calculate_coherence(revisions):
    coh_score=[]        
    for j in range(len(revisions)):
        
        inputtext=revisions[j]

        coh=CoherenceProbability(inputtext)
        coh_prob=coh.coherence_prob
        coh_score.append(coh_prob)          

    return coh_score


def main(args):
    essays_files = get_html_path(args.topic_numbers, args.corpus_directory)
    for revisions_files in tqdm(essays_files, leave=True, desc='Essays'):
        topic_num = int(pathlib.Path(revisions_files[0]).parent.name[len('topic'):])
        for revision_file in tqdm(revisions_files, desc=f'Topic {topic_num}'):
            revision_num = int(pathlib.Path(revision_file).name.split('.')[0][len('rev-'):])
            revision = read_html(revision_file)
            revision = preprossing_text(revision)
            coh_score = calculate_coherence(revision)
            print(json.dumps(dict(topic=topic_num, rev=revision_num, coherence=coh_score)))
            sys.stdout.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate coherence scores for TRC-12 essays")
    parser.add_argument('topic_numbers', nargs='+', type=int, help="Topic numbers to process")
    parser.add_argument('-d', '--corpus-directory',
                        help="Path to the webis-trc-12 dataset's essays/revisions directory",
                        type=pathlib.Path,
                        default='D:/WEBIS_CORPUS/corpus-webis-trc-12/essays/revisions')

    args = parser.parse_args()
 
    start_corenlp_server()
    main(args)
