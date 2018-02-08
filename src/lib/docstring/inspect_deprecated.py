import ast
import os
import re
import typing
from datetime import datetime

DEPRECATED_KEY = ':deprecated:'


class DeprecatedReport:
    def __init__(self, target: str, deprecated_date: datetime):
        self.target = target
        self.deprecated_date = deprecated_date

    def __str__(self):
        return '%s, deprecated: %s' % (self.target, self.deprecated_date)


def inspect_path(path: str) -> typing.List[DeprecatedReport]:
    deprecated_reports = []

    for item_name in os.listdir(path):
        if _is_python_file(path, item_name):
            deprecated_reports += _inspect_source_file(path, item_name)
        elif _is_directory(path, item_name):
            item_path = '/'.join([path, item_name])
            deprecated_reports += inspect_path(item_path)

    return deprecated_reports


def _is_python_file(path: str, name: str) -> bool:
    return os.path.isfile('/'.join([path, name])) and name.endswith('.py')


def _is_directory(path: str, name: str) -> bool:
    return os.path.isdir('/'.join([path, name])) and name != '__pycache__'


def _inspect_source_file(path: str, filename: str) -> typing.List[DeprecatedReport]:
    module = _parse_source_file(path, filename)

    function_defs = [node for node in module.body if isinstance(node, ast.FunctionDef)]
    class_defs = [node for node in module.body if isinstance(node, ast.ClassDef)]

    reports = []

    for function_def in function_defs:
        deprecated_date = _inspect_function_def(function_def)
        if deprecated_date is not None:
            reports.append(DeprecatedReport('/'.join([path, filename]), deprecated_date))

    for class_def in class_defs:
        for deprecated_date in _inspect_class_def(class_def):
            reports.append(DeprecatedReport('/'.join([path, filename]), deprecated_date))

    return reports


def _inspect_class_def(class_def: ast.ClassDef) -> typing.List[datetime]:
    deprecated_dates = []

    class_docstring = _parse_docstring(class_def)
    if class_docstring is not None:
        deprecated_date = _inspect_docstring(class_docstring)
        if deprecated_date is not None:
            deprecated_dates.append(deprecated_date)

    function_defs = [node for node in class_def.body if isinstance(node, ast.FunctionDef)]
    for function_def in function_defs:
        deprecated_date = _inspect_function_def(function_def)
        if deprecated_date is not None:
            deprecated_dates.append(deprecated_date)

    return deprecated_dates


def _inspect_function_def(function_def: ast.FunctionDef) -> datetime:
    docstring = _parse_docstring(function_def)
    if docstring is None:
        return None

    return _inspect_docstring(docstring)


def _inspect_docstring(docstring: str) -> datetime:
    deprecated_date = _parse_deprecated_date(docstring)
    if deprecated_date is not None and deprecated_date < datetime.now():
        return deprecated_date

    return None


def _parse_source_file(path: str, filename: str) -> ast.Module:
    with open('/'.join([path, filename])) as file:
        file_contents = file.read()

    return ast.parse(file_contents)


def _parse_deprecated_date(docstring: str) -> datetime:
    for line in docstring.split('\n'):
        if line.strip().startswith(DEPRECATED_KEY):
            match = re.search(r'(\d+\.\d+\.\d+)', docstring)
            try:
                return datetime.strptime(match.group(1), '%Y.%m.%d')
            except (ValueError, AttributeError):
                raise Exception('unparsable "deprecated" in docstring: %s' % line)

    return None


def _parse_docstring(definition: ast.stmt):
    try:
        return ast.get_docstring(definition)
    except TypeError:
        return None
