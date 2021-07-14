import json
from hashlib import sha256
from time import time


pool = []
prefix_zeros = 4
block_chain = []
MAX_NONCE = 1000000


def new_transaction(sender, receiver, amount):
    transaction = {
        'sender': sender,
        'receiver': receiver,
        'amount': amount,
        'timestamp': time()
    }
    pool.append(transaction)


def mine(previous_hash):
    block = {
        'payload': [p for p in pool],
        'previous_hash': previous_hash,
        'nonce': 0
    }
    pool.clear()
    for nonce in range(MAX_NONCE):
        block['nonce'] = nonce
        current_hash = sha256(json.dumps(block).encode()).hexdigest()
        if current_hash.startswith('0'*prefix_zeros):
            break
    else:
        raise Exception('Unable to find nonce')

    block['hash'] = current_hash
    block_chain.append(block)


def insert_test_transactions_1():
    new_transaction('p1', 'p2', 10)
    new_transaction('p3', 'p4', 5)
    new_transaction('p5', 'p6', 15)
    new_transaction('p2', 'p5', 53)
    new_transaction('p4', 'p6', 45)


def insert_test_transactions_2():
    new_transaction('p4', 'p2', 2)
    new_transaction('p1', 'p6', 6)
    new_transaction('p3', 'p2', 51)
    new_transaction('p4', 'p1', 97)
    new_transaction('p6', 'p1', 46)


if __name__ == '__main__':
    insert_test_transactions_1()
    mine('root')

    insert_test_transactions_2()
    mine(block_chain[-1]['hash'])
    print([block['nonce'] for block in block_chain])
    print([block['hash'] for block in block_chain])


'''
[
   {
      "payload":[
         {
            "sender":"p1",
            "receiver":"p2",
            "amount":10,
            "timestamp":1625416940.2877693
         },
         {
            "sender":"p3",
            "receiver":"p4",
            "amount":5,
            "timestamp":1625416940.2877693
         },
         {
            "sender":"p5",
            "receiver":"p6",
            "amount":15,
            "timestamp":1625416940.2877693
         },
         {
            "sender":"p2",
            "receiver":"p5",
            "amount":53,
            "timestamp":1625416940.2877693
         },
         {
            "sender":"p4",
            "receiver":"p6",
            "amount":45,
            "timestamp":1625416940.2877693
         }
      ],
      "previous_hash":"root",
      "nonce":21317,
      "hash":"0000f83abad9ab2624511c5c6d3068b5128d977d529338e2a35f4b4500b2792e"
   },
   {
      "payload":[
         {
            "sender":"p4",
            "receiver":"p2",
            "amount":2,
            "timestamp":1625416940.6089392
         },
         {
            "sender":"p1",
            "receiver":"p6",
            "amount":6,
            "timestamp":1625416940.6089392
         },
         {
            "sender":"p3",
            "receiver":"p2",
            "amount":51,
            "timestamp":1625416940.6089392
         },
         {
            "sender":"p4",
            "receiver":"p1",
            "amount":97,
            "timestamp":1625416940.6089392
         },
         {
            "sender":"p6",
            "receiver":"p1",
            "amount":46,
            "timestamp":1625416940.6089392
         }
      ],
      "previous_hash":"0000f83abad9ab2624511c5c6d3068b5128d977d529338e2a35f4b4500b2792e",
      "nonce":157202,
      "hash":"0000cfd3eb82c7c2989408c51f1d7df32e7fc25439e4f52774a527f978a6a9eb"
   }
]
'''