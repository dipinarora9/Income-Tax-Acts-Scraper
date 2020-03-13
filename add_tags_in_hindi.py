import json

data = {}

dataInHindi = {}

with open("english.json", "r") as f:
    data = json.load(f)

with open("hindi.json", "r") as f:
    dataInHindi = json.load(f)
i = 0

for title, titleInHindi in zip(data, dataInHindi):
    i += 1
    for section, sectionInHindi in zip(data[title], dataInHindi[titleInHindi]):
        dataInHindi[titleInHindi][sectionInHindi]["tags"] = data[title][section]["tags"]

file = open("finalHindi.json", "w")
json.dump(dataInHindi, file, indent=0)
