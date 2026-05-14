# Hospital 门诊系统（Django）

一个基于 Django + 模板页面的门诊管理示例项目，包含管理员、医生、患者相关页面与接口。

## 功能概览

- 管理员：科室、医生、药品、患者管理
- 医生：接诊、处方、订单处理
- 患者：注册、登录、挂号、缴费、取号

## 运行环境

- Python 3.10+
- macOS / Linux / Windows

## 快速开始（推荐：无数据库依赖）

该仓库默认使用 SQLite，可直接启动预览。

1. 创建并激活虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate
```

1. 安装依赖

```bash
pip install -r requirements.txt
```

1. 初始化本地预览业务表（首次运行必做）

```bash
python manage.py init_nodb
```

1. 启动服务

```bash
python manage.py runserver
```

1. 打开页面

- <http://127.0.0.1:8000/login/>
- <http://127.0.0.1:8000/admin_department/>
- <http://127.0.0.1:8000/patient_home/>
- <http://127.0.0.1:8000/doctor_home/>

## MySQL 模式启动（可选）

1. 安装 MySQL 额外依赖

```bash
pip install -r requirements-mysql.txt
```

1. 复制环境变量模板并按本机数据库修改

```bash
cp .env.example .env
```

1. 设置环境变量（示例）

```bash
export DB_ENGINE=mysql
export DB_NAME=hospital
export DB_HOST=127.0.0.1
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=your_password
```

1. 启动服务

```bash
python manage.py runserver
```

## 环境变量

项目配置位于 [hospital/settings.py](hospital/settings.py)，核心变量如下：

- DJANGO_SECRET_KEY：Django 密钥
- DJANGO_DEBUG：True/False
- DJANGO_ALLOWED_HOSTS：逗号分隔，例如 127.0.0.1,localhost
- DB_ENGINE：sqlite 或 mysql
- SQLITE_PATH：SQLite 文件路径（默认 db.sqlite3）
- DB_NAME / DB_HOST / DB_PORT / DB_USER / DB_PASSWORD：MySQL 参数

参考模板见 [.env.example](.env.example)。

项目启动时会自动读取项目根目录 `.env`（若存在），无需额外引入 dotenv 命令。

## 常用命令

```bash
# 代码检查
python manage.py check

# 初始化 SQLite 业务表（无 MySQL 预览）
python manage.py init_nodb
```

## 项目结构

- [manage.py](manage.py)：Django 启动入口
- [hospital/settings.py](hospital/settings.py)：主配置（支持 sqlite/mysql）
- [hospital/urls.py](hospital/urls.py)：路由
- [hospital/view_*.py](hospital/view_admin.py)：业务接口视图
- [templates](templates)：页面模板
- [static](static)：静态资源

## 已完成的仓库化整理

- 新增根目录 [.gitignore](.gitignore)
- 新增依赖文件 [requirements.txt](requirements.txt) 与 [requirements-mysql.txt](requirements-mysql.txt)
- 新增环境模板 [.env.example](.env.example)
- 主配置改造为环境变量驱动，默认可开箱运行

## 说明

该项目用于学习与演示。生产环境部署请补充：

- 生产级 SECRET_KEY 与 DEBUG=False
- 严格的 ALLOWED_HOSTS
- 生产 WSGI/ASGI 服务与反向代理
- 完整权限、审计与日志策略
