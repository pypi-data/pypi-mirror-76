import websocket
import json
import keras
import numpy as np

websocket.enableTrace(False)

class SendStats(keras.callbacks.Callback):
  def __init__(self, link):
      self.link = link

  def on_train_begin(self, logs={}):
        self.val_loss = []
        self.loss = []
        self.acc = []
        self.val_acc = []
        self.lr = []
  def on_epoch_end(self, batch, logs={}):
    ws = websocket.create_connection(f"wss://schwarzam.art/ws/{self.link}/")

    dictionary ={
                "loss": np.round(logs.get('loss'), decimals=4),
                "val_loss":  np.round(logs.get('val_loss'), decimals=4),
                "acc":  np.round(logs.get('accuracy'), decimals=4),
                "val_acc":  np.round(logs.get('val_accuracy'), decimals=4),
                #"lr": step_decay(len(self.loss))
                }
    dictionary = json.dumps(dictionary)
    ws.send(dictionary)
