import torch
from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory

device = "cuda" if torch.cuda.is_available() else "cpu"
tf = TriplesFactory.from_path('kge_triples.tsv')
results = {}

models = ['TransE', 'DistMult', 'ComplEx'] 

dims = [50, 100]
negs = [1, 5]

training, testing = tf.split()


for model_name in models:
    for dim in dims:
        for negs_per_pos in negs:
            result = pipeline(
                training=training,
                testing=testing,
                model=model_name,
                model_kwargs=dict(embedding_dim=dim),
                negative_sampler_kwargs=dict(num_negs_per_pos=negs_per_pos),
                random_seed=2025,
                device = device
            )
            key = f"{model_name}_dim{dim}_negs{negs_per_pos}"
            results[key] = result.get_metric('mean_reciprocal_rank')

print("\nMRE:")
for k, v in results.items():
    print(f"{k}: {v:.4f}")
