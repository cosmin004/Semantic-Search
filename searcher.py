from sentence_transformers import SentenceTransformer, util, CrossEncoder
import numpy as np
import torch
import streamlit as st
import pandas as pd
import os
import json

class Searcher():
    @staticmethod
    @st.cache
    def load_models():

        Searcher.search_model = SentenceTransformer('msmarco-bert-base-dot-v5')

        Searcher.re_ranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-12-v2")
        
        with open('assets/corpuses.json') as fp:
            Searcher.corpuses = json.load(fp)

        with open('assets/print_corpuses.json') as fp:
            Searcher.print_corpuses = json.load(fp)
    
    @staticmethod
    def search(query):
        query_embedding = Searcher.search_model.encode(query, convert_to_tensor=True)
        results = []
        my_bar = st.progress(0)
        total_corpuses = len(Searcher.corpuses.keys())

        step_size = 1.0 / total_corpuses
        current_step = 0.0
        for c in Searcher.corpuses:
            corpus_embeddings = torch.load('assets/msmarco-bert-base-dot-v5_corpus_embeddings_{}_v1.pt'.format(c))
            scores = util.semantic_search(
                query_embedding,
                corpus_embeddings,
                score_function=util.dot_score,
                top_k=5
            )
            results.append({
                'language': c
            })

            for k in range(len(scores[0])):
                relevance = Searcher.re_ranker.predict([[query, Searcher.corpuses[c][scores[0][k]['corpus_id']]]])

                results[-1]['relevance_{}'.format(k+1)] = relevance[0]
                results[-1]['match_score_{}'.format(k+1)] = scores[0][k]['score']
                results[-1]['original_content_{}'.format(k+1)] = Searcher.print_corpuses[c][scores[0][k]['corpus_id']]
                if c in ['sv', 'fr', 'de']:
                    results[-1]['translated_content_{}'.format(k+1)] = Searcher.corpuses[c][scores[0][k]['corpus_id']]
            my_bar.progress(current_step + step_size)
            current_step += step_size
        return results