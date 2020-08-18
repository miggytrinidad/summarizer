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

# def bert_summarize(user_input, num_sentences_out = 10):
#     model = Summarizer()

#     if checkers.is_url('not a valid url'):
#         user_input = fulltext(requests.get(user_input).text)
    
#     result = model(user_input, num_sentences = num_sentences_out - 1)
#     summary = "".join(result)

#     return summary

def lsa_summary(user_input, num_sentences_out = 10):
    # Latent Semantic Analysis is an unsupervised method of summarization.
    # It combines term frequency techniques with singular value decomposition to summarize texts.

    if checkers.is_url(user_input):
        user_input = fulltext(requests.get(user_input).text)

    full_lsa = ""
    parser = PlaintextParser(user_input, Tokenizer("english"))

    model_lsa = LsaSummarizer()
    result_lsa = model_lsa(parser.document, num_sentences_out)
    for i in result_lsa:
        full_lsa = full_lsa + str(i)

    return full_lsa

def luhn_summary(user_input, num_sentences_out = 10):
    if checkers.is_url(user_input):
        user_input = fulltext(requests.get(user_input).text)

    summary_luhn = ""
    parser = PlaintextParser(user_input, Tokenizer("english"))

    model_luhn = LuhnSummarizer()
    result_luhn = model_luhn(parser.document, num_sentences_out)
    for i in result_luhn:
        summary_luhn = summary_luhn + str(i) + " "
        
    return summary_luhn

def lex_summary(user_input, num_sentences_out = 10):
    if checkers.is_url(user_input):
        user_input = fulltext(requests.get(user_input).text)

    summary_lex = ""
    parser = PlaintextParser(user_input, Tokenizer("english"))

    model_lex = LexRankSummarizer()
    result_lex = model_lex(parser.document, num_sentences_out)
    for i in result_lex:
        summary_lex = summary_lex + str(i) + " "
    return summary_lex
