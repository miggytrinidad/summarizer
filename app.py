from flask import Flask, render_template, request
import json
import summarizers

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/summary')
def summary():
    return render_template("summarize.html")

@app.route('/summarize', methods=['POST'])
def summarized():
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
                        "rouge": False,
                        "summaries": {
                            "BertSum": "Bert Sum",
                            "Latent Semantic Analysis": lsa_summary, 
                            "Luhn": luhn_summary, 
                            "Lex Rank": lex_summary
                            } 
                        }

        return render_template("summarize.html", results = sum_result)
    else:
        return render_template("summarize.html")

if __name__ == "__main__":
    
    app.run(debug = True)