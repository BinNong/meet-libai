<div align='center'>
 <img src="resource/avatar/libai.jpeg" alt="libai avatar" width="200" />

  # 「遇见李白」<img src="asset/images/meet-libai-logo.png" alt="meet-libai logo" width="50" /> meet-libai

</div>



------

[![Release Notes](https://img.shields.io/github/release/BinNong/meet-libai)](https://github.com/BinNong/meet-libai/releases)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/BinNong/meet-libai)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/BinNong/meet-libai)
[![GitHub star chart](https://img.shields.io/github/stars/BinNong/meet-libai?style=social)](https://star-history.com/#BinNong/meet-libai)
[![Dependency Status](https://img.shields.io/librariesio/github/BinNong/meet-libai)](https://libraries.io/github/BinNong/meet-libai)
[![Open Issues](https://img.shields.io/github/issues-raw/BinNong/meet-libai)](https://github.com/BinNong/meet-libai/issues)

 :vertical_traffic_light:  [哔哩哔哩详细视频介绍和引导](https://www.bilibili.com/video/BV17m41167KQ/?spm_id_from=333.788&vd_source=1a1de2338b5f002609ba8cca8fb71a13)

<img src="./asset/images/ui.png" width="50%;" />

### 1. 项目背景

​       李白 :bust_in_silhouette: 作为唐代杰出诗人，其诗歌作品在中国文学史上具有重要地位。近年来，随着数字技术和人工智能的快速发展，传统文化普及推广的形式也面临着创新与变革。国内外对于李白诗歌的研究虽已相当深入，但在数字化、智能化普及方面仍存在不足。因此，本项目旨在通过构建李白知识图谱，结合大模型训练出专业的AI智能体，以生成式对话应用的形式，推动李白文化的普及与推广。

​       随着人工智能技术的发展，知识图谱技术也得到了广泛的应用。知识图谱是一种基于语言知识库的语义表示模型，它能够将结构化的知识表示为图的形式，从而使得机器能够更好地理解和处理自然语言。
​      在知识图谱技术的基础上，开发一个问答系统可以利用知识图谱中的知识来回答用户的问题。<u>该系统可以利用知识图谱来构建以诗人李白为核心的古诗词文化知识图谱</u> :globe_with_meridians: ，并实现基于该知识图谱的问答功能。另外，对图谱进行可视化探索，以更好地理解知识图谱的结构和内容。同时提供，大模型以及rag检索增强的代码实现。



### 2. 项目目标

2.1 :1st_place_medal: 收集整理李白诗歌及其相关文化资料：通过文献调研、数据挖掘等方法，全面收集李白的诗歌作品、生平事迹、历史背景等相关资料，为构建李白知识图谱提供基础数据。

2.2 :2nd_place_medal: 构建李白知识图谱：利用自然语言处理、信息抽取等技术，对收集到的资料进行整理和分析，构建出一个完整的李白知识图谱。该图谱将涵盖李白的生平、诗歌风格、艺术成就等多个方面，为后续的AI智能体训练提供丰富的知识库。

2.3 :3rd_place_medal: 训练专业的AI智能体：基于构建好的李白知识图谱，利用大模型技术训练出具有专业水平的AI智能体。该智能体将具备对李白诗歌的深入理解和鉴赏能力，能够与用户进行高质量的互动。

2.4 :four:开发生成式对话应用：在训练好的AI智能体基础上，开发一款生成式对话应用。该应用将能够实现与用户的实时互动，为用户提供个性化的李白诗歌鉴赏体验。

### 3. 项目技术栈

- Python

- PyTorch

- Transformers

- fastAPI

- DGL

- DGL-KE

- Neo4j

- AC自动机

- RAG

- langchain

- edge-tts

- modelscope

- gradio

- zhipuai

  

### 4. 项目功能

- 数据预处理：对古诗词数据进行清洗、分词、构建知识图谱
- 知识图谱构建：利用知识图谱技术构建以李白为核心的古诗词文化知识图谱
  - 问答系统构建：利用知识图谱中的知识来回答用户的问题   
    - 图谱可视化：对知识图谱进行可视化探索，以更好地理解知识图谱的结构和内容   
- :hotsprings:图谱问答思路：
  
  - :smile_cat:普通流式问答
  - :recycle: 关系型问答：
    - 李白和杜甫的关系是什么
  - :package:属性问答：
    - 李白生于哪一年
  - :gift: 生成语音、图像：
    - 请生成李白在江边喝酒的图片
    - 请生成春望这首诗的语音
 - :green_salad: 趣味性游戏，比如：飞花令💐

### 5. 项目现状

- 构建了一个基于知识图谱的问答系统，该系统能够利用知识图谱中的知识来回答用户的问题。     
- 对图谱进行可视化探索，以更好地理解知识图谱的结构和内容。
- 提供大模型以及rag检索增强的代码实现。

### 6. 项目挑战

- 知识图谱的构建和维护
- 问答系统的实现和优化
- 图谱的可视化探索
- 大模型以及rag检索增强的代码实现

### 7. 项目展望

- 进一步优化问答系统的回答质量和效率
- 探索其他类型的问答任务，如常识 问题、知识推理等
- 持续更新和维护知识图谱，以保持其准确性、完整性和有效性

### 8. 项目技术架构

通过本项目的实施，我们不仅实现了基于知识图谱的问答系统，还积累了丰富的实践经验和知识图谱技术应用经验。在未来的工作中，我们将不断优化问答系统的回答质量和效率，并探索其他类型的问答任务，以满足更多用户的需求。同时，我们将继续更新和维护知识图谱，以保持其准确性、完整性和有效性，为知识图谱技术的发展和应用做出贡献 。以下是项目技术架构图：
![code_flow](asset/images/architecture.png)


### 9. 项目代码结构

请点击这里跳转，[代码结构](docs/code_arch.md):cityscape:

### 10. 核心函数
![get_ans](asset/images/get_ans.png)

------



## 底层主要依赖

- [Transformers](https://huggingface.co/transformers/index.html)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PyTorch](https://pytorch.org/)
- [Gradio](https://gradio.app/)

## 如何启动项目

#### 1. 配置第三方大模型api key

​	:key:使用[智普ai](https://open.bigmodel.cn/)开放平台，请跳转到该平台，申请api key。然后，将api key填入`.env`文件中。

#### 2. 创建python环境（>=python3.10）

- 使用conda来管理python环境，所以请先安装conda ([Install Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)):smile_cat:

- 使用conda命令来创建python环境

  ```bash
  #Create a new environment: Use the following command to create a new Python environment with a specific vesion.(当然国内你可能需要配置conda和pip镜像)
  
  conda create --name myenv python=3.10
  
  #This will create a new environment named myenv with the specified Python version.
  #Activate the environment: Once the environment is created, you need to activate it. 
  
  conda activate myenv
  
  ```

- 安装依赖包

  ```bash
  pip install -r requirements.txt
  ```

#### 3. 建立图数据库<img src="https://dist.neo4j.com/wp-content/uploads/20170726233003/hello-world-neo4j-inc-company-name-change.png" alt="Hello, World: Neo4j, Inc." width="80" />

- ##### 请根据以下指引，安装neo4j

[使用docker安装](https://hub.docker.com/_/neo4j)<img src="https://avatars.githubusercontent.com/u/5429470?s=280&v=4" alt="Docker · GitHub" width="50" />

> You can start a Neo4j container like this:
>
> ```console
> docker run \
>     --publish=7474:7474 --publish=7687:7687 \
>     --volume=$HOME/neo4j/data:/data \
>     neo4j:5.12.0
> ```
>
> which allows you to access neo4j through your browser at [http://localhost:7474](http://localhost:7474/).
>
> This binds two ports (`7474` and `7687`) for HTTP and Bolt access to the Neo4j API. A volume is bound to `/data` to allow the database to be persisted outside the container.
>
> By default, this requires you to login with `neo4j/neo4j` and change the password. You can, for development purposes, disable authentication by passing `--env=NEO4J_AUTH=none` to docker run.

- 当然，也可以不使用docker，直接在你的操作系统上安装neo4j并启动服务即可。

- ##### 安装完成后，将数据导入neo4j     :smiling_imp:

:warning:<u>*注：由于数据的建立和规整涉及第三方版权，本项目不提供完整李白的数据，只提供示例数据*</u>

`Cypher query` 语句如下：

```cypher
# 创建`李白`节点
CREATE (p:`人物`:`唐`{name: '李白', PersonId:32540})

# 创建‘高力士’节点
CREATE (p:`人物`:`唐`{name: '高力士', PersonId:32541})
                      
# 创建李白和高力士的关系
MATCH (a:`人物`:`唐` {PersonId: 32540}), (b:`人物`:`唐` {PersonId: 32541})
CREATE (a)-[r:`李白得罪高力士` {since: 2022, strength: 'strong', Notes: '《李太白全集》卷三五《李太白年譜》：天寶三載，甲申。（五月改"年"爲"載"。四十四歲）太白在翰林，代草王言。然性嗜酒，多沉飮，有時召令撰述，方在醉中，不可待，左右以水沃面，稍解，卽令秉筆，頃之而成。帝甚才之，數侍宴飮。因沉醉引足令高力士脫靴，力士恥之，因摘其詩句以激太眞妃。帝三欲官白，妃輒沮之。又爲張垍讒譖，公自知不爲親近所容，懇求還山，帝乃賜金放歸。又引《松窗錄》：會高力士終以脫靴爲深恥，異日，太眞妃重吟前詞，力士戲曰："比以妃子怨李白深入骨髓，何反拳拳如是？"太眞妃驚曰："何翰林學士能辱人如斯！"力士曰："以飛燕指妃子，是賤之甚矣！"太眞妃深然之。上嘗三欲命李白官，卒爲宮中所捍而止。'}]->(b)
RETURN r
```

以上数据导入完毕之后，再导入元数据节点（改节点用于记录数据版本号的基本信息）

```cypher
CREATE (meta_node:Meta{
    id: 'meta-001',
    title: 'libai-graph meta node',
    text: 'store some meta info',
    timestamp: datetime(),
    version: 1,
    status: 'active'
})
```



- ##### 确认neo4j数据正常之后，配置config文件（以config-local.yaml为例） :pager:  (连接数据库的url，用户名，密码)

```yaml
neo4j:
  url: bolt://localhost:7687
  database: neo4j
  username: neo4j
  password: *****
# 注意： 以上参数，根据你的数据库实际连接为准
```

  


#### 4. 配置文件

有3个配置文件（根据你的需求，决定使用哪个配置，如果没有对应的配置文件，可以拷贝./config/config-local.yaml作为副本，再修改）：

`部署环境配置./config/config-deploy.yaml`
`测试环境配置./config/config-dev.yaml`
`本地开发配置./config/config-local.yaml`

在项目根目录下**<u>新建</u>**`.env`文件作为环境变量配置，并在文件中指定启用哪个环境配置，下面给出一个完整的`.env`内容

```bash
#PY_ENVIRONMENT=dev
PY_ENVIRONMENT=local # 启用本地开发环境
#PY_ENVIRONMENT=deploy
PY_DEBUG=true

# ---------注意-----------------------------------
# 如下模型中只能使用其中的某一个模型，不能同时配置多个模型
# 去对应的官网申请api-key,并替换YOUR API-KEY
# 也可以使用ollama本地运行的模型，api-key设置为ollama
# ⚠️文生图的模型暂时使用zhipuai，因此要配置zhipuai的api-key
# -----------------------------------------------

# 智普ai
LLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
LLM_API_KEY=YOUR API-KEY
MODEL_NAME=glm-4

# kimi
#LLM_BASE_URL=https://api.moonshot.cn/v1
#LLM_API_KEY=YOUR API-KEY
#MODEL_NAME=moonshot-v1-8k

# 百川大模型
#LLM_BASE_URL=https://api.baichuan-ai.com/v1/
#LLM_API_KEY=YOUR API-KEY
#MODEL_NAME=Baichuan4

# 通义千问
#LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
#LLM_API_KEY=YOUR API-KEY
#MODEL_NAME=qwen-long

# 零一万物
#LLM_BASE_URL=https://api.lingyiwanwu.com/v1
#LLM_API_KEY=YOUR API-KEY
#MODEL_NAME=yi-large

# deepseek
# LLM_BASE_URL=https://api.deepseek.com
# LLM_API_KEY=ollama
# MODEL_NAME=deepseek-chat

# 豆包
#LLM_BASE_URL=https://ark.cn-beijing.volces.com/api/v3/
#LLM_API_KEY=YOUR API-KEY
# 注意：对于豆包api，model_name参数填入ENDPOINT_ID，具体申请操作在豆包api官网提供。
#MODEL_NAME=

# ollama
#LLM_BASE_URL=http://localhost:11434/v1/
#LLM_API_KEY=ollama
#MODEL_NAME=qwen2:0.5b

# anyapi
#LLM_BASE_URL=https://api.siliconflow.cn/v1
#LLM_API_KEY=YOUR API-KEY
#MODEL_NAME=Qwen/Qwen2-7B-Instruct

#文生图模型，暂时使用zhipuai
#OPENAI_API_KEY=YOUR API-KEY
ZHIPUAI_API_KEY=YOUR API-KEY

# 这里填入你的组织名
ORGANIZATION_NAME= xxx团队

```

#### 5. 白话文搜古文、古文搜古文

:smiley:由于涉及到内存问题，这个两个服务独立部署。目前暂不开源，感兴趣的读者，可以自己按照如下接口规则独立开发。如果没有这个服务接口，不影响程序运行。

古文搜古文，接口访问示例：

```python
    data = {
        "text": '床前明月光', # 古文
        "conf_key": "chinese-classical", # 预留参数
        "group": "default", # 预留参数
        "size": 5, # 返回个数
        "searcher": 3 # 预留参数
    }
    resp = requests.post("http://172.16.67.150:18880/api/search/nl", data=json.dumps(data))
```

接口返回数据示例：

```json
{
  "retCode": 0,
  "errMsg": null,
  "values": [
    {
      "value": "Ming##@##申佳允##@##天际秋云薄|床前明月光|无由一化羽|回立白苍苍##@##秋兴集古 其八##@##苍苍 天际 秋云 明月",
      "score": 1.0000004768371582
    },
    {
      "value": "Tang##@##李白##@##床前明月光|疑是地上霜|举头望山月|低头思故乡##@##静夜思##@##山月 霜 明月 低头",
      "score": 1.0000004768371582
    },
    {
      "value": "tang##@##李白##@##床前明月光|疑是地上霜|举头望明月|低头思故乡##@##静夜思##@##霜 光 明月 低头",
      "score": 1.0000004768371582
    },
    {
      "value": "Ming##@##高启##@##堂上织流黄|堂前看月光|羞见天孙度|低头入洞房##@##子夜四时歌 其三##@##天孙 月光 洞房 低头",
      "score": 0.7958479523658752
    },
    {
      "value": "Ming##@##黄渊耀##@##凉风落柳梢|微云淡河面|怀中明月光|多赊不为贱##@##夜坐##@##凉风 柳梢 明月 微云",
      "score": 0.7571470737457275
    }
  ]
}
```

score表示得分，value表示一条数据，value中的的各个字段值用##@##隔开 ["朝代","作者", "完整诗篇", "篇名", "关键词"]

#### 6.  玩转飞花令💐

![](./asset/images/fog.png)

[飞花令功能详细安装以及使用](./docs/game_fog.md)

#### 7. 程序启动(三种方式)

- [x] 后台启动 :baby_bottle:

启动shell脚本为`restart.sh`

```bash
> chmod +x ./restart.sh
> ./restart.sh
```

启动成功后可以访问

- webui http://localhost:7860
- api http://localhost:18881/docs
- api doc http://localhost:18881/redoc

- [x] python启动所有任务包括api和webui :radio:

```
python app.py
```

启动成功后可以访问 :mag:

- webui http://localhost:7860
- api http://localhost:18881/docs
- api doc http://localhost:18881/redoc

- [x] python 命令启动 webui :man_juggling:

```bash
python webui.py
```

启动成功后可以访问 :package:

- webui http://localhost:7860

#### 7. 调用程序api构建图数据库的实体索引（在本地创建ac自动机），这一步成功后才可使用图数据
访问api： http://localhost:18881/docs
打开如下图所示, 然后点击build model：

![all_api](asset/images/all_api.png)

接着填写如下如下参数后，点击execute：

![graph_entity_build](asset/images/graph_entity_build.png)



#### 8.知识图谱构建演示demo

 1.按照前面的步骤启动程序之后（程序保持运行），运行根目录下的graph_demo_ui.py：

```bash
python graph_demo_ui.py
```
2. 访问地址：

   ```
   http://127.0.0.1:80
   ```
   如下图在左侧输入原始文本，以英文逗号结尾自动触发构建过程（需要一定的时间等待）！
   ![graph_entity_build](asset/images/llm_graph.jpg)



------

 :vertical_traffic_light:  [哔哩哔哩详细视频介绍和引导](https://www.bilibili.com/video/BV17m41167KQ/?spm_id_from=333.788&vd_source=1a1de2338b5f002609ba8cca8fb71a13)

# Coffee :custard:

如果你愿意，你可以**<u>打赏</u>**我 <img src="https://www.pngitem.com/pimgs/m/145-1450643_providing-encouragement-and-support-to-help-people-icon.png" alt="Providing Encouragement And Support To Help People - Icon, HD Png Download  , Transparent Png Image - PNGitem" width="50" />，不在乎数量，你的一个不小心的举动是我前进的动力 <img src="https://static.vecteezy.com/system/resources/previews/028/086/542/non_2x/keep-going-arrow-succes-challenge-color-icon-illustration-vector.jpg" alt="keep going arrow succes challenge color icon vector illustration 28086542  Vector Art at Vecteezy" width="50" />，业余时间搬砖实属不易。

<img src="asset/qr_code/ali_pay.png" width="200" ><img src="asset/qr_code/wechat_pay.png" width="200" >

