# -*- coding: UTF-8 -*-
#
# Tencent is pleased to support the open source community by making QTA available.
# Copyright (C) 2016THL A29 Limited, a Tencent company. All rights reserved.
# Licensed under the BSD 3-Clause License (the "License"); you may not use this 
# file except in compliance with the License. You may obtain a copy of the License at
# 
# https://opensource.org/licenses/BSD-3-Clause
# 
# Unless required by applicable law or agreed to in writing, software distributed 
# under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
#

'''打包成可执行文件
'''

import os
import sys

def main(version):
    version_items = version.split('.')
    for i in range(len(version_items)):
        version_items[i] = int(version_items[i])
        
    with open('version.py', 'wb') as fp:
        fp.write('version_info=u"%s"' % version)
            
    if sys.platform == 'win32':
        version_file_path = 'version_file.txt'
        with open(os.path.join('res', 'file_version_info.txt'), 'rb') as fp:
            text = fp.read()
            text = text % {'main_ver':  version_items[0],
                           'sub_ver':   version_items[1],
                           'min_ver':   version_items[2],
                           'build_num': version_items[3] if len(version_items) > 3 else 0
                           }
        with open(version_file_path, 'wb') as fp:
            fp.write(text)
        cmdline = 'pyinstaller -F -w ui/app.py -n AndroidUISpy_v%s -i res/androiduispy.ico --add-data=.env/Lib/site-packages/qt4a/androiddriver/tools;qt4a/androiddriver/tools --version-file %s' % (version, version_file_path)
    else:
        cmdline = 'pyinstaller -F -w ui/app.py -n AndroidUISpy -i res/androiduispy.icns --add-data=.env/Lib/python2.7/site-packages/qt4a/androiddriver/tools:qt4a/androiddriver/tools'
    
    os.system(cmdline)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >> sys.stderr, 'usage: python build.py versions'
        exit()
    main(sys.argv[1])
    