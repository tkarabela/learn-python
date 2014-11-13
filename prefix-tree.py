#!/usr/bin/env python3

class Node:
    def __init__(self):
        self.children = {}
        self.end_of_word = False

    def collect_words(self):
        if self.end_of_word:
            yield ""

        for c, subtree in self.children.items():
            for w in subtree.collect_words():
                yield c + w

    def insert_word(self, word):
        if word == "":
            self.end_of_word = True
        else:
            first_letter = word[0]
            suffix = word[1:]

            subtree = self.children.setdefault(first_letter, Node())
            subtree.insert_word(suffix)

    def __contains__(self, word):
        node = self.find_node(word)
        return node is not None and node.end_of_word

    def find_node(self, prefix):
        if prefix == "":
            return self
        else:
            first_letter = prefix[0]
            suffix = prefix[1:]
            if first_letter in self.children:
                return self.children[first_letter].find_node(suffix)
            else:
                return None

    def find_by_prefix(self, prefix):
        node = self.find_node(prefix)
        if node is not None:
            for suffix in node.collect_words():
                yield prefix + suffix


WORDS = """
the be to of and a in that have I it for not on with he as you do at
this but his by from they we say her she or an will my one all would there their what
so up out if about who get which go me when make can like time no just him know take
people into year your good some could them see other than then now look only come its over think also
back after use two how our work first well way even new want because any these give day most us
""".strip().split()

def make_prefix_tree(words):
    root = Node()
    for word in words:
        root.insert_word(word)
    return root

def main():
    tree = make_prefix_tree(WORDS)

    print("Words starting with 'th':", *tree.find_by_prefix("th"))
    print("Is there a word 'they':", "they" in tree)
    print("Is there a word 'thorn':", "thorn" in tree)
    print("How many words are there:", sum(1 for word in tree.collect_words()))


if __name__ == "__main__":
    main()
