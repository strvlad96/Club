import json

data = []
with open ('users.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

users = []
for user in data:
    item = f"{user['name']} {user['surname']} {user['class']}"
    users.append(item)
print(users)

with open('spisok.txt', 'w', encoding='utf-8') as file:
    for user in users:
        file.write(user+'\n')