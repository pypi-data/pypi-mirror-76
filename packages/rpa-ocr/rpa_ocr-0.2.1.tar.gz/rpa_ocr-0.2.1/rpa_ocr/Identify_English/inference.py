# -*- coding:utf-8 -*-
# @author :adolf
import sys
import base64
from typing import List, Any

import cv2
import numpy as np
import os
import torch
import torchvision.transforms as transforms
from PIL import Image

from rpa_ocr.Identify_English.use_alphabet import *
from rpa_ocr.Identify_English.crnn_model import CRNN

# import onnx
import onnxruntime as ort

torch.set_printoptions(precision=8)


class CRNNInference:
    def __init__(self,
                 app_scenes=None,
                 alphabet_mode='eng',
                 short_size=32,
                 verification_length=4,
                 device='cpu',
                 model_path=None,
                 use_onnx=False):
        # general_config = params['GeneralConfig']
        # infer_config = params['InferenceConfig']
        if app_scenes is None:
            print('no app_scenes')
            # sys.exit(1)

        if model_path is None:
            print('no model_path')
            # sys.exit(1)
        self.app_scenes = app_scenes
        print('app_scenes:', app_scenes)

        alphabet = self.read_alphabet(alphabet_mode)
        self.alphabet_dict = {alphabet[i]: i for i in range(len(alphabet))}
        self.decode_alphabet_dict = {v: k for k, v in self.alphabet_dict.items()}

        self.short_size = short_size
        self.verification_length = verification_length

        self.device = device
        self.model_path = os.path.join(model_path,
                                       self.app_scenes + "_verification.pth")
        #
        if use_onnx:
            self.model_path = os.path.join(model_path, self.app_scenes + "_verification.onnx")

        self.transform = transforms.Compose([transforms.ToTensor()])

        self.model = CRNN(imgH=self.short_size, nc=3, nclass=len(alphabet), nh=256)
        # self.init_torch_tensor()
        self.resume()
        if not use_onnx:
            self.model.eval()

        print('success！')

    def init_torch_tensor(self):
        torch.set_default_tensor_type('torch.FloatTensor')
        if self.device != "cpu":
            torch.set_default_tensor_type('torch.cuda.FloatTensor')

    def resume(self):
        self.model.load_state_dict(torch.load(self.model_path, map_location=self.device), strict=True)
        self.model.to(self.device)

    @staticmethod
    def base64_to_opencv(image_base64):
        img = base64.b64decode(image_base64)
        img_array = np.frombuffer(img, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return img

    @staticmethod
    def read_alphabet(alphabet_mode):
        # res_list = list()
        if alphabet_mode == "eng":
            alphabet = english_alphabet
        elif alphabet_mode == "ENG":
            alphabet = english_alphabet_big
        else:
            alphabet = chinese_alphabet

        return alphabet

    def model_infer(self, img):
        with torch.no_grad():
            output = self.model(img)
        output = output.squeeze()
        # print(output.shape)
        _, preds = output.max(1)
        preds_list = preds.tolist()
        # print(preds_list)
        return preds_list

    def predict(self, image):
        if isinstance(image, np.ndarray):
            img = image
        else:
            if isinstance(image, str):
                img = self.base64_to_opencv(image)
            elif isinstance(image, Image.Image):
                img = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)

        imgW = int(img.shape[1] * self.short_size / img.shape[0])
        img = cv2.resize(img, (imgW, self.short_size))

        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # img = img[:, :, :, np.newaxis]
        # print(img.shape)
        img = self.transform(img)
        # img = (img / 255.).astype(np.float32)
        # print(img.dtype)
        # img = torch.from_numpy(img).permute(2, 0, 1)
        # print(img.size())
        img = img.unsqueeze(0)
        # with torch.no_grad():
        #     # print(img.size())
        #     # print(img[0][0][0][0])
        #     # print(img)
        #     output = self.model(img)
        preds_list = self.model_infer(img)
        # print(output)
        # print(output.shape)
        preds_decode_list: List[Any] = [self.decode_alphabet_dict[i] for i in preds_list]
        res_str: str = ""

        for i in range(len(preds_decode_list)):
            if i == 0 and preds_decode_list[i] != '-':
                res_str += preds_decode_list[i]
            if preds_decode_list[i] != preds_decode_list[i - 1] and preds_decode_list[i] != '-':
                res_str += preds_decode_list[i]

        # print(res_str)
        if len(res_str) > self.verification_length:
            res_str = res_str[-self.verification_length:]
        return res_str


class OnnxCRNNInfer(CRNNInference):
    def __init__(self, app_scenes=None,
                 alphabet_mode='eng',
                 short_size=32,
                 verification_length=4,
                 device='cpu',
                 model_path=None):
        self.app_scenes = app_scenes
        self.alphabet_mode = alphabet_mode
        self.short_size = short_size
        self.verification_length = verification_length
        self.device = device
        self.model_path = model_path

        super().__init__(app_scenes=self.app_scenes,
                         alphabet_mode=self.alphabet_mode,
                         short_size=self.short_size,
                         verification_length=self.verification_length,
                         device=self.device,
                         model_path=self.model_path,
                         use_onnx=True)
        # print()

    def resume(self):
        # self.model = onnx.load(self.model_path)
        # self.model.to(self.device)
        # print(self.model_path)
        self.model = ort.InferenceSession(self.model_path)

    def model_infer(self, img):
        img = img.to(self.device).numpy().astype(np.float32)
        outputs = self.model.run(None, {'input': img})
        # print(outputs)
        output = outputs[0]
        # print(output)
        output = output.squeeze()
        # print(output)
        # print(output.shape)
        preds = output.argmax(1)
        preds_list = preds.tolist()
        # print(preds_list)
        return preds_list


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Params to use fro train algorithm")
    parser.add_argument("--app_scenes", "-sc", type=str,
                        default=argparse.SUPPRESS, nargs='?', help="what scenes this model used")
    parser.add_argument("--alphabet_mode", "-a", type=str,
                        default="eng", nargs='?', help="alphabet what is used,'eng','ch','ENG'")
    parser.add_argument("--model_path", "-m", type=str,
                        default=argparse.SUPPRESS, nargs='?', help="path to save model")
    parser.add_argument("--short_size", "-sh", type=int,
                        default=64, nargs='?', help="short_size has to be a multiple of 16")
    parser.add_argument("--verification_length", "-v", type=int, const=True,
                        default=4, nargs='?', help="length of verification")
    parser.add_argument("--device", "-dev", type=str,
                        default="cpu", nargs='?', help="use cpu or gpu;'cpu' or 'cuda'")
    args = parser.parse_args()

    args.app_scenes = 'shandong'
    args.model_path = 'model/'

    crnn = CRNNInference(app_scenes=args.app_scenes,
                         alphabet_mode=args.alphabet_mode,
                         model_path=args.model_path,
                         short_size=args.short_size,
                         verification_length=args.verification_length,
                         device=args.device)

    # crnn_onnx = OnnxCRNNInfer(app_scenes=args.app_scenes,
    #                           alphabet_mode=args.alphabet_mode,
    #                           model_path=args.model_path,
    #                           short_size=args.short_size,
    #                           verification_length=args.verification_length,
    #                           device=args.device)

    # image = cv2.imread('/home/shizai/adolf/ai+rpa/rpa_verification/generate_verification/gen_ver/h6aD.png')
    # image = cv2.imread('test_imgs/2BPX.png')
    image = cv2.imread('test_imgs/5VAH.png')
    #
    print(crnn.predict(image=image))
    # print('========================')
    # print(crnn_onnx.predict(image=image))
