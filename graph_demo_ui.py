# -*- coding: utf-8 -*-
# @Time    : 2024/6/8 16:16
# @Author  : nongbin
# @FileName: graph_demo_ui.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn

from flask import Flask, render_template, request, jsonify
import json
from dotenv import load_dotenv
from icecream import ic

from lang_chain.retriever.knowledge_graph_retriever import generate_graph_info

load_dotenv()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/update_graph', methods=['POST'])
def update_graph():
    raw_text = request.json.get('text', '')
    try:
        result = generate_graph_info(raw_text)
        if '```' in result:
            graph_data=json.loads(result.split('```',2)[1].replace("json", ''))
        else:
            graph_data=json.loads(result)
        ic(graph_data)
        return graph_data
    except Exception as e:
        return {'error': f"Error parsing graph data: {str(e)}"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
