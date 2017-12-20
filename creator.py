import json
from MHT import MerkTree


class Certificate:
    def __init__(self, student_id, name, date, grade):
        self.id = student_id
        self.name = name
        self.date = date
        self.grade = grade

    def to_json(self):
        return {
            'student_id': self.id,
            'name': self.name,
            'date': self.date,
            'grade': self.grade
        }

    def from_json(dic):

        id = dic['student_id']
        name = dic['name']
        date = dic['date']
        grade = dic['grade']

        return Certificate(id, name, date, grade)


    def __str__(self):
        return json.dumps(self.to_json())





certificates = []

certificates.append(Certificate(1, 'Ivan Ivanov', '2017-12-21', '87.7'))
certificates.append(Certificate(2, 'Artur Grigorev', '2017-12-21', '99.7'))
certificates.append(Certificate(3, 'Sathyarth Mishra Sharma', '2017-12-21', '99.7'))
certificates.append(Certificate(4, 'Rasul Khasyanov', '2017-12-21', '99.7'))
certificates.append(Certificate(5, 'Igor Mazhenkov', '2017-12-21', '72.1'))
certificates.append(Certificate(6, 'Evgeniya Babak', '2017-12-21', '92.2'))
certificates.append(Certificate(7, 'Irina Vihrova', '2017-12-21', '89.2'))


certificates_json = [c.to_json() for c in certificates]

cstr = str(certificates[0])
cjs = json.loads(cstr)
c = Certificate.from_json(cjs)

# print(c)



# print(json.dumps(certificates_json[0]))
#
# with open('certificates.json', 'w') as f:
#     json.dump(certificates_json, f)

# tree = MerkTree(messages)
# tree.create_tree()

# pathes = tree.get_hashpathes()

