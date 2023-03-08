from flask import request, jsonify, make_response, json
from app import app
from functools import wraps

import it_core_news_lg
import es_core_news_lg
import ca_core_news_lg
import fr_core_news_lg
import en_core_web_lg
import spacy_fastlang


nlp_it = it_core_news_lg.load()
nlp_es = es_core_news_lg.load()
nlp_ca = ca_core_news_lg.load()
nlp_fr = fr_core_news_lg.load()
nlp_en = en_core_web_lg.load()
nlp_es.add_pipe("language_detector")



@app.route('/')
def hello():
    return "Hello New World!"


@app.route('/ping')
def ping():
    return make_response('pong', 200)


def analyze(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return "Unsopported Content-type", 403

        json = request.json
        doc = extract_ner_es(json['body'])
        request.doc = doc
        return f(*args, **kwargs)
    return wrap


def extract_ner_it(text):
    return nlp_it(text)

def extract_ner_es(text):
    return nlp_es(text)

def extract_ner_ca(text):
    return nlp_ca(text)

def extract_ner_fr(text):
    return nlp_fr(text)

def extract_ner_en(text):
    return nlp_en(text)

@app.route('/ner', methods=['POST'])
@analyze
def extract_ner():

    doc = request.doc

    if doc._.language == 'it':
        doc = extract_ner_it(request.json['body'])
    elif doc._.language == 'ca':
        doc = extract_ner_ca(request.json['body'])
    elif doc._.language == 'fr':
        doc = extract_ner_fr(request.json['body'])
    elif doc._.language == 'en':
        doc = extract_ner_en(request.json['body'])
    elif doc._.language == 'es':
        doc = doc
    else:
        return make_response(jsonify([ "error" , "Unsopported language" ]), 403)


    ret = []
    for ent in doc.ents:
        ret.append({"text": ent.text, "type": ent.label_})


    return make_response(jsonify(ret), 200)


@app.route('/lang', methods=['POST'])
@analyze
def extract_lang():
    return make_response(jsonify(request.doc._.language), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)

