from flask import Flask
from flask import redirect
from flask import request
from flask import render_template
import json

# Cria o Site
site = Flask(__name__)

# Dict das URLs
urls = json.load(open('urls.json', 'r'))

def gerar_form(retorno=''):
    return render_template('index.html') + '\n' + retorno


@site.route('/', methods=['GET', 'POST'])
def index():
    global urls

    # Se for POST
    if request.method == 'POST':

        # Checa se os campos não são vazios
        if request.form['url'] == '' or request.form['path'] == '':
            return gerar_form('PREENCHA OS DOIS CAMPOS')

        # Checar se a URL já existe
        if request.form['path'] in urls.keys():
            return gerar_form('JÁ EXISTE ')

        # Função de Caracteres proibidos
        proibido = '/'
        if request.form['path'].count(proibido) > 0:
            return gerar_form(f'CARACTERES PROIBIDOS: {proibido}')

        # Gerar URL
        # Se não tiver http/https na URL, ele adiciona
        if request.form['url'].find('http://') != 0 and request.form['url'].find('https://') != 0:
            # Adicionando http
            nova_url = 'http://' + request.form['url']
        else:
            nova_url = request.form['url']

        # Salva na variável e no json
        urls.update({request.form['path']: nova_url})
        json.dump(urls, open('urls.json', 'w'))

        return gerar_form('URL GERADA\n\n' + str(urls))

    # Se for GET, apenas gerar os campos
    return gerar_form()


# Joga tudo que não for INDEX para suas URLs
@site.route('/<url>')
def simple_url_post(url):
    global urls

    # Se a URL existir, redireciona
    if url in urls.keys():
        return redirect(f'{urls[url]}')

    # Se não, volta para a página inicial
    else:
        return redirect('/')


# Roda o Site
site.run()
