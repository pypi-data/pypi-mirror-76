import json
import os
from typing import List, Tuple

from wkstools.models import AnnoationLocation, Entity, Relation
from pydantic import parse_obj_as


def _load_json(filename: str) -> dict:
    with open(
        os.path.join(os.path.dirname(__file__), filename), "r", encoding="utf-8",
    ) as f:
        return json.load(f)


def get_nlu_json_response() -> dict:
    return _load_json("./data/nlu_response.json")


def get_nlu_single_entity_json_response() -> dict:
    return _load_json("./data/nlu_response_1_entity.json")


def get_nlu_single_relation_json_response() -> dict:
    return _load_json("./data/nlu_response_1_relation.json")


def get_head_overlapping_entity_relation() -> Tuple[Entity, Relation]:
    head = Entity(
        entity_type="head-type",
        text="head",
        location=AnnoationLocation(start=0, end=4),
        subtype="HEAD",
    )
    tail = Entity(
        entity_type="tail-type",
        text="tail",
        location=AnnoationLocation(start=6, end=9),
        subtype="TAIL",
    )
    relation = Relation(
        relation_type="some-relation-type",
        sentence="head tail",
        subtype="NONE",
        head=head,
        tail=tail,
        score=1.0,
    )
    return (head, relation)


def get_tail_overlapping_entity_relation() -> Tuple[Entity, Relation]:
    head = Entity(
        entity_type="head-type",
        text="head",
        location=AnnoationLocation(start=0, end=4),
        subtype="HEAD",
        score=0.99,
    )
    tail = Entity(
        entity_type="tail-type",
        text="tail",
        location=AnnoationLocation(start=6, end=9),
        subtype="TAIL",
        score=0.99,
    )
    relation = Relation(
        relation_type="some-relation-type",
        sentence="head tail",
        subtype="NONE",
        head=head,
        tail=tail,
        score=1.0,
    )
    return (tail, relation)


def get_non_overlapping_entity_relation() -> Tuple[Entity, Relation]:
    other_entity = Entity(
        entity_type="head-type",
        text="head",
        location=AnnoationLocation(start=10, end=14),
        subtype="HEAD",
        score=0.99,
    )
    head = Entity(
        entity_type="head-type",
        text="head",
        location=AnnoationLocation(start=0, end=4),
        subtype="HEAD",
        score=0.99,
    )
    tail = Entity(
        entity_type="tail-type",
        text="tail",
        location=AnnoationLocation(start=6, end=9),
        subtype="TAIL",
        score=0.99,
    )
    relation = Relation(
        relation_type="some-relation-type",
        sentence="head tail",
        subtype="NONE",
        head=head,
        tail=tail,
        score=1.0,
    )
    return (other_entity, relation)


def get_entities():
    entities = [
        {
            "entity_type": "TYPE1",
            "text": "jährlich",
            "location": {"start": 24, "end": 32},
            "score": 0.98282,
            "subtype": "JAEHRLICH",
        },
        {
            "entity_type": "TYPE1",
            "text": "regelmäßig",
            "location": {"start": 24, "end": 34},
            "score": 0.98282,
            "subtype": "NONE",
        },
    ]
    return parse_obj_as(List[Entity], entities)


def get_different_entities():
    entities = [
        {
            "entity_type": "TYPE1",
            "text": "jährlich",
            "location": {"start": 24, "end": 32},
            "score": 0.98282,
            "subtype": "JAEHRLICH",
        },
        {
            "entity_type": "TYPE2",
            "text": "regelmäßig",
            "location": {"start": 34, "end": 44},
            "score": 0.98282,
            "subtype": "NONE",
        },
    ]
    return parse_obj_as(List[Entity], entities)


def get_different_relations():
    relations = [
        {
            "relation_type": "SAMPLE_RELATION_1",
            "sentence": "TYPE1 TYPE2",
            "score": 0.8,
            "head": {
                "entity_type": "TYPE1",
                "text": "jährlich",
                "location": {"start": 0, "end": 5},
                "score": 0.98282,
                "subtype": "SUBTYPE1",
            },
            "tail": {
                "entity_type": "TYPE2",
                "text": "regelmäßig",
                "location": {"start": 7, "end": 11},
                "score": 0.98282,
                "subtype": "SUBTYPE2",
            },
        },
        {
            "relation_type": "SAMPLE_RELATION_2",
            "sentence": "TYPE3 TYPE4",
            "score": 0.8,
            "head": {
                "entity_type": "TYPE3",
                "text": "jährlich",
                "location": {"start": 10, "end": 15},
                "score": 0.98282,
                "subtype": "SUBTYPE3",
            },
            "tail": {
                "entity_type": "TYPE4",
                "text": "regelmäßig",
                "location": {"start": 17, "end": 21},
                "score": 0.98282,
                "subtype": "SUBTYPE4",
            },
        },
    ]
    return parse_obj_as(List[Relation], relations)


def get_joint_head_head_relations():
    relations = [
        {
            "relation_type": "SAMPLE_RELATION_1",
            "sentence": "type1 type2 type3",
            "score": 0.8,
            "head": {
                "entity_type": "TYPE1",
                "text": "type1",
                "location": {"start": 0, "end": 5},
                "score": 0.98282,
                "subtype": "SUBTYPE1",
            },
            "tail": {
                "entity_type": "TYPE2",
                "text": "type2",
                "location": {"start": 7, "end": 11},
                "score": 0.98282,
                "subtype": "SUBTYPE2",
            },
        },
        {
            "relation_type": "SAMPLE_RELATION_2",
            "sentence": "type1 type2 type3",
            "score": 0.8,
            "head": {
                "entity_type": "TYPE1",
                "text": "type1",
                "location": {"start": 0, "end": 5},
                "score": 0.98282,
                "subtype": "SUBTYPE1",
            },
            "tail": {
                "entity_type": "TYPE3",
                "text": "type3",
                "location": {"start": 12, "end": 15},
                "score": 0.98282,
                "subtype": "SUBTYPE3",
            },
        },
    ]
    return parse_obj_as(List[Relation], relations)


def get_joint_head_tail_relations():
    relations = [
        {
            "relation_type": "SAMPLE_RELATION_1",
            "sentence": "type1 type2 type3",
            "score": 0.8,
            "head": {
                "entity_type": "TYPE1",
                "text": "type1",
                "location": {"start": 0, "end": 5},
                "score": 0.98282,
                "subtype": "SUBTYPE1",
            },
            "tail": {
                "entity_type": "TYPE2",
                "text": "type2",
                "location": {"start": 7, "end": 11},
                "score": 0.98282,
                "subtype": "SUBTYPE2",
            },
        },
        {
            "relation_type": "SAMPLE_RELATION_2",
            "sentence": "type1 type2 type3",
            "score": 0.8,
            "head": {
                "entity_type": "TYPE3",
                "text": "type3",
                "location": {"start": 12, "end": 15},
                "score": 0.98282,
                "subtype": "SUBTYPE3",
            },
            "tail": {
                "entity_type": "TYPE1",
                "text": "type1",
                "location": {"start": 0, "end": 5},
                "score": 0.98282,
                "subtype": "SUBTYPE1",
            },
        },
    ]
    return parse_obj_as(List[Relation], relations)


def get_joint_tail_head_relations():
    relations = [
        {
            "relation_type": "SAMPLE_RELATION_1",
            "sentence": "type1 type2 type3",
            "score": 0.8,
            "head": {
                "entity_type": "TYPE1",
                "text": "type1",
                "location": {"start": 0, "end": 5},
                "score": 0.98282,
                "subtype": "SUBTYPE1",
            },
            "tail": {
                "entity_type": "TYPE2",
                "text": "type2",
                "location": {"start": 7, "end": 11},
                "score": 0.98282,
                "subtype": "SUBTYPE2",
            },
        },
        {
            "relation_type": "SAMPLE_RELATION_2",
            "sentence": "type1 type2 type3",
            "score": 0.8,
            "head": {
                "entity_type": "TYPE2",
                "text": "type2",
                "location": {"start": 7, "end": 11},
                "score": 0.98282,
                "subtype": "SUBTYPE2",
            },
            "tail": {
                "entity_type": "TYPE3",
                "text": "type3",
                "location": {"start": 12, "end": 15},
                "score": 0.98282,
                "subtype": "SUBTYPE3",
            },
        },
    ]
    return parse_obj_as(List[Relation], relations)


def get_joint_tail_tail_relations():
    relations = [
        {
            "relation_type": "SAMPLE_RELATION_1",
            "sentence": "type1 type2 type3",
            "score": 0.8,
            "head": {
                "entity_type": "TYPE1",
                "text": "type1",
                "location": {"start": 0, "end": 5},
                "score": 0.98282,
                "subtype": "SUBTYPE1",
            },
            "tail": {
                "entity_type": "TYPE2",
                "text": "type2",
                "location": {"start": 7, "end": 11},
                "score": 0.98282,
                "subtype": "SUBTYPE2",
            },
        },
        {
            "relation_type": "SAMPLE_RELATION_2",
            "sentence": "type1 type2 type3",
            "score": 0.8,
            "head": {
                "entity_type": "TYPE3",
                "text": "type3",
                "location": {"start": 12, "end": 15},
                "score": 0.98282,
                "subtype": "SUBTYPE3",
            },
            "tail": {
                "entity_type": "TYPE2",
                "text": "type2",
                "location": {"start": 7, "end": 11},
                "score": 0.98282,
                "subtype": "SUBTYPE2",
            },
        },
    ]
    return parse_obj_as(List[Relation], relations)
