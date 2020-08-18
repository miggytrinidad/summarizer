from flask import Flask, render_template, request
from flask_material import Material
import json
import summarizers

app = Flask(__name__)
Material(app)

@app.route("/")
def index():
    return render_template("index.html")




@app.route('/summarize', methods=['POST'])
def summarize():
    if request.method == 'POST':
        user_input = request.form['user_input']

        
        #LSA_Summary
        lsa_summary = summarizers.lsa_summary(user_input, num_sentences_out = 10)

        #luhn_summary
        luhn_summary = summarizers.luhn_summary(user_input, num_sentences_out = 10)

        #LEX_Summary
        lex_summary = summarizers.lex_summary(user_input, num_sentences_out = 10)




        #RESULTS
        sum_result =  {"user_input": user_input, 
                        "summaries": {
                            "lsa_summary": lsa_summary, 
                            "luhn_summary": luhn_summary, 
                            "lex_summary": lex_summary
                            } 
                        }

        return render_template("index.html", results = sum_result)
       

    return render_template("index.html")

if __name__ == "__main__":
    
    app.run(debug = True)