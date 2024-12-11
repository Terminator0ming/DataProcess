# V 23.9.16
# pip install python-docx
# V 23.9.17
# 解决图片前还有一行空白的问题，删掉了冗余代码
# V 23.9.18
# 文字素材库
# V23.9.28
# 调整：paragraph_name 每个段落都要更新

import re
from docx import Document

# 打开.docx文件
doc = Document('D:\\Research Files\\1号文件.docx')
previous_heading_level_2 = None  # 存储上一个二级标题
previous_heading_level_3 = None  # 存储上一个三级标题
previous_heading_level_4 = None  # 存储上一个四级标题

# 遍历所有段落
for paragraph in doc.paragraphs:
    paragraph_name = ''              # 记录当前段落名称
    # 读取段落的样式
    paragraph_style = paragraph.style
    # print('段落样式:', paragraph_style.name)
    # 1级标题不用动
    # 检查是否为2级标题，内容类型
    if paragraph_style.name == 'Heading 2':
        previous_heading_level_2 = paragraph.text
        print(previous_heading_level_2)

    # 检查是否为3级标题，分类标题
    if paragraph_style.name == 'Heading 3':
        previous_heading_level_3 = paragraph.text
        print(previous_heading_level_3)

    # 检查是否为4级标题，文章索引
    if paragraph_style.name == 'Heading 4':
        previous_heading_level_4 = paragraph.text
        print(previous_heading_level_4)

    ## 检查是否为图片
    if paragraph_style.name == 'Normal' and not paragraph.text.strip():
        print('图片')
        paragraph_name = 'FIG'
    elif '【' in paragraph.text:
        paragraph_name = 'TAG'
        print('标签')

    # 只处理标签
    if paragraph_name == 'TAG':
        # print('TAG:', paragraph.text)
        # 使用正则表达式查找所有的【】及其中间的内容
        matches = re.findall(r'【(.*?)】', paragraph.text)
        print('匹配到的内容:', matches)

        i = 0
        if matches[-1] =='':
            raise ValueError
        content_heads = re.compile(r"】(.*?)【").findall(paragraph.text) # 匹配除最后一句之外的
        content_end = re.compile(f"{matches[-1]}】"+r"(.*?)$").findall(paragraph.text)
        content = content_heads+content_end
        if '' in content:
            content.remove('')

        for match in matches:
            print(f'【{match}】\n【{match}】\n{previous_heading_level_4}')
            paragraph.insert_paragraph_before(f'【{match}】')
            new_paragraph = paragraph.insert_paragraph_before(f'【{match}】')
            new_paragraph.style = 'Heading 4'
            paragraph.insert_paragraph_before(previous_heading_level_4)
            # V23.9.23 更新文字素材库
            if len(content) > 0:
                paragraph.insert_paragraph_before(content[i]) # 完整段落
                # paragraph.insert_paragraph_before(re.sub(r'(?<![\,,a-z,0-9])\.','.\n',content[i])) # 分句子
            i += 1

        # V23.9.17 清除图片前的空行
        p = paragraph._element
        p.getparent().remove(p)
        paragraph._p = paragraph._element = None

# 保存修改后的结果
doc_path = 'D:\\Research Files\\2.1号文件.docx'
doc.save(doc_path)
print(f'修改后的文档已保存D:\\ResearchFiles\\2.1号文件.docx')