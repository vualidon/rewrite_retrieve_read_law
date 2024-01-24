from search_engine import rrr_snippets, rrr_pages
from datasets import load_dataset
import pandas as pd
# ds = load_dataset("thangvip/data-compare", split='train')
# ds = ds.shuffle(seed=42)
# data = {
#     "question": [],
#     "answer_bot": [],
#     "real_label": []
# }
# for index, item in enumerate(ds):
#     if index >= 500 and index < 550:
        # try:
        #     data["question"].append(item['question'])
        #     data["answer_bot"].append(rrr_pages(item['question'], n=10))
        #     data["real_label"].append(item['content'])
        # except:
        #     print("ERROR")

        # print(index)
        # print(item['question'])
        # print( item['content'])
        # print("ANSWER: \n",rrr_pages(item['question'], n=10))
        # break
question = """Tôi có thắc mắc: Người phụ trách kinh doanh dịch vụ lữ hành đã có chứng chỉ nghiệp vụ điều hành du lịch nội địa thì có thể kinh doanh dịch vụ lữ hành quốc tế hay không? (Câu hỏi của anh Quyền - Đồng Nai)"""

# data = pd.DataFrame(data)

# data.to_excel("test_result.
# xlsx", index=False)
print("ANSWER: \n",rrr_pages(question, n=10))