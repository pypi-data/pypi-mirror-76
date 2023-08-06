import os
import click
import json
import yaml
from fastutils import dictutils
from fastutils import strutils

class Null(object):
    pass
Null = Null()

def isNull(value):
    return value == Null

def load_json_data(input):
    if input == "-":
        data = json.load(os.sys.stdin)
    elif os.path.exists(input) and os.path.isfile(input):
        with open(input, "rb") as fobj:
            data = json.load(fobj)
    else:
        print("File {} not exists...".format(input), file=os.sys.stderr)
        os.sys.exit(1)
    return data

def load_yaml_data(input):
    if input == "-":
        data = yaml.safe_load(os.sys.stdin)
    elif os.path.exists(input) and os.path.isfile(input):
        with open(input, "rb") as fobj:
            data = yaml.safe_load(fobj)
    else:
        print("File {} not exists...".format(input), file=os.sys.stderr)
        os.sys.exit(1)
    return data

def get(data, path):
    result = dictutils.select(data, path, Null)
    return result


def get_output(value, keep_quote):
    output = json.dumps(value)
    if not keep_quote:
        output = strutils.unquote(output)
    return output

@click.group()
def main():
    pass


@main.group(name="json")
def json_tools():
    "Json tools"
    pass

@main.group(name="yaml")
def yaml_tools():
    "Yaml tools"
    pass


@json_tools.command(name="get")
@click.option("-i", "--input", default="-")
@click.option("-q", "--keep-quote", is_flag=True)
@click.argument("path", nargs=1, required=True)
def json_get(input, path, keep_quote):
    """Get item value from json file.
    """
    data = load_json_data(input)
    result = get(data, path)
    if isNull(result):
        os.sys.exit(1)
    else:
        output = get_output(result, keep_quote)
        print(output)
        os.sys.exit(0)



@yaml_tools.command(name="get")
@click.option("-i", "--input", default="-")
@click.option("-q", "--keep-quote", is_flag=True)
@click.argument("path", nargs=1, required=True)
def yaml_get(input, path, keep_quote):
    """Get item value from yaml file.
    """
    data = load_yaml_data(input)
    result = get(data, path)
    if isNull(result):
        os.sys.exit(1)
    else:
        output = get_output(result, keep_quote)
        print(output)
        os.sys.exit(0)

if __name__ == "__main__":
    main()
