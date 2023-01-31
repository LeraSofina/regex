import re
from pprint import pprint
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
# pprint(contacts_list)

names = []
data = []
for row in contacts_list[1:]:
    row[:3] = [''.join(row[:3])]
    row[0] = re.sub(r'([А-Я])', r' \1', row[0]).split()
    names.append(row[0])
    data.append(row[1:])
    if len(row[0]) < 3:
        row[0].append('')

result = [name + info for name, info in zip(names, data)]

pattern = r'(\+7|8)[\s(]{0,3}(\d{3})[\s)-]{0,3}(\d{3})[-\s]{0,3}(\d{2})[-\s]{0,3}(\d{2})[\s(]{0,3}(доб\.)?[\s]?(\d+)?[\s)]?'
substitution = r'+7(\2)\3-\4-\5 \6\7'
for phone in result:
    phone[5] = re.sub(pattern, substitution, str(phone[5]))


res = []
group_list = []
for i in result:
    if i[:2] not in res:
        res.append(i[:2])
        group_list.append([i[2:]])
    else:
        count = res.index(i[:2])
        group_list[count].append(i[2:])


for y, element in enumerate(group_list):
    if len(element) > 1:
        concat = list(zip(element[0], element[1]))
        for j, elem in enumerate(concat):
           if elem[0] == elem[1]:
                    concat[j] = elem[0]
           elif elem[0] == "":
               concat[j] = elem[1]
           elif elem[1] == "":
               concat[j] = elem[0]
        group_list[y] = concat
    else:
        group_list[y] = [item for y in element for item in y]

for y, name in enumerate(res):
    res[y] = name + group_list[y]

pprint(res)

with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(res)


