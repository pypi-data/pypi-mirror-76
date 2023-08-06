from nornir.core.task import Task, Result
from netnir.helpers import merge_two_dicts
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from typing import Any


def template_file(
    task: Task, template_file: str, jinja_filters: dict = {}, **kwargs: Any,
) -> Result:
    """compile a jinja2 template and write it to a file.

    :param task: nornir task object
    :param template_file: template file name
    :param jinja_filters: jinja2 filters
    :param kwargs: key/value pairs to render templates

    :returns: nornir result object
    """
    template_path = task.host.data["template_path"]
    env = Environment(
        loader=FileSystemLoader(template_path),
        undefined=StrictUndefined,
        trim_blocks=True,
        autoescape=True,
    )
    env.filters.update(jinja_filters)
    template = env.get_template(template_file)
    merged_dicts = merge_two_dicts(kwargs, task.host)
    result = template.render(**merged_dicts)

    return Result(host=task.host, result=result)
