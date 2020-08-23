def get_best_summary(rouge_measures):
  score_board = {"Lex Rank": 0,
                  "Luhn": 0,
                  "Latent Semantic Analysis": 0}

  for rouge in ["rouge-1", "rouge-2", "rouge-l"]:
    temp = {}
    #print("*", rouge)
    for k, v in rouge_measures["summaries"].items():
      temp[k] = v[1][rouge]["r"]
      # print(k, v[1][rouge]["r"])
    
    #sort descending order
    temp = {k: v for k, v in sorted(temp.items(), key=lambda item: item[1], reverse=True)} 
    #print("&&", temp)

    for k, v in temp.items():
      score_board[k] +=  1
      break
    #print("SB", score_board)

  print(score_board)
  best_summary = max(score_board, key=score_board.get)

  return best_summary

def order_summary(best_summary, summaries):
  ordered = {}
  for k, v in summaries["summaries"].items():
    if k == best_summary:
      ordered[k] = summaries["summaries"][k]

  for k, v in summaries["summaries"].items():
    if k != best_summary:
      ordered[k] = summaries["summaries"][k]

  return ordered