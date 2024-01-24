import json


with open("./reward_model_train_data_1901.jsonl", 'r', encoding="utf8") as f:
    lines = f.readlines()


for index,line in enumerate(lines):
    print("Example: ", index)
    item = json.loads(line)
    print("PROMPT: ", item["prompt"])
    print("OPTION 0: ", item["option_0"])
    print("OPTION 1: ", item["option_1"])
    print("OPTION 2: ", item["option_2"])
    print("OPTION 3: ", item["option_3"])

    choose_best = input("Choose best option: ")
    choose_best = "option_" + choose_best
    choose_worst = input("Choose worst option: ")
    choose_worst = "option_" + choose_worst

    with open("rlhf_data_2001.jsonl", "a", encoding="utf-8") as ff:
        item_save = {
            "prompt": item["prompt"],
            "chosen": item[choose_best],
            "rejected": item[choose_worst]
        }
    print("=====================================")
        