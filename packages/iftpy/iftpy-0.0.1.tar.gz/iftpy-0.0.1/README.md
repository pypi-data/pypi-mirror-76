# iftpy

## 介绍
操作infinity歌声合成编辑器iftp文件的python库

## 安装
暂未上架pypi，请将项目文件夹下的iftpy文件夹复制到python安装目录下的Lib文件夹中

## 功能

### iftp文件

- 解析与保存iftp文件
    
    目前可以解析的内容：
    
    - 工程属性：曲速、节拍数
    - 音轨属性：音轨名、独奏、静音
    - 音符属性：起点、终点、音高、歌词

- 导出ust文件（需要[utaufile](https://gitee.com/oxygendioxide/utaufile)）
- 导出mid文件（需要[mido](https://mido.readthedocs.io/en/latest/index.html)）
- 导出dv文件（需要[dvfile](https://gitee.com/oxygendioxide/dvfile)）
- 导出五线谱（需要[music21](http://web.mit.edu/music21/doc/index.html)、[utaufile](https://gitee.com/oxygendioxide/utaufile)和[musescore](http://musescore.org)(独立软件)）

## 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request

## 相关链接

[infinity editor 官网](https://infinityproject.azurewebsites.net/?tdsourcetag=s_pctim_aiomsg)

[infinity editor 项目主页](https://github.com/FangCunWuChang/Infinity)