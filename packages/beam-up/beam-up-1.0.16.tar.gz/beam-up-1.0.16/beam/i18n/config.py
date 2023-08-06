import os
import re
import sys
import logging
import traceback

from beam.config import load_config
from .helpers.hash import hash
from .helpers.yaml import yaml
from .helpers.languages import get_source_and_target_languages
from .helpers.serialize import serialize_text, deserialize_text
from .helpers.translate import cached_translate, FileCache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("")

class Skip(BaseException):
    pass

def transform_data(data, context, filters, parent_key=None):
    if isinstance(data, dict):
        for r in [0,1,2]:
            nd = {}
            for key, value in data.items():
                sv = key.split("|")
                fns = sv[1:]
                relevant_fns = []
                pipes = 0
                new_key = key
                for fn in fns:
                    if not fn: # this matched a pipe
                        pipes += 1
                        continue
                    elif pipes != r:
                        pipes = 0
                        continue
                    pipes = 0
                    relevant_fns.append(fn)
                if len(relevant_fns) == len(fns) or r == 2:
                    new_key = sv[0]
                for fn in relevant_fns:
                    if not fn in filters:
                        logger.warning(f"Skipping undefined filter {fn}...")
                        continue
                    ff = filters[fn]
                    try:
                        if isinstance(value, list):
                            new_value = []
                            for element in value:
                                new_value.append(ff(new_key, element, data, context))
                            value = new_value
                        else:
                            value = ff(new_key, value, data, context)
                    except Skip:
                        raise
                    except:
                        logger.error(f"Error processing key {key} with parent key {parent_key}")
                        raise
                nd[new_key] = value
            data = nd
        nnd = {}
        for key, value in nd.items():
            try:
                full_key = f"{parent_key}.{key}" if parent_key else key
                nnd[key] = transform_data(value, context, filters, parent_key=full_key)
            except Skip:
                pass
        return nnd
    elif isinstance(data, list):
        nd = []
        for i, element in enumerate(data):
            try:
                nd.append(transform_data(element, context, filters, parent_key=f'{i}' if not parent_key else f'{parent_key}.{i}'))
            except Skip:
                pass
        return nd
    else:
        return data

def exists(key, value, data, context):
    path = os.path.join(context["pwd"], value)
    if not os.path.exists(path):
        logger.debug(f"Skipping {path}")
        raise Skip
    return value

keymap = {
    'ä' : 'ae',
    'ö' : 'oe',
    'ü' : 'ue',
    'ß' : 'ss',    
}

def slugify(key, value, data, context):
    title = data["title"].lower().replace(" ", "-")
    for sk, dk in keymap.items():
        title = title.replace(sk, dk)
    title = re.sub(r"[^a-z\-]", "", title)
    if not title: # for 'exotic' languages like Chinese...
        return re.sub(r"[^a-z\-]", "", data["name"].lower().replace(" ", "-"))
    return title

def translate_file(token, site_path, destination_path, source_language, target_language, clean=False):
    count = 0
    source_data = load_config(site_path, with_data=False)
    cache = FileCache(site_path+".trans")

    filters = {
        't' : lambda key, value, data, context: value if source_language == target_language else deserialize_text(cached_translate(serialize_text(value), source_language, target_language, cache, token)),
        'f' : lambda key, value, data, context: value.format(**context),
        'exists?': exists,
        'id' : lambda key, value, data, context: value,
        'ld' : lambda key, value, data, context: value.get(context['target_language'], value['default']),
        'slugify': slugify,
    }

    """
    We iterate through the file, parsing the modifiers and generating a new
    config from them...
    """
    transformed_data = transform_data(source_data, {
        "source_language" : source_language,
        "target_language" : target_language,
        "pwd" : os.path.dirname(site_path),
        }, filters)
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    with open(destination_path, "w") as output_file:
        output_file.write("# Warning, this is an auto-generated file, do not modify!\n" +
                          f"# Modify this file instead: {os.path.relpath(site_path, os.path.dirname(destination_path))}\n")
        output_file.write(yaml.dump(transformed_data, indent=2, sort_keys=True, width=60))

    if clean:
        cache.clean()


def translate_config(token, src_path, clean=False):

    source_language, target_languages = get_source_and_target_languages(src_path, exclude_source=False)

    site_path = os.path.join(src_path, "site-all.yml")
    if not os.path.exists(site_path):
        logger.fatal("Master file does not exist!")
        exit(-1)
    logger.info(f"Translating file '{site_path}' from '{source_language}' to '{', '.join(target_languages)}'...")
    for target_language in target_languages:
        destination_path = os.path.join(src_path, f"site-{target_language}.yml")
        count = translate_file(token, site_path, destination_path, source_language, target_language, clean=clean)
        if count:
            logger.info(f"Translated {count} characters in file {site_path}")
