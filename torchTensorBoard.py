

from matplotlib import pyplot as plt
import torch
import numpy as np

from torch.utils.tensorboard import SummaryWriter, writer

X = torch.linspace(-0.5,0.5,200).reshape(-1,1)
# noise = torch.normal(torch.zeros(200),0.02).reshape(-1,1)
noise = torch.zeros(200).normal_(0,0.02).reshape(-1,1)
y = torch.square(X) + noise
plt.scatter(X.numpy(),y.numpy())
plt.show()

from torch.utils.data import Dataset,DataLoader

class MyDataSet(Dataset):
    def __init__(self):
        self.X = X
        self.y = y
    def __len__(self):
        return len(X)
    def __getitem__(self, idx):
        return {"X":self.X[idx],"y":self.y[idx]}

data = MyDataSet()

trainset, testset = torch.utils.data.random_split(data,[160,40])

traindatabatches = DataLoader(trainset,8)
testdatabatches = DataLoader(testset,8)


writer = SummaryWriter()

model = torch.nn.Sequential(
    torch.nn.Linear(1,10),
    torch.nn.Tanh(), 
    torch.nn.Linear(10,1))

criteron = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters())

for n in range(100):
    trainlosses = []
    for batch in traindatabatches:
        X0 = batch['X']
        y0 = batch['y']
        yhat = model(X0)
        loss = criteron(y0, yhat)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        trainlosses.append(loss.item())
    trainloss = np.mean(trainlosses)
    if n%10 == 0:
        with torch.no_grad():
            testlosses = []
            for batch in testdatabatches:
                X0 = batch['X']
                y0 = batch['y']
                yhat = model(X0)
                loss = criteron(y0, yhat)
                testlosses.append(loss.item())
            testloss = np.mean(testlosses)
            writer.add_scalars('train/loss',{"train":trainloss,"test":testloss}, n)
            # writer.add_scalar('test/loss',testloss,n)
            fig = plt.figure()
            predicts = model(X)
            plt.title(f'iter {n} prediction')
            plt.scatter(X.flatten().numpy(),y.flatten().numpy())
            plt.plot(X.flatten().numpy(),predicts.flatten().numpy(),color='r')
            writer.add_figure(f'predict plot',fig, n)

writer.add_graph(model,X)
