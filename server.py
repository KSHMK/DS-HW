import os
from flask import Flask, request, jsonify, send_from_directory, abort
from flask_cors import CORS
import pyzipper
import hashlib
import logging
import socket
from struct import pack
import datetime
import pickle
import signal
from sys import exit

UPLOAD_FOLDER = './samples'
PORT = 8080

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

with open('sample_list.pickle', 'rb') as handle:
    sample_list = pickle.load(handle)
with open('node_list.pickle', 'rb') as handle:
    node_list = pickle.load(handle)


@app.route('/node', methods=['POST'])
def node_register():
    try:
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        params = request.get_json()
        node_list[ip] = params
        return "OK"
    except Exception as e:
        logging.ERROR(e)
        return "FAILED"

def node_call(filename):
    send_data = pack("<I",len(filename))+filename.encode()
    for ip in node_list.keys():
        try:
            sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sc.settimeout(1)
            sc.connect((ip, PORT))
            sc.send(send_data)
            re = sc.recv(1)
            sc.close()
        except Exception as e:
            continue
    return

@app.route('/node', methods=['PUT'])
def node_result():
    try:
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        params = request.get_json()
        sample_list[params['sample_hash']]['result'].append({"IP":ip,"AV":params['av_name'],
            "result":params['detect_result'],
            "result_time":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            
        return "OK"
    except Exception as e:
        logging.ERROR(e)
        return "FAILED"


@app.route('/sample/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/sample', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return abort(400)
    file = request.files['file']
    if file.filename == '':
        return abort(400)
    if file:
        file_data = file.read()
        file_md5 = hashlib.md5(file_data).hexdigest()
        if file_md5 in sample_list:
            return jsonify({"hash":file_md5})
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],file_md5+'.zip')
        
        zipfile_ob = pyzipper.AESZipFile(file_path, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES)
        zipfile_ob.setpassword(b"infected")
        zipfile_ob.writestr(file_md5,file_data)
        zipfile_ob.close()

        sample_list[file_md5] = {"upload_time":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"result":[]}
        node_call(file_md5)
        return jsonify({"hash":file_md5})
    return abort(400)

@app.route('/result/<hash>')
def sample_result(hash):
    if hash not in sample_list:
        return {"time":'',"result":[]}
    return jsonify({"time":sample_list[hash]["upload_time"],"result":sample_list[hash]['result']})

def exit_handler(signal, frame):
    print("SAVE")
    with open('sample_list.pickle', 'wb') as handle:
        pickle.dump(sample_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('node_list.pickle', 'wb') as handle:
        pickle.dump(node_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_handler) # ctlr + c
    signal.signal(signal.SIGTSTP, exit_handler) # ctlr + z
    app.run(host="0.0.0.0",port=8080,debug=True)