#!/usr/bin/env python3
# Author: Alex Culp
# A simplified Markdown-to-HTML tool. 
# Intended for comment sections, or other size-restricted snippets of Markdown.

import re

def markdown2html(raw_post):
    '''
    Convert simple Markdown snippets to equivalent HTML.
    
    ex = 
    # This is a heading
    This is some heading text

    ## This is a subheading
    This is some subheading text

    Break <br> inserted after newlines

    Text attributes *italic*, **bold**, `monospace`, ~~strikethrough~~

    A [link](http://example.com)

    Shopping list:

       * apples
       * oranges
       * pears

    Numbered list:

       # apples
       # oranges
       # pears

    The rain---not the reign---in
    Spain.
    '''
    
    # first, must swap HTML-specific characters
    ampersand_swap = re.sub(r"&","&amp;", raw_post)
    open_tag_swap = re.sub(r"<", "&lt;", ampersand_swap)
    close_tag_swap = re.sub(r">","&gt;", open_tag_swap)
    
    # quotations
    quote_swap = re.sub(r"\"","&quot", close_tag_swap)

    # h4_swap: literal #, header_text, \n, paragraph_beneath
    header_swap = re.sub(re.compile(r"^#{1} (.+)\n(.+)$", re.M), lambda w: "<h4>{}</h4>\n{}".format(w.group(1),w.group(2)), quote_swap)
    
    # subheader_swap: literal ##, subheader_text, \n, paragraph_beneath
    subheader_swap = re.sub(re.compile(r"^#{2} (.+)\n(.+)$", re.M), lambda w: "<h5>{}</h5>\n{}".format(w.group(1),w.group(2)), header_swap)
    
    # bullet swap: (3-4 spaces(tab), literal *, space, text, \n)+, \n
    bullet_swap = re.sub(re.compile(r"(^ {3,4}\* (.+)\n?)+", re.M), lambda w: "<ul>{}</ul>".format(w.group(0)), subheader_swap)
    
    # ordered swap: (3-4 spaces(tab), literal #, space, text, \n)+, \n
    ordered_swap = re.sub(re.compile(r"(^ {3,4}\# (.+)\n?)+", re.M), lambda w: "<ol>{}</ol>".format(w.group(0)), bullet_swap)
    
    # swap internal list items with li tags
    li_swap = re.sub(re.compile(r" {3,4}[*#]{1} (.+)"), lambda w: "<li>{}</li>".format(w.group(1), ordered_swap), ordered_swap)
    
    # ***bold and italic snippets***
    bold_ital_swap = re.sub(re.compile(r"\*{3}(.+?)\*{3}", re.M), lambda w: "<strong><em>{}</strong></em>".format(w.group(1)), li_swap)
    
    # **bold snippets**
    bold_swap = re.sub(re.compile(r"\*{2}(.+?)\*{2}", re.M), lambda w: "<strong>{}</strong>".format(w.group(1)), bold_ital_swap)
    
    # italics swap
    ital_swap = re.sub(re.compile(r"\*(.+?)\*", re.M), lambda w: "<em>{}</em>".format(w.group(1)), bold_swap)
    
    # ~~strikethrough~~
    strikethrough_swap = re.sub(re.compile(r"~{2}(.+?)~{2}", re.M), lambda w: "<s>{}</s>".format(w.group(1)), ital_swap)
    
    # m o n o s p a c e (line only)
    monospace_swap = re.sub(re.compile(r"`(.+?)`", re.M), lambda w: "<code>{}</code>".format(w.group(1)), strikethrough_swap)
    
    # link swap:  [link](www.myLink.com) --> <a href="www.myLink.com">link</a>
    link_swap = re.sub(re.compile(r"\[(.+?)\]\((.+?)\)", re.M), lambda w: '<a href="{}">{}</a>'.format(w.group(2), w.group(1)), monospace_swap)
    
    # mash swap: The rain in Spain---not the reign---in Spain. --> the rain in Spain&mash;not the reign&mash;in Spain.
    br_swap = re.sub(re.compile(r"(.+)\n", re.M) ,lambda w: '{}<br>'.format(w.group(1)), link_swap)
    
    # emdash swap
    final_output = re.sub(r"-{3}(.+?)-{3}", lambda w: '&mdash;{}&mdash;'.format(w.group(1)), br_swap)
    
    return final_output
