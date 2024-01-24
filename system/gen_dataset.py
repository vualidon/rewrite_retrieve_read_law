import json

with open("./question_queries_second.jsonl", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        new_item = {}
        item = json.loads(line)
        new_item['question'] ="Generate queries: " + item['question']
        new_item['queries'] = "; ".join(item['queries'])
        # print(new_item['queries'])
        with open("./dataset_finetune.jsonl", "a", encoding="utf-8") as ff:
            ff.write(json.dumps(new_item, ensure_ascii=False) + "\n")
        # break