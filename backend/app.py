from flask import Flask,request,jsonify
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import pandas as pd
from collections import Counter
from heapq import nlargest
from flask_cors import CORS
from transformers import pipeline
import sqlite3
DATABASE = "database.db"


summarizer=pipeline('summarization',model='t5-base',tokenizer='t5-base',framework='pt')
nlp = spacy.load('en_core_web_sm')
app=Flask(__name__)
CORS(app)


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS records(
        id INTEGER PRIMARY KEY AUTOINCREMENT,res TEXT NOT NULL) ''')
        conn.commit()

init_db()

def remove_last(str):
    l = len(str)

    cnt = 0
    while l >= 0 and str[l - 1] == '\n':
        cnt += 1
        l -= 1

    str = str[:-cnt]
    return str



def text_summary(txt):
    len(txt)
    doc = nlp(txt)
    tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct and token.text != '\n']
    print("\n\n")
    print(tokens)
    token1 = []
    stopwords = list(STOP_WORDS)
    allowed_pos = ['ADJ', 'PROPN', 'VERB', 'NOUN']

    for token in doc:
        if token.text in stopwords or token.text in punctuation:
            continue
        if token.pos_ in allowed_pos:
            token1.append(token.text)

    word_freq = Counter(tokens)
    max_freq = max(word_freq.values())

    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    sent_token = [sent.text for sent in doc.sents]

    l=len(sent_token)
    sent_score = {}
    for sent in sent_token:

        for word in sent.split():
            if word.lower() in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = word_freq[word]
                else:
                    sent_score[sent] += word_freq[word]

    df = pd.DataFrame(list(sent_score.items()), columns=['Sentence', 'Score'])


    num_sentences = 2
    if l>15:
        num_sentences=6
    elif l>=10:
        num_sentences=4
    elif l>=6:
        num_sentences=3

    nsent = nlargest(num_sentences, sent_score, key=sent_score.get)


    arr=[]
    for sent in sent_token:
        if sent in nsent:
            arr.append(sent)

    res=" ".join(arr)

    return res


def summary_transform(txt):
    summary = summarizer(txt, max_length=150, min_length=50, do_sample=False)
    res=summary[0]['summary_text']
    return res


@app.route('/response')
def responses():
    with sqlite3.connect(DATABASE) as conn:
        cursor=conn.cursor()
        cursor.execute('select * from records')
        recs=cursor.fetchall()

    return {
        "records":recs
    }

def add_record(txt):
    with sqlite3.connect(DATABASE) as conn:
        cursor=conn.cursor()
        cursor.execute("insert into records (res) values (?)",(txt,))
        conn.commit()


@app.route('/summary',methods=['GET','POST'])
def summary():
    data=request.get_json()
    article=data.get('article')

    if article is None:
        return {
            "response": "please provide an article"
        }, 404
    elif  article=="":
        return {
            "response":"please provide an article"
        },404

    res=text_summary(article)
    # print(f"response is {res}")
    add_record(res)

    return {
        "response":res
    },200


@app.route('/')
def main():
    return "<h1>Use /summary to get the summary of article</h1>"

if __name__=='__main__':
    app.run(debug=True)