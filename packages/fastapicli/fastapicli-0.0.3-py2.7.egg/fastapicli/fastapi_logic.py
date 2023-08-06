"""
FastApiCli
author comger@gmail.com

fastapi_logic.py --model=Project
建议在项目 main.py
"""
import sys
import os
import shutil
import argparse
from tornado import template
import fastapicli


def init_logic(model, output):
    """ 生成逻辑代码"""
    loader = template.Loader('.')
    source_path = f"{fastapicli.__path__[0]}/logic.pyt"
    pyfbody = loader.load(source_path).generate(Model=model)
    # 保存位置
    path = f"{str.lower(model)}.py"
    if output:
        path = "{output}/{str.lower(model)}.py"
    
    f = open(path, "w")
    f.write(str(pyfbody, encoding='utf-8'))
    f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', dest='model', type=str, default='Demo', help='target model')
    parser.add_argument('-o', '--output', dest='output', type=str, default=None, help='target output folder')
    args = parser.parse_args()
    init_logic(args.model, args.output)


