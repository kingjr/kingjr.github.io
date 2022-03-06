import os
import pandas as pd
import re
import unidecode


def format(string):
    string = unidecode.unidecode(string.replace(" ", "-").lower())
    return re.sub(r"[^a-z]+\-", "", string)


folder = "./_publications"
# https://scholar.google.com/citations?user=XZOgIwEAAAAJ&hl=en&oi=ao
# export
papers = pd.read_csv("citations.csv")  # download from google scholar

# clean up
years = papers.Year.fillna(0).astype(int)
papers.Year = years
papers = papers.fillna("").astype(str)
papers["day"] = papers.Publication.apply(lambda x: "-01-0%i" % (x != "nan"))
papers["date"] = years.apply(lambda x: str(x) if x > 0 else "") + papers.day

# clear publication
for filename in os.listdir(folder):
    os.unlink(os.path.join(folder, filename))

for _, paper in papers.iterrows():
    if paper.Year == "0":
        continue
    first_author = paper.Authors.split(",")[0]
    first_words = "-".join(paper.Title.split(" ")[:2])

    journal = str(paper.Publication)
    journal = "" if journal == "nan" else journal
    permalink = "_".join(
        (
            paper.date,
            format(journal),
            format(first_author),
            format(first_words),
        )
    )
    txt = "---\n"
    txt += "title: '%s'\n" % paper.Title
    txt += "collection: publications\n"
    # txt += 'permalink: /publications/%s\n' % permalink
    txt += 'permalink: "scholar.google.com/citations?user=XZOgIwEAAAAJ&hl=en&oi=ao"\n'  # noqa
    txt += 'excerpt: ""\n'
    txt += "date: %s\n" % paper.date
    txt += "authors: %s\n" % paper.Authors
    txt += 'venue: "%s"\n' % journal
    txt += 'paperurl: "scholar.google.com/citations?user=XZOgIwEAAAAJ&hl=en&oi=ao"\n'  # noqa
    citation = "%s et al (%s) %s, <i>%s</i>"
    citation = citation % (first_author, paper.Year, paper.Title, journal)

    if len(paper.Volume):
        citation += ", %s" % paper.Volume
    if len(paper.Number):
        citation += "(%s)" % paper.Number
    if len(paper.Pages):
        citation += ": %s" % paper.Pages

    txt += 'citation: "%s"\n' % citation
    txt += "---\n"
    txt += "%s\n" % citation

    # print(txt)

    with open(os.path.join(folder, permalink + ".md"), "w") as f:
        f.write(txt)
