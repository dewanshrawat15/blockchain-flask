import hashlib
import json
from uuid import uuid4
from time import time
from urllib.parse import urlparse

import requests
from flask import Flask, jsonify, request

class BlockChain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        self.new_block(previous_hash='1', proof=100)

app = Flask(__name__)

@app.route('/home', methods=['GET'])
def home():
    response = {
        "message": "Welcome! Status 200"
    }
    return jsonify(response), 200

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='Define the port number for the server to listen on')
    args = parser.parse_args()

    port = args.port

    app.run(host='0.0.0.0', port=port)