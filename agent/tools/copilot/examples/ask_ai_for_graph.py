
from .path_tools import generate_img_path


def get_ask_graph_prompt(question, tmp_file=False):
    pre_prompt = """
Please use matplotlib to draw a graph based on the question. 
The Python function should return a string of file path in `./tmp_imgs/` only 
and the image generated should be stored in that path. 
file path must be:
"""
    example_code = """
Here is an example: 
```python
def func(data):
    import pandas as pd
    import math
    import PIL
    import matplotlib
    import matplotlib.pyplot as plt
    plt.rcParams['font.family'] = 'SimHei' 
    plt.rcParams['axes.unicode_minus'] =False
    # please keep the code above!
    # generate code to perform operations here
    return path
```
"""
    if not tmp_file:
        return "question:"+question + pre_prompt + "`"+generate_img_path()+"`"+example_code
    else:
        return "question:"+question + pre_prompt + "./tmp_imgs/tmp.png" + example_code



