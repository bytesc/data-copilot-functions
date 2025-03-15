from .utils import call_llm_test

from .utils.parse_output import parse_generated_python_code

from .utils.code_executor import execute_py_code_with_data
from .utils.parse_output import assert_png_file
from .examples.ask_ai_for_graph import get_ask_graph_prompt

import logging
import pandas as pd

pd.set_option('display.max_columns', None)


def get_py_code_with_data(question, data, llm, retries=3):
    def slice_dfs(df_dict, lines=3):
        top_five_dict = {}
        for key, df in df_dict.items():
            top_five_dict[key] = df.head(min(lines, len(df)))
        return top_five_dict

    data_slice = slice_dfs(data)
    pre_prompt = """
Define a Python function called `func` 
that takes only a single pandas dataframe called `data` as input parameter
that performs the following operations:
"""

    data_prompt = """
Here is the dataframe sample(it is just data structure samples not real data): 
""" + str(data_slice)

    end_prompt = """
All code should be completed in a single markdown code block without any comments, explanations or cmds.
The function should not be called, do not print anything in the function.
Please import the module you need, modules must be imported inside the function.
Do not mock any data !!! Do not make any example input like real data!!!
"""

    final_prompt = pre_prompt + question + "\n" + data_prompt + end_prompt

    retries_times = 0
    error_msg = ""
    while retries_times <= retries:
        retries_times += 1
        ans = call_llm_test.call_llm(final_prompt + error_msg, llm)
        ans_code = parse_generated_python_code(ans.content)
        if ans_code is not None:
            return ans_code
        else:
            error_msg = """
code should only be in a md code block: 
```python
def func(data):
    import pandas as pd
    import math
    # some python code
```
without any additional comments, explanations or cmds !!!
"""
            logging.error(ans + "No code was generated.")
            print("No code was generated.")
            continue


def get_py_code(question, llm, retries=3):

    pre_prompt = """
Define a Python function called `func` 
that takes no input parameter
that performs the following operations:
"""

    end_prompt = """
Remind:
1. All code should be completed in a single markdown code block without any comments, explanations or cmds.
2. The function should not be called, do not print anything in the function.
3. Please import the module you need, modules must be imported inside the function.
4. Do not mock any data !!! Do not make any example input like real data!!!
5. Never use `input()` in code !!! Never use `input()` in code !!!
6. Do not assign any example input or default value for user to replace with actual data!!! use None instead
"""

    final_prompt = pre_prompt + question + "\n" + end_prompt

    retries_times = 0
    error_msg = ""
    while retries_times <= retries:
        retries_times += 1
        ans = call_llm_test.call_llm(final_prompt + error_msg, llm)
        ans_code = parse_generated_python_code(ans.content)
        if ans_code is not None:
            return ans_code
        else:
            error_msg = """
code should only be in a md code block: 
```python
def func():
    import math
    # some python code
```
without any additional comments, explanations or cmds !!!
"""
            logging.error(ans + "No code was generated.")
            print("No code was generated.")
            continue


def draw_graph_func(question, data, llm, retries=2):
    exp = None
    for i in range(retries):
        question = get_ask_graph_prompt(question)
        err_msg = ""
        for j in range(retries):
            code = get_py_code_with_data(question + err_msg, data, llm)
            if code is None:
                continue
            try:
                result = execute_py_code_with_data(code, data, assert_png_file)
                return result
            except Exception as e:
                err_msg = str(e) + "\n```python\n" +code+"\n```\n"
                print(e)
                exp = e
                continue
    return None
