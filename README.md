# statics-ansible

analysis and static of host info from ansible output 

通过python执行ansible命令统计主机信息


## 说明

### 版本说明

Python >= 3.7

ansible >= 2.0


### 项目说明

通过ansible adhoc批量执行命令（代码中为获取所有docker容器内存情况）；

获取返回值；

统计分析；

输出到csv文件

### 源数据

支持从redis或json文件获取主机信息（数据源为阿里云api）。


统计输出Excel文件，格式为.csv。
