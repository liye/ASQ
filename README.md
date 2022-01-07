# ASQ

#### 2022/01/07 Update #### 

To complement the binary choice format of the task in the original release (see below), we further consider a generative version of the task, as demo-ed in this [notebook](https://github.com/liye/ASQ/blob/generation/constructing_dataset_for_generative_ASQ.ipynb). 

------

Dataset of personal narratives with **A**dvice-**S**eeking **Q**uestions. Version 1.0.  

Distributed together with the paper [Asking the Right Question: Inferring Advice-Seeking Intentions from Personal Narratives](http://www.cs.cornell.edu/~cristian/Advice-seeking_intentions.html). Liye Fu, Jonathan P. Chang and Cristian Danescu-Niculescu-Mizil. NAACL 2019. 

#### Dataset details

The dataset has been split into train, test, heldout sets, with 8865, 2500, 10000 test instances each. Each set is saved as an individual json file inside the [data](https://github.com/cornellNLP/ASQ/tree/master/data) directory. We have further reserved 500 instances for human annotations. Check inside the [annotations](https://github.com/cornellNLP/ASQ/tree/master/annotations) directory for more information. 

#### Usage

You can explore our dataset as follows: 

```python
import json

# read training set
with open("asq_train.json", "r") as f:
	data = json.load(f)

# for each individual test instance, the following fields are provided:
data[0]

# expected output
{"narrative": ..., # the question-stripped narrative 
 "qn1": ..., # candidate question 1 for the given narrative 
 "qn2": ..., # candidate question 2 for the given narrative
 "label": ..., # 0 if qn1 is the correct answer, 1 otherwise
 "id": ...} # Reddit post ID of the post from which the instance is obtained
```
