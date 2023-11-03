from flask import Flask, render_template, url_for
# render_template allows us to render HTML
app = Flask(__name__)
print(__name__)

@app.route('/')
def website():
    # Wants a template folder
    return render_template('index.htm')

@app.route('/about.htm')
def about():
    # Wants a template folder
    return render_template('about.htm')

@app.route('/hello_world')
def hello_world():
    print(url_for('static', filename='favicon.ico'))
    return 'Hello, World!'

@app.route('/blog')
def blog():
    return 'This is my blog'
    
@app.route('/blog/2020/family')
def family_blog():
    return 'This is my family blog'