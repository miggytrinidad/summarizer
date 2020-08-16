from flask import Flask, render_template, request
from flask_material import Material
import json
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

app = Flask(__name__)
Material(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/summarize', methods=['POST'])
def summarize():
    if request.method == 'POST':
        user_input = request.form['user_input']
        # Latent Semantic Analysis is an unsupervised method of summarization.
        # It combines term frequency techniques with singular value decomposition to summarize texts.
        
        full_lsa = ""
        sentence_cnt = 5
        parser = PlaintextParser(user_input, Tokenizer("english"))

        model_lsa = LsaSummarizer()
        result_lsa = model_lsa(parser.document, sentence_cnt)
        for i in result_lsa:
            full_lsa = full_lsa + str(i)
        #print(full_lsa)

        sum_result =  {'user_input': user_input, "summary": full_lsa}

        return render_template("index.html", results = sum_result)
       

    return render_template("index.html")

if __name__ == "__main__":
    
    app.run(debug = True)