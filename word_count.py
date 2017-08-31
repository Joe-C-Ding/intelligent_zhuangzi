# -*- coding: utf-8 -*-
from pprint import pprint
from time import clock

orig_txt = r'data/original_text.txt'
rslt_txt = r'result/word_count.txt'

# count for different characters
token = {}
# count total characters
chars = 0
# how long that a string should be consider as a word
wlen = 4


def count(token, line):
    length = len(line)
    for long in range(1, wlen+1):
        for i in range(length - long + 1):
            word = line[i:i+long]
            if word not in token:
                token[word] = 1
            else:
                token[word] += 1


def filter_word(token, key):
    if key not in token:
        return

    value = token[key]
    length = len(key)
    for long in range(1, length):
        for i in range(length - long + 1):
            word = key[i:i+long]
            if word in token and token[word] <= value:
                token.pop(word)


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

    # don't count punctuation or words appear only once or two
    punctuation = set(" ，。？！、：；‘’“”{}《》")
    # need to extract all keys now, cause token will change size during loop
    keys = list(token.keys())
    for k in keys:
        if punctuation & set(k):
            token.pop(k)
        elif len(k) > 1 and token[k] <= 2:
            token.pop(k)

    # `AB` is a part of `ABC`, so if the count of former is no more that of latter, remove the former
    ks = {k for k in token.keys() if len(k) > 1}
    for k in ks:
        filter_word(token, k)

    # calc frequency and sort the result
    result = [(item[0], item[1], item[1]/chars) for item in token.items()]
    result.sort(key=lambda x: x[1], reverse=True)

    with open(rslt_txt, 'wt', encoding='utf-8') as file:
        file.write("#\tchar\tcount\tfrequency\n")
        for r in result:
            file.write("\t{r[0]}\t{r[1]:4d}\t{r[2]:.6e}\n".format(r=r))

    pprint(result[0:10])

    print("elapsed {}s".format(clock() - start))
