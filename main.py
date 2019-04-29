# WikiFamilyTreeCrawler
# Ricky Galliani

from figure import Figure
from utils import (
    find_birthday,
    find_relatives
)

from bs4 import BeautifulSoup
from random import randint
from time import time, sleep

import requests


if __name__ == '__main__':

    seeds = [
        Figure('William Shakespeare', '/wiki/William_Shakespeare'),
        Figure('Napoleon', '/wiki/Napoleon'),
        Figure('Barack Obama', '/wiki/Barack_Obama'),
        Figure('Albert Einstein', '/wiki/Albert_Einstein'),
        Figure('John F. Kennedy', '/wiki/John_F._Kennedy')
    ]
    queue = seeds
    tree = []

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
                if parent not in tree and parent not in queue:
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
                if spouse not in tree and spouse not in queue:
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
                if child not in tree and child not in queue:
                    queue.append(child)
                # Ensure current figure is in list of child's parents
                if child.parents is None:
                    child.parents = set([figure])
                else:  # Already added parent(s) for this figure
                    child.parents.add(figure)
        except Exception, e:
            print("Error reading children for {}. {}".format(figure.name, e))

        tree.append(figure)
        print(figure)

        figure_count += 1
        sleep(randint(2, 10))
