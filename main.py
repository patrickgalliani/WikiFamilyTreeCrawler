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

import json
import logging
import os
import requests


if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)-15s %(levelname)s: %(message)s',
        level=logging.INFO
    )
    log = logging.getLogger('main')


    seeds = [
        Figure('Barack Obama', 'Barack_Obama'),
        Figure('William Shakespeare', 'William_Shakespeare'),
        Figure('Napoleon', 'Napoleon'),
        Figure('Albert Einstein', 'Albert_Einstein'),
        Figure('John F. Kennedy', 'John_F._Kennedy')
    ]
    queue = seeds
    tree = []

    start_time = time()
    fig_count = 0
    while len(queue) > 0 and fig_count < 25:

        fig = queue.pop(0)
        url = "https://en.wikipedia.org/wiki/{}".format(fig.wiki_extension)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        try:
            fig.born = find_birthday(soup)
        except Exception, e:
            log.warning(
                "Can't find birthday for {} on wiki. ({})".format(fig.name, e)
            )

        try:
            ps = find_relatives(soup, r'Parent*')
            fig.parents = ps if fig.parents is None else fig.parents.union(ps)
            for p in fig.parents:
                # Enqueue all the unseen parents of this figure
                if p not in tree and p not in queue:
                    queue.append(p)
                # Ensure current fig is in list of parent's children
                if p.children is None:
                    p.children = set([fig])
                else:  # Already stored children for this parent
                    p.children.add(fig)
        except Exception, e:
            log.warning(
                "Can't find parents for {} on wiki. ({})".format(fig.name, e)
            )

        try:
            ss = find_relatives(soup, r'Spouse*')
            fig.spouses = ss if fig.spouses is None else fig.spouses.union(ss)
            for s in fig.spouses:
                # Enqueue all the unseen spouses of this figure
                if s not in tree and s not in queue:
                    queue.append(s)
                # Ensure current fig is in list of spouse's spouses
                if s.spouses is None:
                    s.spouses = set([fig])
                else:  # Already stored spouse(s) for this fig
                    s.spouses.add(fig)
        except Exception, e:
            log.warning(
                "Can't find spouse(s) for {} on wiki. ({})".format(fig.name, e)
            )

        try:
            cs = find_relatives(soup, r'Children')
            fig.children = cs if fig.children is None else fig.children.union(cs)
            for c in fig.children:
                # Enqueue all the unseen children of this figure
                if c not in tree and c not in queue:
                    queue.append(c)
                # Ensure current figure is in list of child's parents
                if c.parents is None:
                    c.parents = set([fig])
                else:  # Already added parent(s) for this figure
                    c.parents.add(fig)
        except Exception, e:
            log.warning("Can't find children for {}. ({})".format(fig.name, e))

        tree.append(fig)
        fig_count += 1
        sleep(randint(2, 10))

        log.info("Read data for {}".format(fig.name))
        log.info("Queue Size: {}, Fig Count: {}".format(len(queue), fig_count + 1))

    existing_figs = [
        "figures/{}".format(x) for x in os.listdir('figures')
    ]
    for i, fig in enumerate(tree):
        fig_file = os.path.join(
            'figures',
            "{}.json".format(fig.wiki_extension)
        )
        # Flag to determine whether to write figure data
        # Must write all the unseen figures
        write_fig = fig_file not in existing_figs
        # For all existing figures, see if we've found new data and need
        # to update
        if fig_file in existing_figs:
            existing_fig = None
            with open(fig_file, 'r') as f:
                try:
                    # Read in existing data
                    e = json.load(f)
                    existing_fig = {
                        'name': e['name'],
                        'wiki_extension': e['wiki_extension']
                    }
                    if 'born' in e:
                        existing_fig['born'] = e['born']
                    if 'died' in e:
                        existing_fig['died'] = e['died']
                    if 'parents' in e:
                        existing_fig['parents'] = e['parents']                        
                    if 'spouses' in e:
                        existing_fig['spouses'] = e['spouses'] 
                    if 'siblings' in e:
                        existing_fig['siblings'] = e['siblings'] 
                    if 'children' in e:
                        existing_fig['children'] = e['children'] 
                    # If new fig data is more complete than existing data,
                    # rewrite it
                    if len(fig.to_dict().keys()) > len(existing_fig.keys()):
                        write_fig = True
                        log.warning("Updating record for {} in {}.".format(
                                fig.name,
                                fig_file
                            )
                        )
                except ValueError, e:
                    log.error(
                        "Can't read existing data for {} in {}. ({})".format(
                            fig.name,
                            fig_file,
                            e
                        )
                    )
                    write_fig = True

        if write_fig:
            with open(fig_file, 'w') as f:
                json.dump(fig.to_dict(), f)
                log.info("{}) Wrote record for {} in {}.".format(
                        i + 1,
                        fig.name,
                        fig_file
                    )
                )
