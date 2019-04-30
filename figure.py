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
            self.name == other.name and
            self.wiki_extension == other.wiki_extension and
            self.name == other.name and
            self.born == other.born and
            self.died == other.died and
            self.parents == other.parents and
            self.spouses == other.spouses and
            self.siblings == other.siblings and
            self.children == other.children
        )
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        '''
        Returns True if self has more non-None fields than other.
        '''
        self_fields = [
            self.born is not None,
            self.died is not None,
            self.parents is not None,
            self.spouses is not None,
            self.siblings is not None,
            self.children is not None
        ]
        other_fields = [
            other.born is not None,
            other.died is not None,
            other.parents is not None,
            other.spouses is not None,
            other.siblings is not None,
            other.children is not None
        ]
        return sum(self_fields) > sum(other_fields)

    def __ge__(self, other):
        '''
        Returns True if self has greater than or equal to the number of
        non-None fields than other.
        '''
        self_fields = [
            self.born is not None,
            self.died is not None,
            self.parents is not None,
            self.spouses is not None,
            self.siblings is not None,
            self.children is not None
        ]
        other_fields = [
            other.born is not None,
            other.died is not None,
            other.parents is not None,
            other.spouses is not None,
            other.siblings is not None,
            other.children is not None
        ]
        return sum(self_fields) >= sum(other_fields)     

    def __lt__(self, other):
        '''
        Returns True if self has less non-None fields than other.
        '''
        return not self.__ge__(other)

    def __le__(self, other):
        '''
        Returns True if self has less than or equal to the number of
        non-None fields than other.
        '''
        return not self.__gt__(other)

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

    def to_dict(self):
        '''
        Returns self's data as a dictionary.
        '''
        d = {
            'name': self.name,
            'wiki_extension': self.wiki_extension
        }
        if self.born is not None:
            d['born'] = self.born
        if self.died is not None:
            d['died'] = self.died
        if self.parents:
            d['parents'] = list([x.wiki_extension for x in self.parents])
        if self.spouses:
            d['spouses'] = list([x.wiki_extension for x in self.spouses])
        if self.siblings:
            d['siblings'] = list([x.wiki_extension for x in self.siblings])
        if self.children:
            d['children'] = list([x.wiki_extension for x in self.children])
        return d
