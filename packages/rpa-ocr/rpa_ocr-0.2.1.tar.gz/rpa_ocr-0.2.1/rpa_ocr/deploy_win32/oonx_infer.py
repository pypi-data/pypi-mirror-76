# -*- coding:utf-8 -*-
# @author :adolf
import numpy as np
import onnx
import onnxruntime as ort

model_path = "/datadisk4/adolf/ai+rpa/rpa_verification/model/shandong_verification.onnx"
# model = onnx.load('/datadisk4/adolf/ai+rpa/rpa_verification/model/xiaozhang_verification.onnx')

# print(model)
# rep = backend.prepare(model, device="CPU")  # "CPU" or CUDA:0

# outputs = rep.run(np.random.randn(1, 3, 32, 50).astype(np.float32))
print(ort.get_device())

ort_session = ort.InferenceSession(model_path)

outputs = ort_session.run(None, {'input': np.random.randn(1, 3, 64, 224).astype(np.float32)})

print(outputs[0])
