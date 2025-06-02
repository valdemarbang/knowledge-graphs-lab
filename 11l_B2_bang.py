from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD
import pandas as pd
import random

papers_csv = pd.read_csv('csv/papers_venues.csv', sep='|')

g = Graph()
LAB = Namespace("http://sdm_lab.org/")
g.bind("lab", LAB)

dummy_keywords = ["AI", "Blockchain", "Cybersecurity", "IoT", "NLP", "Cloud"]

for _, row in papers_csv.iterrows():
    paper_uri = URIRef(LAB + f"paper/{row['paperID']}")
    g.add((paper_uri, RDF.type, LAB.Paper))
    g.add((paper_uri, LAB.hasAbstract, Literal(row['abstract'], datatype=XSD.string)))

    # Edition and year
    if pd.notna(row['edition_id']):
        edition_uri = URIRef(LAB + f"edition/{row['edition_id']}")
        g.add((edition_uri, RDF.type, LAB.Edition))
        g.add((paper_uri, LAB.publishedInEdition, edition_uri))
        g.add((edition_uri, LAB.hasYear, Literal(int(row['year']), datatype=XSD.int)))

        if pd.notna(row['city_venue']):
            city_uri = URIRef(LAB + f"city/{row['city_venue'].strip().replace(' ', '_')}")
            g.add((city_uri, RDF.type, LAB.City))
            g.add((edition_uri, LAB.heldInCity, city_uri))

        # Dummy conference attached to edition
        conf_uri = URIRef(LAB + f"conference/{row['edition_id']}")
        venue_uri = URIRef(LAB + f"venue/{row['edition_id']}")
        g.add((conf_uri, RDF.type, LAB.Conference))
        g.add((conf_uri, LAB.isVenue, venue_uri))
        g.add((edition_uri, LAB.isHeldAtVenue, venue_uri))
        g.add((paper_uri, LAB.isPublishedInConference, conf_uri))

    # Authors and Person
    author_ids = str(row['authorIDs']).split(';')
    author_names = str(row['authorNames']).split(';')
    for aid in author_ids:
        author_uri = URIRef(LAB + f"author/{aid.strip()}")
        g.add((author_uri, RDF.type, LAB.Author))
        g.add((author_uri, LAB.isA, LAB.Person))
        g.add((paper_uri, LAB.hasAuthor, author_uri))

    # Citations
    if pd.notna(row['citedPaperID']):
        for cited_id in str(row['citedPaperID']).split(';'):
            cited_uri = URIRef(LAB + f"paper/{cited_id.strip()}")
            g.add((paper_uri, LAB.cites, cited_uri))

    # Volume and Journal
    if pd.notna(row['volume_id']):
        volume_uri = URIRef(LAB + f"volume/{row['volume_id']}")
        g.add((volume_uri, RDF.type, LAB.JournalVolume))
        g.add((paper_uri, LAB.publishedInVolume, volume_uri))

        if pd.notna(row['volume']):
            g.add((volume_uri, LAB.hasVolumeNumber, Literal(int(row['volume']), datatype=XSD.int)))

        if pd.notna(row['journal_name']):
            journal_uri = URIRef(LAB + f"journal/{row['journal_name'].strip().replace(' ', '_')}")
            g.add((journal_uri, RDF.type, LAB.Journal))
            g.add((volume_uri, LAB.partOfJournal, journal_uri))

    # Reviews
    if pd.notna(row['reviewerIDs']) and pd.notna(row['reviewsApprovements']) and pd.notna(row['reviewsDesc']):
        reviewer_ids = str(row['reviewerIDs']).split(';')
        for i, rid in enumerate(reviewer_ids):
            review_uri = URIRef(LAB + f"review/{row['paperID']}_{i}")
            reviewer_uri = URIRef(LAB + f"author/{rid.strip()}")
            g.add((review_uri, RDF.type, LAB.Review))
            g.add((review_uri, LAB.reviewOf, paper_uri))
            g.add((review_uri, LAB.hasReviewer, reviewer_uri))
            g.add((reviewer_uri, LAB.isA, LAB.Person))

    # Dummy keyword
    keyword = random.choice(dummy_keywords)
    g.add((paper_uri, LAB.hasKeyword, Literal(keyword, datatype=XSD.string)))

g.serialize(destination="11l_B2_bang.ttl", format="turtle")
print("ABOX generated with dummy keywords and conferences.")