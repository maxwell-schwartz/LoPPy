def is_branches(knowledge, elements, f1, f2):
    """Determine if given set of words is combo of two types"""

    head, *tail = elements
    head = [head]
    # Divide elements
    # If both functions return True, return True and POS list
    while tail:
        left_truth, left_pos = f1(knowledge, head)
        right_truth, right_pos = f2(knowledge, tail)
        if left_truth and right_truth:
            return True, left_pos + right_pos
        new_head, *tail = tail
        head += [new_head]
    return False, []


def is_wrapped(knowledge, elements, f1, f2, f3):
    """
    Determine if a given set of words is a combo of three types,
    one embedded between two others.

    This is relevant for cases of auxiliary verbs agreeing with
    other verbs:
    e.g. "does the bird eat"
    """

    head, *tail = elements
    head = [head]
    head_truth, head_pos = f1(knowledge, head)
    tail_truth, tail_pos = is_branches(knowledge, tail, f2, f3)
    if head_truth and tail_truth:
        return True, head_pos + tail_pos
    return False, []
