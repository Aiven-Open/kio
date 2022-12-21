def to_snake_case(value: str) -> str:
    """
    >>> to_snake_case("ISRReplicas")
    'isr_replicas'
    >>> to_snake_case("ISR")
    'isr'
    >>> to_snake_case("InSyncReplicas")
    'in_sync_replicas'
    >>> to_snake_case("WhatIsQ")
    'what_is_q'
    """

    groups = []
    current_group = ""
    offset = -1

    while True:
        offset += 1

        current = value[offset]

        try:
            previous = current_group[-1]
        except IndexError:
            current_group += current
            continue

        try:
            subsequent = value[offset + 1]
        except IndexError:
            if previous.islower() and current.isupper():
                groups.append(current_group)
                current_group = current
            else:
                current_group += current
            break

        if (previous.isupper() and current.isupper() and subsequent.islower()) or (
            previous.islower() and current.isupper()
        ):
            groups.append(current_group)
            current_group = current
        else:
            current_group += current

    groups.append(current_group)
    return ("_".join(groups)).lower()


def capitalize_first(value: str) -> str:
    return value[0].capitalize() + value[1:]
