from flask import Flask, request, jsonify
from datetime import datetime
from dotenv import load_dotenv
import pywhatkit as pw
import os

app = Flask(__name__)

load_dotenv()

@app.route('/api', methods = ['GET'])
def index():
    return jsonify("index")

@app.route('/api/send-whatsapp', methods = ['POST'])
def send_whatsapp():
    is_valid = security_validation(request.headers['Wsp_Key'])
    if is_valid != True:
        return jsonify({ "msg": "Acceso Denegado!", "status": False })
 
    message = request.json['message']
    to = request.json['to']
    time = datetime.now()
    try: 
        pw.sendwhatmsg(to, message, time.hour, time.minute + 1)
        return jsonify({ "msg": "Whatsapp enviado con exito!", "status": True })
    except Exception as error:
        return jsonify({ "msg": "Ocurrio un error. Consultar con el administrador", "status": False })


def security_validation(api_key):
    secret_key = os.environ.get('SECRET_KEY')
    if secret_key == api_key:
        return True
    return False


if __name__ == "__main__":
    app.run(debug = True)