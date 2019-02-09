# PyStuck

This is a simple tool for Python 3 which gets you instant help from StackOverflow for your problems. Just include @PyStuck in your project and don't get stuck. The tool uses data crunched from [StackOverflow's Python dataset](https://www.kaggle.com/stackoverflow/pythonquestions/home) from August 2, 2008 and October 19, 2016. 

When you get an exception, it will automatically recommend you relevant questions and their answers to help solve your problem. 

![How it works](https://github.com/dev-td7/PyStuck/raw/master/images/working.png "StackOverflow right in your terminal")

## Easy to Use

There are not many requirements for this tool.

```
html2text==2018.1.9
scikit-learn==0.20.2
pandas==0.23.0
nltk==3.4
```

__Step 0__: Installation
___

_Option 1: Manual installation_

* Download _Questions.csv_ and _Answers.csv_ files from [Kaggle's StackOverflow Python dataset.](https://www.kaggle.com/stackoverflow/pythonquestions/home)
* Clone this repository and add the above .csv files into the repository folder.
* Run prepare_data.py to create data files. The size of these files is large and thus, not included with this repository.

_Option 2: From GitLab_
* Go to [this project's GitLab page](https://gitlab.com/td7/pystuck) and clone the repository. It includes data files.

Soon, the tool will be converted into a library and can be then installed using pip.

__Step 1__: Wrap your program into a function as below:

___

```
def some_wrapper_function():
    # Do something here. It's safe now.
    # Bye
```

__Step 2__: Import PyStuck and put @PyStuck decorator before your wrapper function.

___

```
from PyStuck import PyStuck

@PyStuck
def some_wrapper_function():
    # Do something here. It's safe now.
    # Bye
```

Whenever your program raises an exception, PyStuck will catch it and do it's magic.

## Credits

[StackOverflow's Python dataset from Kaggle](https://www.kaggle.com/stackoverflow/pythonquestions/home)

[StackOverflow.com](https://stackoverflow.com)