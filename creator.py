import json
from MHT import MerkTree


class Certificate:
    def __init__(self, name, date, grade):
        self.name = name
        self.date = date
        self.grade = grade

    def to_json(self):
        return {
            'name': self.name,
            'date': self.date,
            'grade': self.grade
        }


c1 = Certificate('Ivan Ivanov', '2018-01-01', '87.7')
c2 = Certificate('Artur Grigorev', '2018-01-01', '97.7')
c3 = Certificate('Sathyarth Mishra Sharma', '2018-01-01', '98.7')
c4 = Certificate('Rasul Khasyanov', '2018-01-01', '99.7')

certificates = [c1, c2, c3, c4]

messages = [json.dumps(c.to_json()) for c in certificates]

tree = MerkTree(messages)
tree.create_tree()

pathes = tree.get_hashpathes()

