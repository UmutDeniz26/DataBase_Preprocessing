import torch
import os

print(torch.cuda.is_available())
torch.jit.load("UMUT/ms1m_v3_arcface_r100_fp16_constants.pth")


