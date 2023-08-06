""" IBM Watson Natural Language Understanding + Watson Knowledge Studio tools """

__version__ = "0.1.2"

from .wkstools import (
    parse_entities,
    get_entities_by_type,
    get_entities_by_types,
    parse_relations,
    get_relations_by_type,
    get_relations_by_types,
    get_relations_by_head_type,
    get_relations_by_tail_type,
    is_part_of_relations,
    is_same_sentence,
    is_joint_relation,
    is_joint_head_head_relation,
    is_joint_head_tail_relation,
    is_joint_tail_head_relation,
    is_joint_tail_tail_relation,
    get_linked_relations,
)
