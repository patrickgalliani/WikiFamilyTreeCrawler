from bs4 import BeautifulSoup
from datetime import datetime
from hashlib import sha1
from random import randint
from time import time, sleep

import json
import re
import requests
import sys


def unwikify_name(wikified_name):
    return wikified_name.encode('utf-8').strip().replace('_', ' ')


class Figure:
    def __init__(self, name, wiki_extension):
        self.name = name
        self.wiki_extension = wiki_extension
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
                [] if self.parents is None else [s.name for s in self.parents],
            'spouses': 
                [] if self.spouses is None else [s.name for s in self.spouses],
            # 'siblings': [s.name for s in self.siblings],
            'children':
                [] if self.children is None else [c.name for c in self.children]
        })


def find_birthday(soup):
    return soup.find('span', {'class' : 'bday'}).get_text()


def find_death_date(soup):
    return ''


def find_relatives(soup, pattern):
    tags = soup.find(
        'th', {'scope': 'row'}, text=re.compile(pattern)
    ).parent.find_all('a')
    relatives = set()
    for tag in tags:
        name = unwikify_name(tag.text)
        wiki_extension = tag['href'].encode('utf-8').strip()
        if any(c.isalpha() for c in name) and '#' not in wiki_extension:
            relative = Figure(name, wiki_extension)
            relatives.add(relative)
    return relatives


if __name__ == '__main__':
   
    seeds = [
        Figure('Napoleon', '/wiki/Napoleon'),
        Figure('Barack Obama', '/wiki/Barack_Obama'),
        Figure('Albert Einstein', '/wiki/Albert_Einstein'),
        Figure('John F. Kennedy', '/wiki/John_F._Kennedy')
    ]
    queue = seeds
    seen = []

    start_time = time()
    figure_count = 1
    while len(queue) > 0:

        figure = queue.pop(0)
        url = "https://en.wikipedia.org{}".format(figure.wiki_extension)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        try:
            figure.born = find_birthday(soup) 
        except Exception, e:
            print("Error finding birthday for {}. {}".format(figure.name, e))

        try:
            parents = find_relatives(soup, r'Parent*')
            figure.parents = (
                parents if figure.parents is None 
                else figure.parents.union(parents)  
            )

            for parent in figure.parents:
                # Enqueue all the unseen parents of this figure
                if parent not in seen and parent not in queue:
                    queue.append(parent)

                # Ensure current figure is in list of parent's children
                if parent.children is None:
                    parent.children = set([figure])
                else:  # Already stored spouse(s) for this figure
                    parent.children.add(figure)
             
        except Exception, e:
            print("Error reading parents for {}. {}".format(figure.name, e))

        try:
            spouses = find_relatives(soup, r'Spouse*')
            figure.spouses = (
                spouses if figure.spouses is None 
                else figure.spouses.union(spouses)  
            )

            for spouse in figure.spouses:
                # Enqueue all the unseen spouses of this figure
                if spouse not in seen and spouse not in queue:
                    queue.append(spouse)

                # Ensure current figure is in list of spouse's spouses
                if spouse.spouses is None:
                    spouse.spouses = set([figure])
                else:  # Already stored spouse(s) for this figure
                    spouse.spouses.add(figure)
             
        except Exception, e:
            print("Error reading spouses for {}. {}".format(figure.name, e))

        try:
            children = find_relatives(soup, r'Children')
            figure.children = (
                children if figure.children is None
                else figure.children.union(children)
            )

            for child in figure.children:
                # Enqueue all the unseen children of this figure
                if child not in seen and child not in queue:
                    queue.append(child)

                # Ensure current figure is in list of child's parents
                if child.parents is None:
                    child.parents = set([figure])
                else:  # Already added parent(s) for this figure
                    child.parents.add(figure) 

        except Exception, e:
            print("Error reading children for {}. {}".format(figure.name, e))

        seen.append(figure)

        print("{} (in queue: {})) {}: {}".format(figure_count, len(queue), figure.name, figure))

        figure_count += 1
        sleep(randint(2, 10))
