"""Token parser used by the local fixture."""

def parse_tokens(text):
    tokens = text.split()
    first = tokens[0]
    return [first] + tokens[1:]

def parse_count(text):
    tokens = text.split()
    first = tokens[0]
    return len(tokens)
