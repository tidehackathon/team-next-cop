import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import time
import os
import cv2

DRON_PATH = "./dron/"
MAP_MOLES_PATH = "./map/"
IMAGE_SIZE = 224

def cycle(file_pass, array_name, array_label):
  for root, dirs, files in os.walk(file_pass): 
    for i, j in enumerate(files):
      if(".png" in j):       
        img = cv2.imread(f"{file_pass}/{j}")

        if img is None:
            print('Wrong path:', f"{file_pass}/{j}")
        else:
            array_name.append(cv2.cvtColor(cv2.resize( img, (224, 224)), cv2.COLOR_RGB2GRAY))
        
        

        # adding a photo label depending on the folder
        if root == DRON_PATH:
          label_array.append(1)
        else:
          label_array.append(0)
        
        
all_im_array = []
label_array = []

cycle(DRON_PATH, all_im_array, label_array)
cycle(MAP_MOLES_PATH, all_im_array, label_array)


images = np.array(all_im_array)
labels = np.array(label_array)

bit_model = tf.keras.models.load_model("flower_model_bit_0.96875")
bit_model.count_params()


embedding_model = tf.keras.Sequential(
    [
        tf.keras.layers.Input((IMAGE_SIZE, IMAGE_SIZE, 3)),
        tf.keras.layers.Rescaling(scale=1.0 / 255),
        bit_model.layers[1],
        tf.keras.layers.Normalization(mean=0, variance=1),
    ],
    name="embedding_model",
)

def hash_func(embedding, random_vectors):
    embedding = np.array(embedding)

    # Random projection.
    bools = np.dot(embedding, random_vectors) > 0
    return [bool2int(bool_vec) for bool_vec in bools]


def bool2int(x):
    y = 0
    for i, j in enumerate(x):
        if j:
            y += 1 << i
    return y


class Table:
    def __init__(self, hash_size, dim):
        self.table = {}
        self.hash_size = hash_size
        self.random_vectors = np.random.randn(hash_size, dim).T

    def add(self, id, vectors, label):
        # Create a unique indentifier.
        entry = {"id_label": str(id) + "_" + str(label)}

        # Compute the hash values.
        hashes = hash_func(vectors, self.random_vectors)

        # Add the hash values to the current table.
        for h in hashes:
            if h in self.table:
                self.table[h].append(entry)
            else:
                self.table[h] = [entry]

    def query(self, vectors):
        # Compute hash value for the query vector.
        hashes = hash_func(vectors, self.random_vectors)
        results = []

        # Loop over the query hashes and determine if they exist in
        # the current table.
        for h in hashes:
            if h in self.table:
                results.extend(self.table[h])
        return results
    
    
class LSH:
    def __init__(self, hash_size, dim, num_tables):
        self.num_tables = num_tables
        self.tables = []
        for i in range(self.num_tables):
            self.tables.append(Table(hash_size, dim))

    def add(self, id, vectors, label):
        for table in self.tables:
            table.add(id, vectors, label)

    def query(self, vectors):
        results = []
        for table in self.tables:
            results.extend(table.query(vectors))
        return results
    
    
class BuildLSHTable:
    def __init__(
        self,
        prediction_model,
        concrete_function=False,
        hash_size=8,
        dim=2048,
        num_tables=10,
    ):
        self.hash_size = hash_size
        self.dim = dim
        self.num_tables = num_tables
        self.lsh = LSH(self.hash_size, self.dim, self.num_tables)

        self.prediction_model = prediction_model
        self.concrete_function = concrete_function

    def train(self, training_files):
        for id, training_file in enumerate(training_files):
            # Unpack the data.
            image, label = training_file
            if len(image.shape) < 4:
                image = image[None, ...]

            # Compute embeddings and update the LSH tables.
            # More on `self.concrete_function()` later.
            if self.concrete_function:
                features = self.prediction_model(tf.constant(image))[
                    "normalization"
                ].numpy()
            else:
                features = self.prediction_model.predict(image)
            self.lsh.add(id, features, label)

    def query(self, image, verbose=True):
        # Compute the embeddings of the query image and fetch the results.
        if len(image.shape) < 4:
            image = image[None, ...]

        if self.concrete_function:
            features = self.prediction_model(tf.constant(image))[
                "normalization"
            ].numpy()
        else:
            features = self.prediction_model.predict(image)

        results = self.lsh.query(features)
        if verbose:
            print("Matches:", len(results))

        # Calculate Jaccard index to quantify the similarity.
        counts = {}
        for r in results:
            if r["id_label"] in counts:
                counts[r["id_label"]] += 1
            else:
                counts[r["id_label"]] = 1
        for k in counts:
            counts[k] = float(counts[k]) / self.dim
        return counts
# Utility to warm up the GPU.
def warmup():
    dummy_sample = tf.ones((1, IMAGE_SIZE, IMAGE_SIZE, 3))
    for _ in range(100):
        _ = embedding_model.predict(dummy_sample)
        
warmup()

training_files = zip(images, labels)
lsh_builder = BuildLSHTable(embedding_model)
lsh_builder.train(training_files)