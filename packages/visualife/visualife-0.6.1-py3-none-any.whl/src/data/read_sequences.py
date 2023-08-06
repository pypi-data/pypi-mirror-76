import re


def read_clustal(input_text, max_fields=3):

    seqdic = {}
    input_text = input_text.split('\n')
    for line in input_text:
        tokens = line.split()
        if len(tokens) > max_fields or len(tokens) < 2: continue
        if not re.match("[a-zA-Z\-_]",tokens[1]): continue
        if tokens[0] in seqdic:
            z = seqdic[tokens[0]]
            z = z + tokens[1]
            seqdic[tokens[0]] = z
        else:
            seqdic[tokens[0]] = tokens[1]
    for k, v in seqdic.items():
        seqdic[k] = seqdic[k].replace('.','-').replace('~','-')
    return seqdic


def read_msf(input_text):
    return read_clustal(input_text, 2)


def read_fasta(input_text):
    seqdic = {}
    while input_text:
        x = re.search('[>][^>]*',input_text)
        a_list = input_text[x.start():x.end()].split('\n',1)
        seqdic[a_list[0].strip(">")] = ''.join([s for s in a_list[1].strip().split()])
        input_text = input_text[x.end():]
    return seqdic