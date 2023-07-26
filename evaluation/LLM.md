# Dataset

the samples having no type smells: 300
the samples having each type of type smells：100
Total: 900 samples
m
# Data Processing

The labels consist of 0, 1, 2, 3, 4, 5, 6, 7. 0 indicates no type smell, and 1-6 indicate the type id of type smells. 
All the samples in the dataset is uniformly divided into training set, verification set, and test set with a ratio of 8:1:1.

# Experiment

In the experiment, multi-classification accuracy, recall, and F1-measure are used to evaluate the performance of the model. The experiment is repeated three times and the average value is used as the final result.

## ChatGPT

We select gpt-3.5-turbo-16k-0613 model of OpenAI. The context length of the model is set as 16K to prevent code from getting too long beyond the context length.

Hints For the Model：

A type smell is any dynamic typing practice in the source code of a Python program that possibly indicates a deeper problem.
Here we have six types of type smells:

1. The variable is redefined with an inconsistent type object.
2. The values of an argument hold inconsistent types in different function calls.
3. The variable referenced in the statement has inconsistent types.
4. The element is deleted from a container by a dynamically determined index.
5. The attribute is deleted from an object through a dynamically determined name.
6. The attribute is visited based on a dynamically determined name.

Examples:
Type 1 (Inconsistent Assignment Types)：One variable is redefined with an inconsistent type object.

```python
module_name = { QT_API_PYSIDE: 'PySide',
    QT_API_PYQT: 'PyQt4',
    QT_API_PYQTv1: 'PyQt4',
    QT_API_PYQT5: 'PyQt5',
    QT_API_PYQT_DEFAULT: 'PyQt4'}
...
module_name = module_name[api]
```

Type 2 (Inconsistent Argument Types): The values of an argument hold inconsistent types in different function calls.

```python
logging.warning((red.response.http_error.desc, vars(red.response.http_error), url))
...
logging.warning("Starting fetch with curl client")
```

Type 3 (Inconsistent Variable Types): The variable referenced in a statement has inconsistent types.

```python
def get_inventory(enterprise, config):
    if cache_available(config):
        inv = get_cache(‘inventory’, config)
    else:
        …
        inv = generate_inv_from_api(enterprise, config)
    save_cache(inv, config)
```

Type 4 (Dynamic Element Deletion): The element is deleted from a container by a dynamically determined index.

```python
for k, v in list(six.iteritems(namecount)):
    if v == 1:
        del namecount[k]
```

Type 5 (Dynamic Attribute Deletion): One attribute is deleted from an object through a dynamically determined name.

```python
delattr(obj.__class__, self.name)
```

Type 6 (Dynamic Attribute Access): One attribute is visited based on a dynamically determined name.

```python
dep_value = getattr(dep, attr)
```

Please determine which of the following codes contains a code smell or no code smell:

```python
{{CODE_PLACEHOLDER}}
```

Please return the result as json:

```json
{
"smell": [
        {
            "smell_id": SMELL_ID,
            "description": SMELL_DESC
        }
    ]
}
```

Experiment Result：
Macro Precision on all data: 0.3143460154533386

Micro Precision on all data: 0.3636363744735718

Macro Recall on all data: 0.18203464150428772

Micro Recall on all data: 0.3636363744735718

Multi class Precision on all data ([0, Type 1, Type 2, Type 3, Type 4, Type 5, Type6]): 

[0.3671, 0.0000, 0.0000, 1.0000, 0.3333, 0.0000, 0.5000]

Multi class Recall on all data ([0, Type 1, Type 2, Type 3, Type 4, Type 5, Type6]):

 [1.0000, 0.0000, 0.0000, 0.0909, 0.0833, 0.0000, 0.1000]

Multi class F1 on all data ([0, Type 1, Type 2, Type 3, Type 4, Type 5, Type6]):

 [0.5370, 0.0000, 0.0000, 0.1667, 0.1333, 0.0000, 0.1667]

## LLAMA2

Llama2是由meta于2023年7月19日发布的新一代大语言模型，相比于上一代Llama其增加了40%的预训练数据，拓展至4096的上下文长度，分为7B，13B，70B三个版本。
Llama 2在许多基准测试中表现优异，包括推理、编码、熟练度测试和知识测试。
实验环境：l两张显卡NVIDIA TESLA A800 80G。batch size 32，学习率2e-5，最大context长度1024.
由于实验资源所限，我们选择7B版本的Llama2进行微调，采用LORA策略，lora维度为128。

一共训练了200个epoch，3900个step，每20步保存一个检查点

实验过程loss变化：

![](C:\Users\wangjun\Desktop\20230725code%20smell实验\学习率.png)

![](C:\Users\wangjun\Desktop\20230725code%20smell实验\train_loss_epoch.png)

![](C:\Users\wangjun\Desktop\20230725code%20smell实验\trainb_loss_step.png)

![](C:\Users\wangjun\Desktop\20230725code%20smell实验\val_loss_epoch.png)

![](C:\Users\wangjun\Desktop\20230725code%20smell实验\val_loss_step.png)

实验结果：
