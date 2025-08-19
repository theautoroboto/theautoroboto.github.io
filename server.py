from flask import Flask, render_template, url_for
# render_template allows us to render HTML
app = Flask(__name__)

@app.route('/')
def website():
    # Wants a template folder
    return render_template('index.htm')

@app.route('/about.htm')
def about():
    # Wants a template folder
    return render_template('about.htm')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.htm'), 404

if __name__ == '__main__':
    app.run(debug=True)
