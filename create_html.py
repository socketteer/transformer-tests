from html_util import text_to_html, bold_first_instance


def google_search_html(query, results):
    google_html = f'''
<!DOCTYPE html>
<html>

<head>
    <title>{query} - Google Search</title>
    <link rel="shortcut icon" type="image/ico" href="images/favicon.ico" />
    <link rel="stylesheet" type="text/css" href="results.css" />
</head>

<body>
    <div id="header">
        <div id="topbar">
            <img id="searchbarimage" src="images/googlelogo.png" />
            <div id="searchbar" type="text">
                <input id="searchbartext" type="text" value="{query}" />
                <button id="searchbarmic">
                    <img src="images/x.png" />
                </button>
                <button id="searchbarbutton">
                    <svg focusable="false" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path
                            d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z">
                        </path>
                    </svg>
                </button>
            </div>

            <div id="boxesicon"></div>
            <img id="boxesicon" src="images/grid.png" />
            <img id="profileimage" src="images/profpic.jpeg" />
        </div>
        <div id="optionsbar">
            <ul id="optionsmenu1">
                <li id="optionsmenuactive">All</li>
                <li>News</li>
                <li>Videos</li>
                <li>Images</li>
                <li>Maps</li>
                <li>More</li>
            </ul>

            <ul id="optionsmenu2">
                <li>Settings</li>
                <li>Tools</li>
            </ul>
        </div>
    </div>
    <div id="searchresultsarea">
        <p id="searchresultsnumber">About 155,000 results (0.56 seconds) </p>
    '''

    for result in results:
        if len(result["title"]) < 60:
            title = result["title"]
        else:
            title = result["title"][:60] + ' ...'
        url = result["domain"] + result["url"]
        if len(url) > 85:
            url = url[:85] + ' ...'
        if len(result["preview"]) < 147:
            preview = result["date"] + " — " + result["preview"]
        else:
            preview = result["date"] + " — " + result["preview"][:147] + ' ...'
        result_html = f'''
<div class="searchresult">
    <h2>{title}</h2>
    <a>{url}</a> <button>▼</button>
    <p>{preview}</p>
</div>
        '''
        google_html += result_html
    return google_html


def sections(content):
    content['level'] = 1
    content['section'] = 1
    sections_html = ''
    for node in content["TOC"]["children"]:
        sections_html += section(node, content)
    return sections_html


def section(node, content):
    sections_html = ''
    node_url = node['title'].replace(" ", "_")
    section_html = f'''
        <h{1+content['level']}><span class="mw-headline" id="{node_url}">{node['title']}</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title={node_url}&amp;action=edit&amp;section={node['number']}" title="Edit section: {node['title']}">edit</a><span class="mw-editsection-bracket">]</span></span></h{1+content['level']}>'''
    sections_html += section_html
    if 'text' in node:
        sections_html += f'''
{text_to_html(node['text'])}'''

    if 'children' in node:
        content['level'] += 1
        for child in node['children']:
            sections_html += section(child, content)
        content['level'] -= 1
    return sections_html


def TOC_entry(node, content):
    title_url = node['title'].replace(" ", "_")
    item_html = f'''
    <li class="toclevel-{content['level']} tocsection-{content['section']}"><a href="#{title_url}"><span class="tocnumber">{node['number']}</span> <span class="toctext">{node['title']}</span></a>
    '''
    content['section'] += 1
    if 'children' in node:
        item_html += '<ul>'
        content['level'] += 1
        for child in node['children']:
            item_html += TOC_entry(child, content)
        item_html += '</ul>'
        content['level'] -= 1
    item_html += '</li>'
    return item_html


def TOC(content):

    content['level'] = 1
    content['section'] = 1
    TOC_html = '''
<div id="toc" class="toc" role="navigation" aria-labelledby="mw-toc-heading"><input type="checkbox" role="button" id="toctogglecheckbox" class="toctogglecheckbox" style="display:none" /><div class="toctitle" lang="en" dir="ltr"><h2 id="mw-toc-heading">Contents</h2><span class="toctogglespan"><label class="toctogglelabel" for="toctogglecheckbox"></label></span></div>
<ul>
'''

    for node in content["TOC"]["children"]:
        TOC_html += TOC_entry(node, content)

    TOC_html += '''
</ul>
</div>
'''
    return TOC_html


def infobox_entry(entry):
    entry_html = f"""
<tr><th scope="row">{entry['title']}</th><td><div class="plainlist"><ul>"""
    for item in entry['items']:
        entry_html += f"""<li>{item['text']}</li>"""
    entry_html += """</ul></div></td></tr"""
    return entry_html


def infobox(content):
    infobox_html = f"""<table class="infobox vcard" style="width:22em">
<tbody><tr><th colspan="2" style="text-align:center;font-size:125%;font-weight:bold">
<div class="fn" style="display:inline">{content['title']}</div></th></tr><tr><td colspan="2" style="text-align:center">"""
    if 'img' in content['infobox']:
        infobox_html += f"""
<a href="/wiki/File:{content['infobox']['img']['filename']}" class="image">
<img alt={content['infobox']['img']['filename']} src="files/{content['infobox']['img']['filename']}" decoding="async" width="220" height="270" srcset="files/{content['infobox']['img']['filename']}" data-file-width="391" data-file-height="480" /></a>
<div><div style="margin: 1ex auto;">{content['infobox']['img']['description']}<br /></div></div></td></tr>"""
    if 'entries' in content['infobox']:
        for entry in content['infobox']['entries']:
            infobox_html += infobox_entry(entry)
    infobox_html += """<tr style="display:none"><td colspan="2"></td></tr></tbody></table>"""

    return infobox_html


def references_html(content):
    references_begin = f'''
<h2><span class="mw-headline" id="References">References</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="https://en.wikipedia.org/w/index.php?title={content['url']}&amp;action=edit&amp;section=1" title="Edit section: References">edit</a><span class="mw-editsection-bracket">]</span></span></h2>
<div class="mw-references-wrap"><ol class="references">
                                '''

    for reference in content['references']:
        if 'link_title' in reference:
            ref_html = f'''
<li id="cite_note-1"><span class="mw-cite-backlink"><b><a href="#cite_ref-1" aria-label="Jump up" title="Jump up">^</a></b></span> <span class="reference-text">{reference['title']}<a rel="nofollow" class="external free" href="{reference['link_url']}">{reference['link_title']}</a></span>
</li>
                                '''
        else:
            ref_html = f'''
<li id="cite_note-2"><span class="mw-cite-backlink"><b><a href="#cite_ref-2" aria-label="Jump up" title="Jump up">^</a></b></span> <span class="reference-text">{reference['title']}</span>
</li>
                                '''
        references_begin += ref_html

    references_end = '''
</ol></div>
<p><br>
</p>'''
    return references_begin + references_end

# TODO sections, TOC, infobox
def wikipedia_html(content):
    html = f'''
<!DOCTYPE html>
<html class="client-js ve-available" dir="ltr" lang="en"><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<meta charset="UTF-8">
<title>{content['title']} - Wikipedia</title>
<link rel="stylesheet" href="files/load_002.css">
<style>
.mw-editfont-monospace{{{{font-family:monospace,monospace}}.mw-editfont-sans-serif{{{{font-family:sans-serif}}.mw-editfont-serif{{{{font-family:serif}} .mw-editfont-monospace,.mw-editfont-sans-serif,.mw-editfont-serif{{{{font-size:13px; -moz-tab-size:4;tab-size:4; }}.mw-editfont-monospace.oo-ui-textInputWidget,.mw-editfont-sans-serif.oo-ui-textInputWidget,.mw-editfont-serif.oo-ui-textInputWidget{{{{font-size:inherit}}.mw-editfont-monospace.oo-ui-textInputWidget > .oo-ui-inputWidget-input,.mw-editfont-sans-serif.oo-ui-textInputWidget > .oo-ui-inputWidget-input,.mw-editfont-serif.oo-ui-textInputWidget > .oo-ui-inputWidget-input{{{{font-size:13px}}.mw-editfont-monospace.oo-ui-textInputWidget > input.oo-ui-inputWidget-input,.mw-editfont-sans-serif.oo-ui-textInputWidget > input.oo-ui-inputWidget-input,.mw-editfont-serif.oo-ui-textInputWidget > input.oo-ui-inputWidget-input{{{{min-height:32px}}
.mw-ui-button{{{{background-color:#f8f9fa;color:#202122;display:inline-block;-webkit-box-sizing:border-box;-moz-box-sizing:border-box;box-sizing:border-box;min-width:4em;max-width:28.75em;margin:0;padding:6px 12px;border:1px solid #a2a9b1;border-radius:2px;cursor:pointer;vertical-align:middle;font-family:inherit;font-size:1em;font-weight:bold;line-height:1.28571429em;text-align:center;-webkit-appearance:none}}.mw-ui-button:visited{{{{color:#202122}}.mw-ui-button:hover{{{{background-color:#ffffff;color:#404244;border-color:#a2a9b1}}.mw-ui-button:focus{{background-color:#ffffff;color:#202122;border-color:#3366cc;box-shadow:inset 0 0 0 1px #3366cc,inset 0 0 0 2px #ffffff;outline-width:0}}.mw-ui-button:focus::-moz-focus-inner{{border-color:transparent;padding:0}}.mw-ui-button:active,.mw-ui-button.is-on{{background-color:#c8ccd1;color:#000000;border-color:#72777d;box-shadow:none}}.mw-ui-button:disabled{{background-color:#c8ccd1;color:#ffffff;border-color:#c8ccd1;cursor:default}}.mw-ui-button:disabled:hover,.mw-ui-button:disabled:active{{background-color:#c8ccd1;color:#ffffff;box-shadow:none;border-color:#c8ccd1}}.mw-ui-button:not(:disabled){{-webkit-transition:background-color 100ms,color 100ms,border-color 100ms,box-shadow 100ms;-moz-transition:background-color 100ms,color 100ms,border-color 100ms,box-shadow 100ms;transition:background-color 100ms,color 100ms,border-color 100ms,box-shadow 100ms}}.mw-ui-button.mw-ui-quiet,.mw-ui-button.mw-ui-quiet.mw-ui-progressive,.mw-ui-button.mw-ui-quiet.mw-ui-destructive{{background-color:transparent;color:#202122;border-color:transparent}}.mw-ui-button.mw-ui-quiet:hover,.mw-ui-button.mw-ui-quiet.mw-ui-progressive:hover,.mw-ui-button.mw-ui-quiet.mw-ui-destructive:hover{{background-color:transparent;color:#404244;border-color:transparent;box-shadow:none}}.mw-ui-button.mw-ui-quiet:active,.mw-ui-button.mw-ui-quiet.mw-ui-progressive:active,.mw-ui-button.mw-ui-quiet.mw-ui-destructive:active{{background-color:transparent;color:#000000;border-color:transparent}}.mw-ui-button.mw-ui-quiet:focus,.mw-ui-button.mw-ui-quiet.mw-ui-progressive:focus,.mw-ui-button.mw-ui-quiet.mw-ui-destructive:focus{{background-color:transparent;color:#202122;border-color:transparent;box-shadow:none}}.mw-ui-button.mw-ui-quiet:disabled,.mw-ui-button.mw-ui-quiet.mw-ui-progressive:disabled,.mw-ui-button.mw-ui-quiet.mw-ui-destructive:disabled,.mw-ui-button.mw-ui-quiet:disabled:hover,.mw-ui-button.mw-ui-quiet.mw-ui-progressive:disabled:hover,.mw-ui-button.mw-ui-quiet.mw-ui-destructive:disabled:hover,.mw-ui-button.mw-ui-quiet:disabled:active,.mw-ui-button.mw-ui-quiet.mw-ui-progressive:disabled:active,.mw-ui-button.mw-ui-quiet.mw-ui-destructive:disabled:active{{background-color:transparent;color:#72777d;border-color:transparent}}.mw-ui-button.mw-ui-progressive{{background-color:#3366cc;color:#fff;border:1px solid #3366cc}}.mw-ui-button.mw-ui-progressive:hover{{background-color:#447ff5;border-color:#447ff5}}.mw-ui-button.mw-ui-progressive:focus{{box-shadow:inset 0 0 0 1px #3366cc,inset 0 0 0 2px #ffffff}}.mw-ui-button.mw-ui-progressive:active,.mw-ui-button.mw-ui-progressive.is-on{{background-color:#2a4b8d;border-color:#2a4b8d;box-shadow:none}}.mw-ui-button.mw-ui-progressive:disabled{{background-color:#c8ccd1;color:#fff;border-color:#c8ccd1}}.mw-ui-button.mw-ui-progressive:disabled:hover,.mw-ui-button.mw-ui-progressive:disabled:active{{background-color:#c8ccd1;color:#fff;border-color:#c8ccd1;box-shadow:none}}.mw-ui-button.mw-ui-progressive.mw-ui-quiet{{color:#3366cc}}.mw-ui-button.mw-ui-progressive.mw-ui-quiet:hover{{background-color:transparent;color:#447ff5}}.mw-ui-button.mw-ui-progressive.mw-ui-quiet:active{{color:#2a4b8d}}.mw-ui-button.mw-ui-progressive.mw-ui-quiet:focus{{background-color:transparent;color:#3366cc}}.mw-ui-button.mw-ui-destructive{{background-color:#dd3333;color:#fff;border:1px solid #dd3333}}.mw-ui-button.mw-ui-destructive:hover{{background-color:#ff4242;border-color:#ff4242}}.mw-ui-button.mw-ui-destructive:focus{{box-shadow:inset 0 0 0 1px #dd3333,inset 0 0 0 2px #ffffff}}.mw-ui-button.mw-ui-destructive:active,.mw-ui-button.mw-ui-destructive.is-on{{background-color:#b32424;border-color:#b32424;box-shadow:none}}.mw-ui-button.mw-ui-destructive:disabled{{background-color:#c8ccd1;color:#fff;border-color:#c8ccd1}}.mw-ui-button.mw-ui-destructive:disabled:hover,.mw-ui-button.mw-ui-destructive:disabled:active{{background-color:#c8ccd1;color:#fff;border-color:#c8ccd1;box-shadow:none}}.mw-ui-button.mw-ui-destructive.mw-ui-quiet{{color:#dd3333}}.mw-ui-button.mw-ui-destructive.mw-ui-quiet:hover{{background-color:transparent;color:#ff4242}}.mw-ui-button.mw-ui-destructive.mw-ui-quiet:active{{color:#b32424}}.mw-ui-button.mw-ui-destructive.mw-ui-quiet:focus{{background-color:transparent;color:#dd3333}}.mw-ui-button.mw-ui-big{{font-size:1.3em}}.mw-ui-button.mw-ui-block{{display:block;width:100%;margin-left:auto;margin-right:auto}}input.mw-ui-button::-moz-focus-inner,button.mw-ui-button::-moz-focus-inner{{margin-top:-1px;margin-bottom:-1px}}a.mw-ui-button{{text-decoration:none}}a.mw-ui-button:hover,a.mw-ui-button:focus{{text-decoration:none}}.mw-ui-button-group > *{{min-width:48px;border-radius:0;float:left}}.mw-ui-button-group > *:first-child{{border-top-left-radius:2px;border-bottom-left-radius:2px}}.mw-ui-button-group > *:not(:first-child){{border-left:0}}.mw-ui-button-group > *:last-child{{border-top-right-radius:2px;border-bottom-right-radius:2px}}.mw-ui-button-group .is-on .button{{cursor:default}}
.mw-ui-icon{{position:relative;line-height:1.5em;min-height:1.5em;min-width:1.5em}}span.mw-ui-icon{{display:inline-block}}.mw-ui-icon.mw-ui-icon-element{{text-indent:-999px;overflow:hidden;width:3.5em;min-width:3.5em;max-width:3.5em}}.mw-ui-icon.mw-ui-icon-element:before{{left:0;right:0;position:absolute;margin:0 1em}}.mw-ui-icon.mw-ui-icon-element.mw-ui-icon-large{{width:4.625em;min-width:4.625em;max-width:4.625em;line-height:4.625em;min-height:4.625em}}.mw-ui-icon.mw-ui-icon-element.mw-ui-icon-large:before{{min-height:4.625em}}.mw-ui-icon.mw-ui-icon-before:before,.mw-ui-icon.mw-ui-icon-element:before{{background-position:50% 50%;background-repeat:no-repeat;background-size:100% auto;float:left;display:block;min-height:1.5em;content:''}}.mw-ui-icon.mw-ui-icon-before:before{{position:relative;width:1.5em;margin-right:1em}}.mw-ui-icon.mw-ui-icon-small:before{{background-size:66.67% auto}}
.cite-accessibility-label{{ top:-99999px;clip:rect(1px,1px,1px,1px); position:absolute !important;padding:0 !important;border:0 !important;height:1px !important;width:1px !important; overflow:hidden}}:target .mw-cite-targeted-backlink{{font-weight:bold}}.mw-cite-up-arrow-backlink{{display:none}}:target .mw-cite-up-arrow-backlink{{display:inline}}:target .mw-cite-up-arrow{{display:none}}
.ve-init-mw-progressBarWidget{{height:1em;overflow:hidden;margin:0 25%}}.ve-init-mw-progressBarWidget-bar{{height:1em;width:0}} .ve-init-mw-progressBarWidget{{background-color:#fff;-webkit-box-sizing:border-box;-moz-box-sizing:border-box;box-sizing:border-box;height:0.875em;border:1px solid #36c;border-radius:0.875em;box-shadow:0 1px 1px rgba(0,0,0,0.15)}}.ve-init-mw-progressBarWidget-bar{{background-color:#36c;height:0.875em}}
.rt-tooltip{{position:absolute;z-index:100;max-width:350px;background:#fff;color:#222;font-size:13px;line-height:1.5em;border:1px solid #c8ccd1;border-radius:3px;box-shadow:0 15px 45px -10px rgba(0,0,0,0.3);overflow-wrap:break-word}}.rt-tooltip.rt-tooltip-insideWindow{{z-index:110}}.rt-tooltipContent{{padding:8px 11px}}.rt-tooltip-above .rt-tooltipContent{{margin-bottom:-8px;padding-bottom:16px}}.rt-tooltip-below .rt-tooltipContent{{margin-top:-10px;padding-top:18px}}.rt-tooltipTail,.rt-tooltipTail:after{{position:absolute;width:12px;height:12px}}.rt-tooltipTail{{background:#c8ccd1;background:-webkit-linear-gradient(bottom left,#c8ccd1 50%,rgba(0,0,0,0) 50%);background:linear-gradient(to top right,#c8ccd1 50%,rgba(0,0,0,0) 50%)}}.rt-tooltipTail:after{{content:"";background:#fff;bottom:1px;left:1px}}.rt-tooltip-above .rt-tooltipTail{{-webkit-transform:rotate(-45deg);transform:rotate(-45deg);-webkit-transform-origin:100% 100%;transform-origin:100% 100%;bottom:0;left:15px}}.rt-tooltip-below .rt-tooltipTail{{-webkit-transform:rotate(135deg);transform:rotate(135deg);-webkit-transform-origin:0 0;transform-origin:0 0;top:0;left:27px}}.rt-settingsLink{{background-image:linear-gradient(transparent,transparent),url(data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22utf-8%22%3F%3E%0D%0A%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2024%2024%22%3E%0D%0A%20%20%20%20%3Cpath%20fill%3D%22%23555%22%20d%3D%22M20%2014.5v-2.9l-1.8-.3c-.1-.4-.3-.8-.6-1.4l1.1-1.5-2.1-2.1-1.5%201.1c-.5-.3-1-.5-1.4-.6L13.5%205h-2.9l-.3%201.8c-.5.1-.9.3-1.4.6L7.4%206.3%205.3%208.4l1%201.5c-.3.5-.4.9-.6%201.4l-1.7.2v2.9l1.8.3c.1.5.3.9.6%201.4l-1%201.5%202.1%202.1%201.5-1c.4.2.9.4%201.4.6l.3%201.8h3l.3-1.8c.5-.1.9-.3%201.4-.6l1.5%201.1%202.1-2.1-1.1-1.5c.3-.5.5-1%20.6-1.4l1.5-.3zM12%2016c-1.7%200-3-1.3-3-3s1.3-3%203-3%203%201.3%203%203-1.3%203-3%203z%22%2F%3E%0D%0A%3C%2Fsvg%3E);float:right;cursor:pointer;margin:-4px -4px 0 8px;height:24px;width:24px;border-radius:2px;background-position:center center;background-repeat:no-repeat;background-size:24px 24px}}.rt-settingsLink:hover{{background-color:#eee}}.rt-target{{background-color:#def}}.rt-enableSelect{{font-weight:bold}}.rt-settingsFormSeparator{{margin:0.85714286em 0}}.rt-numberInput.rt-numberInput{{width:150px}}.rt-tooltipsForCommentsField.rt-tooltipsForCommentsField.rt-tooltipsForCommentsField{{margin-top:1.64285714em}}.rt-disabledHelp{{border-collapse:collapse}}.rt-disabledHelp td{{padding:0}}.rt-disabledNote.rt-disabledNote{{vertical-align:bottom;padding-left:0.36em;font-weight:bold}}@-webkit-keyframes rt-fade-in-up{{0%{{opacity:0;-webkit-transform:translate(0,20px);-moz-transform:translate(0,20px);transform:translate(0,20px) }}100%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);transform:translate(0,0) }}}}@-moz-keyframes rt-fade-in-up{{0%{{opacity:0;-webkit-transform:translate(0,20px);-moz-transform:translate(0,20px);transform:translate(0,20px) }}100%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);transform:translate(0,0) }}}}@keyframes rt-fade-in-up{{0%{{opacity:0;-webkit-transform:translate(0,20px);-moz-transform:translate(0,20px);transform:translate(0,20px) }}100%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);transform:translate(0,0) }}}}@-webkit-keyframes rt-fade-in-down{{0%{{opacity:0;-webkit-transform:translate(0,-20px);-moz-transform:translate(0,-20px);transform:translate(0,-20px) }}100%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);transform:translate(0,0) }}}}@-moz-keyframes rt-fade-in-down{{0%{{opacity:0;-webkit-transform:translate(0,-20px);-moz-transform:translate(0,-20px);transform:translate(0,-20px) }}100%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);transform:translate(0,0) }}}}@keyframes rt-fade-in-down{{0%{{opacity:0;-webkit-transform:translate(0,-20px);-moz-transform:translate(0,-20px);transform:translate(0,-20px) }}100%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);transform:translate(0,0) }}}}@-webkit-keyframes rt-fade-out-down{{0%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);transform:translate(0,0) }}100%{{opacity:0;-webkit-transform:translate(0,20px);-moz-transform:translate(0,20px);transform:translate(0,20px) }}}}@-moz-keyframes rt-fade-out-down{{0%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);transform:translate(0,0) }}100%{{opacity:0;-webkit-transform:translate(0,20px);-moz-transform:translate(0,20px);transform:translate(0,20px) }}}}@keyframes rt-fade-out-down{{0%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);transform:translate(0,0) }}100%{{opacity:0;-webkit-transform:translate(0,20px);-moz-transform:translate(0,20px);transform:translate(0,20px) }}}}@-webkit-keyframes rt-fade-out-up{{0%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);transform:translate(0,0) }}100%{{opacity:0;-webkit-transform:translate(0,-20px);-moz-transform:translate(0,-20px);transform:translate(0,-20px) }}}}@-moz-keyframes rt-fade-out-up{{0%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);transform:translate(0,0) }}100%{{opacity:0;-webkit-transform:translate(0,-20px);-moz-transform:translate(0,-20px);transform:translate(0,-20px) }}}}@keyframes rt-fade-out-up{{0%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);transform:translate(0,0) }}100%{{opacity:0;-webkit-transform:translate(0,-20px);-moz-transform:translate(0,-20px);transform:translate(0,-20px) }}}}.rt-fade-in-up{{-webkit-animation:rt-fade-in-up 0.2s ease forwards;-moz-animation:rt-fade-in-up 0.2s ease forwards;animation:rt-fade-in-up 0.2s ease forwards }}.rt-fade-in-down{{-webkit-animation:rt-fade-in-down 0.2s ease forwards;-moz-animation:rt-fade-in-down 0.2s ease forwards;animation:rt-fade-in-down 0.2s ease forwards }}.rt-fade-out-down{{-webkit-animation:rt-fade-out-down 0.2s ease forwards;-moz-animation:rt-fade-out-down 0.2s ease forwards;animation:rt-fade-out-down 0.2s ease forwards }}.rt-fade-out-up{{-webkit-animation:rt-fade-out-up 0.2s ease forwards;-moz-animation:rt-fade-out-up 0.2s ease forwards;animation:rt-fade-out-up 0.2s ease forwards }}
@-webkit-keyframes centralAuthPPersonalAnimation{{0%{{opacity:0;-webkit-transform:translateY(-20px)}}100%{{opacity:1;-webkit-transform:translateY(0)}}}}@-moz-keyframes centralAuthPPersonalAnimation{{0%{{opacity:0;-moz-transform:translateY(-20px)}}100%{{opacity:1;-moz-transform:translateY(0)}}}}@-o-keyframes centralAuthPPersonalAnimation{{0%{{opacity:0;-o-transform:translateY(-20px)}}100%{{opacity:1;-o-transform:translateY(0)}}}}@keyframes centralAuthPPersonalAnimation{{0%{{opacity:0;transform:translateY(-20px)}}100%{{opacity:1;transform:translateY(0)}}}}.centralAuthPPersonalAnimation{{-webkit-animation-duration:1s;-moz-animation-duration:1s;-o-animation-duration:1s;animation-duration:1s;-webkit-animation-fill-mode:both;-moz-animation-fill-mode:both;-o-animation-fill-mode:both;animation-fill-mode:both;-webkit-animation-name:centralAuthPPersonalAnimation;-moz-animation-name:centralAuthPPersonalAnimation;-o-animation-name:centralAuthPPersonalAnimation;animation-name:centralAuthPPersonalAnimation}}
.uls-menu{{border-radius:2px; font-size:medium}}.uls-search,.uls-language-settings-close-block{{border-top-right-radius:2px;border-top-left-radius:2px}}.uls-language-list{{border-bottom-right-radius:2px;border-bottom-left-radius:2px}}.uls-menu.callout:before,.uls-menu.callout:after{{border-top:10px solid transparent;border-bottom:10px solid transparent;display:inline-block; top:17px;position:absolute;content:''}}.uls-menu.callout.selector-right:before{{ border-left:10px solid #c8ccd1; right:-11px}}.uls-menu.callout.selector-right:after{{ border-left:10px solid #fff; right:-10px}}.uls-menu.callout.selector-left:before{{ border-right:10px solid #c8ccd1; left:-11px}}.uls-menu.callout.selector-left:after{{ border-right:10px solid #fff; left:-10px}}.uls-ui-languages button{{margin:5px 15px 5px 0;white-space:nowrap;overflow:hidden}}.uls-search-wrapper-wrapper{{position:relative;padding-left:40px;margin-top:5px;margin-bottom:5px}}.uls-icon-back{{background:transparent url(/w/extensions/UniversalLanguageSelector/resources/images/back-grey-ltr.svg?e226b) no-repeat scroll center center;background-size:28px;height:32px;width:40px;display:block;position:absolute;left:0;border-right:1px solid #c8ccd1;opacity:0.8}}.uls-icon-back:hover{{opacity:1;cursor:pointer}}.uls-menu .uls-no-results-view .uls-no-found-more{{background-color:#fff}}.uls-menu .uls-no-results-view h3{{padding:0 28px;margin:0;color:#54595d;font-size:1em;font-weight:normal}}   .skin-vector .uls-menu{{border-color:#c8ccd1;-webkit-box-shadow:0 2px 2px 0 rgba(0,0,0,0.25);box-shadow:0 2px 2px 0 rgba(0,0,0,0.25);font-size:0.875em}}.skin-vector .uls-search{{border-bottom-color:#c8ccd1}}.skin-vector .uls-search-label{{opacity:0.51;-webkit-transition:opacity 250ms;-moz-transition:opacity 250ms;transition:opacity 250ms}}.skin-vector .uls-search-wrapper:hover .uls-search-label{{opacity:0.87}}.skin-vector .uls-filtersuggestion{{color:#72777d}}.skin-vector .uls-lcd-region-title{{color:#54595d}}
@media print{{#centralNotice{{display:none}}}}.cn-closeButton{{display:inline-block;background:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUBAMAAAB/pwA+AAAAElBMVEUAAAAQEBDPz88AAABAQEDv7+9oe1vvAAAABnRSTlMA3rLe3rJS22KzAAAARElEQVQI12PAAUIUQCSTK5BwFgIxFU1AhKECUFAYKAAioXwwBeZChMGCEGGQIFQYJohgIhQgtCEMQ7ECYTHCOciOxA4AADgJTXIb9s8AAAAASUVORK5CYII=) no-repeat;width:20px;height:20px;text-indent:20px;white-space:nowrap;overflow:hidden}}
#uls-settings-block{{background-color:#f8f9fa;border-top:1px solid #c8ccd1;padding-left:10px;line-height:1.2em;border-radius:0 0 2px 2px}}#uls-settings-block > button{{background:left top transparent no-repeat;background-size:20px auto;color:#54595d;display:inline-block;margin:8px 15px;border:0;padding:0 0 0 26px;font-size:medium;cursor:pointer}}#uls-settings-block > button:hover{{color:#202122}}#uls-settings-block > button.display-settings-block{{background-image:url(/w/extensions/UniversalLanguageSelector/resources/images/display.svg?b78f7)}}#uls-settings-block > button.input-settings-block{{background-image:url(/w/extensions/UniversalLanguageSelector/resources/images/input.svg?e7c85)}}</style><style>
.mw-mmv-overlay{{position:fixed;top:0;left:0;right:0;bottom:0;z-index:1000;background-color:#000}}body.mw-mmv-lightbox-open{{overflow-y:auto;  }}body.mw-mmv-lightbox-open #mw-page-base,body.mw-mmv-lightbox-open #mw-head-base,body.mw-mmv-lightbox-open #mw-navigation,body.mw-mmv-lightbox-open #content,body.mw-mmv-lightbox-open #footer,body.mw-mmv-lightbox-open #globalWrapper{{ display:none}}body.mw-mmv-lightbox-open > *{{ display:none}}body.mw-mmv-lightbox-open > .mw-mmv-overlay,body.mw-mmv-lightbox-open > .mw-mmv-wrapper{{display:block}}.mw-mmv-filepage-buttons{{margin-top:5px}}.mw-mmv-filepage-buttons .mw-mmv-view-expanded,.mw-mmv-filepage-buttons .mw-mmv-view-config{{display:block;line-height:inherit}}.mw-mmv-filepage-buttons .mw-mmv-view-expanded.mw-ui-icon:before{{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 1024 768%22%3E %3Cpath d=%22M851.2 71.6L690.7 232.1l-40.1-40.3-9.6 164.8 164.8-9.3-40.3-40.4L926 146.4l58.5 58.5L997.6 0 792.7 13.1%22/%3E %3Cpath d=%22M769.6 89.3H611.9l70.9 70.8 7.9 7.5m-47.1 234.6l-51.2 3 3-51.2 9.4-164.4 5.8-100.3H26.4V768h883.1V387l-100.9 5.8-165 9.4zM813.9 678H113.6l207.2-270.2 31.5-12.9L548 599.8l105.9-63.2 159.8 140.8.2.6zm95.6-291.9V228l-79.1 78.9 7.8 7.9%22/%3E %3C/svg%3E")}}.mw-mmv-filepage-buttons .mw-mmv-view-config.mw-ui-icon:before{{background-image:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 1024 768%22%3E %3Cpath d=%22M897 454.6V313.4L810.4 299c-6.4-23.3-16-45.7-27.3-65.8l50.5-71.4-99.4-100.2-71.4 50.5c-20.9-11.2-42.5-20.9-65.8-27.3L582.6-1H441.4L427 85.6c-23.3 6.4-45.7 16-65.8 27.3l-71.4-50.5-100.3 99.5 50.5 71.4c-11.2 20.9-20.9 42.5-27.3 66.6L127 313.4v141.2l85.8 14.4c6.4 23.3 16 45.7 27.3 66.6L189.6 607l99.5 99.5 71.4-50.5c20.9 11.2 42.5 20.9 66.6 27.3l14.4 85.8h141.2l14.4-86.6c23.3-6.4 45.7-16 65.8-27.3l71.4 50.5 99.5-99.5-50.5-71.4c11.2-20.9 20.9-42.5 27.3-66.6l86.4-13.6zm-385 77c-81.8 0-147.6-66.6-147.6-147.6 0-81.8 66.6-147.6 147.6-147.6S659.6 302.2 659.6 384 593.8 531.6 512 531.6z%22/%3E %3C/svg%3E");opacity:0.75}}.mw-mmv-filepage-buttons .mw-mmv-view-config.mw-ui-icon:before:hover{{opacity:1}}.mw-mmv-button{{background-color:transparent;min-width:0;border:0;padding:0;overflow-x:hidden;text-indent:-9999em}}
.ve-init-mw-tempWikitextEditorWidget{{border:0;padding:0;color:inherit;line-height:1.5em;width:100%;-moz-tab-size:4;tab-size:4; }}.ve-init-mw-tempWikitextEditorWidget:focus{{outline:0;padding:0}}.ve-init-mw-tempWikitextEditorWidget::selection{{background:rgba(109,169,247,0.5); }}
#p-lang .body ul .uls-trigger,#p-lang .pBody ul .uls-trigger{{background-image:none;padding:0}} .mw-interlanguage-selector,.mw-interlanguage-selector:active{{background-image:url(/w/extensions/UniversalLanguageSelector/resources/images/language-base20.svg?2004a);background-position:left 4px center;background-repeat:no-repeat;background-size:16px;margin:4px 0 8px;padding:4px 8px 4px 26px;font-size:13px;font-weight:normal;text-align:left;cursor:pointer}}.mw-interlanguage-selector.selector-open{{background-color:#c8ccd1}}.interlanguage-uls-menu:before,.interlanguage-uls-menu:after{{border-top:10px solid transparent;border-bottom:10px solid transparent;display:inline-block; top:17px;position:absolute;content:''}}.interlanguage-uls-menu.selector-right:before{{ border-left:10px solid #c8ccd1; right:-11px}}.interlanguage-uls-menu.selector-right:after{{ border-left:10px solid #fff; right:-10px}}.interlanguage-uls-menu.selector-left:before{{ border-right:10px solid #c8ccd1; left:-11px}}.interlanguage-uls-menu.selector-left:after{{ border-right:10px solid #fff; left:-10px}}</style><style>
.ve-activated .ve-init-mw-desktopArticleTarget-editableContent #toc,.ve-activated #siteNotice,.ve-activated .mw-indicators,.ve-activated #t-print,.ve-activated #t-permalink,.ve-activated #p-coll-print_export,.ve-activated #t-cite,.ve-deactivating .ve-ui-surface,.ve-active .ve-init-mw-desktopArticleTarget-editableContent,.ve-active .ve-init-mw-tempWikitextEditorWidget{{display:none}} .ve-activating .ve-ui-surface{{height:0;padding:0 !important; overflow:hidden}} .ve-loading #content > :not(.ve-init-mw-desktopArticleTarget-loading-overlay), .ve-activated .ve-init-mw-desktopArticleTarget-uneditableContent{{pointer-events:none;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none;opacity:0.5}}.ve-activated #firstHeading{{ -webkit-user-select:text;-moz-user-select:text;-ms-user-select:text;user-select:text;pointer-events:auto;cursor:text}}.ve-activated #firstHeading a{{ pointer-events:none}}.ve-activated #catlinks{{cursor:pointer}}.ve-activated #catlinks a{{opacity:1}}.ve-activated #content{{position:relative}} .ve-init-mw-desktopArticleTarget-loading-overlay{{position:absolute;top:1.25em;left:0;right:0;z-index:1;margin-top:-0.5em}}.ve-init-mw-desktopArticleTarget-toolbarPlaceholder{{transition:height 250ms ease;height:0; }} .oo-ui-element-hidden{{display:none !important; }}  .mw-editsection{{ unicode-bidi:-moz-isolate;unicode-bidi:-webkit-isolate;unicode-bidi:isolate}}.mw-editsection:before{{content:'\200B'}}.mw-editsection a{{white-space:nowrap}}.mw-editsection-divider{{color:#54595d}}  .ve-init-mw-desktopArticleTarget-toolbarPlaceholder{{border-bottom:1px solid #c8ccd1;box-shadow:0 1px 1px 0 rgba(0,0,0,0.1)}}.ve-init-mw-desktopArticleTarget-toolbarPlaceholder-open{{height:42px}} .ve-init-mw-desktopArticleTarget-toolbar,.ve-init-mw-desktopArticleTarget-toolbarPlaceholder{{font-size:0.875em;margin:-1.42857143em -0.57142857em 1.42857143em -0.57142857em}}.skin-vector-legacy .ve-init-mw-desktopArticleTarget-toolbar,.skin-vector-legacy .ve-init-mw-desktopArticleTarget-toolbarPlaceholder{{ margin:-1.14em -1.14em 1.14em -1.14em; }}@media screen and (min-width:982px){{.skin-vector-legacy .ve-init-mw-desktopArticleTarget-toolbar,.skin-vector-legacy .ve-init-mw-desktopArticleTarget-toolbarPlaceholder{{ margin:-1.43em -1.71em 1.43em -1.71em}}}}</style><style>
.oo-ui-icon-infoFilled,.mw-ui-icon-infoFilled:before{{background-image:url(/w/load.php?modules=ext.popups.icons&image=infoFilled&format=rasterized&lang=en&skin=vector&version=1ys7s);background-image:linear-gradient(transparent,transparent),url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3Einfo%3C/title%3E%3Cpath d=%22M10 0C4.477 0 0 4.477 0 10s4.477 10 10 10 10-4.477 10-10S15.523 0 10 0zM9 5h2v2H9zm0 4h2v6H9z%22/%3E%3C/svg%3E")}}.oo-ui-image-invert.oo-ui-icon-infoFilled,.mw-ui-icon-infoFilled-invert:before{{background-image:url(/w/load.php?modules=ext.popups.icons&image=infoFilled&variant=invert&format=rasterized&lang=en&skin=vector&version=1ys7s);background-image:linear-gradient(transparent,transparent),url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3Einfo%3C/title%3E%3Cg fill=%22%23fff%22%3E%3Cpath d=%22M10 0C4.477 0 0 4.477 0 10s4.477 10 10 10 10-4.477 10-10S15.523 0 10 0zM9 5h2v2H9zm0 4h2v6H9z%22/%3E%3C/g%3E%3C/svg%3E")}}.oo-ui-image-progressive.oo-ui-icon-infoFilled,.mw-ui-icon-infoFilled-progressive:before{{background-image:url(/w/load.php?modules=ext.popups.icons&image=infoFilled&variant=progressive&format=rasterized&lang=en&skin=vector&version=1ys7s);background-image:linear-gradient(transparent,transparent),url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3Einfo%3C/title%3E%3Cg fill=%22%2336c%22%3E%3Cpath d=%22M10 0C4.477 0 0 4.477 0 10s4.477 10 10 10 10-4.477 10-10S15.523 0 10 0zM9 5h2v2H9zm0 4h2v6H9z%22/%3E%3C/g%3E%3C/svg%3E")}}.oo-ui-icon-settings,.mw-ui-icon-settings:before{{background-image:url(/w/load.php?modules=ext.popups.icons&image=settings&format=rasterized&skin=vector&version=1ys7s);background-image:linear-gradient(transparent,transparent),url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 xmlns:xlink=%22http://www.w3.org/1999/xlink%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3Esettings%3C/title%3E%3Cg transform=%22translate%2810 10%29%22%3E%3Cpath id=%22a%22 d=%22M1.5-10h-3l-1 6.5h5m0 7h-5l1 6.5h3%22/%3E%3Cuse transform=%22rotate%2845%29%22 xlink:href=%22%23a%22/%3E%3Cuse transform=%22rotate%2890%29%22 xlink:href=%22%23a%22/%3E%3Cuse transform=%22rotate%28135%29%22 xlink:href=%22%23a%22/%3E%3C/g%3E%3Cpath d=%22M10 2.5a7.5 7.5 0 000 15 7.5 7.5 0 000-15v4a3.5 3.5 0 010 7 3.5 3.5 0 010-7%22/%3E%3C/svg%3E")}}.oo-ui-image-invert.oo-ui-icon-settings,.mw-ui-icon-settings-invert:before{{background-image:url(/w/load.php?modules=ext.popups.icons&image=settings&variant=invert&format=rasterized&skin=vector&version=1ys7s);background-image:linear-gradient(transparent,transparent),url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 xmlns:xlink=%22http://www.w3.org/1999/xlink%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3Esettings%3C/title%3E%3Cg fill=%22%23fff%22%3E%3Cg xmlns:xlink=%22http://www.w3.org/1999/xlink%22 transform=%22translate%2810 10%29%22%3E%3Cpath id=%22a%22 d=%22M1.5-10h-3l-1 6.5h5m0 7h-5l1 6.5h3%22/%3E%3Cuse transform=%22rotate%2845%29%22 xlink:href=%22%23a%22/%3E%3Cuse transform=%22rotate%2890%29%22 xlink:href=%22%23a%22/%3E%3Cuse transform=%22rotate%28135%29%22 xlink:href=%22%23a%22/%3E%3C/g%3E%3Cpath d=%22M10 2.5a7.5 7.5 0 000 15 7.5 7.5 0 000-15v4a3.5 3.5 0 010 7 3.5 3.5 0 010-7%22/%3E%3C/g%3E%3C/svg%3E")}}.oo-ui-image-progressive.oo-ui-icon-settings,.mw-ui-icon-settings-progressive:before{{background-image:url(/w/load.php?modules=ext.popups.icons&image=settings&variant=progressive&format=rasterized&skin=vector&version=1ys7s);background-image:linear-gradient(transparent,transparent),url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 xmlns:xlink=%22http://www.w3.org/1999/xlink%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E%3Ctitle%3Esettings%3C/title%3E%3Cg fill=%22%2336c%22%3E%3Cg xmlns:xlink=%22http://www.w3.org/1999/xlink%22 transform=%22translate%2810 10%29%22%3E%3Cpath id=%22a%22 d=%22M1.5-10h-3l-1 6.5h5m0 7h-5l1 6.5h3%22/%3E%3Cuse transform=%22rotate%2845%29%22 xlink:href=%22%23a%22/%3E%3Cuse transform=%22rotate%2890%29%22 xlink:href=%22%23a%22/%3E%3Cuse transform=%22rotate%28135%29%22 xlink:href=%22%23a%22/%3E%3C/g%3E%3Cpath d=%22M10 2.5a7.5 7.5 0 000 15 7.5 7.5 0 000-15v4a3.5 3.5 0 010 7 3.5 3.5 0 010-7%22/%3E%3C/g%3E%3C/svg%3E")}}
.mw-ui-icon-popups-close:before{{background-image:url(/w/load.php?modules=ext.popups.images&image=popups-close&format=rasterized&skin=vector&version=5uovv);background-image:linear-gradient(transparent,transparent),url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E %3Ctitle%3E close %3C/title%3E %3Cpath d=%22M4.34 2.93l12.73 12.73-1.41 1.41L2.93 4.35z%22/%3E %3Cpath d=%22M17.07 4.34L4.34 17.07l-1.41-1.41L15.66 2.93z%22/%3E %3C/svg%3E")}}.mw-ui-icon-preview-generic:before{{background-image:url(/w/load.php?modules=ext.popups.images&image=preview-generic&format=rasterized&lang=en&skin=vector&version=5uovv);background-image:linear-gradient(transparent,transparent),url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E %3Ctitle%3E sad face %3C/title%3E %3Cpath d=%22M2 0a2 2 0 0 0-2 2v18l4-4h14a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm4 4c1.336 0 2.007 1.617 1.06 2.56-.943.947-2.56.276-2.56-1.06A1.5 1.5 0 0 1 6 4zm8 0c1.336 0 2.007 1.617 1.06 2.56-.943.947-2.56.276-2.56-1.06A1.5 1.5 0 0 1 14 4zm-4 5c2.61 0 4.83.67 5.65 3H4.35C5.17 9.67 7.39 9 10 9z%22/%3E %3C/svg%3E")}}.mw-ui-icon-footer:before{{background-image:url(/w/load.php?modules=ext.popups.images&image=footer&format=rasterized&lang=en&skin=vector&version=5uovv);background-image:linear-gradient(transparent,transparent),url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 xmlns:xlink=%22http://www.w3.org/1999/xlink%22 width=%22230%22 height=%22179%22 viewBox=%220 0 230 179%22%3E %3Cdefs%3E %3Crect id=%22a%22 width=%22201%22 height=%2213%22 rx=%222%22/%3E %3Crect id=%22b%22 width=%22201%22 height=%22169%22 y=%2210%22 rx=%222%22/%3E %3Crect id=%22c%22 width=%2230%22 height=%222%22 x=%22135%22 y=%22158%22 rx=%221%22/%3E %3C/defs%3E %3Cg fill=%22none%22 fill-rule=%22evenodd%22%3E %3Cg transform=%22matrix%281 0 0 -1 0 13%29%22%3E %3Cuse fill=%22%23f8f9fa%22 xlink:href=%22%23a%22/%3E %3Crect width=%22199%22 height=%2211%22 x=%221%22 y=%221%22 stroke=%22%23a2a9b1%22 stroke-width=%222%22 rx=%222%22/%3E %3C/g%3E %3Cuse fill=%22%23fff%22 xlink:href=%22%23b%22/%3E %3Crect width=%22199%22 height=%22167%22 x=%221%22 y=%2211%22 stroke=%22%23a2a9b1%22 stroke-width=%222%22 rx=%222%22/%3E %3Cg opacity=%22.4%22 fill=%22%2372777d%22 transform=%22translate%2867 35%29%22%3E %3Crect width=%2273%22 height=%222%22 y=%227%22 fill=%22%23c8ccd1%22 rx=%221%22/%3E %3Crect width=%2281%22 height=%222%22 y=%2231%22 rx=%221%22/%3E %3Crect width=%2232%22 height=%222%22 y=%2285%22 rx=%221%22/%3E %3Crect width=%2273%22 height=%222%22 x=%2235%22 y=%2285%22 rx=%221%22/%3E %3Crect width=%2217%22 height=%222%22 y=%2245%22 rx=%221%22/%3E %3Crect width=%2217%22 height=%222%22 x=%2291%22 y=%2245%22 rx=%221%22/%3E %3Crect width=%2268%22 height=%222%22 x=%2220%22 y=%2245%22 rx=%221%22/%3E %3Crect width=%2217%22 height=%222%22 y=%2278%22 rx=%221%22/%3E %3Crect width=%2237%22 height=%222%22 x=%2272%22 y=%2278%22 rx=%221%22/%3E %3Crect width=%2249%22 height=%222%22 x=%2220%22 y=%2278%22 rx=%221%22/%3E %3Crect width=%2224%22 height=%222%22 x=%2284%22 y=%2231%22 rx=%221%22 transform=%22matrix%28-1 0 0 1 192 0%29%22/%3E %3Crect width=%2281%22 height=%222%22 y=%2266%22 rx=%221%22/%3E %3Crect width=%2214%22 height=%222%22 x=%2254%22 y=%2224%22 rx=%221%22/%3E %3Crect width=%2237%22 height=%222%22 x=%2271%22 y=%2224%22 rx=%221%22/%3E %3Crect width=%2251%22 height=%222%22 y=%2224%22 rx=%221%22/%3E %3Crect width=%22108%22 height=%222%22 y=%2259%22 rx=%221%22/%3E %3Crect width=%22108%22 height=%222%22 y=%2252%22 rx=%221%22/%3E %3Crect width=%22108%22 height=%222%22 y=%2292%22 rx=%221%22/%3E %3Crect width=%22108%22 height=%222%22 y=%2238%22 rx=%221%22/%3E %3Crect width=%2251%22 height=%222%22 rx=%221%22/%3E %3C/g%3E %3Crect width=%2230%22 height=%222%22 x=%2267%22 y=%22158%22 fill=%22%2372777d%22 opacity=%22.4%22 rx=%221%22/%3E %3Crect width=%2230%22 height=%222%22 x=%2299%22 y=%22158%22 fill=%22%2372777d%22 opacity=%22.4%22 rx=%221%22/%3E %3Cuse fill=%22%2336c%22 xlink:href=%22%23c%22/%3E %3Crect width=%2233%22 height=%225%22 x=%22133.5%22 y=%22156.5%22 stroke=%22%23ffc057%22 stroke-opacity=%22.447%22 stroke-width=%223%22 rx=%222.5%22/%3E %3Ccircle cx=%2234%22 cy=%2249%22 r=%2219%22 fill=%22%23eaecf0%22/%3E %3Cg fill=%22%23a2a9b1%22 transform=%22translate%285 5%29%22%3E %3Ccircle cx=%221.5%22 cy=%221.5%22 r=%221.5%22/%3E %3Ccircle cx=%226%22 cy=%221.5%22 r=%221.5%22/%3E %3Ccircle cx=%2210.5%22 cy=%221.5%22 r=%221.5%22/%3E %3C/g%3E %3Cpath stroke=%22%23ff00af%22 d=%22M174.5 159.5h54.01%22 stroke-linecap=%22square%22/%3E %3C/g%3E %3C/svg%3E")}}.mw-ui-icon-preview-disambiguation:before{{background-image:url(/w/load.php?modules=ext.popups.images&image=preview-disambiguation&format=rasterized&lang=en&skin=vector&version=5uovv);background-image:linear-gradient(transparent,transparent),url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E %3Ctitle%3E articles %3C/title%3E %3Cpath d=%22M5 0v2h11v14h2V2a2 2 0 0 0-2-2z%22/%3E %3Cpath d=%22M13 20a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2zM9 5h4v5H9zM4 5h4v1H4zm0 2h4v1H4zm0 2h4v1H4zm0 2h9v1H4zm0 2h9v1H4zm0 2h9v1H4z%22/%3E %3C/svg%3E")}}.mw-ui-icon-reference-generic:before{{background-image:url(/w/load.php?modules=ext.popups.images&image=reference-generic&format=rasterized&skin=vector&version=5uovv);background-image:linear-gradient(transparent,transparent),url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E %3Ctitle%3E reference %3C/title%3E %3Cpath d=%22M15 10l-2.78-2.78L9.44 10V1H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2z%22/%3E %3C/svg%3E")}}.mw-ui-icon-reference-book:before{{background-image:url(/w/load.php?modules=ext.popups.images&image=reference-book&format=rasterized&lang=en&skin=vector&version=5uovv);background-image:linear-gradient(transparent,transparent),url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E %3Ctitle%3E book %3C/title%3E %3Cpath d=%22M15 2a7.65 7.65 0 0 0-5 2 7.65 7.65 0 0 0-5-2H1v15h4a7.65 7.65 0 0 1 5 2 7.65 7.65 0 0 1 5-2h4V2zm2.5 13.5H14a4.38 4.38 0 0 0-3 1V5s1-1.5 4-1.5h2.5z%22/%3E %3Cpath d=%22M9 3.5h2v1H9z%22/%3E %3C/svg%3E")}}.mw-ui-icon-reference-journal:before{{background-image:url(/w/load.php?modules=ext.popups.images&image=reference-journal&format=rasterized&lang=en&skin=vector&version=5uovv);background-image:linear-gradient(transparent,transparent),url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E %3Ctitle%3E journal %3C/title%3E %3Cpath d=%22M2 18.5A1.5 1.5 0 0 0 3.5 20H5V0H3.5A1.5 1.5 0 0 0 2 1.5zM6 0v20h10a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zm7 8H8V7h5zm3-2H8V5h8z%22/%3E %3C/svg%3E")}}.mw-ui-icon-reference-news:before{{background-image:url(/w/load.php?modules=ext.popups.images&image=reference-news&format=rasterized&lang=en&skin=vector&version=5uovv);background-image:linear-gradient(transparent,transparent),url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E %3Ctitle%3E newspaper %3C/title%3E %3Cpath d=%22M5 2a2 2 0 0 0-2 2v12a1 1 0 0 1-1-1V5h-.5A1.5 1.5 0 0 0 0 6.5v10A1.5 1.5 0 0 0 1.5 18H18a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2zm1 2h11v4H6zm0 6h6v1H6zm0 2h6v1H6zm0 2h6v1H6zm7-4h4v5h-4z%22/%3E %3C/svg%3E")}}.mw-ui-icon-reference-web:before{{background-image:url(/w/load.php?modules=ext.popups.images&image=reference-web&format=rasterized&lang=en&skin=vector&version=5uovv);background-image:linear-gradient(transparent,transparent),url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22 viewBox=%220 0 20 20%22%3E %3Ctitle%3E browser %3C/title%3E %3Cpath d=%22M2 2a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2zm2 1.5A1.5 1.5 0 1 1 2.5 5 1.5 1.5 0 0 1 4 3.5zM18 16H2V8h16z%22/%3E %3C/svg%3E")}}</style><style>
@-webkit-keyframes mwe-popups-fade-in-up{{0%{{opacity:0;-webkit-transform:translate(0,20px);-moz-transform:translate(0,20px);-ms-transform:translate(0,20px);transform:translate(0,20px)}}100%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);-ms-transform:translate(0,0);transform:translate(0,0)}}}}@-moz-keyframes mwe-popups-fade-in-up{{0%{{opacity:0;-webkit-transform:translate(0,20px);-moz-transform:translate(0,20px);-ms-transform:translate(0,20px);transform:translate(0,20px)}}100%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);-ms-transform:translate(0,0);transform:translate(0,0)}}}}@keyframes mwe-popups-fade-in-up{{0%{{opacity:0;-webkit-transform:translate(0,20px);-moz-transform:translate(0,20px);-ms-transform:translate(0,20px);transform:translate(0,20px)}}100%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);-ms-transform:translate(0,0);transform:translate(0,0)}}}}@-webkit-keyframes mwe-popups-fade-in-down{{0%{{opacity:0;-webkit-transform:translate(0,-20px);-moz-transform:translate(0,-20px);-ms-transform:translate(0,-20px);transform:translate(0,-20px)}}100%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);-ms-transform:translate(0,0);transform:translate(0,0)}}}}@-moz-keyframes mwe-popups-fade-in-down{{0%{{opacity:0;-webkit-transform:translate(0,-20px);-moz-transform:translate(0,-20px);-ms-transform:translate(0,-20px);transform:translate(0,-20px)}}100%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);-ms-transform:translate(0,0);transform:translate(0,0)}}}}@keyframes mwe-popups-fade-in-down{{0%{{opacity:0;-webkit-transform:translate(0,-20px);-moz-transform:translate(0,-20px);-ms-transform:translate(0,-20px);transform:translate(0,-20px)}}100%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);-ms-transform:translate(0,0);transform:translate(0,0)}}}}@-webkit-keyframes mwe-popups-fade-out-down{{0%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);-ms-transform:translate(0,0);transform:translate(0,0)}}100%{{opacity:0;-webkit-transform:translate(0,20px);-moz-transform:translate(0,20px);-ms-transform:translate(0,20px);transform:translate(0,20px)}}}}@-moz-keyframes mwe-popups-fade-out-down{{0%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);-ms-transform:translate(0,0);transform:translate(0,0)}}100%{{opacity:0;-webkit-transform:translate(0,20px);-moz-transform:translate(0,20px);-ms-transform:translate(0,20px);transform:translate(0,20px)}}}}@keyframes mwe-popups-fade-out-down{{0%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);-ms-transform:translate(0,0);transform:translate(0,0)}}100%{{opacity:0;-webkit-transform:translate(0,20px);-moz-transform:translate(0,20px);-ms-transform:translate(0,20px);transform:translate(0,20px)}}}}@-webkit-keyframes mwe-popups-fade-out-up{{0%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);-ms-transform:translate(0,0);transform:translate(0,0)}}100%{{opacity:0;-webkit-transform:translate(0,-20px);-moz-transform:translate(0,-20px);-ms-transform:translate(0,-20px);transform:translate(0,-20px)}}}}@-moz-keyframes mwe-popups-fade-out-up{{0%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);-ms-transform:translate(0,0);transform:translate(0,0)}}100%{{opacity:0;-webkit-transform:translate(0,-20px);-moz-transform:translate(0,-20px);-ms-transform:translate(0,-20px);transform:translate(0,-20px)}}}}@keyframes mwe-popups-fade-out-up{{0%{{opacity:1;-webkit-transform:translate(0,0);-moz-transform:translate(0,0);-ms-transform:translate(0,0);transform:translate(0,0)}}100%{{opacity:0;-webkit-transform:translate(0,-20px);-moz-transform:translate(0,-20px);-ms-transform:translate(0,-20px);transform:translate(0,-20px)}}}}.mwe-popups-fade-in-up{{-webkit-animation:mwe-popups-fade-in-up 0.2s ease forwards;-moz-animation:mwe-popups-fade-in-up 0.2s ease forwards;animation:mwe-popups-fade-in-up 0.2s ease forwards}}.mwe-popups-fade-in-down{{-webkit-animation:mwe-popups-fade-in-down 0.2s ease forwards;-moz-animation:mwe-popups-fade-in-down 0.2s ease forwards;animation:mwe-popups-fade-in-down 0.2s ease forwards}}.mwe-popups-fade-out-down{{-webkit-animation:mwe-popups-fade-out-down 0.2s ease forwards;-moz-animation:mwe-popups-fade-out-down 0.2s ease forwards;animation:mwe-popups-fade-out-down 0.2s ease forwards}}.mwe-popups-fade-out-up{{-webkit-animation:mwe-popups-fade-out-up 0.2s ease forwards;-moz-animation:mwe-popups-fade-out-up 0.2s ease forwards;animation:mwe-popups-fade-out-up 0.2s ease forwards}}  #mwe-popups-settings{{z-index:1000;background:#fff;width:420px;border:1px solid #a2a9b1;box-shadow:0 2px 2px 0 rgba(0,0,0,0.25);border-radius:2px;font-size:14px}}#mwe-popups-settings header{{-webkit-box-sizing:border-box;-moz-box-sizing:border-box;box-sizing:border-box;border-bottom:1px solid #c8ccd1;position:relative;display:table;width:100%;padding:5px 7px 5px 0}}#mwe-popups-settings header > div{{display:table-cell;width:3.5em;vertical-align:middle;cursor:pointer}}#mwe-popups-settings header h1{{margin-bottom:0.6em;padding-top:0.5em;border:0;width:100%;font-family:sans-serif;font-size:18px;font-weight:bold;text-align:center}}#mwe-popups-settings .mwe-ui-icon-popups-close{{opacity:0.87;-webkit-transition:opacity 100ms;-moz-transition:opacity 100ms;transition:opacity 100ms}}#mwe-popups-settings .mwe-ui-icon-popups-close:hover{{opacity:0.73}}#mwe-popups-settings .mwe-ui-icon-popups-close:active{{opacity:1}}#mwe-popups-settings main{{display:block;width:350px;padding:32px 0 24px;margin:0 auto}}#mwe-popups-settings main p{{color:#54595d;font-size:17px;margin:16px 0 0}}#mwe-popups-settings main p:first-child{{margin-top:0}}#mwe-popups-settings main form img,#mwe-popups-settings main form input,#mwe-popups-settings main form label{{vertical-align:top}}#mwe-popups-settings main form img{{margin-right:60px}}#mwe-popups-settings main form input{{display:inline-block;margin:0 10px 0 0;padding:0}}#mwe-popups-settings main form label{{font-size:13px;display:inline-block;line-height:16px;width:300px}}#mwe-popups-settings main form label > span{{color:#000;font-size:18px;font-weight:bold;display:block;margin-bottom:5px;line-height:18px}}.mwe-popups-settings-help{{font-size:13px;font-weight:800;margin:40px;position:relative}}.mwe-popups-settings-help .mw-ui-icon:before,.mwe-popups-settings-help .mw-ui-icon{{height:140px;width:180px;max-width:none;margin:0}}.mwe-popups-settings-help p{{left:180px;bottom:20px;position:absolute}}.mwe-popups{{background:#fff;position:absolute;z-index:110;-webkit-box-shadow:0 30px 90px -20px rgba(0,0,0,0.3),0 0 1px 1px rgba(0,0,0,0.05);box-shadow:0 30px 90px -20px rgba(0,0,0,0.3),0 0 1px 1px rgba(0,0,0,0.05);padding:0;display:none;font-size:14px;line-height:20px;min-width:300px;border-radius:2px; }}.mwe-popups .mw-ui-icon{{font-size:16px}}.mwe-popups .mw-ui-icon-preview-disambiguation,.mwe-popups .mw-ui-icon-preview-generic{{{{margin:21px 0 8px 0;opacity:0.25}}.mwe-popups .mwe-popups-container{{color:#202122;margin-top:-9px;padding-top:9px;text-decoration:none}}.mwe-popups .mwe-popups-container footer{{padding:16px;margin:0;font-size:10px;position:absolute;bottom:0;left:0}}.mwe-popups .mwe-popups-extract{{margin:16px;display:block;color:#202122;text-decoration:none;position:relative;   }}.mwe-popups .mwe-popups-extract:hover{{text-decoration:none}}.mwe-popups .mwe-popups-extract:after{{content:' ';position:absolute;bottom:0;width:25%;height:20px;background-color:transparent;pointer-events:none}}.mwe-popups .mwe-popups-extract[dir='ltr']:after{{ right:0; background-image:-webkit-linear-gradient(to right,rgba(255,255,255,0),#ffffff 50%); background-image:-moz-linear-gradient(to right,rgba(255,255,255,0),#ffffff 50%); background-image:linear-gradient(to right,rgba(255,255,255,0),#ffffff 50%)}}.mwe-popups .mwe-popups-extract[dir='rtl']:after{{ left:0; background-image:-webkit-linear-gradient(to left,rgba(255,255,255,0),#ffffff 50%); background-image:-moz-linear-gradient(to left,rgba(255,255,255,0),#ffffff 50%); background-image:linear-gradient(to left,rgba(255,255,255,0),#ffffff 50%)}}.mwe-popups .mwe-popups-extract p{{margin:0}}.mwe-popups .mwe-popups-extract ul,.mwe-popups .mwe-popups-extract ol,.mwe-popups .mwe-popups-extract li,.mwe-popups .mwe-popups-extract dl,.mwe-popups .mwe-popups-extract dd,.mwe-popups .mwe-popups-extract dt{{margin-top:0;margin-bottom:0}}.mwe-popups svg{{overflow:hidden}}.mwe-popups.mwe-popups-is-tall{{width:450px}}.mwe-popups.mwe-popups-is-tall > div > a > svg{{vertical-align:middle}}.mwe-popups.mwe-popups-is-tall .mwe-popups-extract{{width:215px;height:180px;overflow:hidden;float:left}}.mwe-popups.mwe-popups-is-tall footer{{width:215px;left:0}}.mwe-popups.mwe-popups-is-not-tall{{width:320px}}.mwe-popups.mwe-popups-is-not-tall .mwe-popups-extract{{min-height:40px;max-height:140px;overflow:hidden;margin-bottom:47px;padding-bottom:0}}.mwe-popups.mwe-popups-is-not-tall footer{{width:290px}}.mwe-popups.mwe-popups-type-generic .mwe-popups-extract,.mwe-popups.mwe-popups-type-disambiguation .mwe-popups-extract{{min-height:auto;padding-top:4px;margin-bottom:60px;margin-top:0}}.mwe-popups.mwe-popups-type-generic .mwe-popups-read-link,.mwe-popups.mwe-popups-type-disambiguation .mwe-popups-read-link{{font-weight:bold;font-size:12px}}.mwe-popups.mwe-popups-type-generic .mwe-popups-extract:hover + footer .mwe-popups-read-link,.mwe-popups.mwe-popups-type-disambiguation .mwe-popups-extract:hover + footer .mwe-popups-read-link{{text-decoration:underline}}.mwe-popups.mwe-popups-no-image-pointer:before{{content:'';position:absolute;border:8px solid transparent;border-top:0;border-bottom:8px solid rgba(0,0,0,0.07000000000000001);top:-8px;left:10px}}.mwe-popups.mwe-popups-no-image-pointer:after{{content:'';position:absolute;border:11px solid transparent;border-top:0;border-bottom:11px solid #ffffff;top:-7px;left:7px}}.mwe-popups.flipped-x.mwe-popups-no-image-pointer:before{{left:auto;right:10px}}.mwe-popups.flipped-x.mwe-popups-no-image-pointer:after{{left:auto;right:7px}}.mwe-popups.mwe-popups-image-pointer:before{{content:'';position:absolute;border:9px solid transparent;border-top:0;border-bottom:9px solid #a2a9b1;top:-9px;left:9px;z-index:111}}.mwe-popups.mwe-popups-image-pointer:after{{content:'';position:absolute;border:12px solid transparent;border-top:0;border-bottom:12px solid #ffffff;top:-8px;left:6px;z-index:112}}.mwe-popups.mwe-popups-image-pointer.flipped-x:before{{content:'';position:absolute;border:9px solid transparent;border-top:0;border-bottom:9px solid #a2a9b1;top:-9px;left:293px}}.mwe-popups.mwe-popups-image-pointer.flipped-x:after{{content:'';position:absolute;border:12px solid transparent;border-top:0;border-bottom:12px solid #ffffff;top:-8px;left:290px}}.mwe-popups.mwe-popups-image-pointer .mwe-popups-extract{{padding-top:16px;margin-top:200px}}.mwe-popups.mwe-popups-image-pointer > div > a > svg{{margin-top:-8px;position:absolute;z-index:113;left:0}}.mwe-popups.flipped-x.mwe-popups-is-tall{{min-height:242px}}.mwe-popups.flipped-x.mwe-popups-is-tall:before{{content:'';position:absolute;border:9px solid transparent;border-top:0;border-bottom:9px solid #a2a9b1;top:-9px;left:420px;z-index:111}}.mwe-popups.flipped-x.mwe-popups-is-tall > div > a > svg{{margin:0;margin-top:-8px;margin-bottom:-7px;position:absolute;z-index:113;right:0}}.mwe-popups.flipped-x-y:before{{content:'';position:absolute;border:9px solid transparent;border-bottom:0;border-top:9px solid #a2a9b1;bottom:-9px;left:293px;z-index:111}}.mwe-popups.flipped-x-y:after{{content:'';position:absolute;border:12px solid transparent;border-bottom:0;border-top:12px solid #ffffff;bottom:-8px;left:290px;z-index:112}}.mwe-popups.flipped-x-y.mwe-popups-is-tall{{min-height:242px}}.mwe-popups.flipped-x-y.mwe-popups-is-tall:before{{content:'';position:absolute;border:9px solid transparent;border-bottom:0;border-top:9px solid #a2a9b1;bottom:-9px;left:420px}}.mwe-popups.flipped-x-y.mwe-popups-is-tall:after{{content:'';position:absolute;border:12px solid transparent;border-bottom:0;border-top:12px solid #ffffff;bottom:-8px;left:417px}}.mwe-popups.flipped-x-y.mwe-popups-is-tall > div > a > svg{{margin:0;margin-bottom:-9px;position:absolute;z-index:113;right:0}}.mwe-popups.flipped-y:before{{content:'';position:absolute;border:8px solid transparent;border-bottom:0;border-top:8px solid #a2a9b1;bottom:-8px;left:10px}}.mwe-popups.flipped-y:after{{content:'';position:absolute;border:11px solid transparent;border-bottom:0;border-top:11px solid #ffffff;bottom:-7px;left:7px}}.mwe-popups-is-tall polyline{{-webkit-transform:translate(0,0);-moz-transform:translate(0,0);-ms-transform:translate(0,0);transform:translate(0,0)}}.mwe-popups-is-tall.flipped-x-y polyline{{-webkit-transform:translate(0,-8px);-moz-transform:translate(0,-8px);-ms-transform:translate(0,-8px);transform:translate(0,-8px)}}.mwe-popups-is-tall.flipped-x polyline{{-webkit-transform:translate(0,8px);-moz-transform:translate(0,8px);-ms-transform:translate(0,8px);transform:translate(0,8px)}}.rtl .mwe-popups-is-tall polyline{{-webkit-transform:translate(-100%,0);-moz-transform:translate(-100%,0);-ms-transform:translate(-100%,0);transform:translate(-100%,0)}}.rtl .mwe-popups-is-tall.flipped-x-y polyline{{-webkit-transform:translate(-100%,-8px);-moz-transform:translate(-100%,-8px);-ms-transform:translate(-100%,-8px);transform:translate(-100%,-8px)}}.rtl .mwe-popups-is-tall.flipped-x polyline{{-webkit-transform:translate(-100%,8px);-moz-transform:translate(-100%,8px);-ms-transform:translate(-100%,8px);transform:translate(-100%,8px)}}@supports (clip-path:polygon(1px 1px)){{.mwe-popups.flipped-x .mwe-popups-container,.mwe-popups.flipped-x-y .mwe-popups-container{{--x2:var(--pseudo-radius);--x3:calc(100% - var(--pointer-offset) - (var(--pointer-width) / 2));--x4:calc(100% - var(--pointer-offset));--x5:calc(100% - var(--pointer-offset) + (var(--pointer-width) / 2));--x6:calc(100% - var(--pseudo-radius))}}.mwe-popups.flipped-y .mwe-popups-container,.mwe-popups.flipped-x-y .mwe-popups-container{{--y1:100%;--y2:calc(100% - var(--pointer-height));--y3:calc(100% - var(--pointer-height) - var(--pseudo-radius));--y4:var(--pseudo-radius);--y5:0;margin-bottom:-9px;margin-top:0}}.mwe-popups .mwe-popups-container{{--x1:0;--x2:var(--pseudo-radius);--x3:calc(var(--pointer-offset) - (var(--pointer-width) / 2));--x4:var(--pointer-offset);--x5:calc(var(--pointer-offset) + (var(--pointer-width) / 2));--x6:calc(100% - var(--pseudo-radius));--x7:100%;--y1:0;--y2:var(--pointer-height);--y3:calc(var(--pointer-height) + var(--pseudo-radius));--y4:calc(100% - var(--pseudo-radius));--y5:100%;padding-top:0;display:flex;background:#fff;--pseudo-radius:2px;--pointer-height:8px;--pointer-width:16px;--pointer-offset:26px;clip-path:polygon(var(--x2) var(--y2),var(--x3) var(--y2),var(--x4) var(--y1),var(--x5) var(--y2),var(--x6) var(--y2),var(--x7) var(--y3),var(--x7) var(--y4),var(--x6) var(--y5),var(--x2) var(--y5),var(--x1) var(--y4),var(--x1) var(--y3))}}.mwe-popups .mwe-popups-thumbnail{{object-fit:cover;outline:1px solid rgba(0,0,0,0.1)}}.mwe-popups.mwe-popups-is-tall{{flex-direction:row}}.mwe-popups.mwe-popups-is-tall .mwe-popups-discreet{{order:1}}.mwe-popups.mwe-popups-is-tall .mwe-popups-discreet .mwe-popups-thumbnail{{min-width:215px;height:250px}}.mwe-popups.mwe-popups-is-not-tall .mwe-popups-thumbnail{{width:320px;min-height:200px}}.mwe-popups.mwe-popups-is-not-tall .mwe-popups-container{{flex-direction:column}}.mwe-popups:before{{display:none}}.mwe-popups:after{{display:none}}.mwe-popups.mwe-popups-image-pointer .mwe-popups-extract{{margin-top:0}}}}.mwe-popups-settings-icon{{display:block;overflow:hidden;font-size:16px;width:1.5em;height:1.5em;padding:3px;float:right;margin:4px 4px 2px 4px;text-indent:-1em;border-radius:2px;opacity:0.67;-webkit-transition:background-color 100ms,opacity 100ms;-moz-transition:background-color 100ms,opacity 100ms;transition:background-color 100ms,opacity 100ms}}.mwe-popups-settings-icon:hover{{background-color:#eaecf0}}.mwe-popups-settings-icon:active{{background-color:#c8ccd1;opacity:1}}.mwe-popups .mwe-popups-title{{display:block;font-weight:bold;margin:0 16px}}#mw-content-text .reference a[href*='#'] *{{pointer-events:none}}.mwe-popups.mwe-popups-type-reference .mwe-popups-title{{margin:0 0 16px}}.mwe-popups.mwe-popups-type-reference .mw-ui-icon{{vertical-align:middle}}.mwe-popups.mwe-popups-type-reference .mw-ui-icon.mw-ui-icon-element{{min-width:1.5em;width:1.5em}}.mwe-popups.mwe-popups-type-reference .mw-ui-icon.mw-ui-icon-element:before{{margin:0}}.mwe-popups.mwe-popups-type-reference .mw-ui-icon.mw-ui-icon-reference-generic{{ margin-left:-2px}}.mwe-popups.mwe-popups-type-reference .mwe-popups-extract{{margin-right:0;margin-bottom:16px;max-height:inherit}}.mwe-popups.mwe-popups-type-reference .mwe-popups-extract .mwe-popups-scroll{{max-height:371px;overflow:auto;padding-right:16px}}.mwe-popups.mwe-popups-type-reference .mwe-popups-extract .mw-parser-output{{overflow-wrap:break-word}}.mwe-popups.mwe-popups-type-reference .mwe-popups-extract:after{{display:none}}.mwe-popups.mwe-popups-type-reference .mwe-popups-extract .mwe-popups-fade{{position:absolute;width:100%;height:20px;background-color:transparent;background-image:-webkit-linear-gradient(top,rgba(255,255,255,0),#ffffff);background-image:-moz-linear-gradient(top,rgba(255,255,255,0),#ffffff);background-image:linear-gradient(rgba(255,255,255,0),#ffffff);opacity:0;pointer-events:none;-webkit-transition:opacity 250ms ease;-moz-transition:opacity 250ms ease;transition:opacity 250ms ease}}.mwe-popups.mwe-popups-type-reference .mwe-popups-extract.mwe-popups-fade-out .mwe-popups-fade{{opacity:1}}.mwe-popups.mwe-popups-type-reference .mwe-popups-extract .mwe-collapsible-placeholder{{font-weight:bold;margin:1em 0;position:relative}}.mwe-popups.mwe-popups-type-reference .mwe-popups-extract .mwe-collapsible-placeholder .mw-ui-icon{{position:absolute}}.mwe-popups.mwe-popups-type-reference .mwe-popups-extract .mwe-collapsible-placeholder .mwe-collapsible-placeholder-label{{margin-left:2em}}.mwe-popups-overlay{{background-color:rgba(255,255,255,0.9);z-index:999;position:fixed;height:100%;width:100%;top:0;bottom:0;left:0;right:0;display:flex;justify-content:center;align-items:center}}#mwe-popups-svg{{position:absolute;top:-1000px}}</style><meta name="ResourceLoaderDynamicStyles" content="">
<link rel="stylesheet" href="files/load.css">
<meta name="generator" content="MediaWiki 1.36.0-wmf.27">
<meta name="referrer" content="origin">
<meta name="referrer" content="origin-when-crossorigin">
<meta name="referrer" content="origin-when-cross-origin">
<link rel="preconnect" href="https://upload.wikimedia.org/">
<link rel="alternate" media="only screen and (max-width: 720px)" href="https://en.m.wikipedia.org/wiki/{content['url']}">
<link rel="alternate" type="application/x-wiki" title="Edit this page" href="https://en.wikipedia.org/w/index.php?title={content['url']}&amp;action=edit">
<link rel="edit" title="Edit this page" href="https://en.wikipedia.org/w/index.php?title={content['url']}&amp;action=edit">
<link rel="apple-touch-icon" href="https://en.wikipedia.org/static/apple-touch/wikipedia.png">
<link rel="shortcut icon" href="https://en.wikipedia.org/static/favicon/wikipedia.ico">
<link rel="search" type="application/opensearchdescription+xml" href="https://en.wikipedia.org/w/opensearch_desc.php" title="Wikipedia (en)">
<link rel="EditURI" type="application/rsd+xml" href="https://en.wikipedia.org/w/api.php?action=rsd">
<link rel="license" href="https://creativecommons.org/licenses/by-sa/3.0/">
<link rel="canonical" href="https://en.wikipedia.org/wiki/{content['url']}">
<link rel="dns-prefetch" href="https://login.wikimedia.org/">
<link rel="dns-prefetch" href="https://meta.wikimedia.org/">
</head>
<body class="mediawiki ltr sitedir-ltr mw-hide-empty-elt ns-0 ns-subject mw-editable page-{content['url']} rootpage-{content['url']} skin-vector action-view skin-vector-legacy"><div id="mw-page-base" class="noprint"></div>
<div id="mw-head-base" class="noprint"></div>
<div id="content" class="mw-body" role="main">
    <a id="top"></a>
    <div id="siteNotice" class="mw-body-content"><div id="centralNotice"></div><!-- CentralNotice --></div>
    <div class="mw-indicators mw-body-content">
    </div>
    <h1 id="firstHeading" class="firstHeading" lang="en">{content['title']}</h1>
    <div id="bodyContent" class="mw-body-content">'''

    if 'infobox' in content:
        html += infobox(content)
    #html += f'''<p><b>{content['title']}</b>{text_to_html(content['introduction'], leading_break=False)}</p>'''
    html += f'''<p>{bold_first_instance(content['title'], text_to_html(content['introduction'], leading_break=False))}</p>'''
    if 'TOC' in content:
        html += TOC(content)
        html += sections(content)
    else:
        # TODO stub
        pass

    if 'references' in content:
        html += references_html(content)


#     html += '''
# </div><noscript><img src="//en.wikipedia.org/wiki/Special:CentralAutoLogin/start?type=1x1" alt="" title="" width="1" height="1" style="border: none; position: absolute;" /></noscript>
# <div class="printfooter">Retrieved from "<a dir="ltr" href="https://en.wikipedia.org/w/index.php?title=PAGE_URL&amp;oldid=991748146">https://en.wikipedia.org/w/index.php?title=PAGE_TITLE&amp;oldid=991748146</a>"</div></div>
#     <div id="catlinks" class="catlinks" data-mw="interface"><div id="mw-normal-catlinks" class="mw-normal-catlinks"><a href="https://en.wikipedia.org/wiki/Help:Category" title="Help:Category">Categories</a>: <ul>'''
#
#     if 'categories' in content:
#         for category in content['categories']:
#             cat_html = f'''
#         <li><a href="PLACEHOLDER_LINK" title="CAT_TITLE">{category}</a></li>'''
#             html += cat_html

    html += f'''
</ul></div></div>
    </div>'''
    html += ''''</div>
<div id="mw-data-after-content">
    <div class="read-more-container"></div>
</div>

<div id="mw-navigation">
    <h2>Navigation menu</h2>
    <div id="mw-head">
        <!-- Please do not use role attribute as CSS selector, it is deprecated. -->
<nav id="p-personal" class="mw-portlet mw-portlet-personal vector-menu" aria-labelledby="p-personal-label" role="navigation">
    <h3 id="p-personal-label">
        <span>Personal tools</span>
    </h3>
    <div class="vector-menu-content">
        <ul class="vector-menu-content-list"><li id="pt-anonuserpage">Not logged in</li><li id="pt-anontalk"><a href="https://en.wikipedia.org/wiki/Special:MyTalk" title="Discussion about edits from this IP address [Alt+Shift+n]" accesskey="n">Talk</a></li><li id="pt-anoncontribs"><a href="https://en.wikipedia.org/wiki/Special:MyContributions" title="A list of edits made from this IP address [Alt+Shift+y]" accesskey="y">Contributions</a></li><li id="pt-createaccount"><a href="ARTICLE_URL_CREATEACCOUNT" title="You are encouraged to create an account and log in; however, it is not mandatory">Create account</a></li><li id="pt-login"><a href="ARTICLE_URL_LOGIN" title="You're encouraged to log in; however, it's not mandatory. [Alt+Shift+o]" accesskey="o">Log in</a></li></ul>

    </div>
</nav>

        <div id="left-navigation">
            <!-- Please do not use role attribute as CSS selector, it is deprecated. -->
<nav id="p-namespaces" class="mw-portlet mw-portlet-namespaces vector-menu vector-menu-tabs" aria-labelledby="p-namespaces-label" role="navigation">
    <h3 id="p-namespaces-label">
        <span>Namespaces</span>
    </h3>
    <div class="vector-menu-content">
        <ul class="vector-menu-content-list"><li id="ca-nstab-main" class="selected"><a href="https://en.wikipedia.org/wiki/{content['url']}" title="View the content page [Alt+Shift+c]" accesskey="c">Article</a></li><li id="ca-talk"><a href="https://en.wikipedia.org/wiki/Talk:{content['url']}" rel="discussion" title="Discuss improvements to the content page [Alt+Shift+t]" accesskey="t">Talk</a></li></ul>

    </div>
</nav>

            <!-- Please do not use role attribute as CSS selector, it is deprecated. -->
<nav id="p-variants" class="mw-portlet mw-portlet-variants emptyPortlet vector-menu vector-menu-dropdown" aria-labelledby="p-variants-label" role="navigation">
    <input type="checkbox" class="vector-menu-checkbox" aria-labelledby="p-variants-label">
    <h3 id="p-variants-label">
        <span>Variants</span>
    </h3>
    <div class="vector-menu-content">
        <ul class="vector-menu-content-list"></ul>

    </div>
</nav>

        </div>
        <div id="right-navigation">
            <!-- Please do not use role attribute as CSS selector, it is deprecated. -->
<nav id="p-views" class="mw-portlet mw-portlet-views vector-menu vector-menu-tabs" aria-labelledby="p-views-label" role="navigation">
    <h3 id="p-views-label">
        <span>Views</span>
    </h3>
    <div class="vector-menu-content">
        <ul class="vector-menu-content-list"><li id="ca-view" class="selected collapsible"><a href="https://en.wikipedia.org/wiki/{content['url']}">Read</a></li><li id="ca-edit" class="collapsible"><a href="https://en.wikipedia.org/w/index.php?title={content['url']}&amp;action=edit" title="Edit this page [Alt+Shift+e]" accesskey="e">Edit</a></li><li id="ca-history" class="collapsible"><a href="https://en.wikipedia.org/w/index.php?title={content['url']}&amp;action=history" title="Past revisions of this page [Alt+Shift+h]" accesskey="h">View history</a></li></ul>

    </div>
</nav>

            <!-- Please do not use role attribute as CSS selector, it is deprecated. -->
<nav id="p-cactions" class="mw-portlet mw-portlet-cactions emptyPortlet vector-menu vector-menu-dropdown" aria-labelledby="p-cactions-label" role="navigation">
    <input type="checkbox" class="vector-menu-checkbox" aria-labelledby="p-cactions-label">
    <h3 id="p-cactions-label">
        <span>More</span>
    </h3>
    <div class="vector-menu-content">
        <ul class="vector-menu-content-list"></ul>

    </div>
</nav>

            <div id="p-search" role="search">
    <h3>
        <label for="searchInput">Search</label>
    </h3>
    <form action="/w/index.php" id="searchform">
        <div id="simpleSearch" data-search-loc="header-navigation">
            <input type="search" name="search" placeholder="Search Wikipedia" autocapitalize="sentences" title="Search Wikipedia [Alt+Shift+f]" accesskey="f" id="searchInput">
            <input type="hidden" name="title" value="Special:Search">
            <input type="submit" name="fulltext" value="Search" title="Search Wikipedia for this text" id="mw-searchButton" class="searchButton mw-fallbackSearchButton">
            <input type="submit" name="go" value="Go" title="Go to a page with this exact name if it exists" id="searchButton" class="searchButton">
        </div>
    </form>
</div>

        </div>
    </div>

<div id="mw-panel">
    <div id="p-logo" role="banner">

        <img alt="Stub icon" src="files/wikipedia.png" decoding="async" srcset="files/wikipedia.png 1.5x, files/wikipedia.png 2x" data-file-width="241" data-file-height="201" width="150" height="150">
    </div>
    <!-- Please do not use role attribute as CSS selector, it is deprecated. -->
<nav id="p-navigation" class="mw-portlet mw-portlet-navigation vector-menu vector-menu-portal portal" aria-labelledby="p-navigation-label" role="navigation">
    <h3 id="p-navigation-label">
        <span>Navigation</span>
    </h3>
    <div class="vector-menu-content">
        <ul class="vector-menu-content-list"><li id="n-mainpage-description"><a href="https://en.wikipedia.org/wiki/Main_Page" title="Visit the main page [Alt+Shift+z]" accesskey="z">Main page</a></li><li id="n-contents"><a href="https://en.wikipedia.org/wiki/Wikipedia:Contents" title="Guides to browsing Wikipedia">Contents</a></li><li id="n-currentevents"><a href="https://en.wikipedia.org/wiki/Portal:Current_events" title="Articles related to current events">Current events</a></li><li id="n-randompage"><a href="https://en.wikipedia.org/wiki/Special:Random" title="Visit a randomly selected article [Alt+Shift+x]" accesskey="x">Random article</a></li><li id="n-aboutsite"><a href="https://en.wikipedia.org/wiki/Wikipedia:About" title="Learn about Wikipedia and how it works">About Wikipedia</a></li><li id="n-contactpage"><a href="https://en.wikipedia.org/wiki/Wikipedia:Contact_us" title="How to contact Wikipedia">Contact us</a></li><li id="n-sitesupport"><a href="https://donate.wikimedia.org/wiki/Special:FundraiserRedirector?utm_source=donate&amp;utm_medium=sidebar&amp;utm_campaign=C13_en.wikipedia.org&amp;uselang=en" title="Support us by donating to the Wikimedia Foundation">Donate</a></li></ul>

    </div>
</nav>

    <!-- Please do not use role attribute as CSS selector, it is deprecated. -->
<nav id="p-interaction" class="mw-portlet mw-portlet-interaction vector-menu vector-menu-portal portal" aria-labelledby="p-interaction-label" role="navigation">
    <h3 id="p-interaction-label">
        <span>Contribute</span>
    </h3>
    <div class="vector-menu-content">
        <ul class="vector-menu-content-list"><li id="n-help"><a href="https://en.wikipedia.org/wiki/Help:Contents" title="Guidance on how to use and edit Wikipedia">Help</a></li><li id="n-introduction"><a href="https://en.wikipedia.org/wiki/Help:Introduction" title="Learn how to edit Wikipedia">Learn to edit</a></li><li id="n-portal"><a href="https://en.wikipedia.org/wiki/Wikipedia:Community_portal" title="The hub for editors">Community portal</a></li><li id="n-recentchanges"><a href="https://en.wikipedia.org/wiki/Special:RecentChanges" title="A list of recent changes to Wikipedia [Alt+Shift+r]" accesskey="r">Recent changes</a></li><li id="n-upload"><a href="https://en.wikipedia.org/wiki/Wikipedia:File_Upload_Wizard" title="Add images or other media for use on Wikipedia">Upload file</a></li></ul>

    </div>
</nav>
<!-- Please do not use role attribute as CSS selector, it is deprecated. -->
<nav id="p-tb" class="mw-portlet mw-portlet-tb vector-menu vector-menu-portal portal" aria-labelledby="p-tb-label" role="navigation">
    <h3 id="p-tb-label">
        <span>Tools</span>
    </h3>
    <div class="vector-menu-content">
        <ul class="vector-menu-content-list"><li id="t-whatlinkshere"><a href="https://en.wikipedia.org/wiki/Special:WhatLinksHere/{content['url']}" title="List of all English Wikipedia pages containing links to this page [Alt+Shift+j]" accesskey="j">What links here</a></li><li id="t-recentchangeslinked"><a href="https://en.wikipedia.org/wiki/Special:RecentChangesLinked/{content['url']}" rel="nofollow" title="Recent changes in pages linked from this page [Alt+Shift+k]" accesskey="k">Related changes</a></li><li id="t-upload"><a href="https://en.wikipedia.org/wiki/Wikipedia:File_Upload_Wizard" title="Upload files [Alt+Shift+u]" accesskey="u">Upload file</a></li><li id="t-specialpages"><a href="https://en.wikipedia.org/wiki/Special:SpecialPages" title="A list of all special pages [Alt+Shift+q]" accesskey="q">Special pages</a></li><li id="t-permalink"><a href="https://en.wikipedia.org/w/index.php?title={content['url']}&amp;oldid=991748146" title="Permanent link to this revision of this page">Permanent link</a></li><li id="t-info"><a href="https://en.wikipedia.org/w/index.php?title={content['url']}&amp;action=info" title="More information about this page">Page information</a></li><li id="t-cite"><a href="https://en.wikipedia.org/w/index.php?title=Special:CiteThisPage&amp;page={content['url']}&amp;id=991748146&amp;wpFormIdentifier=titleform" title="Information on how to cite this page">Cite this page</a></li><li id="t-wikibase"><a href="https://www.wikidata.org/wiki/Special:EntityPage/Q5503153" title="Structured data on this page hosted by Wikidata [Alt+Shift+g]" accesskey="g">Wikidata item</a></li></ul>

    </div>
</nav>
<!-- Please do not use role attribute as CSS selector, it is deprecated. -->
<nav id="p-coll-print_export" class="mw-portlet mw-portlet-coll-print_export vector-menu vector-menu-portal portal" aria-labelledby="p-coll-print_export-label" role="navigation">
    <h3 id="p-coll-print_export-label">
        <span>Print/export</span>
    </h3>
    <div class="vector-menu-content">
        <ul class="vector-menu-content-list"><li id="coll-download-as-rl"><a href="https://en.wikipedia.org/w/index.php?title=Special:DownloadAsPdf&amp;page={content['url']}&amp;action=show-download-screen" title="Download this page as a PDF file">Download as PDF</a></li><li id="t-print"><a href="https://en.wikipedia.org/w/index.php?title={content['url']}&amp;printable=yes" title="Printable version of this page [Alt+Shift+p]" accesskey="p">Printable version</a></li></ul>

    </div>
</nav>

    <!-- Please do not use role attribute as CSS selector, it is deprecated. -->
<nav id="p-lang" class="mw-portlet mw-portlet-lang vector-menu vector-menu-portal portal" aria-labelledby="p-lang-label" role="navigation"><button class="uls-settings-trigger" title="Language settings"></button>
    <h3 id="p-lang-label">
        <span>Languages</span>
    </h3>
    <div class="vector-menu-content">
        <ul class="vector-menu-content-list"><li class="interlanguage-link interwiki-de">
		'''

    if 'languages' in content:
        for language in content['languages']:
            lang_html = f'''
<li class="interlanguage-link interwiki-de"><a href="LANG_URL_PLACEHOLDER" title="{language}" hreflang="de" class="interlanguage-link-target" lang="de">{language}</a></li>
            '''
            html += lang_html

    html += f'''
</ul>
<div class="after-portlet after-portlet-lang"><span class="wb-langlinks-edit wb-langlinks-link"><a href="https://www.wikidata.org/wiki/Special:EntityPage/Q5503153#sitelinks-wikipedia" title="Edit interlanguage links" class="wbc-editpage">Edit links</a></span></div>
</div>
</nav>

</div>

</div>
<footer id="footer" class="mw-footer" role="contentinfo">
    <ul id="footer-info">
    <li id="footer-info-lastmod"> This page was last edited on 1 December 2020, at 16:52<span class="anonymous-show">&nbsp;(UTC)</span>.</li>
    <li id="footer-info-copyright">Text is available under the <a rel="license" href="https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License">Creative Commons Attribution-ShareAlike License</a><a rel="license" href="https://creativecommons.org/licenses/by-sa/3.0/" style="display:none;"></a>;
additional terms may apply.  By using this site, you agree to the <a href="https://foundation.wikimedia.org/wiki/Terms_of_Use">Terms of Use</a> and <a href="https://foundation.wikimedia.org/wiki/Privacy_policy">Privacy Policy</a>. Wikipedia® is a registered trademark of the <a href="https://www.wikimediafoundation.org/">Wikimedia Foundation, Inc.</a>, a non-profit organization.</li>
</ul>

    <ul id="footer-places">
    <li id="footer-places-privacy"><a href="https://foundation.wikimedia.org/wiki/Privacy_policy" class="extiw" title="wmf:Privacy policy">Privacy policy</a></li>
    <li id="footer-places-about"><a href="https://en.wikipedia.org/wiki/Wikipedia:About" title="Wikipedia:About">About Wikipedia</a></li>
    <li id="footer-places-disclaimer"><a href="https://en.wikipedia.org/wiki/Wikipedia:General_disclaimer" title="Wikipedia:General disclaimer">Disclaimers</a></li>
    <li id="footer-places-contact"><a href="https://en.wikipedia.org/wiki/Wikipedia:Contact_us">Contact Wikipedia</a></li>
    <li id="footer-places-mobileview"><a href="https://en.m.wikipedia.org/w/index.php?title={content['url']}&amp;mobileaction=toggle_view_mobile" class="noprint stopMobileRedirectToggle">Mobile view</a></li>
    <li id="footer-places-developers"><a href="https://www.mediawiki.org/wiki/Special:MyLanguage/How_to_contribute">Developers</a></li>
    <li id="footer-places-statslink"><a href="https://stats.wikimedia.org/#/en.wikipedia.org">Statistics</a></li>
    <li id="footer-places-cookiestatement"><a href="https://foundation.wikimedia.org/wiki/Cookie_statement">Cookie statement</a></li>
<li style="display: none;"><a href="#">Enable previews</a></li></ul>

    <ul id="footer-icons" class="noprint">
    <li id="footer-copyrightico"><a href="https://wikimediafoundation.org/"><img src="files/wikimedia-button.png" srcset="files/wikimedia-button-1.png 1.5x, files/wikimedia-button-2x.png 2x" alt="Wikimedia Foundation" loading="lazy" width="88" height="31"></a></li>
    <li id="footer-poweredbyico"><a href="https://www.mediawiki.org/"><img src="files/poweredby_mediawiki_88x31.png" alt="Powered by MediaWiki" srcset="files/poweredby_mediawiki_132x47.png 1.5x, files/poweredby_mediawiki_176x62.png 2x" loading="lazy" width="88" height="31"></a></li>
</ul>

    <div style="clear: both;"></div>
</footer>
<a accesskey="v" href="https://en.wikipedia.org/wiki/{content['url']}?action=edit" class="oo-ui-element-hidden"></a></body></html>
            '''

    return html