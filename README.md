# smart class


✨ **基于代码生成和函数调用(function call)的大语言模型(LLM)智能体**

通过自然语言提问，使用大语言模型智能解析数据库结构，对数据进行智能多表结构化查询和统计计算，根据查询结果智能绘制多种图表。
支持自定义函数(function call)和Agent调用，多智能体协同。
基于代码生成的思维链(COT)。
实现智能体对用户的反问，解决用户提问模糊、不完整的情况。
Pywebio 交互式前端网页，不必须 openai api，100%纯 Python 代码。

🚩[English Readme](./README.en.md)

- [基于大语言模型 (LLM) 的<u>**可解释型**</u>自然语言数据库查询系统 (RAG) https://github.com/bytesc/data-copilot-steps](https://github.com/bytesc/data-copilot-steps)
- [基于大语言模型 (LLM)和并发预测模型的自然语言数据库查询系统 (RAG) (https://github.com/bytesc/data-copilot-v2](https://github.com/bytesc/data-copilot-v2)

🚩[个人网站：www.bytesc.top](http://www.bytesc.top)

🔔 如有项目相关问题，欢迎在本项目提出`issue`，我一般会在 24 小时内回复。

## 功能简介

- 1, 基于代码生成的大语言模型智能体(AI Agent)。
- 2, 实现智能体对用户的反问，解决用户提问模糊、不完整的情况。
- 3, 智能体支持灵活的自定义函数调用(function call)和思维链(COT)
- 4, 实现多智能体的合作调用
- 5, 智能体实现智能绘制多种统计图表
- 6, 智能体实现基于机器学习的智能成绩预测 
- 7, 能够处理大语言模型表现不稳定等异常情况
- 8, 支持 `openai` 格式(如 `glm` ,`deepseek`, `qwen`)的 api 接口


## 创新点
- 基于代码生成的智能体(Agent)支持灵活的自定义函数调用(function call)和思维链(COT)
- 引入函数依赖图(Function Graph)的概念，实现自定义函数调用
- 引入智能体函数(Agent as Function)的概念，实现多智能体(Agent)的合作调用
- 实现智能体(Agent)对用户的反问，解决用户提问模糊、不完整的情况
- 包含输出断言和异常处理，能够处理大语言模型表现不稳定等异常情况

## 技术路线

### AI agent 

基本程序流水线图：

![](./readme_static/流程图1.png)

![](./readme_static/流程图2.png)


基本流程：
1. **Question**: 用户自然语言问题提问
2. **RAG**: 通过检索增强生成(RAG)获取背景知识
3. **Function Selection**: LLM 根据函数基本信息选择多个函数，通过函数依赖图(Function Graph)获得可用函数列表和详细注释（函数包括非智能体函数(Custum Function)和调用其它智能体的函数(Agent as Function)，实现多智能体协同）
4. **Function Calls Chain**: LLM 根据函数列表和详细注释，生成调用多个函数的 python 代码并执行
5. **Result Review**: LLM 回顾总结整个流程，评估问题是否解决，没有解决则反问用户，使其澄清问题或者提供更多信息


## 展示

### 演示

智能数据库查询、统计计算和绘图(Agent 协同)

![](./readme_static/r1.png)

地图标注(自定义function call)

![](./readme_static/r2.png)

智能绘图不满意，可以交互式绘图

![](./readme_static/r3.png)

用户提供信息不足以完成任务时，反问用户使其补充信息(Result Review)

![](./readme_static/r4.png)

### 原理

函数调用链(Function Call Chain)和智能体函数(Agent as Function)，实现多智能体协同原理示例

![](./readme_static/f1.png)

函数依赖图(Function Graph)和非智能体函数(Custom Functions)原理示例

![](./readme_static/f2.png)


## 如何使用

### 安装依赖

python 版本 3.10

```bash
pip install -r requirement.txt
```

### 配置文件

`config.yaml`
```yml
# config
server_port: 8003
server_host: "0.0.0.0"
# 填写数据库连接
mysql: "mysql+pymysql://root:123456@localhost:3306/smart_class2"

static_path: "http://127.0.0.1:8003/"
```

### 大语言模型配置

`agent\utils\llm_access\`文件夹包含大语言模型配置

`agent\utils\llm_access\LLM.py` 填写大语言模型(LLM)链接
```python
def get_llm():
    # 此处填写大语言模型(LLM)链接
    llm = OpenAI(api_key=get_api_key_from_file("./agent/utils/llm_access/api_key_openai.txt"),
                 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
    return llm
    # https://open.bigmodel.cn/api/paas/v4/
    # https://api.deepseek.com/v1/
    # https://dashscope.aliyuncs.com/compatible-mode/v1
```

`agent\tools\copilot\utils\call_llm_test.py`和 `agent\tools\rag\utils\call_llm_test.py` 填写模型名称
```python
def call_llm(question, llm):
    response = llm.chat.completions.create(
        model="qwen-max",  # 此处填写模型名称
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": question},
        ],
        stream=False
    )
    # glm-4
    # deepseek-chat
    # qwen-max
```

新建文件：`agent\utils\llm_access\api_key_openai.txt` 在其中填写`api-key`

`api-key`获取链接：
- 阿里云:[https://bailian.console.aliyun.com/](https://bailian.console.aliyun.com/)
- deepseek:[https://api-docs.deepseek.com/](https://api-docs.deepseek.com/)
- glm:[https://open.bigmodel.cn/](https://open.bigmodel.cn/)



### 运行

```bash
# 服务端
python ./main.py
# 客户端
python ./front.py
```

### 自定义 function call

在 `agent/tools/custom_tools_def.py` 中定义自定义函数

需要写规范、详细的注释，前三行是函数基本功能信息，之后是详细信息

例子：

```python
from typing import List, Tuple, Optional
from .map.get_onemap_minimap import get_minimap_func

def get_minimap(lat_lng_list: Optional[List[Tuple[float, float]]] = None,
                postcode_list: Optional[List[str]] = None) -> str:
    """
    get_minimap(lat_lng_list: Optional[List[Tuple[float, float]]] = None, postcode_list: Optional[List[str]] = None) -> str:
    Generate an HTML iframe for a minimap with optional markers in latitude and longitude pairs or or postal codes.
    Returns an HTML iframe string.

    The function creates an HTML iframe that embeds a minimap from OneMap.sg.
    Users can specify a list of latitude and longitude pairs or postal codes
    to be marked on the map.

    Args:
    - lat_lng_list (Optional[List[Tuple[float, float]]]): A list of tuples,
      where each tuple contains a latitude and longitude pair for a marker.
      Default is None.
    - postcode_list (Optional[List[str]]): A list of postal codes to be marked
      on the map. Default is None.

    Returns:
    - str: An HTML iframe string that can be embedded in a webpage to display
      the minimap with the specified markers.

    Example usage:
    ```python
    get_minimap_func(lat_lng_list=[(1.2996492424497, 103.8447478575), (1.29963489170907, 103.845842317726)])
    get_minimap_func(postcode_list=["123456"])
    ```

    """
    html = get_minimap_func(lat_lng_list, postcode_list)
    return html
```

然后在 `agent/tools/get_function_info.py` 中注册函数

import 函数之后，在 `FUNCTION_DICT` 中添加函数，在 `FUNCTION_IMPORT ` 中添加 import 语句

例如：

```python
from .custom_tools_def import get_minimap  # 导入


FUNCTION_DICT = {
    "query_database": query_database,
    "draw_graph": draw_graph,
    "get_minimap": get_minimap   # 注册
}

FUNCTION_IMPORT = {
    query_database: "from agent.tools.tools_def import query_database",
    draw_graph: "from agent.tools.tools_def import draw_graph",
    get_minimap: "from agent.tools.custom_tools_def import get_minimap"  # 添加 import
}
```

`ASSIST_FUNCTION_DICT` 定义了函数的依赖关系图。

例如：

```python
ASSIST_FUNCTION_DICT = {
    # predict_grade_for_stu: [from_username_to_uid, from_lesson_name_to_lesson_num],
}
```

# 开源许可证

此翻译版本仅供参考，以 LICENSE 文件中的英文版本为准

MIT 开源许可证：

版权所有 (c) 2025 bytesc

特此授权，免费向任何获得本软件及相关文档文件（以下简称“软件”）副本的人提供使用、复制、修改、合并、出版、发行、再许可和/或销售软件的权利，但须遵守以下条件：

上述版权声明和本许可声明应包含在所有副本或实质性部分中。

本软件按“原样”提供，不作任何明示或暗示的保证，包括但不限于适销性、特定用途适用性和非侵权性。在任何情况下，作者或版权持有人均不对因使用本软件而产生的任何索赔、损害或其他责任负责，无论是在合同、侵权或其他方面。
