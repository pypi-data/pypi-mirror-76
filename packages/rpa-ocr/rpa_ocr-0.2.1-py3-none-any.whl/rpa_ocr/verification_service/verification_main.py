# -*- coding:utf-8 -*-
# @author :adolf
import os
import yaml

# from rpa_ocr.Identify_English.inference import CRNNInference
from rpa_ocr.Identify_English.inference import OnnxCRNNInfer


def ocr_pipeline_main(image_with_base64, app_scenes):
    # config_path = os.path.join('verification_service/config', scenes + '.yaml')
    # with open(config_path, 'r') as fp:
    #     config = yaml.load(fp.read(), Loader=yaml.FullLoader)
    #
    with open('rpa_ocr/verification_service/config.yaml', 'r') as fp:
        config = yaml.load(fp.read(), Loader=yaml.FullLoader)

    # print(base_config)
    # print(config)
    # for key, value in base_config.items():
    #     base_config[key] = config[key]

    # print(base_config)

    app_scenes_config = config.get(app_scenes, {})
    short_size = app_scenes_config.get("short_size", 32)
    alphabet_mode = app_scenes_config.get("alphabet_mode", "eng")
    verification_length = app_scenes_config.get("verification_length", 4)
    # crnn = CRNNInference(app_scenes=app_scenes,
    #                      model_path='model/',
    #                      short_size=short_size,
    #                      alphabet_mode=alphabet_mode,
    #                      verification_length=verification_length,
    #                      )
    # res_str = crnn.predict(image_with_base64)
    crnn_onnx = OnnxCRNNInfer(app_scenes=app_scenes,
                              model_path='model/',
                              short_size=short_size,
                              alphabet_mode=alphabet_mode,
                              verification_length=verification_length)
    res_str = crnn_onnx.predict(image_with_base64)
    return res_str


if __name__ == '__main__':
    import base64
    import random

    img_path = '/home/shizai/adolf/data/shandong/FKHV.png'
    with open(img_path, 'rb') as f:
        image = f.read()
        image_base64 = str(base64.b64encode(image), 'utf-8')

    ocr_predict = ocr_pipeline_main(image_base64, 'shandong')
    print(ocr_predict)

    # img_p = '/home/shizai/adolf/data/jindie/'
    # img_list = os.listdir(img_p)
    # random.shuffle(img_list)
    # total = 200
    # positive = 0
    # for img_name in img_list[:total]:
    #     with open(os.path.join(img_p, img_name), 'rb') as f:
    #         image = f.read()
    #         image_base64 = str(base64.b64encode(image), 'utf-8')
    #
    #     ocr_predict = ocr_pipeline_main(image_base64, 'jindie')
    #     # print(ocr_predict)
    #     # print(img_name)
    #     # print('---------')
    #     if ocr_predict == img_name.split('.')[0]:
    #         positive += 1
    #     else:
    #         print(img_name)
    #         print(ocr_predict)
    #
    # print('accuracy', positive / total)
