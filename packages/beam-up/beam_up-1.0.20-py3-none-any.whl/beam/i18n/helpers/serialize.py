import re
import base64

def serialize_code(match):
    """
    We retain the original value inside because it can provide meaningful context
    to the translation API. However, we ignore the translated value.
    """
    return f"<code>{match.group(1)}</code>"

def serialize_ignore(match):
    # brackets don't match
    if not len(match.group(1)) == len(match.group(3)):
        return match.group(0)
    bi = base64.urlsafe_b64encode(match.group(0).encode("utf-8")).decode("ascii")
    return f"<ignore v=\"{bi}\" />"

def deserialize_ignore(match):
    bs = base64.urlsafe_b64decode(match.group(1)).decode("utf-8")
    return bs

def serialize_md_link(match):
    if len(match.groups()) == 2:
        bi = base64.urlsafe_b64encode(match.group(2).encode("utf-8")).decode("ascii")
        return f"<md-link href=\"{bi}\">{match.group(1)}</md-link>"
    else:
        return f"<md-link>{match.group(1)}</md-link>"

def deserialize_md_link(match):
    if len(match.groups()) == 2:
        bs = base64.urlsafe_b64decode(match.group(1)).decode("utf-8")
        return f"[{match.group(2)}]({bs})"
    else:
        return f"[{match.group(1)}]"
    return bs


def deserialize_text(text):
    """
    Undoes what the serialization did below.
    """

    # sometimes space after HTML tags gets removed, we fix that here
    text = re.sub(r"</([a-zA-Z\-]+)>([^$\.\;\<\n\s])", "</\\1> \\2", text)

    text = re.sub(r"<md-heading\s+v=\"(.*?)\"\s*>(.*?)</md-heading>", "\\1 \\2", text)
    text = re.sub(r"<md-list\s+v=\"(.*?)\"\s*>(.*?)</md-list>", "\\1 \\2", text)
    text = re.sub(r"<md-it>(.*?)</md-it>", "*\\1*", text)
    text = re.sub(r"<md-strong>(.*?)</md-strong>", "**\\1**", text)
    text = re.sub(r"<md-strong-it>(.*?)</md-strong-it>", "***\\1***", text)
    text = re.sub(r"<md-link\s+href=\"(.*?)\"\s*>(.*?)</md-link>", deserialize_md_link, text)
    text = re.sub(r"<md-link>(.*?)</md-link>", deserialize_md_link, text)
    # ignore needs to be deserialized last, as it can occur encoded e.g. in a
    # markdown link that was converted itself...
    text = re.sub(r"<ignore\s+v=\"(.*?)\"\s*/>", deserialize_ignore, text)
    text = text.replace("&amp;", "&")
    return text

def serialize_text(text):
    """
    Serializes text so that DeepL can effectively translate it.

    Currently, this replaces both common Markdown directives and some Jinja
    directives that might get in the way of a proper translation.
    """
    # ignore Jinja filters and JS/Python styled string formatting directives
    replaced_text = ""
    remaining_text = text
    while remaining_text:
        # this is a really simple HTML tag detector. It assumes that no
        # unescaped '<' characters occur in the source code, which is usually
        # a reasonable assumption. This is not a standard-compliant HTML parser!
        match = re.match(r"^([^<]*?)((?!\\)<.*?(?!\\)>)", remaining_text)
        if match:
            plaintext = match.group(1)
            html = match.group(2)
            if plaintext:
                replaced_text += serialize_plaintext(plaintext)
            replaced_text += html
            remaining_text = remaining_text[len(match.group(0)):]
        else:
            replaced_text += serialize_plaintext(remaining_text)
            break
    return replaced_text

def serialize_plaintext(text):
    # we ignore everything inside backticks
    text = re.sub(r"`(.*?)`", serialize_code, text)
    # we ignore everything inside unescaped brackets ({...})
    text = re.sub(r"((?:(?!\\)\{)+)(.*?)((?:(?!\\)\})+)", serialize_ignore, text)
    # we replace Markdown headings
    text = re.sub(r"^(\#+)\s*(.+?)(\n|$)", "<md-heading v=\"\\1\">\\2</md-heading>\\3", text, re.MULTILINE)
    # we replace Markdown list elements
    text = re.sub(r"^(\s*\*|\-|\d+\.)\s+(.+?)(\n|$)", "<md-list v=\"\\1\">\\2</md-list>\\3", text, re.MULTILINE)
    # we replace strong, italicized and strong italicized text
    text = re.sub(r"(?:(?![\\])\*){3}([^\*\n]+)(?:(?![\\])\*){3}", "<md-strong-it>\\1</md-strong-it>", text)
    text = re.sub(r"(?:(?![\\])\*){2}([^\*\n]+)(?:(?![\\])\*){2}", "<md-strong>\\1</md-strong>", text)
    text = re.sub(r"(?:(?![\\])\*){1}([^\*\n]+)(?:(?![\\])\*){1}", "<md-it>\\1</md-it>", text)

    # we replace Markdown links
    text = re.sub(r"(?!\\)\[([^\]]+?)(?!\\)\](?!\\)\(([^\)]+?)(?!\\)\)",serialize_md_link
        , text)
    text = re.sub(r"(?!\\)\[([^\]]+?)(?!\\)\]",
        serialize_md_link, text)

    return text