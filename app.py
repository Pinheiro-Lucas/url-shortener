from flask import *
import json

app = Flask(__name__)

# Simple URL database with json
db_path = "db.json"
db = json.load(open(db_path, 'r'))

# Custom page
page = "index.html"


@app.route('/', methods=['GET', 'POST'])
def index():
    # POST method
    if request.method == 'POST':

        # Empty
        if request.form['url'] == '' or request.form['path'] == '':
            return render_template(page, error='PREENCHA OS DOIS CAMPOS')

        # Dupplicated values
        if request.form['path'] in db.keys():
            return render_template(page, error='JÁ EXISTE ')

        # Avoid special characters into URL that can breaks the program
        special_characters = '/'
        if request.form['path'].count(special_characters) > 0:
            return render_template(page, error=f'CARACTERES PROIBIDOS: {special_characters}')

        # Force https
        new_url = request.form['url']
        if new_url.count('http') == 0:
            new_url = 'https://' + new_url

        # Save json file (database)
        db.update({request.form['path']: new_url})
        json.dump(db, open(db_path, 'w'))

        return render_template(page, error='URL GERADA\n\n' + str(db))

    # GET method (just render the page)
    return render_template(page)


# URL redirect
@app.route('/<url>')
def simple_url_post(url):
    # Check if url exists
    if url in db.keys():
        return redirect(db[url])
    return redirect('/')


app.run()
