import json
import os

import wkstools
from devtools import debug


def _get_sample_nlu_response():
    with open(
        os.path.join(os.path.dirname(__file__), "nlu_response.json"),
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


if __name__ == "__main__":
    nlu_response = _get_sample_nlu_response()
    relations = wkstools.parse_relations(nlu_response)
    entities = wkstools.parse_entities(nlu_response)
    linked_relations = wkstools.get_linked_relations(
        relations, head_relation_type="specifiesValue"
    )

    print("Relations found in sample NLU response:")
    debug(relations)

    print("\nEntities found in sample NLU response:")
    debug(entities)

    print(
        "\nLinked relations of type operator->value->unit found in sample NLU response:"
    )
    debug(linked_relations)
