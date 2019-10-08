


# Jupyter Notebook 教程

> 时间：2019.05.17
> 环境：anaconda3.7
> 参考网址：https://www.baidu.com/link?url=JWQrDPzhlFkrMdav9T1TfLhczJMu_gd_Au4QB4RqSExUkp50WWweXqmfSknJ40mzGiMN5asCGpOYVL-lAZTR9dpDXyxSYkrRNmaK0EIBNn7&wd=&eqid=b3aeed340000673e000000025cdeba5f

## 1. 安装和配置

### 1.1 安装

通过anaconda navigator 安装特定虚拟环境下的jupyter notebook

- 1. 打开anaconda navigator
- 2. 选择虚拟环境
- 3. 选择jupyter notebook项目，点击install按钮进行安装

### 1.2 配置

#### 1.2.1 更改默认文件夹

> 参考网址：https://www.cnblogs.com/LOW-ctfer/p/10029442.html

- 1. 修改配置文件
    - 1.1 文件名叫   `jupyter_notebook_config.py`
    - 1.2 应该是在C盘用户个人文件夹下的.jupyter里，如果没有的话，在Anaconda终端运行以下命令（不是Anadonca安装的就Windows命令行内操作）: `jupyter notebook --generate-config`
    - 1.3 打开配置文件，找到：
    ```
        ## The directory to use for notebooks and kernels. 
        #c.NotebookApp.notebook_dir = ''
    ```
    - 1.4 修改为：
    ```
        ## The directory to use for notebooks and kernels. 
        c.NotebookApp.notebook_dir = 'G:\Jupyter'
    ```
- 2. 注意事项：
    - 路径为自己想要保存的地方
    - **一定要把 # 去掉**
    - 文件夹提前建好，否则会出现闪退

