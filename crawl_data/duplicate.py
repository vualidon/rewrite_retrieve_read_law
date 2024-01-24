import json
titles = []
with open("./data_major_cate.jsonl", "r", encoding="utf-8") as f:
    data = f.readlines()
    for line in data:
        line = json.loads(line)
        title = line['title']
        if title in titles:
            continue
        else:
            titles.append(title)
            with open("./data_final.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(line, ensure_ascii=False) + "\n")
        