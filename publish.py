from os import environ
from typeform import Typeform
import yaml
import sys
from copy import deepcopy

token = environ.get("TYPEFORM_TOKEN")

if not token:
    raise ValueError("TYPEFORM_TOKEN is not set")

typeform = Typeform(token)


def simple_always_jump(source, target):
    return {
        "type": "field",
        "ref": source,
        "actions": [
            {
                "action": "jump",
                "details": {"to": {"type": "field", "value": target}},
                "condition": {"op": "always", "vars": []},
            }
        ],
    }


def simple_no_jump(source, target, jump_from=None):
    if jump_from is None:
        jump_from = source
    return {
        "type": "field",
        "ref": jump_from,
        "actions": [
            {
                "action": "jump",
                "details": {"to": {"type": "field", "value": target}},
                "condition": {
                    "op": "is",
                    "vars": [
                        {"type": "field", "value": source},
                        {"type": "constant", "value": False},
                    ],
                },
            }
        ],
    }


def parse_question(res):
    questions = []
    logic = []
    jump_ref_counter = 0
    for yqu in deepcopy(res):
        q = {}
        if "type" not in yqu:
            assert "choices" in yqu, yqu
        q["title"] = yqu.pop("title")
        prop = {}
        if "ref" in yqu:
            q["ref"] = yqu.pop("ref")
        if "always_jump_to" in yqu or "otherwise_jump_to":
            t = yqu.pop("always_jump_to", yqu.pop("otherwise_jump_to"))
            logic.append(simple_always_jump(q["ref"], t))
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
        elif "type" in yqu and yqu["type"] == "yes_no_jump":
            yqu.pop("type")
            q["type"] = "yes_no"
            if_no_jump_to = yqu.pop("if_no_jump_to")

            if q.get("ref", None) is not None:
                ref = q["ref"]
            else:
                jump_ref_counter += 1
                ref = f"jump_source_{jump_ref_counter}"
                q["ref"] = ref

            jump_from = yqu.pop("jump_from", None)
            if jump_from:
                logic.append(
                    simple_no_jump(source=ref, target=jump_to, jump_from=jump_from)
                )
            else:
                logic.append(simple_no_jump(source=ref, target=jump_to))
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

        res = yqu.pop("matthias", None)
        if res:
            print(res)
        assert not yqu, yqu
        questions.append(q)
    return questions, logic


def publish(questions, logic, id, title):
    typeform.forms.update(id, {"title": title, "fields": questions, "logic": logic})


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Usage: python publish.py <filename>")
    with open(sys.argv[1]) as f:
        res = yaml.safe_load(f.read())

    questions, logic = parse_question(res["questions"])

    publish(questions, logic, res["id"], res["title"])
