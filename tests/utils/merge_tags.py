def merge_tags_unique(*lists):
    """ Merges lists of tags without repetitions, preserving order. """
    seen = set()
    result = []
    for lst in lists:
        for item in lst:
            if item not in seen:
                seen.add(item)
                result.append(item)
    return result
