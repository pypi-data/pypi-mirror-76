from pathlib import Path
from copy import deepcopy
import json


class SchemaRenderer:

    list_resolver = {"allOf", "anyOf", "oneOf", "items"}
    schema_cache = {}

    def __init__(self, path):
        pth = Path(path)
        self.root_directory = pth.parent
        self.schema = json.load(open(path))

    def _resolve_ref(self, ref, working_schema, working_path):
        path, _, fragment = ref.partition("#")
        other_schema = None
        new_working_path = None
        if path:
            path = Path(working_path, path)
            new_working_path = path.parent.resolve()
            other_schema = json.load(open(path))
        working_schema = deepcopy(other_schema or working_schema)
        doc_part = deepcopy(other_schema or working_schema)
        fragment_parts = [part for part in fragment.split("/") if part]
        for fragment_part in fragment_parts:
            doc_part = doc_part[fragment_part]
        return doc_part, working_schema, new_working_path or working_path

    def _resolve_dict(self, dictionary, working_schema, working_path):
        data = dict()

        if "$ref" in dictionary:
            loaded_data, temp_working_schema, temp_working_path = self._resolve_ref(
                dictionary["$ref"], working_schema, working_path
            )
            return self._resolve_dict(
                loaded_data, temp_working_schema, temp_working_path
            )

        for key, item in dictionary.items():
            new_value = item
            if isinstance(item, dict):
                if key == "definitions":
                    continue
                new_value = self._resolve_dict(item, working_schema, working_path)
            elif isinstance(item, list) and key in SchemaRenderer.list_resolver:
                new_value = [
                    self._resolve_dict(it, working_schema, working_path) for it in item
                ]
            data[key] = new_value
        return data

    def render(self):
        return self._resolve_dict(self.schema, self.schema, self.root_directory)
