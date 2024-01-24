import openai
from listApi import list_api
import pathlib
import textwrap
import time
import google.generativeai as genai 


# response = model.generate_content("Xin chào, bạn tên là")
# print(response.text)

def rewrite_gemini(question):

    genai.configure(api_key="AIzaSyC6m606g-gh4_pg_BLF7ogypud-ht3xGYw")
    model = genai.GenerativeModel('gemini-pro')
    try:
        prompt = f"""
        Think step by step to answer this question, and provide search engine queries for knowledge
        that you need. Split the queries with ’;’ and end the queries with ’**’.  
        Question: Tôi nên học ngành Công nghệ thông tin ở trường Tôn Đức Thắng hay trường đại học Công nghệ thông tin?
        Queries: ngành công nghệ thông tin ở trường Tôn Đức Thắng; ngành công nghệ thông tin ở trường đại học Công nghệ thông tin; so sánh trường đại học Tôn Đức Thắng và trường đại học Công nghệ thông tin**
        Question: Em đã có bằng MOS, vậy em có được miễn môn Cơ sở tin học ở trường đại học Tôn Đức Thắng không?
        Queries: môn cơ sở tin học ở trường đại học Tôn Đức Thắng; chứng chỉ MOS và miễn môn tại trường Tôn Đức Thắng; điều kiện miễn môn cơ sở tin học trường đại học Tôn Đức Thắng**
        Question: {question}
        Queries:
        """
        response = model.generate_content(prompt)
        return [q.strip() for q in response.parts[0].text.split(";")]
        # return response.parts[0].text
    except Exception as e:
        print(e)

def rating_gemini(item):

    genai.configure(api_key="AIzaSyC6m606g-gh4_pg_BLF7ogypud-ht3xGYw")
    model = genai.GenerativeModel('gemini-pro')
    try:
        prompt = f"""
        Think step by step to answer this question.
        You will give a question and 4 options which every option is a list of query for search engine.
        You should consider which option is the best for the question and the worst for the question.
        If the option has some unrelated query, or include the person's information, penalize it.
        Your answer should be in this format:
        BEST: option_x
        WORST: option_y

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
        # time.sleep(10)
        # rewrite_gemini(question)

print(rewrite_gemini("Cho tôi hỏi nếu tôi đi tù ra thì có dễ xin việc không?"))

def rewrite(question, list_api=list_api, idx=0):
    client = openai.OpenAI(api_key=list_api[idx])
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"""Think step by step to answer this question, and provide search engine queries for knowledge
            that you need. Split the queries with ’;’ and end the queries with ’**’.  
            Question: Tôi nên học ngành Công nghệ thông tin ở trường Tôn Đức Thắng hay trường đại học Công nghệ thông tin?
            Queries: ngành công nghệ thông tin ở trường Tôn Đức Thắng; ngành công nghệ thông tin ở trường đại học Công nghệ thông tin; so sánh trường đại học Tôn Đức Thắng và trường đại học Công nghệ thông tin**
            Question: Em đã có bằng MOS, vậy em có được miễn môn Cơ sở tin học ở trường đại học Tôn Đức Thắng không?
            Queries: môn cơ sở tin học ở trường đại học Tôn Đức Thắng; chứng chỉ MOS và miễn môn tại trường Tôn Đức Thắng; điều kiện miễn môn cơ sở tin học trường đại học Tôn Đức Thắng**
            Question: {question}
            Queries:""",
            temperature=0,
            max_tokens=1500
        )

        return [q.strip() for q in response.choices[0].text.split(";")]
    except Exception as e:
        # print(type())
        print(e.args[0])
        if "exceeded your current quota" in e.args[0] or "Incorrect API key provided" in e.args[0]:
            list_api.pop(0)
            rewrite(question, list_api, 0)
        else:
            rewrite(question, list_api, (idx+1)%len(list_api))

def rewrite_gpt4(question, list_api=list_api, idx=0):
    if len(list_api) == 0:
        print("No API key left.")
        return {"error": "No API key left."}
    try:
        client = openai.OpenAI(api_key=list_api[idx])
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": f"""Think step by step to answer this question, and provide search engine queries for knowledge
            that you need. Split the queries with ’;’ and end the queries with ’**’. 
            Question: Tôi nên học ngành Công nghệ thông tin ở trường Tôn Đức Thắng hay trường đại học Công nghệ thông tin?
            Queries: ngành công nghệ thông tin ở trường Tôn Đức Thắng; ngành công nghệ thông tin ở trường đại học Công nghệ thông tin; so sánh trường đại học Tôn Đức Thắng và trường đại học Công nghệ thông tin**
            Question: Em đã có bằng MOS, vậy em có được miễn môn Cơ sở tin học ở trường đại học Tôn Đức Thắng không?
            Queries: môn cơ sở tin học ở trường đại học Tôn Đức Thắng; chứng chỉ MOS và miễn môn tại trường Tôn Đức Thắng; điều kiện miễn môn cơ sở tin học trường đại học Tôn Đức Thắng**
                """},
                {"role": "user", "content": f"Question: {question}. Queries:"}
            ],  
            temperature=0.2,
        )
        return [q.strip() for q in response.choices[0].message.content.split(";")]
    except Exception as e:
        # print(type())
        print(e.args[0])
        if "exceeded your current quota" in e.args[0] or "Incorrect API key provided" in e.args[0]:
            list_api.pop(0)
            rewrite(question, list_api, 0)
        else:
            rewrite(question, list_api, (idx+1)%len(list_api))

def generate_answer(prompt, context, list_api=list_api, idx=0):
    if len(list_api) == 0:
        print("No API key left.")
        return {"error": "No API key left."}
    try:
        client = openai.OpenAI(api_key=list_api[idx])
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"""You are a helpful assistant.\
                Your name is LEGALBOT.\
                Your job is to answer questions about law base on your knowledge and context given.\
                You are given a context: {context}"""},
                {"role": "user", "content": f"{prompt}"},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        # print(type())
        print(e.args[0])
        if "exceeded your current quota" in e.args[0]:
            list_api.pop(0)
            generate_answer(prompt, context, list_api, 0)
        else:
            generate_answer(prompt, context, list_api, (idx+1)%len(list_api))