from dewiki_functions import *
import os

#wiki_xml_file = 'F:/simplewiki-20210401/simplewiki-20210401.xml'  # update this
wiki_xml_file = '/Users/green/inbox/PlainTextWikipedia/data/simplewiki-latest-pages-articles.xml'  # update this
json_save_dir = '/Users/green/inbox/PlainTextWikipedia/temp/'

if __name__ == '__main__':
    # create temp dir if not exist
    if not os.path.exists(json_save_dir):
        os.makedirs(json_save_dir)

    process_file_text(wiki_xml_file, json_save_dir)
