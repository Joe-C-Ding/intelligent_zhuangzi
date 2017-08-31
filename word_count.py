# -*- coding: utf-8 -*-
from pprint import pprint
from time import clock

orig_txt = r'data/original_text.txt'
rslt_txt = r'result/word_count.txt'

# count for different characters
token = {}
# count total characters
chars = 0


def count(token, line):
    for char in line:
        try:
            token[char] += 1
        except KeyError:
            token[char] = 1

if __name__ == '__main__':
    start = clock()

    with open(orig_txt, 'rt', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            # skip empty line or comments
            if not line or line[0] == '#':
                continue
            # skip names of title, volume or chapter
            if line[-4:-1] == '{{{':
                continue

            chars += len(line)
            count(token, line)

    # don't count punctuation
    for c in " ，。？！、：；‘’“”{}《》":
        token.pop(c, 0)

    # calc frequency and sort the result
    result = [(item[0], item[1], item[1]/chars) for item in token.items()]
    result.sort(key=lambda x: x[1], reverse=True)

    with open(rslt_txt, 'wt', encoding='utf-8') as file:
        file.write("#\tchar\tcount\tfrequency\n")
        for r in result:
            file.write("\t{r[0]}\t{r[1]:4d}\t{r[2]:.6e}\n".format(r=r))

    print("species {}; counts: {}".format(len(token), chars))
    pprint(result[0:10])

    print("elapsed {}s".format(clock() - start))
