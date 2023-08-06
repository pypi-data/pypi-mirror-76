from flask import Flask, jsonify,request
from flask_cors import CORS
from googletrans import Translator
app = Flask(__name__)
CORS(app, support_credentials=True,  resources={r"/*": {"origins": "*"}} )
@app.route('/',methods=['GET', 'POST'])
def getdata():
    if (request.method == 'POST'):
        msg = request.args.get('msg','msg') 
        src= str(request.args.get('src','src'))
        dest =str(request.args.get('dest','dest'))
        trans = Translator()
        tn = trans.translate(msg ,src=src, dest=dest)
        text = str(tn.text)
        return text
if __name__ == '__main__':
    app.run( host='192.168.0.109',port=8080, debug=True)
