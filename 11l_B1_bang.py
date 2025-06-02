from rdflib import Graph, Namespace, RDF, RDFS, Literal
from rdflib.namespace import XSD
from graphviz import Digraph

g = Graph()
LAB = Namespace("http://sdm_lab.org/")
g.bind("lab", LAB)

# Classes 
classes = [
    "Paper", "Author", "Reviewer", "Conference", "Workshop", "Edition", "Proceedings",
    "Journal", "JournalVolume", "Review", "City", "Person", "Venue", "Keywords"
]

for c in classes:
    g.add((LAB[c], RDF.type, RDFS.Class))

properties = [
    ("hasAuthor", "Paper", "Author"),
    ("hasKeyword", "Paper", "Keywords"),
    ("cites", "Paper", "Paper"),
    ("publishedInEdition", "Paper", "Edition"),
    ("publishedInVolume", "Paper", "JournalVolume"),
    ("isPublishedInConference", "Paper", "Conference"),
    ("isPublishedInWorkshop", "Paper", "Workshop"),
    ("hasProceedings", "Edition", "Proceedings"),
    ("heldInCity", "Edition", "City"),
    ("isHeldAtVenue", "Edition", "Venue"),
    ("hasYear", "Edition", "xsd:int"),
    ("partOfJournal", "JournalVolume", "Journal"),
    ("hasVolumeNumber", "JournalVolume", "xsd:int"),
    ("hasEditionNumber", "Edition", "xsd:int"),
    ("hasAbstract", "Paper", "xsd:string"),
    ("reviewOf", "Review", "Paper"),
    ("hasReviewer", "Review", "Author"),
    ("isA", "Reviewer", "Person"),
    ("isA", "Author", "Person"),
    ("isVenue", "Conference", "Venue"),
    ("isVenue", "Workshop", "Venue"),
]

# Add property declarations, domains, and ranges to RDF graph
for name, domain, range_ in properties:
    g.add((LAB[name], RDF.type, RDF.Property))
    if domain:
        g.add((LAB[name], RDFS.domain, LAB[domain]))
    if range_:
        if range_.startswith("xsd:"):
            g.add((LAB[name], RDFS.range, getattr(XSD, range_.split(":")[1])))
        else:
            g.add((LAB[name], RDFS.range, LAB[range_]))

g.serialize(destination="11l_B1_bang.ttl", format="turtle")
g.serialize(destination="11l_B1_bang.rdfs", format="xml")

dot = Digraph(comment='TBOX graph')
dot.attr('node', shape='box')

for cls in classes:
    dot.node(cls)

for prop, domain, rng in properties:
    if rng:
        dot.edge(domain, rng, label=prop)

dot.render("images/tbox_diagram", format='png', cleanup=True)