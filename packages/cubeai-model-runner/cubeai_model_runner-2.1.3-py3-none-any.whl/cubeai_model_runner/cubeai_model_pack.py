# -*- coding: utf-8 -*-
import os
import sys
import shutil
import yaml
from .build_so import SoBuilder


def get_model_name():
    try:
        with open('./application.yml', 'r') as f:
            yml = yaml.load(f, Loader=yaml.SafeLoader)
    except:
        print('错误： 模型配置文件application.yml不存在！')
        return None

    try:
        name = yml['model']['name']
    except:
        print('错误： 未指定模型名称！')
        print('请在application.yml文件中编辑修改...')
        return None

    try:
        python = str(yml['python']['version'])
    except:
        print('错误： 未指定Python版本号！')
        print('请在application.yml文件中编辑修改...')
        return None


    if not python.startswith('3.'):
        print('错误： Python版本号必须是3且3.5以上！')
        print('请在application.yml文件中编辑修改...')
        return None

    if not sys.version.startswith(python):
        print('错误： 声明的Python版本号与当前运行环境（{}）不一致！'.format(sys.version[:sys.version.find(' ')]))
        print('请在application.yml文件中编辑修改...')
        return None

    try:
        model_runner = yml['model_runner']['version']
    except:
        print('错误： 未指定model_runner版本号！')
        print('请在application.yml文件中编辑修改...')
        return None

    if model_runner != 'v2':
        print('错误： model_runner版本号必须是“v2”！')
        print('请在application.yml文件中编辑修改...')
        return None

    if not os.path.exists('requirements.txt'):
        print('错误： requirements.txt文件不存在！')
        return None

    return name


def pack_model():
    name = get_model_name()
    if name is None:
        return

    os.system('rm -rf ./out')
    os.system('mkdir out')
    os.system('mkdir out/{}'.format(name))
    os.system('cp ./application.yml ./out/{}/'.format(name))
    os.system('cp ./requirements.txt ./out/{}/'.format(name))
    os.system('cp -rf ./core ./out/{}/'.format(name))
    dst_path = './out/{}'.format(name)
    shutil.make_archive(dst_path, 'zip', dst_path)  # 将目标文件夹自动压缩成.zip文件
    shutil.rmtree('./out/{}/'.format(name))
    print('模型打包完成！ 输出位置： ./out/{}.zip'.format(name))
    
    
def pack_model_bin():
    name = get_model_name()
    if name is None:
        return

    os.system('rm -rf ./out')
    os.system('mkdir out')
    os.system('mkdir out/{}'.format(name))
    os.system('cp ./application.yml ./out/{}/'.format(name))
    os.system('cp ./requirements.txt ./out/{}/'.format(name))
    
    so_builder = SoBuilder('core')
    so_builder.build_so()
    os.system('mv ./build/core ./out/{}/'.format(name))
    shutil.rmtree('build')
    
    dst_path = './out/{}'.format(name)
    shutil.make_archive(dst_path, 'zip', dst_path)  # 将目标文件夹自动压缩成.zip文件
    shutil.rmtree('./out/{}/'.format(name))
    print('模型打包完成！ 输出位置： ./out/{}.zip'.format(name))


if __name__ == '__main__':
    pack_model()
