# 使用一个基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 将项目文件复制到容器中
COPY . /app

# 安装依赖
RUN pip install -r requirements.txt

# 执行应用
CMD ["python", "main.py"]
