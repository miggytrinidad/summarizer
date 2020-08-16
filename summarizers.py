from summarizer import Summarizer

text = "run"
model = Summarizer()
result = model(text)
full = "".join(result)
print(full)
