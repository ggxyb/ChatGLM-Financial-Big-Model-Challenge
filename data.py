from bs4 import BeautifulSoup

# 打开文件并读取内容
def read_html(filePath:str):
    print(filePath)
    with open(filePath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建一个BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser')

    balance = []
    profit = []
    cashflow = []
    # 遍历所有的标签
    # 状态1，进入财务报表
	# 状态2：找到合并资产负债表
	# 状态3：退出合并资产负债表，找寻合并利润表
	# 状态4：找到合并利润表
	# 状态5：退出合并利润表，找寻合并现金流量表
	# 状态6：找到合并现金流量表
    conditionFlag = 0
    for tag in soup.children:
        if tag.name:
            if conditionFlag == 0:
                if tag.name=="h" and len(tag.contents)>=1 and  tag.contents[0].endswith('财务报表') and len(tag.contents[0])<=8:
                    conditionFlag = 1
            elif conditionFlag == 1:
                if len(tag.contents)>=1 and '合并资产负债表' in tag.contents[0]:
                    conditionFlag = 2
            elif conditionFlag == 2:
                if tag.name=="table":
                    trs = tag.children
                    for tr in trs:
                        if tr.name:
                            tds = tr.children
                            td_list = []
                            for td in tds:
                                if td.name:
                                    td_list.append(td)
                            if len(td_list)==3:
                                balance.append((td_list[0].contents[0].replace('\n',''),td_list[1].contents[0].replace('\n','')))
                            elif len(td_list)==4:
                                balance.append((td_list[0].contents[0].replace('\n',''),td_list[2].contents[0].replace('\n','')))
                elif tag.name!="table" and len(tag.contents)>=1 and '母公司资产负债表' in tag.contents[0]:
                    conditionFlag = 3
                elif tag.name!="table" and len(tag.contents)>=1 and '合并利润表' in tag.contents[0]:
                    conditionFlag = 4
            elif conditionFlag == 3:
                if tag.name!="table" and len(tag.contents)>=1 and '合并利润表' in tag.contents[0]:
                    conditionFlag = 4
            elif conditionFlag == 4:
                if tag.name=="table":
                    trs = tag.children
                    for tr in trs:
                        if tr.name:
                            tds = tr.children
                            td_list = []
                            for td in tds:
                                if td.name:
                                    td_list.append(td)
                            if len(td_list)==3:
                                profit.append((td_list[0].contents[0].replace('\n',''),td_list[1].contents[0].replace('\n','')))
                            elif len(td_list)==4:
                                profit.append((td_list[0].contents[0].replace('\n',''),td_list[2].contents[0].replace('\n','')))
                elif tag.name!="table" and len(tag.contents)>=1 and '母公司利润表' in tag.contents[0]:
                    conditionFlag = 5
                elif tag.name!="table" and len(tag.contents)>=1 and '合并现金流量表' in tag.contents[0]:
                    conditionFlag = 6
            elif conditionFlag == 5:
                if tag.name!="table" and len(tag.contents)>=1 and '合并现金流量表' in tag.contents[0]:
                    conditionFlag = 6
            elif conditionFlag == 6:
                if tag.name=="table":
                    trs = tag.children
                    for tr in trs:
                        if tr.name:
                            tds = tr.children
                            td_list = []
                            for td in tds:
                                if td.name:
                                    td_list.append(td)
                            if len(td_list)==3:
                                cashflow.append((td_list[0].contents[0].replace('\n',''),td_list[1].contents[0].replace('\n','')))
                            elif len(td_list)==4:
                                cashflow.append((td_list[0].contents[0].replace('\n',''),td_list[2].contents[0].replace('\n','')))
                elif tag.name!="table" and len(tag.contents)>=1 and '母公司现金流量表' in tag.contents[0]:
                    conditionFlag = 7
                    break
                elif tag.name!="table" and len(tag.contents)>=1 and '合并所有者权益变动表' in tag.contents[0]:
                    conditionFlag = 8
                    break
    return balance,profit,cashflow
            
# html_path= '/home/llm/ChatGLM-Financial-Big-Model-Challenge/financial_text/html/2022-06-25__龙星化工股份有限公司__002442__龙星化工__2019年__年度报告.html'
# read_html(html_path)
# # read_html('/home/llm/ChatGLM-Financial-Big-Model-Challenge/FinanceChatGLM/data_extract/数据处理过程目录/html结果/2020-01-23__浙江海翔药业股份有限公司__002099__海翔药业__2019年__年度报告.html')

import os

html_path = '/home/llm/ChatGLM-Financial-Big-Model-Challenge/financial_text/html/'
# 输出的文件位置
out_dir = "/home/llm/ChatGLM-Financial-Big-Model-Challenge/financial_text/html_result/"

finish_path = out_dir
finish_files = os.listdir(finish_path)
finish_names=[]
for file in finish_files:
    file = file.replace(".txt_balance.txt","")
    file = file.replace(".txt_profit.txt","")
    file = file.replace(".txt_cashflow.txt","")
    if file not in finish_names:
        finish_names.append(file)



html_files = os.listdir(html_path)
html_names = []
for file in html_files:
    file = file.replace(".html","")
    if file not in finish_names:
        html_names.append(file)




for name in html_names:
    balance,profit,cashflow = read_html(html_path+"/"+name+".html")
    with open(out_dir+name+".txt_balance.txt", 'w') as f:
        for t in balance:
            try:
                f.write(t[0]+'\001'+t[1]+'\n')
            except:
                continue
    with open(out_dir+name+".txt_profit.txt", 'w') as f:
        for t in profit:
            try:
                f.write(t[0]+'\001'+t[1]+'\n')
            except:
                continue
    with open(out_dir+name+".txt_cashflow.txt", 'w') as f:
        for t in cashflow:
            try:
                f.write(t[0]+'\001'+t[1]+'\n')
            except:
                continue