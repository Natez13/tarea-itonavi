# Main

from flask import Flask, render_template
from flask import send_from_directory

from routes.products_routes import product_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='https://friendly-space-funicular-xxq5x7jxggg296j5-5000.app.github.dev')
 
app.static_folder = 'static'

# Registrar Blueprint
app.register_blueprint(product_bp)

@app.route('/styles.css')
def styles():
    return send_from_directory('static', 'styles.css', mimetype='text/css')

@app.route('/')
def home():
    return 'Hello, World!'
    #return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
