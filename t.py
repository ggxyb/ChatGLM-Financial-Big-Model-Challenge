import os
import shutil

# 获取所有txt文件的路径
txt_files = [os.path.join(root, file) for root, dirs, files in os.walk('/home/llm/ChatGLM-Financial-Big-Model-Challenge/financial_text/alltxt') for file in files if file.endswith('.txt')]

# 创建目标文件夹
os.makedirs('/home/llm/ChatGLM-Financial-Big-Model-Challenge/financial_text/1000_txt', exist_ok=True)

# 复制文件
for file in txt_files[:50]:
    shutil.copy(file, '/home/llm/ChatGLM-Financial-Big-Model-Challenge/financial_text/1000_txt')

