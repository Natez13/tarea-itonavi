# Main

from flask import Flask, render_template
from flask import send_from_directory

#from routes.products_routes import product_bp

app = Flask(__name__)
 
#app.static_folder = 'static'

# Registrar Blueprint
#app.register_blueprint(product_bp)

#@app.route('/styles.css')
#def styles():
    #return send_from_directory('static', 'styles.css', mimetype='text/css')

@app.route('/')
def home():
    return 'Hello, World!'
    #return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
