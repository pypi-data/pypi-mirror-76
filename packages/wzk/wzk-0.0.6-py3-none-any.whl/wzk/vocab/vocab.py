vocab = None


class WordNotFoundError(Exception):
    def __init__(self, wd):
        self.wd = wd

    def __str__(self):
        return "word %s not found in vocabulary" % self.wd


def make_csv():
    import csv
    with open('../../words.csv') as f:
        reader = csv.reader(f)
        lines = list(reader)
        word_dict = {}
        for line in lines:
            word_dict[line[0]] = line[1]

    with open('vocabulary.txt', 'w') as out:
        print(word_dict, file=out)


def load_vocab():
    # global vocab
    # vocab_path = pkg_resources.resource_filename("wzk", "vocab/vocabulary.txt")
    # with open(vocab_path) as f:
    #     vocab = eval(f.read().strip())
    global vocab
    from .vocabulary import vocab as _vocab
    vocab = _vocab


def lookup(word):
    if vocab is None:
        load_vocab()
    if word in vocab.keys():
        return vocab[word]
    raise WordNotFoundError(word)


if __name__ == '__main__':
    print(lookup("book"))