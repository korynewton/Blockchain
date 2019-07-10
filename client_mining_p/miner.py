import hashlib
import requests
import json

import sys


# TODO: Implement functionality to search for a proof
def proof_of_work(prev_proof):
    proof = 0
    while validate_pow(prev_proof, proof) is False:
        proof += 1
    return proof


def validate_pow(prev_proof, proof):
    guess = f'{prev_proof}{proof}'.encode()
    guess_hashed = hashlib.sha256(guess).hexdigest()

    return guess_hashed[:4] == '0000'


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        req = requests.get("http://localhost:5000/chain").json()
        prev_proof = req["chain"][-1]["proof"]
        new_proof = proof_of_work(prev_proof)

        # TODO: When found, POST it to the server {"proof": new_proof}
        response = requests.post(
            "http://localhost:5000/mine", json={"proof": new_proof}).json()

        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if response["message"] == "New Block Forged":
            coins_mined += 1
            print(response["message"])
            print('total coins mined: ', coins_mined)
