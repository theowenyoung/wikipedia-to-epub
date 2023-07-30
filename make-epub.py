import os
import json
from ebooklib import epub

# 获取所有的 json 文件
json_files = [f for f in sorted(os.listdir('./temp')) if f.endswith('.json')]

# 将文件分组，每 1000 个文件为一组, 按文件名排序，文件名 1.json, 2.json, 3.json ...

#  按文件名排序
json_files.sort(key=lambda x: int(x.split('.')[0]))

# 每 450万字符为 个文件为一组

# 用于存储分组后的文件

# read json file

currentLength = 0

# group for store every group with files
# 二维数组 group
file_groups = []
currentGroupIndex = 0
for filename in json_files:

    with open(os.path.join('./temp', filename), 'r') as f:
        data = json.load(f)

    textLength = len(data['text'])
    currentLength += textLength
    # if group[currentGroupIndex] not exist, so create it
    if len(file_groups) <= currentGroupIndex:
        file_groups.append([])

    file_groups[currentGroupIndex].append(filename)


    if currentLength > 4500000:
        print('yes ' + str(currentLength))

        currentLength = 0
        currentGroupIndex += 1











# file_groups = [json_files[x:x+3000] for x in range(0, len(json_files), 3000)]

# 打印分组信息
print('共有 {} 组文件'.format(len(file_groups)))






exit(0)
# 为每一组文件创建一本电子书
for i, group in enumerate(file_groups):
    # 创建新的电子书
    book = epub.EpubBook()

    # 设置元数据
    book.set_identifier('id123456'+str(i))
    book.set_title('Simple English Wikipedia ' + str(i))
    book.set_language('en')

    book.add_author('Owen')

    # 用于存储章节的列表
    chapters = []

    # 遍历每一组文件
    # 每3000 个文件为一组
    for filename in group:
        # 打开并读取文件
        with open(os.path.join('./temp', filename), 'r') as f:
            data = json.load(f)

        # 为每个文件创建一个章节
        chapter = epub.EpubHtml(title=data['title'], file_name='chap_' + data['id'] + '.xhtml', lang='en')
        chapter.content = u'<h1>' + data['title'] + '</h1><p>' + data['text'] + '</p>'

        # 将章节添加到书中
        book.add_item(chapter)

        # 将章节添加到章节列表中
        chapters.append(chapter)

    # 定义书的结构
    book.toc = (epub.Link(chapters[0].file_name, 'Introduction', 'intro'),
                (epub.Section('Simple English Wikipedia'), chapters))

    # 将书的结构添加到书中
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # 定义书的逻辑
    book.spine = ['nav'] + chapters

    # 写入文件
    # write to output folder
    # create if it doesn't exist
    if not os.path.exists('./output'):
        os.makedirs('./output')

    # epub.write_epub('simple' + str(i) + '.epub', book, {})
    epub.write_epub(os.path.join('./output', 'simple-english-wikiepedia-' + str(i) + '.epub'), book, {})

    print('完成创建电子书: simple-english-wikiepedia-' + str(i) + '.epub')
    # 打印大小
    print('电子书大小: {} KB'.format(os.path.getsize(os.path.join('./output', 'simple-english-wikiepedia-' + str(i) + '.epub')) / 1024))
