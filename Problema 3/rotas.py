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
    return render_template ('login.html')

app.run(debug=True)