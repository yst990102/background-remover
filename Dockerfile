# 使用官方 Python 镜像作为基础镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制应用程序代码到容器中
COPY . /app

# 安装 Flask 及其依赖
RUN pip install -r requirements.txt

# 暴露端口，这个端口号应该与 Flask 应用程序中的端口号一致
EXPOSE 5000

# 启动 Flask 应用程序
CMD ["flask", "run"]
