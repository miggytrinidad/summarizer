#bert_summarize
import requests
#from summarizer import Summarizer
from newspaper import fulltext
#lsa_summary
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
#luhn_summary
from sumy.summarizers.luhn import LuhnSummarizer
#lex_summary
from sumy.summarizers.lex_rank import LexRankSummarizer 

from validator_collection import validators, checkers

from rouge import Rouge 

#bert
import torch
import torchvision
from summarizer import Summarizer

def get_rouge_scores(generated_summary, ref_summary):
    rouge = Rouge()
    r_scores = rouge.get_scores(generated_summary, ref_summary)

    scores = {}
    for rouge, outputs in r_scores[0].items():
        temp_output = {}
        for output, value in outputs.items():
            temp_output[output] = round(value, 3)
        
        scores[rouge] = temp_output

    return scores

def lsa_summary(user_input, ref_summary, check_mode = False, num_sentences_out = 10):
    # Latent Semantic Analysis is an unsupervised method of summarization.
    # It combines term frequency techniques with singular value decomposition to summarize texts.

    rouge_score = 0
    if checkers.is_url(user_input):
        user_input = fulltext(requests.get(user_input).text)

    full_lsa = ""
    parser = PlaintextParser(user_input, Tokenizer("english"))

    model_lsa = LsaSummarizer()
    result_lsa = model_lsa(parser.document, num_sentences_out)
    for i in result_lsa:
        full_lsa = full_lsa + str(i)

    if check_mode:
        rouge_score = get_rouge_scores(full_lsa, ref_summary)
    
        

    return full_lsa, rouge_score

def luhn_summary(user_input, ref_summary, check_mode = False, num_sentences_out = 10):
    rouge_score = 0

    if checkers.is_url(user_input):
        user_input = fulltext(requests.get(user_input).text)

    summary_luhn = ""
    parser = PlaintextParser(user_input, Tokenizer("english"))

    model_luhn = LuhnSummarizer()
    result_luhn = model_luhn(parser.document, num_sentences_out)
    for i in result_luhn:
        summary_luhn = summary_luhn + str(i) + " "

    if check_mode:
        rouge_score = get_rouge_scores(summary_luhn, ref_summary)
        

    return summary_luhn, rouge_score


def lex_summary(user_input, ref_summary, check_mode = False, num_sentences_out = 10):
    rouge_score = 0
    if checkers.is_url(user_input):
        user_input = fulltext(requests.get(user_input).text)

    summary_lex = ""
    parser = PlaintextParser(user_input, Tokenizer("english"))

    model_lex = LexRankSummarizer()
    result_lex = model_lex(parser.document, num_sentences_out)
    for i in result_lex:
        summary_lex = summary_lex + str(i) + " "

    if check_mode:
        rouge_score = get_rouge_scores(summary_lex, ref_summary)
        
    return summary_lex, rouge_score

