from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

tf = TriplesFactory.from_path('kge_triples.tsv')
training, testing = tf.split()

# best model from task C3
result = pipeline(
    training=training,
    testing=testing,
    model="TransE",
    model_kwargs=dict(embedding_dim=50),
    negative_sampler_kwargs=dict(num_negs_per_pos=5),
    random_seed=2025,
    device=device
)

entity_to_id = result.training.entity_to_id
embeddings = result.model.entity_representations[0](indices=None).detach().numpy()

# Extract author entities and their embeddings
author_ids = [e for e in entity_to_id if e.startswith("<http://sdm_lab.org/author/")]
author_indices = [entity_to_id[e] for e in author_ids]
author_embeddings = embeddings[author_indices]

# clustering with k means
kmeans = KMeans(n_clusters=3, random_state=2025)
labels = kmeans.fit_predict(author_embeddings)

# Too many dimensions to plot, reduce using PCA to 2 dimensions
pca = PCA(n_components=2)
points_2d = pca.fit_transform(author_embeddings)

plt.figure(figsize=(8, 6))
plt.scatter(points_2d[:, 0], points_2d[:, 1], c=labels, cmap='tab10', s=50)
plt.title("Author Clusters using PCA")
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.savefig("author_clusters_C4.png")
plt.show()