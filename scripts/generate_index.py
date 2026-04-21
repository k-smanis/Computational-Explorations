import os
import json
import re
import yaml
from collections import defaultdict

PROBLEMS_DIR = "problems"
OUTPUT_METADATA = "metadata.yaml"
OUTPUT_INDEX = "INDEX.md"

TAG_PATTERN = re.compile(r"^[a-z0-9-]+$")


class ValidationError(Exception):
    pass


def extract_metadata_from_ipynb(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        nb = json.load(f)

    if "cells" not in nb or len(nb["cells"]) == 0:
        raise ValidationError(f"{filepath}: no cells found")

    first_cell = nb["cells"][0]

    if first_cell.get("cell_type") != "markdown":
        raise ValidationError(f"{filepath}: first cell must be markdown")

    source = "".join(first_cell.get("source", []))

    match = re.search(r"```yaml\s*(.*?)\s*```", source, re.DOTALL)

    if not match:
        raise ValidationError(f"{filepath}: missing YAML code block")

    yaml_block = match.group(1)

    try:
        metadata = yaml.safe_load(yaml_block)
    except Exception as e:
        raise ValidationError(f"{filepath}: YAML parsing error: {e}")

    return metadata


def validate_metadata(metadata, filepath):
    if not isinstance(metadata, dict):
        raise ValidationError(f"{filepath}: metadata must be a dict")

    if "tags" not in metadata:
        raise ValidationError(f"{filepath}: missing 'tags'")

    tags = metadata["tags"]

    if not isinstance(tags, list) or len(tags) == 0:
        raise ValidationError(f"{filepath}: 'tags' must be a non-empty list")

    for tag in tags:
        if not isinstance(tag, str) or not TAG_PATTERN.match(tag):
            raise ValidationError(
                f"{filepath}: invalid tag '{tag}' (must match [a-z0-9-]+)"
            )


def collect_problems():
    problems = []

    for file in os.listdir(PROBLEMS_DIR):
        if not file.endswith(".ipynb"):
            continue

        path = os.path.join(PROBLEMS_DIR, file)

        metadata = extract_metadata_from_ipynb(path)
        validate_metadata(metadata, path)

        title = metadata.get("title", file.replace(".ipynb", ""))

        problems.append(
            {
                "title": title,
                "path": path.replace("\\", "/"),
                "tags": metadata["tags"],
            }
        )

    if not problems:
        return []

    return problems


def write_metadata_yaml(problems):
    with open(OUTPUT_METADATA, "w", encoding="utf-8") as f:
        yaml.dump({"problems": problems}, f, sort_keys=False)


def write_index_md(problems):
    tag_map = defaultdict(list)

    for p in problems:
        for tag in p["tags"]:
            tag_map[tag].append(p)

    with open(OUTPUT_INDEX, "w", encoding="utf-8") as f:
        f.write("# Index\n\n")

        for tag in sorted(tag_map.keys()):
            f.write(f"## {tag}\n\n")
            for p in tag_map[tag]:
                f.write(f"- [{p['title']}]({p['path']})\n")
            f.write("\n")


def main():
    try:
        problems = collect_problems()
        write_metadata_yaml(problems)
        write_index_md(problems)
        print("Generated metadata.yaml and INDEX.md successfully.")
    except ValidationError as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
