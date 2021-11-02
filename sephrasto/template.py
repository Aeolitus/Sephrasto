from pathlib import Path

import yaml

template_root = Path(__file__).parent.parent / "templates"


def available_templates():
    return [f for f in template_root.rglob("*.yaml")]


def find_template_path(filename: str) -> Path:
    for f in available_templates():
        if f.stem == Path(filename).stem:
            return f
    raise ValueError(f"Could not find {filename} in templates{available_templates()}")


def character():
    char_template = template_root / "Charakter.yaml"
    return load_nested_yaml(char_template)


def load_nested_yaml(file):
    with open(file, "r", encoding="utf8") as file:
        try:
            d = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
    for k, v in d.items():
        if isinstance(v, str) and v.endswith(".yaml"):

            d[k] = load_nested_yaml(find_template_path(v))
    return d
