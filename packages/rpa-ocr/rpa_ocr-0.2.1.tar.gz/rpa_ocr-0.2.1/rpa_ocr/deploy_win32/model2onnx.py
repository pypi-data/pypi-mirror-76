# -*- coding:utf-8 -*-
# @author :adolf
from torch import nn
import torch.onnx
from rpa_ocr.Identify_English.crnn_model import CRNN


def convert_model(torch_model, onnx_path):
    # torch_model.load_state_dict(torch.load(model_path, map_location="cpu"))
    torch_model.eval()
    # x = torch.randn(batch_size, 1, 224, 224, requires_grad=True)
    x = torch.randn(1, 3, 64, 85).to('cpu')

    torch.onnx.export(
        torch_model,
        x,
        onnx_path,
        export_params=True,
        verbose=False,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={
            "input":
                {
                    0: "batch_size", 3: "w"
                },
            "output": {
                0: "batch_size"
            }
        }
    )


if __name__ == '__main__':
    torchmodel = CRNN(imgH=64, nc=3, nclass=63, nh=256)
    model_path = '/home/shizai/adolf/model/shandong_verification.pth'
    torchmodel.load_state_dict(torch.load(model_path, map_location="cpu"))
    convert_model(torch_model=torchmodel, onnx_path="model/shandong_verification.onnx")
