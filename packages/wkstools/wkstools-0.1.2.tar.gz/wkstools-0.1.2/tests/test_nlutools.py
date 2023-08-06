import pytest
import tests.utils as utils
from wkstools import (
    get_entities_by_type,
    get_entities_by_types,
    get_linked_relations,
    get_relations_by_head_type,
    get_relations_by_tail_type,
    get_relations_by_type,
    get_relations_by_types,
    is_joint_head_head_relation,
    is_joint_head_tail_relation,
    is_joint_relation,
    is_joint_tail_head_relation,
    is_joint_tail_tail_relation,
    is_part_of_relations,
    is_same_sentence,
    parse_entities,
    parse_relations,
)
from wkstools.models import AnnoationLocation, Entity, Relation

""" Testing entity parsing and filtering """


def test_parse_entities():
    nlu_response = utils.get_nlu_json_response()
    extracted_entities = parse_entities(nlu_response)
    assert len(extracted_entities) == 6
    for entity in extracted_entities:
        assert entity.score > 0.0
        assert type(entity.location) is AnnoationLocation
        assert entity.location.start is not None
        assert entity.location.end is not None
        assert entity.entity_type
        assert entity.subtype
        assert entity.text

    assert len(parse_entities(None)) == 0


def test_parse_specific_entity():
    nlu_response = utils.get_nlu_single_entity_json_response()
    extracted_entities = parse_entities(nlu_response)
    assert len(extracted_entities) == 1
    extracted_entity = extracted_entities[0]
    assert extracted_entity.entity_type == "QUESTION_MARKER"
    assert extracted_entity.text == "Welche"
    assert extracted_entity.location.start == 0
    assert extracted_entity.location.end == 6
    assert extracted_entity.score >= 0.98
    assert extracted_entity.subtype == "QUESTION"


def test_get_entities_by_type():
    entities = utils.get_entities()
    filtered_entities = get_entities_by_type(entities, "TYPE1")
    assert len(filtered_entities) == 2


def test_get_entities_by_types():
    entities = utils.get_different_entities()
    filtered_entities = get_entities_by_types(entities, ["TYPE1", "TYPE2"])
    assert len(filtered_entities) == 2

    filtered_entities = get_entities_by_types(entities, [])
    assert len(filtered_entities) == 0

    filtered_entities = get_entities_by_types(entities, ["TYPE1"])
    assert len(filtered_entities) == 1
    assert filtered_entities[0].entity_type == "TYPE1"


""" Testing relation parsing and filtering """


def test_parse_relations():
    nlu_response = utils.get_nlu_json_response()
    parsed_relation = parse_relations(nlu_response)
    assert len(parsed_relation) == 4
    for relation in parsed_relation:
        assert type(relation) is Relation
        assert relation.relation_type
        assert relation.sentence
        assert relation.score > 0.0
        assert type(relation.head) is Entity
        assert type(relation.tail) is Entity

    assert len(parse_relations(None)) == 0


def test_parse_specific_relation():
    nlu_response = utils.get_nlu_single_relation_json_response()
    parsed_relations = parse_relations(nlu_response)
    assert len(parsed_relations) == 1
    parsed_relation = parsed_relations[0]
    assert parsed_relation.relation_type == "FragtNach"
    assert (
        parsed_relation.sentence == "welche Handys mit Gwicht von unter 165 g gibt es?"
    )
    assert parsed_relation.score >= 0.985
    assert parsed_relation.head.entity_type == "QUESTION_MARKER"
    assert parsed_relation.head.text == "Welche"
    assert parsed_relation.head.location.start == 0
    assert parsed_relation.head.location.end == 6
    assert parsed_relation.head.score is None
    assert parsed_relation.head.subtype == "NONE"
    assert parsed_relation.tail.entity_type == "PRODUKT"
    assert parsed_relation.tail.text == "Handys"
    assert parsed_relation.tail.location.start == 7
    assert parsed_relation.tail.location.end == 13
    assert parsed_relation.tail.score is None
    assert parsed_relation.tail.subtype == "SMARTPHONE"


def test_get_relations_by_type():
    relations = utils.get_different_relations()
    relation_with_certain_type = get_relations_by_type(relations, "SAMPLE_RELATION_1")
    assert relation_with_certain_type == [relations[0]]

    relation_with_certain_type = get_relations_by_type(relations, "SAMPLE_RELATION_2")
    assert relation_with_certain_type == [relations[1]]

    relation_with_certain_type = get_relations_by_type(relations, "UNKNOWN")
    assert relation_with_certain_type == []

    relation_with_certain_type = get_relations_by_type([], "UNKNOWN")
    assert relation_with_certain_type == []


def test_get_relations_by_types():
    relations = utils.get_different_relations()
    relation_with_certain_type = get_relations_by_types(
        relations, ["SAMPLE_RELATION_1"]
    )
    assert relation_with_certain_type == [relations[0]]

    relation_with_certain_type = get_relations_by_types(
        relations, ["SAMPLE_RELATION_2"]
    )
    assert relation_with_certain_type == [relations[1]]

    relation_with_certain_type = get_relations_by_types(
        relations, ["SAMPLE_RELATION_1", "SAMPLE_RELATION_2"]
    )
    assert relation_with_certain_type == relations

    relation_with_certain_type = get_relations_by_types(relations, ["UNKNOWN"])
    assert relation_with_certain_type == []

    relation_with_certain_type = get_relations_by_types([], ["UNKNOWN"])
    assert relation_with_certain_type == []


def test_get_relations_by_head_type():
    relations = utils.get_different_relations()
    relation_with_certain_type = get_relations_by_head_type(relations, "TYPE1")
    assert relation_with_certain_type == [relations[0]]

    relation_with_certain_type = get_relations_by_head_type(relations, "SUBTYPE1")
    assert relation_with_certain_type == [relations[0]]

    relation_with_certain_type = get_relations_by_head_type(relations, "TYPE2")
    assert relation_with_certain_type == []

    relation_with_certain_type = get_relations_by_head_type(relations, "SUBTYPE2")
    assert relation_with_certain_type == []

    relation_with_certain_type = get_relations_by_head_type(relations, "TYPE3")
    assert relation_with_certain_type == [relations[1]]

    relation_with_certain_type = get_relations_by_head_type(relations, "SUBTYPE3")
    assert relation_with_certain_type == [relations[1]]

    relation_with_certain_type = get_relations_by_head_type(relations, "UNKNOWN")
    assert relation_with_certain_type == []

    relation_with_certain_type = get_relations_by_head_type([], "UNKNOWN")
    assert relation_with_certain_type == []


def test_get_relations_by_tail_type():
    relations = utils.get_different_relations()
    relation_with_certain_type = get_relations_by_tail_type(relations, "TYPE1")
    assert relation_with_certain_type == []

    relation_with_certain_type = get_relations_by_tail_type(relations, "SUBTYPE1")
    assert relation_with_certain_type == []

    relation_with_certain_type = get_relations_by_tail_type(relations, "TYPE2")
    assert relation_with_certain_type == [relations[0]]

    relation_with_certain_type = get_relations_by_tail_type(relations, "SUBTYPE2")
    assert relation_with_certain_type == [relations[0]]

    relation_with_certain_type = get_relations_by_tail_type(relations, "TYPE4")
    assert relation_with_certain_type == [relations[1]]

    relation_with_certain_type = get_relations_by_tail_type(relations, "SUBTYPE4")
    assert relation_with_certain_type == [relations[1]]

    relation_with_certain_type = get_relations_by_tail_type(relations, "UNKNOWN")
    assert relation_with_certain_type == []

    relation_with_certain_type = get_relations_by_tail_type([], "UNKNOWN")
    assert relation_with_certain_type == []


""" Testing logical functions """


def test_is_part_of_relations_no_overlap():
    entity, relation = utils.get_non_overlapping_entity_relation()
    assert is_part_of_relations(entity, [relation]) is False
    assert is_part_of_relations([], [relation]) is False
    assert is_part_of_relations(entity, []) is False
    assert is_part_of_relations([], []) is False


def test_is_part_of_relations_entity_head_overlap():
    entity, relation = utils.get_head_overlapping_entity_relation()
    assert is_part_of_relations(entity, [relation]) is True
    assert is_part_of_relations([], [relation]) is False
    assert is_part_of_relations(entity, []) is False
    assert is_part_of_relations([], []) is False


def test_is_part_of_relations_entity_tail_overlap():
    entity, relation = utils.get_tail_overlapping_entity_relation()
    assert is_part_of_relations(entity, [relation]) is True
    assert is_part_of_relations([], [relation]) is False
    assert is_part_of_relations(entity, []) is False
    assert is_part_of_relations([], []) is False


def test_is_same_sentence():
    relations = utils.get_different_relations()

    assert is_same_sentence(relations[0], relations[0])
    assert is_same_sentence(relations[1], relations[1])

    assert not is_same_sentence(relations[0], relations[1])
    assert not is_same_sentence(None, relations[1])
    assert not is_same_sentence(relations[1], None)
    assert not is_same_sentence(None, None)


def test_is_joint_relation():
    head_head_rel = utils.get_joint_head_head_relations()
    assert is_joint_relation(head_head_rel[0], head_head_rel[1])
    assert is_joint_head_head_relation(head_head_rel[0], head_head_rel[1])
    assert not is_joint_head_tail_relation(head_head_rel[0], head_head_rel[1])
    assert not is_joint_tail_tail_relation(head_head_rel[0], head_head_rel[1])
    assert not is_joint_tail_head_relation(head_head_rel[0], head_head_rel[1])

    head_tail_rel = utils.get_joint_head_tail_relations()
    assert is_joint_relation(head_tail_rel[0], head_tail_rel[1])
    assert not is_joint_head_head_relation(head_tail_rel[0], head_tail_rel[1])
    assert is_joint_head_tail_relation(head_tail_rel[0], head_tail_rel[1])
    assert not is_joint_tail_tail_relation(head_tail_rel[0], head_tail_rel[1])
    assert not is_joint_tail_head_relation(head_tail_rel[0], head_tail_rel[1])

    tail_head_rel = utils.get_joint_tail_head_relations()
    assert is_joint_relation(tail_head_rel[0], tail_head_rel[1])
    assert not is_joint_head_head_relation(tail_head_rel[0], tail_head_rel[1])
    assert not is_joint_head_tail_relation(tail_head_rel[0], tail_head_rel[1])
    assert not is_joint_tail_tail_relation(tail_head_rel[0], tail_head_rel[1])
    assert is_joint_tail_head_relation(tail_head_rel[0], tail_head_rel[1])

    tail_tail_rel = utils.get_joint_tail_tail_relations()
    assert is_joint_relation(tail_tail_rel[0], tail_tail_rel[1])
    assert not is_joint_head_head_relation(tail_tail_rel[0], tail_tail_rel[1])
    assert not is_joint_head_tail_relation(tail_tail_rel[0], tail_tail_rel[1])
    assert is_joint_tail_tail_relation(tail_tail_rel[0], tail_tail_rel[1])
    assert not is_joint_tail_head_relation(tail_tail_rel[0], tail_tail_rel[1])


def test_get_linked_relation():
    head_head_rel = utils.get_joint_head_head_relations()
    with pytest.raises(ValueError):
        linked_relations = get_linked_relations(head_head_rel)

    linked_relations = get_linked_relations(
        head_head_rel, head_relation_type="SAMPLE_RELATION_1"
    )
    assert len(linked_relations) == 1
    assert linked_relations[0][0] == head_head_rel[0]
    assert linked_relations[0][1] == head_head_rel[1]

    linked_relations = get_linked_relations(
        head_head_rel, tail_relation_type="SAMPLE_RELATION_2"
    )
    assert len(linked_relations) == 1
    assert linked_relations[0][0] == head_head_rel[0]
    assert linked_relations[0][1] == head_head_rel[1]

    linked_relations = get_linked_relations(
        head_head_rel,
        head_relation_type="SAMPLE_RELATION_1",
        tail_relation_type="SAMPLE_RELATION_2",
    )
    assert len(linked_relations) == 1
    assert linked_relations[0][0] == head_head_rel[0]
    assert linked_relations[0][1] == head_head_rel[1]

    linked_relations = get_linked_relations(
        head_head_rel,
        head_relation_type="SAMPLE_RELATION_3",
        tail_relation_type="SAMPLE_RELATION_4",
    )
    assert len(linked_relations) == 0


def test__annotation_location_model():
    loc1 = AnnoationLocation(start=0, end=1)
    loc2 = AnnoationLocation(start=1, end=2)
    loc3 = AnnoationLocation(start=0, end=1)
    repr(loc1)
    str(loc1)
    assert hash(loc1) != hash(loc2)
    assert hash(loc1) == hash(loc3)
    assert loc1 < loc2
    assert loc1 != loc2
    assert loc1 == loc3
