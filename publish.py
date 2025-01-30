from os import environ
from typeform import Typeform
import yaml
import sys
from copy import deepcopy

token = environ.get("TYPEFORM_TOKEN")

if not token:
    raise ValueError("TYPEFORM_TOKEN is not set")

typeform = Typeform(token)


def parse_question(res):
    questions = []
    for yqu in deepcopy(res):
        q = {}
        if "type" not in yqu:
            assert "choices" in yqu, yqu
        q["title"] = yqu.pop("title")
        prop = {}
        if "description" in yqu:
            prop["description"] = yqu.pop("description")

        if "choices" in yqu and yqu.get("type", None) in ("multiple_choices", None):
            q["type"] = "multiple_choice"

            q["properties"] = prop
            if yqu.pop("multiple", False):
                prop["allow_multiple_selection"] = True
            if yqu.pop("other", False):
                prop["allow_other_choice"] = True
            prop["choices"] = []
            choices = yqu.pop("choices")
            for c in choices:
                if c.strip().startswith("::"):
                    assert c == "::other_please_type::"
                    prop["allow_other_choice"] = True
                    continue
                prop["choices"].append({"label": c})
        elif "type" in yqu and yqu["type"] in ("number", "statement"):
            q["type"] = yqu.pop("type")
            q["properties"] = prop
        elif yqu["type"] == "opinion_scale":
            q["type"] = yqu.pop("type")
            if "start" in yqu:
                start = yqu.pop("start")
                assert start in (1, 0)
                if start == 1:
                    prop["start_at_one"] = True
                if start == 0:
                    pass  # the default.
            prop["steps"] = yqu.pop("steps", 11)
            if "labels" in yqu:
                labels = yqu.pop("labels")
                assert len(labels) in [2, 3]
                if len(labels) == 2:
                    prop["labels"] = {"left": labels[0], "right": labels[1]}
                elif len(labels) == 3:
                    prop["labels"] = {
                        "left": labels[0],
                        "center": labels[1],
                        "right": labels[2],
                    }
                    print(prop)
                else:
                    assert False
            q["properties"] = prop
        elif yqu["type"] == "long_text":
            q["type"] = yqu.pop("type")
            # nothing to do
        elif yqu["type"] == "ranking":
            q["type"] = yqu.pop("type")
            choices = yqu.pop("choices")
            prop["choices"] = []
            q["properties"] = prop
            for c in choices:
                prop["choices"].append({"label": c})
        else:
            assert False, q
        assert not yqu, yqu
        questions.append(q)
    return questions


def publish(questions, id="Oq55zKog", title="Sphinx Survey oct 17"):
    typeform.forms.update(id, {"title": title, "fields": questions})


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Usage: python publish.py <filename>")
    with open(sys.argv[1]) as f:
        res = yaml.safe_load(f.read())

    publish(parse_question(res["questions"]), res["id"])
