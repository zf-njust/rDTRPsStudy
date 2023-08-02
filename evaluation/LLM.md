# Analysis of Type Smell Detection using Large Language Models

## Introduction

Type smells are indicators of poor code quality that can lead to various problems such as maintenance issues, poor performance, and even security vulnerabilities. In recent years, large language models such as GPT-3 and GPT4 have shown remarkable performance in various natural language processing tasks. Here we present an analysis of type smell detection using large language models.

## Data

We collected a dataset of 900 code samples, which were labeled as having either one of six types of type smells or no type smell at all. Among the samples, 300 had no type smell, and the remaining 600 had different type smells (100 samples for each type smell).

## Data Processing

We shuffled the dataset and split it into training, validation, and test sets in the 8:1:1 ratio uniformly. Next, we process the code and type smell labels into a format suitable for the large language model to read. Each large language model was evaluated on the same test samples.

First, we need a system prompt to instruct the large language model to play a certain role in the dialogue. Here, we use the prompt "Now you are a programming expert with extensive python coding experience." Next, we assemble the code snippets to be detected in markdown format and give the task prompt, which is to detect type smells.

## Model and Experiment

To compare the performance of different large language models in type smell detection, we selected two models as our experimental objects: ChatGPT and Llama2. ChatGPT is a state-of-the-art online language model developed by OpenAI. Llama2 is a new generation large language model released by Meta.

We treat the type smell detection problem as a 7-class classification task, where label 0 represents no type smell, and label 1 ot 6 represent the six types of type smells. We evaluated the performance of the models using multi-class accuracy, recall, and F1 score.

## Model1 - ChatGPT

We used the GPT-3.5-turbo-16k-0613 model from OpenAI to detect type smells, which has a maximum context length of 16K. This context length is sufficient to prevent code samples from exceeding the maximum length. To further improve the model's few-shot learning ability, we provide example code snippets for each type of type smell.

Here is the specific prompt template we used for ChatGPT to detect type smells:

A type smell is any dynamic typing related characteristic in the source code of a Python program that possibly indicates a deeper problem.
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

Please determine which of the following codes contains a type smell or no type smell:

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

## ChatGPT-Results

Macro Precision on all data: 0.3143460154533386

Micro Precision on all data: 0.3636363744735718

Macro Recall on all data: 0.18203464150428772

Micro Recall on all data: 0.3636363744735718

Multi class Precision on all data:

[0.3671, 0.0000, 0.0000, 1.0000, 0.3333, 0.0000, 0.5000]

Multi class Recall on all data:

[1.0000, 0.0000, 0.0000, 0.0909, 0.0833, 0.0000, 0.1000]

Multi class F1 on all data:

[0.5370, 0.0000, 0.0000, 0.1667, 0.1333, 0.0000, 0.1667]

## Model2-Llama2

The recent release of Llama2, a new generation large language model by Meta, has opened up new possibilities for type smell detection. Compared to its predecessor, Llama, Llama2 has a 40% increase in pre-training data and extends to a context length of 4096, available in three versions - 7B, 13B, and 70B. Llama2 has demonstrated superior performance in many benchmark tests, including inference, encoding, proficiency, and knowledge testing.

Fine-tuning is a technique used in machine learning to adapt a pre-trained model to a specific task by further training on a smaller labeled dataset. Fine-tuning allows the pre-trained model to leverage its knowledge of the language to learn task-specific features from the labeled data and improve its performance on the target task.

The fine-tuning process involves initializing the pre-trained language model with its weights, adding a task-specific layer in the model, and then training the model on the labeled dataset. During training, the model updates its parameters to minimize the loss function to adapt to downstream tasks such as type smell detection.

Due to limited local computational resources, we had access to only two NVIDIA TESLA A100 80G graphics cards. Therefore, we selected the 7B version of the Llama2 model for our experiments. To further optimize our computational efficiency, we used the LORA (Low-Rank Adaptation of Large Language Models) method and set the LORA dimension was set to 128.

LoRA (Low-Rank Adaptation) is a technique proposed for natural language processing that allows for efficient adaptation of pre-trained language models to specific tasks or domains. The approach involves freezing the weights of a pre-trained model and introducing trainable rank decomposition matrices into each layer of the Transformer architecture used in the model. By doing so, the number of trainable parameters for downstream tasks is greatly reduced, making it more feasible to fine-tune larger models.

We use a batch size of 32, a learning rate of 2e-5, and a maximum context length of 1024. The model is trained for a total of 200 epochs with 3900 steps, and checkpoints are saved every 20 steps. We evaluate the model on the test set every 100 steps.


## Llama2-Results

Precision, recall, and F-measure are shown in the csv files.





