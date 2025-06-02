import torch
from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory
from scipy.spatial.distance import euclidean

device = "cuda" if torch.cuda.is_available() else "cpu"

tf = TriplesFactory.from_path('kge_triples.tsv')

training, testing = tf.split()

result = pipeline(
    training=training,
    testing=testing,
    model="TransE",
    model_kwargs=dict(
        embedding_dim=128,
    ),
    training_kwargs=dict(
        num_epochs=20
    ),
    optimizer_kwargs=dict(
        lr=0.01,
    ),
    negative_sampler_kwargs=dict(
        num_negs_per_pos=1,
    ),
    random_seed=2025,
    device = device
)

model = result.model
entity_to_id = tf.entity_to_id
relation_to_id = tf.relation_to_id
id_to_entity = {v: k for k, v in entity_to_id.items()}

paper_entity = '<http://sdm_lab.org/paper/0a22389bd99b7efe3627ec6fc77ddaf3ff5e2faa>'
paper_vec = model.entity_representations[0](indices=torch.LongTensor([entity_to_id[paper_entity]])).detach().numpy()[0]

cites_vec = model.relation_representations[0](indices=torch.LongTensor([relation_to_id['<http://sdm_lab.org/cites>']])).detach().numpy()[0]
estimated_cited_vec = paper_vec + cites_vec

hasAuthor_vec = model.relation_representations[0](indices=torch.LongTensor([relation_to_id['<http://sdm_lab.org/hasAuthor>']])).detach().numpy()[0]
estimated_author_vec = estimated_cited_vec - hasAuthor_vec

# Loop through all authors to find the closest
closest_author = None
closest_distance = float('inf')

for entity, eid in entity_to_id.items():
    if 'author' in entity:  
        actual_vec = model.entity_representations[0](indices=torch.LongTensor([eid])).detach().numpy()[0]
        dist = euclidean(estimated_author_vec, actual_vec) # calc euclidean
        if dist < closest_distance:
            closest_author = entity
            closest_distance = dist

print(f"Closest author: {closest_author}")
print(f"Distance: {closest_distance}")