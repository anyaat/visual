import os
import time
import hashlib
import seaborn as sns 
import networkx as nx
import matplotlib.pyplot as plt
from celery import Celery
from random import choice
from bigrams import word_bigram
from itertools import combinations
from gensim.models import Word2Vec
from forms import ChooseModel
from dm_graphs import graph_reduce, MST_pathfinder
from flask import Flask, render_template, redirect, url_for, request, jsonify, make_response, flash
from flask.views import MethodView


DEFAULT_PORT = 5000
ADDITIVE_FOR_UID = 1000


try:
    from os import getuid
except ImportError:
    def getuid():
        return DEFAULT_PORT - ADDITIVE_FOR_UID


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'mongodb://localhost/celery'
app.config['CELERY_RESULT_BACKEND'] = 'amqp://guest:guest@localhost:5672//'
app.config['SECRET_KEY'] = 'my_secret_key'


celery = Celery(app.name, 
         broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


root = '/home/anya/python/web/app/'
model_rus = Word2Vec.load_word2vec_format('ruscorpora.bin', binary=True)
model_eng = Word2Vec.load_word2vec_format('bnc.bin', binary=True)
lemmatize = True
tag_list = 'S A V ADV'.split()
#tags_list = 'ADJ VERB SUBST UNC ADV'
   

def process_query(userQuery, model_name):
    query = userQuery.strip()
    if '_' in query:
        query_split = query.split('_')
        if query_split[-1] in tag_list:
            query = ''.join(query_split[:-1]).lower() + '_' + query_split[-1]
        else:
            return "Incorrect part of speech tag!"
    elif model_name == 'ruscorpora':
        return "Please, type a word and its POS tag. We can't perform lemmatization and part of speech tagging on hosting!"
        # if lemmatize:
        #     query = tagword(query)
        # else:
        #     return "Incorrect part of speech tag!"
    return query


def plot(query, model, associates, model_name):
    plotFile = "%s.png" % (query)
    if not plotFile in os.listdir(root + 'static/plots/'):
        associates = set([pair[1] for pair in associates])
        edges = ((a.split('_')[0], b.split('_')[0], model.similarity(a,b)) for a, b in combinations(associates, 2))
        G = nx.Graph()
        G.add_weighted_edges_from(edges)
        NG = graph_reduce(G)
        MST = MST_pathfinder(NG)
        posi = nx.spring_layout(MST)
        nx.draw_networkx_nodes(MST, posi, node_size=100, node_color='#3498db', alpha=0.3)
        nx.draw_networkx_edges(MST, posi, width=2, alpha=0.4, edge_color='#3498db')
        nx.draw_networkx_labels(MST, posi, font_size=12, font_color='#34495e', font_family='sans-serif', weight='bold')
        if model_name == 'ruscorpora':
            plt.title(query.split('_')[0] + ' (' + query.split('_')[1] + ')', fontsize=16, fontweight='bold')
        else:
            plt.title(query, fontsize=16, fontweight='bold')
        # mm = hashlib.md5()
        # name = '_'.join([m, query]).encode('utf-8')
        # mm.update(name)
        plt.savefig(root + 'static/plots/' + query + '.png', dpi=150, bbox_inches='tight')
        plt.clf()
    imagePath = 'plots/' + plotFile
    return imagePath


@app.route('/russian/', methods=['GET', 'POST'])
def russian():
    if request.method == 'POST':
        try:
            input_data = request.form['query']
        except:
            return render_template('russian.html', error="Something wrong with your query!")
        if input_data.replace('_', '').replace('-', '').isalnum():
            model_name = 'ruscorpora'
            query = process_query(input_data, model_name)
            if query == 'Incorrect tag!' or query.startswith('Please, type'):
                error = query
                return render_template('russian.html', error=error)
            try:
                associates = set([(round(pair[1], 4), pair[0]) for pair in model_rus.most_similar(positive=query, topn=20)][:10])
            except KeyError:
                return render_template('russian.html', error=\
                    "Sorry, your word is not in the models vocabulary. Please, check the spelling")
            associates = sorted(associates, reverse=True)
            imagePath = plot(query, model_rus, associates, model_name)

            return render_template('russian.html', result=associates, word=query.split('_')[0], pos=query.split('_')[-1], model=model_name, imagePath=imagePath)
    return render_template('russian.html')


@app.route('/russian/word/<word>/', methods=['GET', 'POST'])
def russian_word(word):
    if word.replace('_', '').replace('-', '').isalnum():
        model_name = 'ruscorpora'
        query = process_query(word, model_name)
        if query == 'Incorrect tag!' or query.startswith('Please, type'):
            error = query
            return render_template('russian.html', error=error)       
        try:
            associates = set([(round(pair[1], 4), pair[0]) for pair in model_rus.most_similar(positive=query, topn=20)][:10])
        except KeyError:
            return render_template('russian.html', error=\
                "Sorry, your word is not in the models vocabulary. Please, check the spelling")
        associates = sorted(associates, reverse=True)
        imagePath = plot(query, model_rus, associates, model_name)

        return render_template('russian.html', result=associates, word=query.split('_')[0], pos=query.split('_')[-1], model=model_name, imagePath=imagePath)
    return render_template('russian.html')


@app.route('/english/', methods=['GET', 'POST'])
def english():
    if request.method == 'POST':
        try:
            input_data = request.form['query']
        except:
            return render_template('english.html', error="Something wrong with your query!")
        if input_data.replace('_', '').replace('-', '').isalnum():
            model_name = 'bnc'
            query = process_query(input_data, model_name)
            if query == 'Incorrect tag!' or query.startswith('Please, type'):
                error = query
                return render_template('english.html', error='Your query %s is incorrect' % error)
            try:
                associates = set([(round(pair[1], 4), pair[0]) for pair in model_eng.most_similar(positive=query, topn=20)][:10])
            except KeyError:
                return render_template('english.html', error=\
                    "Sorry, your word is not in the models vocabulary. Please, check the spelling")
            associates = sorted(associates, reverse=True)
            imagePath = plot(query, model_eng, associates, model_name)
            return render_template('english.html', result=associates, word=query, imagePath=imagePath)
    return render_template('english.html')


@app.route('/english/word/<word>/', methods=['GET', 'POST'])
def english_word(word):
    if word.replace('_', '').replace('-', '').isalnum():
        model_name = 'bnc'
        query = process_query(word, model_name)
        if query == 'Incorrect tag!' or query.startswith('Please, type'):
            error = query
            return render_template('english.html', error=error)    
        try:
            associates = set([(round(pair[1], 4), pair[0]) for pair in model_eng.most_similar(positive=query, topn=20)][:10])
        except KeyError:
            return render_template('english.html', error=\
                "Sorry, your word is not in the models vocabulary. Please, check the spelling")
        associates = sorted(associates, reverse=True)
        imagePath = plot(query, model_eng, associates, model_name)
        return render_template('english.html', result=associates, word=query, imagePath=imagePath)
    return render_template('english.html')


@app.route('/ajax/')
def ajax():
    return render_template('ajax.html')


@app.route('/ajax/count', methods=['POST'])
def count():
    word = request.form['word']
    name = request.form['name']

    if name and word:
        return jsonify({'input' : [word, name]})
    return jsonify({'error' : 'Missing data! Please, fill in both forms!'})


@celery.task(bind=True)
def long_task(self):
    input_word = choice(['президент', 'мир', 'путешествие', 'спектакль', 'компания'])
    bigrams = word_bigram(input_word)
    total = len(bigrams)
    results = []
    message = ''
    for i in range(total):
        for word in bigrams[i][0].split():
            if word != input_word:
                if not message:
                    message = word
                results.append(bigrams[i][0] + ': ' + str(bigrams[i][1]))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 
                                'total': total,
                                'status': message})
        time.sleep(5)
    final = [input_word] + [results]
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': final}


@app.route('/ajax/longtask', methods=['POST'])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/ajax/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    print(task)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info), 
        }
    return jsonify(response)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)