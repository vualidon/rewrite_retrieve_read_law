from generate import rewrite, rewrite_gpt4, rewrite_gemini
from datasets import load_dataset
import json
import time

# ds = load_dataset("thangvip/qa-tvlpl-11k", split="train")
ds = load_dataset("thangvip/reward-model-data-rewrite", split="train")


training_ds = ds.shuffle(seed=42).select(range(11000))
# 300: gpt-4

print(training_ds)
count = 0
for index, line in enumerate(training_ds):
    if index > 3000 + 2165:
        try:
            question = line['question']
            # if ":" in question:
            #     question = question.split(":")[1].strip()
            # if "Câu hỏi":
            #     question = question.split("Câu hỏi")[0].strip()
            # question = question.replace("-", "").replace("(", "").strip()
            # print(question)
            time.sleep(0.7)
            queries = rewrite_gemini(question=question)
            if '**' in queries[-1]:
                queries[-1] = queries[-1].replace("**",'')
            # print(queries)
            with open("./question_queries_second.jsonl", "a", encoding="utf-8") as f:
                item = {
                    "question": question,
                    "queries": queries
                }
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
            count += 1
            if count % 100 == 0:
                print(count)
        except Exception as e:
            print(e)
            with open("./error.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(line, ensure_ascii=False) + "\n")
        # break