def fzmatch(haystack, needle, casesensitive=None):
    """Very simple fuzzy match, checks to see if all the characters in needed
    are in the haystack in left-to-right order.

    The function will attempt to match a space character, if no match is found
    space is ignored and moves on to matching the next character.

    Args:
        haystack        - text to search
        needed          - matching text
        casesensitive   - True = sensitive, False = insensitive, None = smart

    Returns:
        - match, score: Match pattern and Match score

        - If any of the characters are not found, (None, -1) is returned.

          Note: that the algorithm will not back-track, so if it matches 'x' and
          next character in needle is 'y' and there was an unmatched 'y' before
          'x' in haystack the match will fail.

        - Match pattern is a copy of haystack with any non-matching characters
          changed in to spaces.

        - Score reflects how good a match is, with sequencial characters having a
          better score than those spread out
    """
    if casesensitive is None:
        casesensitive = not needle.islower()

    result = ''
    length = len(haystack)
    idx = 0
    score = 1000
    for ch in needle:
        ch_score = 100
        while idx < length:
            # exact match advance one
            if ((casesensitive and ch == haystack[idx]) or
                    (not casesensitive and ch.lower() == haystack[idx].lower())):
                result += haystack[idx]
                idx += 1
                break

            # no match, but was space, ignore
            elif ch == ' ':
                break

            # no match, check next one
            ch_score -= 10
            result += ' '
            idx += 1

        else:
            # we hit the end of haystack without a match
            return None, -1

        score += ch_score

    # pad with spaces, since they didn't match
    while idx < length:
        result += ' '
        idx += 1
        score -= 1

    return result, score
