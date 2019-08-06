from os.path import dirname, realpath, basename, isfile
from os.path import join as join_path
import glob
import importlib.util

from jinja2 import Environment, FileSystemLoader, select_autoescape

from unix_colors import unixnify

TEMPLATES_PATH = join_path(dirname(realpath(__file__)), 'howto_templates')


def load_howto_codes(howto_codes_path):
    glob_path = join_path(glob.escape(howto_codes_path), '*')
    return {
        basename(file_path): unixnify(file_path)
        for file_path in glob.glob(glob_path)
        if isfile(file_path)
    }


def load_howto(howto_path, title):
    template_paths = [
        howto_path, 
        TEMPLATES_PATH,
    ]
    env = Environment(
        loader=FileSystemLoader(template_paths),
        autoescape=select_autoescape(['html', 'xml'])
    )

    howto_codes_path = join_path(howto_path, 'codes')
    howto_template = env.get_template('howto.html')

    return howto_template.render(
        title=title, 
        codes=load_howto_codes(howto_codes_path),
    )


def load_module(task_path):
    task_spec = importlib.util.spec_from_file_location('task', task_path)
    task_module = importlib.util.module_from_spec(task_spec)
    task_spec.loader.exec_module(task_module)
