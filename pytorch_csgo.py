import os, glob, json
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()
        # self.linear_relu_stack = nn.Sequential(
        #     nn.Linear(6, 512),
        #     nn.ReLU(),
        #     nn.Linear(512, 512),
        #     nn.ReLU(),
        #     nn.Linear(512, 2),
        # )
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(6, 2)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

model = NeuralNetwork().to(device)

# logits = model(torch.tensor([data[1][0:6]]))
# pred_probab = nn.Softmax(dim=1)(logits)
# y_pred = pred_probab.argmax(1)
# print(f"Predicted class: {y_pred}")

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

def train(data, model, loss_fn, optimizer):
    N = 0
    size = len(data)
    model.train()
    for datatuple in data:
        X = datatuple[0]
        y = datatuple[1]
        X, y = X.to(device), y.to(device)

        # Compute prediction error
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if N % 1000 == 0:
            loss, current = loss.item(), N
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")
        N += 1

def test(data_test, model, loss_fn):
    size = len(data_test)
    model.eval()
    correct = 0
    test_loss = 0
    with torch.no_grad():
        for datatuple in data_test:
            X = datatuple[0]
            y = datatuple[1]
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%)\n")

traindata = json.load(open("traindata.json"))
finaltrain = []
for num in np.random.randint(0, len(traindata), 100000):
    finaltrain.append(tuple([torch.tensor([traindata[num][0:6]]), torch.tensor([traindata[num][6]])]))
testdata = json.load(open("testdata.json"))
finaltest = []
for num in np.random.randint(0, len(testdata), 10000):
    finaltest.append(tuple([torch.tensor([testdata[num][0:6]]), torch.tensor([testdata[num][6]])]))

epochs = 1
for t in range(epochs):
    print(f"Epoch {t+1}\n-------------------------------")
    train(finaltrain, model, loss_fn, optimizer)
    test(finaltest, model, loss_fn)
print("Done!")

# print(testdata[510][0:6])
# print(testdata[720][0:6])
# print(model(torch.tensor([testdata[510][0:6]])))
# print(model(torch.tensor([testdata[720][0:6]])))
