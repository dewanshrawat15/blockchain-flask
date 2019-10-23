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

    def register_node(self, address):
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.add.nodes(parsed_url.netloc)
        elif parsed_url.path:
            self.add.nodes(parsed_url.path)
        else:
            raise ValueError('Invalid Url')
    
    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print('f{last_block}')
            print('f{block}')
            print("\n-----------\n")
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

    def resolve_conflicts(self):
        neighbors = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbors:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

            if length > max_length and self.valid_chain(chain):
                max_length = length
                new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

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