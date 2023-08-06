# -*- coding: utf-8 -*-

"""
@date: 2020/8/12 下午10:02
@file: cli.py.py
@author: zj
@description: 
"""

import os
import sys

from zlogo.config.defaults import default_argument_parser
from zlogo.util.misc import get_version, check_file_exist, generate_png, generate_svg_path
from zlogo.util.utility import parse_config, write_yaml_config, get_file_dir


def parse():
    info = parse_config()
    # print(info)

    parser = default_argument_parser()
    args = parser.parse_args()
    # print(args)

    if args.version:
        print('zlogo: v{}'.format(get_version()))
        sys.exit(0)

    if args.config_file:
        if check_file_exist(args.config_file):
            cinfo = parse_config(args.config_file)
            info.update(cinfo)

    if args.logo:
        info['logo'] = args.logo
        info['output'] = args.logo + '.svg'
    if args.font and check_file_exist(args.font):
        info['font'] = args.font
    if args.fontsize:
        info['fontSize'] = args.fontsize
    if args.padding:
        info['padding'] = args.padding
    if args.color:
        info['path']['fill'] = args.color
    if args.output:
        if os.path.isdir(args.output):
            info['output'] = generate_svg_path(args.output, info['logo'])
        elif args.output.split('.')[-1] == 'svg':
            info['output'] = args.output

    # 写入配置好的文件
    write_yaml_config(info)

    return info


def main():
    info = parse()

    # 执行logo生成操作
    cmd_path = os.path.join(get_file_dir(), '../tool/logo')
    config_dir = os.path.join(get_file_dir(), '../config/')
    flag = os.system(f'{cmd_path} -c {config_dir}')
    if flag != 0:
        exit(0)

    # 同时生成.png图片
    if os.path.isabs(info['output']):
        generate_png(info['output'])
    else:
        output_path = os.path.abspath(info['output'])
        generate_png(output_path)


if __name__ == '__main__':
    main()
