from rdflib import Graph, RDF
from collections import Counter

# Load RDF graph
g = Graph()
g.parse("11l_B2_bang.ttl", format="turtle")

total_triples = len(g)

type_counts = Counter()
for s, p, o in g.triples((None, RDF.type, None)):
    type_counts[o] += 1

properties = set(g.predicates())

property_counts = Counter()
for s, p, o in g:
    property_counts[p] += 1

print(f"Total RDF Triples: {total_triples}")
print(f"Number of Classes: {len(type_counts)}")
print(f"Number of Properties: {len(properties)}")

print("\nInstances per Class:")
for cls, count in type_counts.items():
    print(f"  {cls.split('/')[-1]}: {count}")

print("\nTriples per Property:")
for prop, count in property_counts.items():
    print(f"  {prop.split('/')[-1]}: {count}")
