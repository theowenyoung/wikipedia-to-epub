from threading import Thread
import os
import json
import re
from html2text import html2text as htt
import wikitextparser as wtp
from markdownify import markdownify as md
from wikimarkup.parser import BaseParser

def wikipediaLinkHook(parser_env, namespace, body):
    # namespace is going to be 'Wikipedia'
    (article, pipe, text) = body.partition('|')
    href = article.strip().capitalize().replace(' ', '_')
    text = (text or article).strip()
    return '%s' % (text)

def dewiki(text):

    # parser = BaseParser()
    # parser.registerInternalLinkHook('*', wikipediaLinkHook)
    # text = parser.parse(text)
    text = wtp.parse(text).plain_text()  # wiki to plaintext
    # text = htt(text)  # remove any HTML
    # text = text.replace('\\n',' ')  # replace newlines
    # text = re.sub('\s+', ' ', text)  # replace excess whitespace
    # replace \n with <br />
    # replace greater than 2 newline with 2 newline
    # remove line text start thumb|
    text = re.sub('thumb\|.*\n', '', text)

    text = re.sub('\n{2,}', '\n\n', text)
    text = text.replace('\n', '<br />')


    return text


def analyze_chunk(text):
    try:
        if '<redirect title="' in text:  # this is not the main article
            return None
        if '(disambiguation)' in text:  # this is not an article
            return None
        else:
            title = text.split('<title>')[1].split('</title>')[0]
            title = htt(title)
            if ':' in title:  # most articles with : in them are not articles we care about
                return None
        serial = text.split('<id>')[1].split('</id>')[0]
        content = text.split('</text')[0].split('<text')[1].split('>', maxsplit=1)[1]
        content = dewiki(content)
        return {'title': title.strip(), 'text': content.strip(), 'id': serial.strip()}
    except Exception as oops:
        print(oops)
        return None


def save_article(article, savedir):
    doc = analyze_chunk(article)
    if doc:
        print('SAVING:', doc['title'])
        filename = doc['id'] + '.json'
        with open(savedir + filename, 'w', encoding='utf-8') as outfile:
            json.dump(doc, outfile, sort_keys=True, indent=1, ensure_ascii=False)



def process_file_text(filename, savedir):
    article = ''
    counter = 0  # initialize counter

    # check is savedir exists, if not create it
    if not os.path.exists(savedir):
        os.makedirs(savedir)


    # remove all files inthe savedir
    for file in os.listdir(savedir):
        # print file name
        # print("File Name : ",savedir, file)
        os.remove(savedir + file)

    with open(filename, 'r', encoding='utf-8') as infile:
        for line in infile:
            if '<page>' in line:
                article = ''
            elif '</page>' in line:  # end of article
                counter += 1  # increment counter each time an article is processed
                Thread(target=save_article, args=(article, savedir)).start()
                # if counter >= 3:  # if 3 articles have been processed, break the loop
                #     break
            else:
                article += line
