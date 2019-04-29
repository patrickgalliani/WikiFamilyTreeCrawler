# WikiFamilyTreeCrawler
# Ricky Galliani


import json
from hashlib import sha1


class Figure:

    def __init__(self, name, wiki_extension):
        self.name = name
        self.wiki_extension = wiki_extension  # unique identifier
        self.born = None
        self.died = None
        self.parents = None
        self.spouses = None
        self.siblings = None
        self.children = None

    def __eq__(self, other):
        return (
            self.wiki_extension == other.wiki_extension
        ) or (
            self.name == other.name and
            self.born == other.born
        )

    def __hash__(self):
        return int(
            sha1("{}".format(self.wiki_extension)).hexdigest(), 16
        ) % (10 ** 8)

    def __repr__(self):
        return json.dumps({
            'name': self.name,
            'wiki_extension': self.wiki_extension,
            'born': self.born,
            # 'died': self.died,
            'parents':
                [] if self.parents is None
                else [s.name for s in self.parents],
            'spouses':
                [] if self.spouses is None
                else [s.name for s in self.spouses],
            # 'siblings': [s.name for s in self.siblings],
            'children':
                [] if self.children is None
                else [c.name for c in self.children]
        })
