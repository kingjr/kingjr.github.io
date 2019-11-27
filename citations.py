import os
import pandas as pd

import re


papers = pd.read_csv('files/citations.csv')
years = papers.Year.fillna(0).astype(int)
papers = papers.fillna('').astype(str)
papers['Year'] = years
folder = './_publications'

# clear publication
for filename in os.listdir(folder):
    os.unlink(os.path.join(folder, filename))

for _, paper in papers.iterrows():
    first_author = paper.Authors.split(',')[0]
    first_words = '-'.join(paper.Title.split(' ')[:3])
    first_words = re.sub(r"[^A-Za-z]+", '', first_words)
    if paper.Year > 0:
        year = str(paper.Year)
    else:
        year = ''
    journal = str(paper.Publication)
    journal = '' if journal == 'nan' else journal
    permalink = '_'.join((year, journal, first_author, first_words))
    txt = '---\n'
    txt += "title: '%s'\n" % paper.Title
    txt += 'collection: publications\n'
    txt += 'permalink: /publications/%s\n' % permalink
    txt += 'venue: "%s"\n' % journal
    txt += 'date: %s\n' % year
    citation = "'%s et al (%s) %s, <i>%s</i>'"
    citation = citation % (first_author, year, paper.Title, journal)

    if len(paper.Volume):
        citation += ', %s' % paper.Volume
    if len(paper.Number):
        citation += '(%s)' % paper.Number
    if len(paper.Pages):
        citation += ': %s' % paper.Pages

    txt += 'citation: %s\n' % citation
    txt += '---\n'
    txt += '%s\n' % citation

    with open(os.path.join(folder, permalink+'.md'), 'w') as f:
        f.write(txt)
