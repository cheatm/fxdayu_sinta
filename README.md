# fxdayu_sinta

用于抓取sina tick数据并合成K线数据写入MongoDB。


## 用pip安装

> pip install git+https://github.com/cheatm/fxdayu_sinta.git

## 初始化

### 创建配置文件
PATH为要存储文件的目录
> sinta init config PATH
可以通过添加环境变量FXDAYU来指定配置文件的目录
例如添加环境变量FXDAYU=~/fxdayu，配置文件会生成在~/fxdayu/sinta/目录中

### 创建文件索引
可以用参数 -s yyyy-mm-dd, -e yyyy-mm-dd 指定索引长度
> sinta init create

## 下载tick数据

可以用参数 -s yyyy-mm-dd, -e yyyy-mm-dd 指定请求范围
> sinta request tick

下载数据所用时间可能较长，可以先指定一段较短时间的数据测试。

## 根据tick数据文件更新主索引：
> sinta master file

## 讲tick数据整理成一分钟数据写入数据库
> sinta write master

## 根据数据库更新主索引
> sinta master db

## 扩展主索引
可用参数 -s yyyy-mm-dd, -e yyyy-mm-dd 指定扩展范围
> sinta master update




