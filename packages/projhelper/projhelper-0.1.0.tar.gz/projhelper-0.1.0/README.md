# 概括

## 说明
    本包名字为*packer*,使用方法包括...

### 打包方法
    python .\setup.py sdist
### 安装方法
    pip install projhelper

###调用方法
    1:在main.py 里 切换到工作目录, :
        import sys
        import os
        s_BaseDir=os.path.dirname(os.path.abspath(__file__)).__str__()
        s_scriptDir=os.path.join(s_BaseDir,'../script')
        sys.path.append(s_scriptDir)#设置项目路径
        sys.path.append(s_BaseDir)#设置项目路径
        os.chdir(s_BaseDir)
    2:调用方法:
        调用如 python main.py [prod|dev|test] xxx  
        
        用到 loadConf 模块时 需要加环境参数 prod等 用于调用配置, 调用如 python main.py [prod|dev|test] xxx  
            调用项目第一个参数为 调用环境 prod|dev|test ,作用于配置文件 ,后面可以添加参数给项目使用
                    配置文件:
                        prod|dev|test 对应着 应用目录下的 conf/conf_xxx.cfg文件 可参考本 本模块的conf/conf_dev.cfg 
                    如果没用到 配置文件模块  可以不添加 prod|dev|test参数
        #调用logger时 ， 项目里不能再引入其他的logger ，否则可能输出为空
    
### 参数说明

### 错误反馈

###版本说明