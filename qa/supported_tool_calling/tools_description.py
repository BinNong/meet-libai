# -*- coding: utf-8 -*-
# @Time    : 2024/8/28 17:35
# @Author  : nongbin
# @FileName: tools_description.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn

GET_PERSONAL_PROFILE = {
    "type": "function",
    "function": {
        "name": "get_personal_profile",
        "description": "根据人的姓名，介绍这个人的基本信息",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "人的姓名",
                },
            }
        },
        "required": ["name"]
    }
}

GET_RELATION_INFO = {
    "type": "function",
    "function": {
        "name": "get_relation_info",
        "description": "根据两个人的姓名，获取两个人的关联信息",
        "parameters": {
            "type": "object",
            "properties": {
                "first_entity_name": {
                    "type": "string",
                    "description": "第一个人的姓名",
                },
                "second_entity_name": {
                    "type": "string",
                    "description": "第二个人的姓名",
                }
            }
        }
    }
}

GET_HELLO_INFO = {
    "type": "function",
    "function": {
        "name": "get_hello_info",
        "description": "回应用户的问候，比如，用户问候“您好”，就要调用这个工具",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "用户问候的内容",
                }
            }
        }
    }
}

GENERATE_IMAGES = {
    "type": "function",
    "function": {
        "name": "generate_images",
        "description": "根据用户的描述，生成图片",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "用户的描述",
                }
            }
        }
    }
}

GENERATE_SPEECH = {
    "type": "function",
    "function": {
        "name": "generate_speech",
        "description": "根据用户的描述，生成语音",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "用户的描述",
                },
                "language": {
                    "type": "string",
                    "description": "语音的语言",
                    "enum": ["陕西话", "东北话", "粤语"]
                },
                "gender": {
                    "type": "string",
                    "description": "语音的性别",
                    "enum": ["男声", "女声"]
                }
            },
            "required": ["text"]
        }
    }
}
GENERATE_VIDEO = {
    "type": "function",
    "function": {
        "name": "generate_video",
        "description": "根据用户的描述，生成视频",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "用户的描述",
                }
            }
        }
    }
}
SEARCH_DOCUMENTS = {
    "type": "function",
    "function": {
        "name": "search_documents",
        "description": "根据用户文献检索要求，检索相应的文献，并回答问题",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "用户的描述",
                }
            }
        }
    }
}
GENERATE_PPT = {
    "type": "function",
    "function": {
        "name": "generate_ppt",
        "description": "根据用户的要求，生成PPT演示文档",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "用户的描述",
                }
            }
        }
    }
}
SEARCH_POETRY_BY_CHINESE = {
    "type": "function",
    "function": {
        "name": "search_poetry_by_chinese",
        "description": "根据白话文搜索古文",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "用户提供的内容",
                }
            }
        }
    }
}
SEARCH_POETRY_BY_POETRY = {
    "type": "function",
    "function": {
        "name": "search_poetry_by_poetry",
        "description": "利用古文搜索古文",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "用户提供的内容",
                }
            }
        }
    }
}
