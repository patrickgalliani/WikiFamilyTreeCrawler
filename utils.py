# WikiFamilyTreeCrawler
# Ricky Galliani


from figure import Figure

import re


def unwikify_name(wikified_name):
    return wikified_name.encode('utf-8').strip().replace('_', ' ')


def find_birthday(soup):
    return soup.find('span', {'class': 'bday'}).get_text()


def find_death_date(soup):
    return ''


def find_relatives(soup, pattern):
    tags = soup.find(
        'th', {'scope': 'row'}, text=re.compile(pattern)
    ).parent.find_all('a')
    relatives = set()
    for tag in tags:
        wiki_extension = (
        	tag['href'].encode('utf-8').strip().replace('/wiki/', '')
        )
        name = unwikify_name(wiki_extension)
        if any(c.isalpha() for c in name) and '#' not in wiki_extension:
            relative = Figure(name, wiki_extension)
            relatives.add(relative)
    return relatives
