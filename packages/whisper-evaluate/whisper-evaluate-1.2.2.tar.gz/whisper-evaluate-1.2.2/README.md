# whisper-evaluate

Evaluate the effectiveness of the Whisper model.

## Install
从pypi安装:
```shell script
pip install whisper-evaluate
```
从本地安装:
```shell script
git clone https://git.xindong.com/fengyanglu/whisper-evaluate.git
cd whisper-evaluate
pip install dist/whisper_evaluate-1.2.0-py3-none-any.whl
```

## How to use
参考[test.py](./test.py)
```shell script
from whisper_evaluate import Report
import pprint

if __name__ == '__main__':
    # 有三个参数: 
    # task_name: 任务名称
    # xd_other_type: 语心除了整体和政治,需要计算的分类指标, 传入一个list 如: ["色情", "辱骂"]
    # wy_other_type: 网易除了整体和政治,需要计算的分类指标
    rep = Report(task_name="testv1.1")
    # 生成评估报告
    # 三个参数是 标准测试数据文件路径/语心原始结果数据文件路径/网易原始结果数据文件路径 
    result = rep.report("test_data/test-data-standard-latest.csv",
                   "test_data/test-data-standard-latest-whisper1.1-res.txt",
                   "test_data/test_antispam_0727.txt")
    pprint.pprint(result)
    # 保存统计备查数据 和 计算结果
    rep.save()
    


    # 单独计算whisper结果
    result = rep.whisper_report("test_data/test-data-standard-latest.csv",
                   "test_data/test-data-standard-latest-whisper1.1-res.txt")
    pprint.pprint(result)
    
    # 单独计算netease结果
    result = rep.netease_report("test_data/test-data-standard-latest.csv",
                   "test_data/test_antispam_0727.txt")
    pprint.pprint(result)

    
```

## APIS

### WhisperStatistics
- 初始化模型计算对象
```python
from whisper_evaluate import WhisperStatistics
ws = WhisperStatistics("path/to/test_stand_file", "path/to/result_file")
```

- 评估模型
```python
# 整体和政治之外需要计算的分类
other_type = []
ws.count_all(other_type)
```

- 获取评估结果
```python
ws.indicator
```

### NetEaseStatistics
- 初始化模型计算对象
```python
from whisper_evaluate import NetEaseStatistics
ns = NetEaseStatistics("path/to/test_stand_file", "path/to/result_file")
```

- 评估模型
```python
# 整体和政治之外需要计算的分类
other_type = []
ns.count_all(other_type)
```

- 获取评估结果
```python
ns.indicator
```