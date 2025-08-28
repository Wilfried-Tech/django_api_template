import html2text


def htmltotext(html: str):
    parser = html2text.HTML2Text()
    parser.strong_mark = ''
    parser.emphasis_mark = ''
    return parser.handle(html)
