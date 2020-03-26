"""
调用js获取内容
"""
import os
import json
import subprocess as sp
import random

node = '/home/weiyinfu/Documents/node-v12.13.1-linux-x64/bin/node'


def js_eval_json(content):
    js = f"""
const x={content}
console.log(JSON.stringify(x,null,2))
"""
    filename = f'temp{random.randint(0, 1000)}.js'
    try:
        open(filename, 'w').write(js)
        res = sp.check_output(f'{node} {filename}', shell=True)
        return json.loads(res)
    finally:
        os.remove(filename)


if __name__ == '__main__':
    print(js_eval_json('"haha"'))
