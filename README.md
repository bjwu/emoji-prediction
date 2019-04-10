## emoji-prediction
emoji prediction given a text using machine learning techniques


#### REF:

`sklearn_experiments.py`：使用TFIDF处理文本，将emoji直接当作target，做监督学习进行预测的方法。此文件并未使用HADOOP，SPARK。

`recommend.py`: 对于`sklearn_experiments.py`预测出来的模型，对于输入新的句子进行emoji预测的脚本。

`w2v_training3.py`：以`sklearn_experiments.py`为模版，使用pyspark的word2vec模型训练爬取出来的twitter数据训练词向量（词向量长度可调），
word2vec模型可将一个句子利用训练好的词向量生成一个句向量（`'features'`列）。 之后用了LR模型进行了学习，模型保存在HADOOP中：

几个问题：
1. 模型一定要保存在HADOOP中吗？可否直接保存在内存中？

2. 模型保存在HADOOP中后怎么load？（单纯pyspark语法问题）



