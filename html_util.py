
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