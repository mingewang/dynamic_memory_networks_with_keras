# Adopted from https://github.com/vchudinov/dynamic_memory_networks_with_keras
#
# python3 train_and_eval.py --settings_file ./my.json

from dmn import DynamicMemoryNetwork
from preprocess import load_dataset
from keras import optimizers
import json
import argparse

parser = argparse.ArgumentParser(description='DMN+ Trainer')
parser.add_argument('--settings_file', type=str,
                    help='path to a json with settings')

settings = parser.parse_args()
config_file = settings.settings_file
json_data=open(config_file).read()
settings = json.loads(json_data)

print("----- Loading Dataset ----")

max_len, trainset, testset = load_dataset(emb_location=settings["path_to_embeddings"],
                                           babi_location=settings["path_to_train_task"],
                                           babi_test_location=settings["path_to_test_task"],
                                           emb_dim=settings["embeddings_size"])

input_shape = trainset[0][0].shape
question_shape = trainset[1][0].shape
num_classes = len(trainset[2][0])

print("----- Dataset Loaded. Compiling Model -----")
dmn_net = DynamicMemoryNetwork(save_folder=settings["model_folder"])
dmn_net.build_inference_graph(
    input_shape=input_shape,
    question_shape=question_shape,
    num_classes=num_classes,
    units=settings["hidden_units"],
    batch_size=settings["batch_size"],
    memory_steps=settings["memory_steps"],
    l_rate=settings["learning_rate"],
    l_decay=settings["learning_decay"],
    dropout=settings["dropout"])

print("------ Model Compiled. Training -------")

#dmn_net.load_weights( settings["model_folder"] + "/dmn-{epoch:02d}_trained")
dmn_net.fit(trainset[0], trainset[1], trainset[2],
            epochs=settings["epochs"],
            validation_split=settings["validation_split"],
            l_rate= settings["learning_rate"],
            l_decay=settings["learning_decay"],)

if testset is not None:
    print("----- Model Trained. Evaluating -----")
    loss, acc = dmn_net.model.evaluate(x=[testset[0], testset[1]],y=testset[2], batch_size=settings["batch_size"])
    print("Test Loss: {}, Test Accuracy: {}".format(loss,acc))


