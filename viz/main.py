# import the Flask class from the flask module
from flask import Flask, render_template, send_from_directory

# create the application object
app = Flask(__name__)

@app.route('/')
def index():
    # render a template
    return render_template('index.html')

@app.route('/CA1Models.csv')
def CA1Models():
    # render dataset in parent directory

    return send_from_directory('../', 'CA1Models.csv')

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
