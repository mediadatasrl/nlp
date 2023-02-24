from flask import Flask, request, jsonify, make_response
from spacy import displacy
from spacy.lang.it import Italian

import it_core_news_lg


app = Flask(__name__)
nlp = it_core_news_lg.load()



@app.route('/')
def hello():
	return "Hello New World!"


@app.route('/test')
def test():
    text = ("Dal 21 febbraio al 27 febbraio 2023 torna Milano Moda Donna, la settimana di sfilate dedicata alle collezioni autunno/inverno 2023-2024. Il calendario annunciato dal Presidente della Camera Moda Carlo Capasa è ricco: prevede 165 appuntamenti: 59  sfilate e 70 presentazioni (il programma completo sulla piattaforma di Camera Moda). Le aspettative sono alte per i 'big', molto attesi i debutti dei brand emergenti.  Nel 2022, l’industria italiana della moda ha resistito alle pressioni negative della congiuntura. Dopo la brillante crescita di inizio anno (fatturato +20% nel primo semestre), i dati del quarto trimestre confermano una dinamica elevata, smentendo le attese di una frenata netta per la crisi energetica e portando il fatturato del 2022 oltre +18%. La dinamica del fatturato è alimentata anche dalla crescita di costi e prezzi di vendita. I prezzi industriali nella filiera moda sono aumentati del 7,1%%, l’inflazione al consumo (+1,5%) è stata però inferiore a quella media (+8,7%) (dati Fashion Economics Trend).  C'è grande attesa per alcuni ritorni: Ferragamo è in calendario dopo il debutto di settembre sotto la direzione creativa del britannico Maximilian Davis, designer classe 1995, già molto apprezzato da star come Rihanna e Dua Lipa. Troviamo anche Glenn Martens che disegna Diesel. Confermato Prada con Miuccia e Raf Simons, e Gucci che tuttavia è senza direttore creativo per questa collezione; il nuovo direttore creativo Santo De Sarno lavorerà alle prossime collezioni del brand. Ancora: GCDS, Marco Rambaldi, ACT n°1. Tra i debutti in calendario c'è quello, molto atteso, del designer Tomo Koizumi supportato da Dolce & Gabbana, in linea con l'iniziativa che l'anno scorso ha visto la partecipazione di Matty Bovan.  In digitale, invece, presenteranno le loro collezioni Münn, AVAVAV, Husky e Laura Biagiotti.")
    doc = nlp(text)
    ret = ""
    for ent in doc.ents:
        ret += ent.label_
        ret += " | "
        ret += ent.text

    return ret


@app.route('/ner', methods=['POST'])
def extract_ner():
    text = request.form.get('q')
    doc = nlp(text)
    ret = []
    for ent in doc.ents:
        ret.append({ent.text: ent.label_})


    return make_response(jsonify(ret), 200)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8100)


