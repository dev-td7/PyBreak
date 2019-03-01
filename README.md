# PyBreak - StackOverflow in your terminal

This is a simple tool for Python 3 which brings StackOverflow in your terminal. Just include @PyBreak in your project and don't get stuck. The tool uses data crunched from [StackOverflow's Python dataset](https://www.kaggle.com/stackoverflow/pythonquestions/home) from August 2, 2008 and October 19, 2016. 

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

* Download _Questions.csv_ and _Answers.csv_ files from [My GitLab repository](https://gitlab.com/td7/pybreak/tree/master/data)
* Clone this repository and add the above .csv files into the repository folder (Recommended). Or you can directly download model files from my GitLab (Not recommended).
* Run prepare_data.py to create data files. The size of these files is large and thus, not included with this repository.

Soon, the tool will be converted into a library and can be then installed using pip.

__Step 1__: Wrap your program into a function as below:

___

```
def some_wrapper_function():
    # Do something here. It's safe now.
    # Bye
```

__Step 2__: Import PyBreak and put @PyBreak decorator before your wrapper function.

___

```
from PyBreak import PyBreak

@PyBreak
def some_wrapper_function():
    # Do something here. It's safe now.
    # Bye
```

Whenever your program raises an exception, PyBreak will catch it and do it's magic.

## Credits

[StackOverflow's Python dataset from Kaggle](https://www.kaggle.com/stackoverflow/pythonquestions/home)

[StackOverflow.com](https://stackoverflow.com)