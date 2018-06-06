# coding=utf-8
import json

with open('transport_old.json') as f:
    data = json.load(f)

t_types = []
marks = {}

data = data['types']
for i in range(len(data)):
    t_types.append({'id': i, 'name': data[i]['title']})
    brands = data[i]['brands']
    for brand in brands:
        mark_name, model_name = brand['marks'][0]['title'].split(maxsplit=1)
        if 'шасси' in model_name:
            continue
        if 'на базе' in model_name:
            continue
        marks[mark_name] = marks.get(mark_name, [])
        for mark in brand['marks']:
            name = mark['title'].split(maxsplit=1)[1]
            if 'шасси' in name:
                continue
            if 'на базе' in name:
                continue
            marks[mark_name].append({"name": name, "type": i})

marksL = []
for key, value in marks.items():
    marksL.append({"name": key, "models": value})

data = {"type": t_types, "marks": marksL}

j = json.dumps(data, ensure_ascii=True).encode('utf8')

with open('transport.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)
