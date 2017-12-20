import numpy as np
# import pandas as pd
import hashlib, json, sys
from collections import OrderedDict
from utils import hash_msg

# 1. Declare the class trees
class MerkTree:

    # 2. Initiate the class object
    def __init__(self, listoftransaction=None, dataoftransaction=None):
        self.messages = listoftransaction
        self.listoftransaction = listoftransaction
        self.past_transaction = OrderedDict()
        self.hash_pairs = OrderedDict()
        # self.dataoftransaction = dataoftransaction

    # 3. Create the Merkle Tree
    def create_tree(self):

        # 3.0 Continue on the declaration
        listoftransaction = self.listoftransaction
        past_transaction = self.past_transaction
        temp_transaction = []

        # 3.1 Loop until the list finishes
        for index in range(0, len(listoftransaction), 2):

            # 3.2 Get the most left element
            current = listoftransaction[index]

            # 3.3 If there is still index left get the right of the left most element
            if index + 1 != len(listoftransaction):
                current_right = listoftransaction[index + 1]

            # 3.4 If we reached the limit of the list then make a empty string
            else:
                current_right = ''

            # 3.5 Apply the Hash 256 function to the current values
            current_hash = hash_msg(current)

            # 3.6 If the current right hash is not a '' <- empty string
            if current_right != '':
                current_right_hash = hash_msg(current_right)

            # 3.7 Add the Transaction to the dictionary
            past_transaction[listoftransaction[index]] = current_hash

            # 3.8 If the next right is not empty
            if current_right != '':
                past_transaction[listoftransaction[index + 1]] = current_right_hash

            if current_right != '':
                self.hash_pairs[current] = (current_right_hash, 'r')
                self.hash_pairs[current_right] = (current_hash, 'l')
            else:
                self.hash_pairs[current] = ('', 'r')

            # 3.9 Create the new list of transaction
            if current_right != '':
                temp_transaction.append(current_hash + current_right_hash)

            # 3.01 If the left most is an empty string then only add the current value
            else:
                temp_transaction.append(current_hash)

        # 3.02 Update the variables and rerun the function again
        if len(listoftransaction) != 1:
            self.listoftransaction = temp_transaction
            self.past_transaction = past_transaction

            # 3.03 Call the function repeatly again and again until we get the root
            self.create_tree()

    # 4. Return the past Transaction
    def Get_past_transacion(self):
        return self.past_transaction

    # 5. Get the root of the transaction
    def Get_Root_leaf(self):
        last_key = list(self.past_transaction.keys())[-1]
        return self.past_transaction[last_key]

    def get_hashpath(self, msg):
        path = []
        next = msg
        while next in self.hash_pairs:

            pair, side = self.hash_pairs[next]
            path.append((pair, side))

            next_hashed = hash_msg(next)

            if side == 'r':
                next = next_hashed + pair
            elif side == 'l':
                next = pair + next_hashed

        if path[-1][0] == '':
            path = path[:-1]

        return path

    def get_hashpathes(self):
        pathes = {msg:self.get_hashpath(msg) for msg in self.messages}
        return pathes


# person1 = {'name': 'Bob', 'age': '22'}
# person2 = {'name': 'Alice', 'age': '23'}
#
# json_data1 = open('files/unsigned12.json').read()
# data1 = json.loads(json_data1)
# json_data2 = open('files/unsigned.json').read()
# data2 = json.loads(json_data2)
# json_data3 = open('files/signed.json').read()
# data3 = json.loads(json_data3)
#
#
#
# # b) Give list of transaction
# msg1 = json.dumps(data1, sort_keys=True)
# msg2 = json.dumps(data2, sort_keys=True)
# msg3 = json.dumps(data3, sort_keys=True)
# transaction = [msg1, msg2, msg3]
#
# # c) pass on the transaction list
# Jae_Tree = MerkTree(transaction)
# # Jae_Tree.listoftransaction = transaction
# # Jae_Tree.dataoftransaction = values
#
#
# # d) Create the Merkle Tree transaction
# Jae_Tree.create_tree()
#
# # e) Retrieve the transaction
# past_transaction = Jae_Tree.Get_past_transacion()