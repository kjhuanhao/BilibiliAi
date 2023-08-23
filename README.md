# BilibiliAI

## 项目介绍
一个用于总结B站视频的AI助手

## 项目特色
- [x] 私信发送回复
- [x] 使用openai接口
- [x] 自实现递归文本分割，可以动态分割过长文本
- [x] 可免费服务器部署

## 如何部署

### 配置
你需要修改`config.toml.example`为`config.toml`并配置好里面的信息，与哔哩哔哩有关的参数可在cookies里找到

### 运行
本项目使用Codesandbox部署: https://codesandbox.io/

1. 将项目通过`github`导入
2. 按下`Ctrl + shift + p`进行`rebuild`
3. 构建完成之后，在终端运行`pip install -r requirements.txt`安装本项目的依赖

若确保以上流程没用问题，使用下面的命令即可启动程序，若无异常，恭喜你成功运行了本项目
```shell
python main.py
```