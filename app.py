from flask import Flask, render_template, request
import json
import summarizers
import evaluate

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
    default_state = {"check_mode": True}
    return render_template("summary.html", default_state = default_state)

@app.route('/summary_results', methods=['POST'])
def summarized():
    if request.method == 'POST':
        user_input = request.form['user_input']
        summary_length = int(request.form['summary_length'])

        if request.form.get('checkmode'):
            check_mode = request.form['checkmode']
            ref_summary = request.form['ref_summary']
        else:
            check_mode = False
            ref_summary = ""

        #LSA_Summary
        lsa_summary = summarizers.lsa_summary(user_input, ref_summary, check_mode, num_sentences_out = summary_length)
        
        #luhn_summary
        luhn_summary = summarizers.luhn_summary(user_input, ref_summary, check_mode, num_sentences_out = summary_length)

        #LEX_Summary
        lex_summary = summarizers.lex_summary(user_input, ref_summary, check_mode, num_sentences_out = summary_length)

        #RESULTS
        sum_result =  {"user_input": user_input,
                        "summary_length": summary_length,
                        "check_mode": check_mode,
                        "ref_summary": ref_summary,
                        "summaries": {  
                            "Latent Semantic Analysis": lsa_summary, 
                            "Luhn": luhn_summary, 
                            "Lex Rank": lex_summary
                        }
                        }

        if request.form.get('checkmode'):
            #get best summary
            best_summary = evaluate.get_best_summary(sum_result)
            sum_result["best_summary"] = best_summary

            #Arrange summaries
            sum_result["summaries"] = evaluate.order_summary(best_summary, sum_result)

        

        return render_template("summary_results.html", results = sum_result)
    else:
        return render_template("summary.html")

if __name__ == "__main__":
    app.run(debug = True)