from flask import Flask, request, Response, render_template, send_file
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


@app.route('/', methods=['GET', 'POST','PUT'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    data = request.form
    filedata = request.files.get('file')
    print(data)
    print(filedata.read())
    # return data.get('name','no name')
    return send_file('abc.txt', as_attachment=True)

app.run(port=5432)
