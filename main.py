import json
from hashlib import sha256
from time import time
from random import randint


pool = []
difficulty = 4
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


def mine():
    previous_hash = 'root'
    if len(block_chain) > 0:
        previous_hash = block_chain[-1]['hash']

    block = {
        'header': {
            'merkle_root': get_merkle_root(pool),
            'previous_hash': previous_hash,
            'difficulty': difficulty
        },
        'transactions': [p for p in pool]
    }
    pool.clear()
    for nonce in range(MAX_NONCE):
        block['header']['nonce'] = nonce
        current_hash = sha256(json.dumps(block['header']).encode()).hexdigest()
        if current_hash.startswith('0'*difficulty):
            break
    else:
        raise Exception('Unable to find nonce')

    block['hash'] = current_hash
    block_chain.append(block)
    print_block_data(block)


def print_blockchain_data():
    for block in block_chain:
        print_block_data(block)


def print_block_data(block):
    print(f'hash: {block["hash"]} | nonce: {block["header"]["nonce"]}')


def get_merkle_root(transactions):
    transaction_hashes = [sha256(json.dumps(t).encode()).hexdigest() for t in transactions]
    return merkle(transaction_hashes)


def merkle(hash_list):
    if len(hash_list) == 1:
        return hash_list[0]
    new_hash_list = []
    for i in range(0, len(hash_list)-1, 2):
        new_hash_list.append(hash_pair(hash_list[i], hash_list[i+1]))
    if len(hash_list) % 2 == 1:
        new_hash_list.append(hash_pair(hash_list[-1], hash_list[-1]))
    return merkle(new_hash_list)


def hash_pair(a, b):
    return sha256((a+b).encode()).hexdigest()


def insert_test_transactions(n):
    for _ in range(n):
        new_transaction(f'p{randint(1,50)}', f'p{randint(1,50)}', randint(1, 100))


def validate():
    last_hash = 'root'
    for block in block_chain:
        merkle_root = get_merkle_root(block['transactions'])
        if merkle_root != block['header']['merkle_root']:
            raise Exception('Merkle root has been tampered')

        temporary_header = {
            'merkle_root': block['header']['merkle_root'],
            'previous_hash': last_hash,
            'difficulty': block['header']['difficulty'],
            'nonce': block['header']['nonce']
        }
        block_hash = sha256(json.dumps(temporary_header).encode()).hexdigest()
        if block_hash != block['hash']:
            raise Exception(f'Block hash has been tampered! {block_hash} != {block["hash"]}')
        last_hash = block['hash']
    print('Blockchain is valid')


def create_test_chain():
    insert_test_transactions(1)
    mine()

    insert_test_transactions(50)
    mine()

    insert_test_transactions(500)
    mine()

    insert_test_transactions(1000)
    mine()

    insert_test_transactions(5000)
    mine()


def find_new_hash(block):
    for nonce in range(MAX_NONCE):
        block['header']['nonce'] = nonce
        current_hash = sha256(json.dumps(block['header']).encode()).hexdigest()
        if current_hash.startswith('0'*difficulty):
            break
    else:
        raise Exception('Unable to find nonce')

    block['hash'] = current_hash


if __name__ == '__main__':
    create_test_chain()
    validate()
