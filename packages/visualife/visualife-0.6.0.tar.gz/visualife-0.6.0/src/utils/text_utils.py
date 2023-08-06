def fix_python_code(python_text):
    """Reformats Python source to correct some formatting issues.

    Python code copied & pasted or extracted from HTML page may be incorrectly formatted.
    This function attempts to fix the following:

      - proper indentation of the whole code
      - removes double quote characters on both ends of the text
    """
    python_text.replace('\t', ' ').strip('"')
    lines = python_text.split("\n")
    i = 0
    while lines[i].find("import") == -1: i += 1
    n_spaces = len(lines[i]) - len(lines[i].lstrip())
    out = ""
    for l in lines:
        out += l[n_spaces:] + "\n"
    return out


def consecutive_find(string, shortest_accepted=2, allowed_chars=[]):
    """Detects ranges of identical characters in a given string

    :param string: input string
    :param shortest_accepted: shortest substring accepted
    :param allowed_chars: list of allowed characters: the returned list will hold a given block if and only if
    its character is on the list; when the list is empty, all characters are allowed
    :return: a list of segments defining substrings of identical characters
    """

    current = 0
    next = 0
    i_start = 0
    list_of_blocks = []
    while True:
        next += 1
        while next != len(string) and string[current] == string[next]:
            current += 1
            next += 1

        if current - i_start + 1 >= shortest_accepted:
            if len(allowed_chars) == 0 or string[current] in allowed_chars:
                list_of_blocks.append([i_start,current,string[current]])
        current += 1
        i_start = current

        if next == len(string):
          return list_of_blocks


def substitute_template(template, subst_dict):
    """Simple text template replacement utility

    :param template: a template string
    :param subst_dict: dictionary of template_key:replacement pairs
    :return: result of all substitutions
    """
    for key, val in subst_dict.items():
        template = template.replace(key, str(val))

    return template


def from_string(text, first, last, default):
    s = text[first:last].strip()
    return s if len(s) > 0 else default
