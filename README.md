# Wikipedia to epub

Convert [Simple English Wikipedia](https://simple.wikipedia.org/wiki/Main_Page) to several epubs.

Fork from [PlainTextWikipedia](https://github.com/daveshap/PlainTextWikipedia)

> 维基百科的格式似乎还是很复杂的，转出来之后有一些章节 ePub阅读器无法解析，（放弃中）

[示例 ePub 文件下载](https://github.com/theowenyoung/wikipedia-to-epub/releases)

## Usage

[Download](https://dumps.wikimedia.org/simplewiki/latest/) `simplewiki-latest-pages-articles.xml.bz2` to `simplewiki-latest-pages-articles.xml` 

Change `wiki_to_text.py` to your own path.

```bash
pip install -r REQUIREMENTS.TXT
```

```bash
python3 wiki_to_text.py
```


```bash
python3 make-epub.py
```


