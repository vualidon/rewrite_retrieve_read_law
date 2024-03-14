# import openai
# # from listApi import list_api
# import pathlib
import textwrap
import time
import google.generativeai as genai 
import dotenv
import os
from IPython.display import Markdown
from google.ai.generativelanguage_v1beta.types.content import Content
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import warnings
warnings.filterwarnings("ignore")

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))




dotenv.load_dotenv()
# google_api_key = os.getenv("GOOGLE_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

# response = model.generate_content("Xin chào, bạn tên là")
# print(response.text)
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-pro')

def classification_question(question):
    try:
        prompt = f"""
        You are a helpful assistant. Your mission is to classify that the question is about law, rule or not.
        If the question is about law or rule, you have to answer "YES".
        If the question is not about law or rule, you have to answer "NO".
        Question: {question}
        Classify:
        """
        response = model.generate_content(prompt)
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        print(e)
        return "Xin lỗi, hiện tại tôi không thể trả lời câu hỏi này. Đã có lỗi xảy ra khi thực hiện trả lời câu hỏi."

# print(classification_question("xin chào, bạn tên gì?"))

def generate_queries(question):
    tokenizer = AutoTokenizer.from_pretrained("thangvip/vi-t5-rewriter-rlhf")
    model_rewrite = AutoModelForSeq2SeqLM.from_pretrained("thangvip/vi-t5-rewriter-rlhf")
    question = "Generate queries: " + question
    input_ids = tokenizer(question, return_tensors="pt").input_ids
    outputs = model_rewrite.generate(input_ids)
    return tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

def response_without_context(question, history=""):
    try:
        completed_prompt = f"""\
        #ROLE
        You are a helpful assistant, your name are "LAWLINKER".
        Your job is to answer questions about law base on your knowledge and context given.

        #INSTRUCTION
        You are given history (optional) and a question.
        If history is given, you should consider it as a part of context.
        Your answer always be clear and detailed.
        When you can answer the question, also provide the source of your answer.

        #QUESTION
        {question}

        #HISTORY
        {history}

        #ANSWER
        """
        response = model.generate_content(completed_prompt)
        return response.candidates[0].content.parts[0].text
    # return 
    except Exception as e:
        print(e)
        return "Xin lỗi, hiện tại tôi không thể trả lời câu hỏi này. Đã có lỗi xảy ra khi thực hiện trả lời câu hỏi."

def response_gemini(question, context="", history=""):
    try:
        completed_prompt = f"""\
        #ROLE
        You are a helpful assistant name "LAWLINKER".
        Your job is to answer questions about law base on your knowledge and context given.

        #INSTRUCTION
        You are given context paragraphs, history (optional) and a question.
        If the information in the context and your knowledge is not enough to answer the question,\
        you have to response: "Xin lỗi, hiện tại tôi không thể trả lời câu hỏi này".
        If history is given, you should consider it as a part of context.
        When you can answer the question, also provide the source of your answer.
        Your answer always be clear and detailed.
        The source should be summarized in 1-2 sentences.

        #CONTEXT
        {context}

        #HISTORY
        {history}

        #QUESTION
        {question}

        #ANSWER
        """
        response = model.generate_content(completed_prompt)
        return response.candidates[0].content.parts[0].text
    # return 
    except Exception as e:
        print(e)
        return "Xin lỗi, hiện tại tôi không thể trả lời câu hỏi này. Đã có lỗi xảy ra khi thực hiện trả lời câu hỏi."


# print(generate_queries("Làm sao để có được sổ đỏ với mảnh đất của mình?"))




def rewrite_gemini(question):
    
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

# print(rewrite_gemini("Cho tôi hỏi nếu tôi đi tù ra thì có dễ xin việc không?"))

# def rewrite(question, list_api=list_api, idx=0):
#     client = openai.OpenAI(api_key=list_api[idx])
#     try:
#         response = client.completions.create(
#             model="gpt-3.5-turbo-instruct",
#             prompt=f"""Think step by step to answer this question, and provide search engine queries for knowledge
#             that you need. Split the queries with ’;’ and end the queries with ’**’.  
#             Question: Tôi nên học ngành Công nghệ thông tin ở trường Tôn Đức Thắng hay trường đại học Công nghệ thông tin?
#             Queries: ngành công nghệ thông tin ở trường Tôn Đức Thắng; ngành công nghệ thông tin ở trường đại học Công nghệ thông tin; so sánh trường đại học Tôn Đức Thắng và trường đại học Công nghệ thông tin**
#             Question: Em đã có bằng MOS, vậy em có được miễn môn Cơ sở tin học ở trường đại học Tôn Đức Thắng không?
#             Queries: môn cơ sở tin học ở trường đại học Tôn Đức Thắng; chứng chỉ MOS và miễn môn tại trường Tôn Đức Thắng; điều kiện miễn môn cơ sở tin học trường đại học Tôn Đức Thắng**
#             Question: {question}
#             Queries:""",
#             temperature=0,
#             max_tokens=1500
#         )

#         return [q.strip() for q in response.choices[0].text.split(";")]
#     except Exception as e:
#         # print(type())
#         print(e.args[0])
#         if "exceeded your current quota" in e.args[0] or "Incorrect API key provided" in e.args[0]:
#             list_api.pop(0)
#             rewrite(question, list_api, 0)
#         else:
#             rewrite(question, list_api, (idx+1)%len(list_api))

# def rewrite_gpt4(question, list_api=list_api, idx=0):
#     if len(list_api) == 0:
#         print("No API key left.")
#         return {"error": "No API key left."}
#     try:
#         client = openai.OpenAI(api_key=list_api[idx])
#         response = client.chat.completions.create(
#             model="gpt-4-1106-preview",
#             messages=[
#                 {"role": "system", "content": f"""Think step by step to answer this question, and provide search engine queries for knowledge
#             that you need. Split the queries with ’;’ and end the queries with ’**’. 
#             Question: Tôi nên học ngành Công nghệ thông tin ở trường Tôn Đức Thắng hay trường đại học Công nghệ thông tin?
#             Queries: ngành công nghệ thông tin ở trường Tôn Đức Thắng; ngành công nghệ thông tin ở trường đại học Công nghệ thông tin; so sánh trường đại học Tôn Đức Thắng và trường đại học Công nghệ thông tin**
#             Question: Em đã có bằng MOS, vậy em có được miễn môn Cơ sở tin học ở trường đại học Tôn Đức Thắng không?
#             Queries: môn cơ sở tin học ở trường đại học Tôn Đức Thắng; chứng chỉ MOS và miễn môn tại trường Tôn Đức Thắng; điều kiện miễn môn cơ sở tin học trường đại học Tôn Đức Thắng**
#                 """},
#                 {"role": "user", "content": f"Question: {question}. Queries:"}
#             ],  
#             temperature=0.2,
#         )
#         return [q.strip() for q in response.choices[0].message.content.split(";")]
#     except Exception as e:
#         # print(type())
#         print(e.args[0])
#         if "exceeded your current quota" in e.args[0] or "Incorrect API key provided" in e.args[0]:
#             list_api.pop(0)
#             rewrite(question, list_api, 0)
#         else:
#             rewrite(question, list_api, (idx+1)%len(list_api))

# def generate_answer(prompt, context, list_api=list_api, idx=0):
#     if len(list_api) == 0:
#         print("No API key left.")
#         return {"error": "No API key left."}
#     try:
#         client = openai.OpenAI(api_key=list_api[idx])
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": f"""You are a helpful assistant.\
#                 Your name is LEGALBOT.\
#                 Your job is to answer questions about law base on your knowledge and context given.\
#                 You are given a context: {context}"""},
#                 {"role": "user", "content": f"{prompt}"},
#             ],
#             temperature=0.2,
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         # print(type())
#         print(e.args[0])
#         if "exceeded your current quota" in e.args[0]:
#             list_api.pop(0)
#             generate_answer(prompt, context, list_api, 0)
#         else:
#             generate_answer(prompt, context, list_api, (idx+1)%len(list_api))