import torch.nn as nn
import torch.nn.functional as F
import torch
import numpy as np
from loss import *

class MultiDAE(nn.Module):
    """
    Container module for Multi-DAE.

    Multi-DAE : Denoising Autoencoder with Multinomial Likelihood
    See Variational Autoencoders for Collaborative Filtering
    https://arxiv.org/abs/1802.05814
    """

    def __init__(self, p_dims, q_dims=None, dropout=0.5):
        super(MultiDAE, self).__init__()
        self.p_dims = p_dims
        if q_dims:
            assert q_dims[0] == p_dims[-1], "In and Out dimensions must equal to each other"
            assert q_dims[-1] == p_dims[0], "Latent dimension for p- and q- network mismatches."
            self.q_dims = q_dims
        else:
            self.q_dims = p_dims[::-1]

        self.dims = self.q_dims + self.p_dims[1:]
        self.layers = nn.ModuleList([nn.Linear(d_in, d_out) for
            d_in, d_out in zip(self.dims[:-1], self.dims[1:])])
        self.drop = nn.Dropout(dropout)
        
        self.init_weights()
    
    def forward(self, input):
        h = F.normalize(input)
        h = self.drop(h)

        for i, layer in enumerate(self.layers):
            h = layer(h)
            if i != len(self.layers) - 1:
                h = F.tanh(h)
        return h

    def init_weights(self):
        for layer in self.layers:
            # Xavier Initialization for weights
            size = layer.weight.size()
            fan_out = size[0]
            fan_in = size[1]
            std = np.sqrt(2.0/(fan_in + fan_out))
            layer.weight.data.normal_(0.0, std)

            # Normal Initialization for Biases
            layer.bias.data.normal_(0.0, 0.001)



class MultiVAE(nn.Module):
    """
    Container module for Multi-VAE.

    Multi-VAE : Variational Autoencoder with Multinomial Likelihood
    See Variational Autoencoders for Collaborative Filtering
    https://arxiv.org/abs/1802.05814
    """

    def __init__(self, p_dims, q_dims=None, dropout=0.5):
        super(MultiVAE, self).__init__()
        self.p_dims = p_dims #[200, 600, 6807]
        if q_dims: # 만약 encoder 차원을 decoder와 다르게 설정하고 싶다면, 입력해주면 된다. 다만 encoder의 output 차원과 decoder의 input 차원이 동일해야 된다.
            assert q_dims[0] == p_dims[-1], "In and Out dimensions must equal to each other"
            assert q_dims[-1] == p_dims[0], "Latent dimension for p- and q- network mismatches."
            self.q_dims = q_dims
        else:
            self.q_dims = p_dims[::-1] # [6807, 600, 200] decoder의 반대로 차원 설정 -> 마지막에 도출하는 평균, 분산 값이 각각 200개씩 있다. 

        # Last dimension of q- network is for mean and variance
        temp_q_dims = self.q_dims[:-1] + [self.q_dims[-1] * 2] # temp_q_dims = [6807, 600, 400] -> 마지막 차원을 2배 해주는 것은 평균과 분산을 따로 구해야 되기 때문이다.
        self.q_layers = nn.ModuleList([nn.Linear(d_in, d_out) for
            d_in, d_out in zip(temp_q_dims[:-1], temp_q_dims[1:])]) # encoder : nn.Linear([6807, 600]), nn.Linear([600, 400])
        self.p_layers = nn.ModuleList([nn.Linear(d_in, d_out) for
            d_in, d_out in zip(self.p_dims[:-1], self.p_dims[1:])]) # decoder : nn.Linear([200, 600]) , nn.Linear([600,6807])
        
        self.drop = nn.Dropout(dropout)
        self.init_weights()
    
    def forward(self, input):
        mu, logvar = self.encode(input) # encoder를 통해 평균과 로그 분산 계산
        z = self.reparameterize(mu, logvar) # 평균과 분산으로 sampling -> 해당 경우 유저별로 200개의 값이 나온다
        return self.decode(z), mu, logvar # sample들을 decoder에 넣어 최종 확률 값 도출 #R끝끝
    
    def encode(self, input):
        h = F.normalize(input) # 값들을 정규화
        h = self.drop(h) # dropout rate으로 값들을 무작위로 0으로 만들어준다 -> 시청한 item만 원래 포함하고 있지만, overfitting을 방지하기 위해 몇개를 0으로 바꿔준다.
        
        for i, layer in enumerate(self.q_layers): 
            h = layer(h) 
            if i != len(self.q_layers) - 1: # 만약 마지막이 아니라면, tanh를 씌워준다
                h = F.tanh(h)
            else: # 만약 마지막 layer라면
                mu = h[:, :self.q_dims[-1]] # 결과 값의 [0 : 200]은 평균
                logvar = h[:, self.q_dims[-1]:] # 결과 값의 [200 : 400]은 분산
        return mu, logvar

    def reparameterize(self, mu, logvar):
        if self.training:
            std = torch.exp(0.5 * logvar) # e^(0.5*log(std^2)) = e^log(std) = std
            eps = torch.randn_like(std) # std의 차원만큼 N(0,1) normal distribution에서 추출
            return eps.mul(std).add_(mu) # eps x std + mu
        else:
            return mu
    
    def decode(self, z):
        h = z
        for i, layer in enumerate(self.p_layers): 
            h = layer(h)
            if i != len(self.p_layers) - 1: # 만약 마지막 layer가 아니라면 tanh를 씌워준다
                h = F.tanh(h) # TODO : 왜 마지막에 softmax를 씌워주지 않는가?
                # softmax을 씌우지 않은 값이 loss function에서 사용되기 때문에

        return h

    def init_weights(self):
        for layer in self.q_layers:
            # Xavier Initialization for weights
            size = layer.weight.size()
            fan_out = size[0]
            fan_in = size[1]
            std = np.sqrt(2.0/(fan_in + fan_out))
            layer.weight.data.normal_(0.0, std)

            # Normal Initialization for Biases
            layer.bias.data.normal_(0.0, 0.001)
        
        for layer in self.p_layers:
            # Xavier Initialization for weights
            size = layer.weight.size()
            fan_out = size[0]
            fan_in = size[1]
            std = np.sqrt(2.0/(fan_in + fan_out))
            layer.weight.data.normal_(0.0, std)

            # Normal Initialization for Biases
            layer.bias.data.normal_(0.0, 0.001)