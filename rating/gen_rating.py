import pathlib
import textwrap
import time
import google.generativeai as genai 
import json

def rating_gemini(item):

    genai.configure(api_key="AIzaSyC6m606g-gh4_pg_BLF7ogypud-ht3xGYw")
    model = genai.GenerativeModel('gemini-pro')
    try:
        prompt = f"""
        Think step by step to answer this question. \n
        You will give a question and 4 options which every option is a list of query for search engine.\n
        The purpose of the query is to find the information by search engine to answer the question.\n
        You should consider which option is the best for the question and the worst for the question.\n
        Best option: has the most relevant query to the question; extract the best keyword from the question; not include the person's information such as name of questioner.\n
        Worst option: has the least relevant query to the question; extract the wrong keyword from the question; include the person's information such as name of questioner; include the unrelated query.\n 
        Your answer should be in this format:
        ```
        BEST: option_x
        WORST: option_y

        REASON:
        ```
        prompt: {item['prompt']}  
        option_0: {item['option_0']}
        option_1: {item['option_1']}
        option_2: {item['option_2']}
        option_3: {item['option_3']}

        Rating:
        """
        response = model.generate_content(prompt)
        return response.parts[0].text
        # return response.parts[0].text
    except Exception as e:
        print(e)


with open("./reward_model_train_data_2001.jsonl", 'r', encoding='utf-8') as f:
    data = f.readlines()

data = [json.loads(d) for d in data]
for item in data:
    time.sleep(0.5)
    try:
        result_item = {
            "prompt": item["prompt"]
        }
        response = rating_gemini(item)
        # print(respone)
        response = response.split("\n")
        best = [r.strip() for r in response if "BEST:" in r]
        worst = [r.strip() for r in response if "WORST:" in r]
        best_option = best[0].split(":")[1].strip()
        worst_option = worst[0].split(":")[1].strip()
        result_item["chosen"] = item[best_option]
        result_item["rejected"] = item[worst_option]
        # print(result_item)
        with open("./rating_result.jsonl", 'a', encoding='utf-8') as f:
            f.write(json.dumps(result_item, ensure_ascii=False) + "\n")
    # break
    except Exception as e:
        print(e)
        with open("./rating_result_error.jsonl", 'a', encoding='utf-8') as f:
            f.write(json.dumps(result_item, ensure_ascii=False) + "\n")
        continue