from flask import Flask, request, jsonify, make_response, json
#from spacy import displacy
from spacy.lang.it import Italian
from spacy.lang.es import Spanish
from spacy.lang.ca import Catalan

import it_core_news_lg
import es_core_news_lg
import ca_core_news_lg
import spacy_fastlang


app = Flask(__name__)
nlp_it = it_core_news_lg.load()
nlp_es = es_core_news_lg.load()
nlp_ca = ca_core_news_lg.load()
nlp_es.add_pipe("language_detector")



@app.route('/')
def hello():
	return "Hello New World!"

def extract_ner_it(text):
    return nlp_it(text)

def extract_ner_es(text):
    return nlp_es(text)

def extract_ner_ca(text):
    return nlp_ca(text)

@app.route('/ner', methods=['POST'])
def extract_ner():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return make_response(jsonify([ "Content-Type not supported" ]), 403)

    json = request.json
    #return make_response(json, 403)
    #text = request.form.get('q')
    text = json['body']
    doc = extract_ner_es(text)
   
    if doc._.language == 'it':
        doc = extract_ner_it(text)
    elif doc._.language == 'ca':
        doc = extract_ner_ca(text)
    elif doc._.language == 'es':
        doc = doc
    else:
        return make_response(jsonify([ "error" , "Unsopported language" ]), 403)


    ret = []
    for ent in doc.ents:
        ret.append({"text": ent.text, "type": ent.label_})


    return make_response(jsonify(ret), 200)
    ret = ""
    for ent in doc.ents:
        ret += ent.label_
        ret += " | "
        ret += ent.text

    return ret


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8100)


