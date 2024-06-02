# -*- coding: utf-8 -*-
# @Time    : 2024/2/22 10:39
# @Author  : nongbin
# @FileName: webui_test.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn

import gradio as gr

with gr.Blocks() as demo:
   gr.Image(interactive=True)
   gr.Image(interactive=False)

demo.launch(share=True)