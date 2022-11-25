from flask import Flask, render_template, request

app = Flask(__name__)

# ---------------------------------------
#Pagina inicial
@app.route("/",  methods = ['GET'])
def index():
    return render_template ('index.html')

# ---------------------------------------
#Página de login
@app.route("/login", methods = ['GET', 'POST'])
def login():
    print()

app.run(debug=True)