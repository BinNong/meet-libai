# -*- coding: utf-8 -*-
# @Time    : 2024/3/9 10:05
# @Author  : nongbin
# @FileName: model_error.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn

# 定义一些模型错误类型，包括模型加载错误，模型构建错误，模型推理错误等
class ModelError(Exception):
    code = -100


class ModelLoadError(ModelError):
    code = -1

    def __init__(self, message: str | None = None):
        super().__init__(f"Failed to load model: {message if message else ''}")


class ModelSaveError(ModelError):
    code = -2

    def __init__(self):
        super().__init__(f"Failed to save model")


class ModelBuildError(ModelError):
    code = -3

    def __init__(self, message: str = ""):
        super().__init__(f"Failed to build model: {message}")


class ModelInferenceError(ModelError):
    code = -4

    def __init__(self):
        super().__init__(f"Failed to perform inference on model")


class ModelDisplayError(ModelError):
    code = -5

    def __init__(self, message: str = ""):
        super().__init__(f"Failed to display model: {message}")
