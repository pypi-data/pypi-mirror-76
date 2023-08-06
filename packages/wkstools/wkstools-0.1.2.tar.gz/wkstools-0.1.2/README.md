wkstools
=============
wkstools is a small convenience library that provides utilities to efficiently work with entities and relations provided by IBM Natural Language Understanding.

![PyPI - License](https://img.shields.io/pypi/l/wkstools)
![PyPI](https://img.shields.io/pypi/v/wkstools)

## Intuition

When using IBM Watson Knowledge Studio (WKS) models in IBM Natural Language Understanding (NLU), in most cases the resulting JSON requires post-processing to work with the extracted entities and relations.
This is where wkstools comes to help:

Let's assume you have trained a machine learning model in IBM Watson Knowledge Studio that recognizes relations between quantifiers, numbers and units. 
`"I want a smartphone that weighs no more than 160 g."`

If we want to build a tool that allows natural language searches for smartphone against a product database, you need to understand the relevant concepts in a structured manner. 
For the above example it will be helpful to extract the relations that point from the operator (`no more than`) to the (`value`) and the unit (`g`).

See the `intuition.py` and `nlu_response.json` in the exmaples folder to have a running example.


## Requirements

- Python 3.6+
- Pydantic

## Installation
```console
$ pip install wkstools
```

## Usage

### Parse entities and relations
To parse the NLU JSON response retrieved from IBM Natural Language Understanding, use:
```python
import wkstools

# Your NLU JSON response to process
nlu_response = '{..., "relations": [{"type": "specifiesValue", ...], "entities": [...]}' 

entities = wkstools.parse_entities(nlu_response)
relations = wkstools.parse_relations(nlu_response)
```
See the entity and relation models for available fields.

### Access specific relations
```python
import wkstools

# Your NLU JSON response to process
nlu_response = '{..., "relations": [{"type": "specifiesValue", ...], "entities": [...]}' 

relations = wkstools.parse_relations(nlu_response)

value_relations = wkstools.get_relations_by_type(relations, "specifiesValue")
```

## Testing
To lint and test, run:
```console
$ ./scripts/test.sh
```

To get the html coverage report run:
```console
$ ./scripts/test-cov-report.sh
```

## License
This project is licensed under the terms of the MIT license.