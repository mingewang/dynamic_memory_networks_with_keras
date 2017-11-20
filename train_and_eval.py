from dmn import DynamicMemoryNetwork
from preprocess_2 import load_dataset
import numpy as np
from keras import optimizers
batch_size = 50
emb_dim = 100
emb_location = '/home/penguinofdoom/Downloads/glove.6B/glove.6B.100d.txt'
babi_task_location = '/home/penguinofdoom/Downloads/tasks_1-20_v1-2/en-10k/qa1_single-supporting-fact_train.txt'
model_folder="dmn"
input_units = 16
episodic_memory_units = 16


x_train, q_train, y_train, max_len = load_dataset(babi_task_location, emb_location)

output_memory_units = len(y_train[0])

dmn_net = DynamicMemoryNetwork( model_folder=model_folder,
                                input_units=input_units,
                                memory_units=episodic_memory_units,
                                max_seq=3,
                                output_units=output_memory_units
                                )

print(x_train.shape)
print(q_train.shape)
print(y_train.shape)
dmn_net.build_inference_graph(x_train, q_train, batch_size=batch_size, dropout=0.3, units=100)
dmn_net.fit(x_train, q_train, y_train, batch_size=batch_size, epochs=256)
print("Model compiled")
