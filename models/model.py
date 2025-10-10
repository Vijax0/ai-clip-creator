from torch import nn
import torch


def load_model(model, weights_path, device="cpu"):
    model.load_state_dict(torch.load(weights_path, weights_only=True))
    model.to(device)
    if device != "cpu":
        model.half()

    model.eval()
    return model


class Conv1dBlock(nn.Module):
    def __init__(self, in_features, out_features, kernel_size=3, stride=1, padding=1, dilation=1):
        super().__init__()

        self.conv1d = nn.Conv1d(in_features, out_features, kernel_size=kernel_size, stride=stride, padding=padding, dilation=dilation)
        self.instancenorm = nn.InstanceNorm1d(out_features, affine=True)
        self.relu = nn.ReLU()

    def forward(self, X):
        X = self.conv1d(X)
        X = self.instancenorm(X)
        X = self.relu(X)

        return X


class VideoAutoClipper(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv1dblock_1 = Conv1dBlock(40, 64)
        self.conv1dblock_2 = Conv1dBlock(64, 128, kernel_size=3, padding=2, dilation=2)

        self.conv1dblock_3 = Conv1dBlock(128, 256, kernel_size=3, padding=4, dilation=4)
        self.conv1dblock_4 = Conv1dBlock(256, 512, kernel_size=3, padding=8, dilation=8)

        self.conv1dblock_5 = Conv1dBlock(512, 1024, kernel_size=3, padding=16, dilation=16)
        self.conv1dblock_6 = Conv1dBlock(1024, 2048, kernel_size=3, padding=32, dilation=32)

        self.conv1dblock_7 = Conv1dBlock(2048, 4096, kernel_size=3, padding=16, dilation=16)
        self.conv1dblock_8 = Conv1dBlock(4096, 1024, kernel_size=3, padding=8, dilation=8)

        self.LSTM = nn.LSTM(1024, 1024, batch_first=True)
        self.conv1dblock_9 = Conv1dBlock(1024, 256, kernel_size=3, padding=2, dilation=2)

        self.dropout = nn.Dropout(0.5)
        self.conv1dfinal = nn.Conv1d(256, 1, kernel_size=1)

    def forward(self, X):
        X = self.conv1dblock_1(X)
        X = self.conv1dblock_2(X)

        X = self.conv1dblock_3(X)
        X = self.conv1dblock_4(X)

        X = self.conv1dblock_5(X)
        X = self.conv1dblock_6(X)

        X = self.conv1dblock_7(X)
        X = self.conv1dblock_8(X)

        X = X.view(X.size(0), X.size(2), X.size(1))
        X, _ = self.LSTM(X)
        X = X.view(X.size(0), X.size(2), X.size(1))
        X = self.conv1dblock_9(X)

        X = self.dropout(X)
        X = self.conv1dfinal(X)

        return X.squeeze()


class VideoAutoClipper2(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv1dblock_1 = Conv1dBlock(40, 64)
        self.conv1dblock_2 = Conv1dBlock(64, 128, kernel_size=3, padding=2, dilation=2)

        self.conv1dblock_3 = Conv1dBlock(128, 256, kernel_size=3, padding=4, dilation=4)
        self.conv1dblock_4 = Conv1dBlock(256, 512, kernel_size=3, padding=8, dilation=8)

        self.conv1dblock_5 = Conv1dBlock(512, 1024, kernel_size=3, padding=8, dilation=8)
        self.LSTM = nn.LSTM(1024, 1024, batch_first=True, bidirectional=True)

        self.conv1dblock_6 = Conv1dBlock(2048, 4096, kernel_size=1, padding=0)
        self.conv1dblock_7 = Conv1dBlock(4096, 8192, kernel_size=3, padding=8, dilation=8)

        self.conv1dblock_8 = Conv1dBlock(8192, 4096, kernel_size=3, padding=8, dilation=8)
        self.conv1dblock_9 = Conv1dBlock(4096, 2048, kernel_size=3, padding=8, dilation=8)

        self.conv1dblock_10 = Conv1dBlock(2048, 1024, kernel_size=3, padding=2, dilation=2)
        self.conv1dblock_11 = Conv1dBlock(1024, 512, kernel_size=3, padding=2, dilation=2)
    
        self.conv1dblock_12 = Conv1dBlock(512, 256, kernel_size=1, padding=0)
        self.dropout = nn.Dropout(0.5)
        self.conv1dfinal = nn.Conv1d(256, 1, kernel_size=1, padding=0)

    def forward(self, X):
        X = self.conv1dblock_1(X)
        X = self.conv1dblock_2(X)

        X = self.conv1dblock_3(X)
        X = self.conv1dblock_4(X)

        X = self.conv1dblock_5(X)
        X, _ = self.LSTM(X.view(X.size(0), X.size(2), X.size(1)))

        X = self.conv1dblock_6(X.view(X.size(0), X.size(2), X.size(1)))
        X = self.conv1dblock_7(X)

        X = self.conv1dblock_8(X)
        X = self.conv1dblock_9(X)

        X = self.conv1dblock_10(X)
        X = self.conv1dblock_11(X)

        X = self.conv1dblock_12(X)
        X = self.dropout(X)
        X = self.conv1dfinal(X)

        return X.squeeze()
