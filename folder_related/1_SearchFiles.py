
'''
File: 1_SearchFiles.py
Project: folder_related
File Created: Friday, 19th October 2018 9:32:14 pm
Author: xiaofeng (sxf1052566766@163.com)
-----
Last Modified: Friday, 19th October 2018 9:32:37 pm
Modified By: xiaofeng (sxf1052566766@163.com>)
-----
Copyright 2018.06 - 2018 onion Math, onion Math
'''

""" Find all files with the specified suffix under the path """

import os

file_list = []


def SearchFiles(root_dir, suffix):
    global file_list
    assert os.path.exists(root_dir)
    try:
        dir_list = os.listdir(root_dir)
        for files in dir_list:
            child_dir = os.path.join(root_dir, files)
            if os.path.isdir(child_dir):
                SearchFiles(child_dir, suffix)
            elif os.path.isfile(child_dir) and os.path.splitext(child_dir)[1] in suffix:
                file_list.append(child_dir)
    except Exception as e:
        print('ERROR：', e)



# root_dir = '/usr/xx/data'
# suffix = ['.png', '.jpg', '.py']
# SearchFiles(root_dir, ['.png', 'jpg', '.py'])
