import os
import yaml
import pypandoc
import random
import string
import re

from .tell import tell
from .parse import _parse, ParserState
from .chunks import YAMLDataChunk, MarkdownChunk, HTMLChunk
from .core import _parse, cast, arrange_assides
from .figure import Figure
from .button import Button
from .video import Video
from .lines import Lines
from .hint import Hint
from .code import Code
from .table import Table

def transform_page_to_html(lines, template, filepath, abort_draft):
    chunks = _parse(lines, filepath)
    chunks = cast(chunks)
    chunks = arrange_assides(chunks)

    content = []
    content.append('<div class="page">')
    if len(chunks)==0:
        pass
    else:
        first_chunk = chunks[0]
        if isinstance(first_chunk, MarkdownChunk) and not first_chunk.is_section:
            content.append('    <section class="content">')

    for chunk in chunks:
        if 'status' in chunk.page_variables and abort_draft and chunk.page_variables['status'] == 'draft':
            content.append('<mark>This site is under construction.</mark>')
            break
        if isinstance(chunk, YAMLDataChunk):
            pass
        elif isinstance(chunk, MarkdownChunk):
            if chunk.is_section:
                # open a new section
                content.append('    </section>')
                content.append('    <section class="content">')
            content.append(chunk.to_html())
            for aside in chunk.asides:
                content.append(aside.to_html())
        else:
            content.append(chunk.to_html())
            for aside in chunk.asides:
                content.append(aside.to_html())

    content.append('    </section>')
    content.append('</div>')
    content = '\n'.join(content)
    parameters = {'content': content}
    html = template.format(**parameters)
    return html

def _create_target(source_file_path, target_file_path, template_file_path, overwrite):
    if not os.path.isfile(target_file_path):
        return True
    if overwrite:
        return True
    if not os.path.isfile(template_file_path):
        return os.path.getmtime(target_file_path) < os.path.getmtime(source_file_path)
    else:
        return os.path.getmtime(target_file_path) < os.path.getmtime(source_file_path) or os.path.getmtime(target_file_path) < os.path.getmtime(template_file_path)

def write_file(html, target_file_path):
    encoding = 'utf-8'
    try:
        with open(target_file_path, "w", encoding=encoding) as html_file:
            html_file.write(html)
    except UnicodeEncodeError as error:
        tell('Encoding error when writing file {}.'.format(target_file_path))
        character = error.object[error.start:error.end]
        line = html.count("\n",0,error.start)+1
        tell('Character {} in line {} cannot be saved with encoding {}.'.format(character, line, encoding))
        with open(target_file_path, "w", encoding=encoding, errors='ignore') as html_file:
            html_file.write(html)

def process_file(source_file_path, target_file_path, template, abort_draft):
     with open(source_file_path, 'r', encoding='utf-8') as file:
          lines = file.readlines()
          tell('{}'.format(source_file_path), 'info')
          html = transform_page_to_html(lines, template, source_file_path, abort_draft)
          write_file(html, target_file_path)

def default_html_template():
    html = []
    html.append('<head><title></title></head>')
    html.append('<body>')
    html.append('{content}')
    html.append('</body>')
    html.append('</html>')
    return '\n'.join(html)

def load_html_template(template_path):
    try:
        with open(template_path, 'r', encoding='utf-8', errors="surrogateescape") as templatefile:
            template = templatefile.read()
            tell('Loading template {}.'.format(template_path), 'info')
            return template
    except FileNotFoundError:
        tell('Template file missing. Expected at {}. Using default template.'.format(template_path), 'warn')
        return default_html_template()

def build_html(input_path, output_path, template_file, rebuild_all_pages = True, abort_draft = True, verbose=False):
    #global LOG_VERBOSE
    LOG_VERBOSE = verbose
    template = load_html_template(template_file)
    for filename in os.listdir(input_path):
        source_file_path = os.path.join(input_path, filename)
        if os.path.isfile(source_file_path) and filename.endswith('.md'):
            target_file_name = os.path.splitext(os.path.basename(filename))[0] + '.html'
            target_file_path = os.path.join(output_path, target_file_name)
            if _create_target(source_file_path, target_file_path, template_file, rebuild_all_pages):
                process_file(source_file_path, target_file_path, template, abort_draft)