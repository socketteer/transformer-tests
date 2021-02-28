import re


def text_to_html(text, leading_break=True):
    html = ''
    paragraphs = text.split('\n')
    if leading_break:
        html += f"""<p>{paragraphs[0]}</p>"""
    else:
        html += f"""{paragraphs[0]}</p>"""
    for paragraph in paragraphs[1:]:
        html += f"""<p>{paragraph}</p>"""
    return html


# matches strings bookended by first and last word of pattern
# case insensitive
def bold_first_instance(pattern, string):
    words = pattern.split(' ')
    try:
        if len(words) > 1:
            match = re.findall(rf'(?i){words[0]}.*?{words[-1]}', string)[0]
        else:
            match = re.findall(rf'(?i){pattern}', string)[0]
    except IndexError:
        return string
    return re.sub(match, f'<b>{match}</b>', string, 1)