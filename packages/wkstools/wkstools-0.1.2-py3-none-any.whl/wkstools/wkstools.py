from typing import List, Tuple, Optional

from wkstools.models import AnnoationLocation, Entity, Relation


def parse_entities(nlu_response: dict) -> List[Entity]:
    """Extracts the entities in a structured manner to simplify the analysis from a NLU
        text analysis result.

    Arguments:
        nlu_response {dict} -- The response dictionary from NLU

    Returns:
        List[Entity] -- Returns a list of entities. Each entity is a dictionary
            containing the entity type, the score, the text, the location of the entity
            annotation in the text. Also the entity subtype is extracted if found.
            Returns an empty array if no nlu_response is provided or if no entities
            are found.
    """
    if nlu_response is None or "entities" not in nlu_response:
        return []

    entities = nlu_response["entities"]

    return list(
        map(
            lambda entity: Entity(
                entity_type=entity.get("type"),
                text=entity.get("text"),
                location=AnnoationLocation(
                    start=entity.get("mentions")[0].get("location")[0],
                    end=entity.get("mentions")[0].get("location")[1],
                ),
                score=entity.get("mentions")[0].get("confidence"),
                subtype=entity.get("disambiguation").get("subtype")[0],
            ),
            entities,
        )
    )


def get_entities_by_type(entities: List[Entity], valid_type: str) -> List[Entity]:
    """Get entities that match a given type name.

    Arguments:
        entities {List[Entity]} -- A list of entities extracted from a NLU response
        type_name {str} -- The name of the entity type

    Returns:
        List[dict] -- A list of entity dictionaries matching the type name
    """

    return list(
        filter(
            lambda entity: (
                entity.entity_type == valid_type or entity.subtype == valid_type
            ),
            entities,
        )
    )


def get_entities_by_types(
    entities: List[Entity], type_names: List[str]
) -> List[Entity]:
    """Get entities that match one of the given type names.

    Arguments:
        entities {List[Entity]} -- A list of entities extracted from a NLU response
        type_name {List[str]} -- The names of valid entity types

    Returns:
        List[dict] -- A list of entity dictionaries matching one of the type names
    """
    return list(
        filter(
            lambda entity: entity.entity_type in type_names
            or entity.subtype in type_names,
            entities,
        )
    )


def parse_relations(nlu_response: dict) -> List[Relation]:
    """Extracts the relations and their head and tail entities in
       a structured manner to simplify the analysis from a NLU text analysis
       result.

    Arguments:
        nlu_response {dict} -- The response dictionary from NLU

    Returns:
        List[Relation] -- Returns a list of relations. Each relation is a dictionary
            containing the relation type, the score,the sentence
            as well as the head and the tail entities with their respective parameters.
            Returns an empty array if no nlu_response is provided or if no relations are
            found.
    """
    if nlu_response is None or "relations" not in nlu_response:
        return []

    relations = nlu_response["relations"]
    return list(
        map(
            lambda relation: Relation(
                relation_type=relation.get("type"),
                sentence=relation.get("sentence"),
                score=relation.get("score"),
                head=_get_argument(relation, 0),
                tail=_get_argument(relation, 1),
            ),
            relations,
        )
    )


def get_relations_by_type(relations: List[Relation], type_name: str) -> List[Relation]:
    """Get relations that match a given type name.

    Arguments:
        relations {List[Relation]} -- A list of relations extracted from a NLU response
        type_name {str} -- The name of the relation type

    Returns:
        List[Relation] -- A list of relations matching the type name
    """
    return list(filter(lambda relation: relation.relation_type == type_name, relations))


def get_relations_by_types(relations: List[Relation], type_names: List[Relation]):
    """Get relations that match one of the given type names.

    Arguments:
        relations {List[Relation]} -- A list of relations extracted from a NLU response
        type_name {str} -- The name of the relation types

    Returns:
        List[Relation] -- A list of relation dictionaries matching one of the type names
    """
    return list(
        filter(lambda relation: relation.relation_type in type_names, relations)
    )


def get_relations_by_head_type(
    relations: List[Relation], type_name: str
) -> List[Relation]:
    """Get relations whose head type or subtype matches the type name.

    Arguments:
        relations {List[Relation]} -- A list of relations extracted from a NLU response
        type_name {str} -- The name of the entity type to filter for

    Returns:
        List[Relation] -- A list of relations matching the head type or subtype
    """
    return list(
        filter(
            lambda relation: (
                relation.head.entity_type == type_name
                or relation.head.subtype == type_name
            ),
            relations,
        )
    )


def get_relations_by_tail_type(
    relations: List[Relation], type_name: str
) -> List[Relation]:
    """Get relations whose tail type or subtype matches the type name.

    Arguments:
        relations {List[Relation]} -- A list of relations extracted from a NLU response
        type_name {str} -- The name of the entity type to filter for

    Returns:
        List[Relation] -- A list of relations matching the tail type or subtype
    """
    return list(
        filter(
            lambda relation: (
                relation.tail.entity_type == type_name
                or relation.tail.subtype == type_name
            ),
            relations,
        )
    )


def is_part_of_relations(entity: Entity, relations: List[Relation]) -> bool:
    """Check if `entity` is part of `relations`. This is the case if the location
       of the entity overlaps with either the head or the tail of the relation.

    Arguments:
        entity {Entity} -- A NLU entity object
        relations {List[Relation]} -- A list of relations extracted from a NLU response

    Returns:
        bool -- Returns true if the entity is an argument of one of the relations
    """
    if entity is None or relations is None or entity == [] or relations == []:
        return False

    matches = list(
        filter(
            lambda relation: relation.head.location.start == entity.location.start
            or relation.tail.location.start == entity.location.start,
            relations,
        )
    )

    if len(matches) > 0:
        return True
    else:
        return False


def is_joint_relation(first_relation: Relation, second_relation: Relation) -> bool:
    return (
        is_joint_head_head_relation(first_relation, second_relation)
        or is_joint_head_tail_relation(first_relation, second_relation)
        or is_joint_tail_head_relation(first_relation, second_relation)
        or is_joint_tail_tail_relation(first_relation, second_relation)
    )


def is_joint_head_head_relation(
    first_relation: Relation, second_relation: Relation
) -> bool:
    return _is_relation_joint_on(first_relation, "head", second_relation, "head")


def is_joint_head_tail_relation(
    first_relation: Relation, second_relation: Relation
) -> bool:
    return _is_relation_joint_on(first_relation, "head", second_relation, "tail")


def is_joint_tail_head_relation(
    first_relation: Relation, second_relation: Relation
) -> bool:
    return _is_relation_joint_on(first_relation, "tail", second_relation, "head")


def is_joint_tail_tail_relation(
    first_relation: Relation, second_relation: Relation
) -> bool:
    return _is_relation_joint_on(first_relation, "tail", second_relation, "tail")


def is_same_sentence(first_relation: Relation, second_relation: Relation) -> bool:
    if first_relation is None or second_relation is None:
        return False

    return first_relation.sentence == second_relation.sentence


def get_linked_relations(
    relations: List[Relation],
    head_relation_type: Optional[str] = None,
    tail_relation_type: Optional[str] = None,
) -> List[Tuple[Relation, Relation]]:
    if head_relation_type is None and tail_relation_type is None:
        raise ValueError(
            "Specify either head_relation_type or tail_relation_type"
            " for filtering joint relations."
        )
    if head_relation_type is not None:
        head_relations = get_relations_by_type(relations, head_relation_type)
    else:
        head_relations = relations

    if tail_relation_type is not None:
        tail_relations = get_relations_by_type(relations, tail_relation_type)
    else:
        tail_relations = relations

    linked_relations = []

    for head_relation in head_relations:
        if (
            head_relation.head.location is not None
            and head_relation.head.location.start is not None
        ):
            connected_relations = list(
                filter(
                    lambda relation: (
                        head_relation != relation
                        and (
                            is_joint_head_head_relation(head_relation, relation)
                            or is_joint_head_tail_relation(head_relation, relation)
                            or is_joint_tail_head_relation(head_relation, relation)
                            or is_joint_tail_tail_relation(head_relation, relation)
                        )
                    ),
                    tail_relations,
                )
            )

            if len(connected_relations) > 0:
                for connection in connected_relations:
                    linked_relations.append((head_relation, connection))

    return linked_relations


def _is_relation_joint_on(
    first_relation: Relation,
    first_location_specifier: str,
    second_relation: Relation,
    second_location_specifier: str,
) -> bool:
    if (
        first_relation.head.location is not None
        and second_relation.head.location is not None
        and first_relation.dict()[first_location_specifier]["location"]["start"]
        == second_relation.dict()[second_location_specifier]["location"]["start"]
        and first_relation.dict()[first_location_specifier]["location"]["end"]
        == second_relation.dict()[second_location_specifier]["location"]["end"]
    ):
        return True
    else:
        return False


def _get_argument(relation: dict, position: int) -> Entity:
    """Extracts the argument entity from a given relation at the given position.
        The method assumes the standard response schema for arguments of the Watson
        Natural Language Understanding relation representation. See the API
        documentation for more information.

    Arguments:
        relation {dict} -- A Watson Natural Language Understanding relation
        id {int} -- The position of the relation, can be either 0 or 1 in this API

    Returns:
        Entity -- Returns a dictionary containing the structured entity argument at the
        specified position.
    """

    return Entity(
        entity_type=relation.get("arguments", [])[position]
        .get("entities")[0]
        .get("type"),
        text=relation.get("arguments", [])[position].get("entities")[0].get("text"),
        location=AnnoationLocation(
            start=relation.get("arguments", [])[position].get("location")[0],
            end=relation.get("arguments", [])[position].get("location")[1],
        ),
        subtype=relation.get("arguments", [])[position]
        .get("entities")[0]
        .get("disambiguation")
        .get("subtype")[0],
    )
