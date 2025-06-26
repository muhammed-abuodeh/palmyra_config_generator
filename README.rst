Palmyra Configuration Generator
=============

Introduction
------------
When annotating trees using `Palmyra <https://palmyra.camel-lab.com/>`_, you have the choice of using one of the built-in configuration files,
allowing you to use the POS tags, dependency relation labels, and (in some configuration files) moprhological features.

If you have your own tags and labels to use, you may use this tool to generate your own configuration file to upload when annotating a conll file.

Currently, this tool does not generate morphological features.

Installation
------------
1. Clone this repo

2. Set up a virtual environment and install the required packages:

.. code-block:: bash

    pip install -r requirements.txt

Creating the configuration input
--------------------------------
A tsv file is required to generate the configuration file. You can refer to the sample tsv files in the data folder. 
The sample_output.config is the result of passing sample.tsv.


The only required columns are 'type' and 'label'. If you add a 'group' column the labels will appear grouped in Palmyra.

The 'type' can be 'pos' or 'relation'.


The 'keys' column gives the ability to use keyboard shortcuts when annotating. If this column is not added, the generator
will automatically take the lowercase version of the first character of each label. For Arabic, we use the shortcut_list.tsv map in the data folder.


Finally, the default POS tag should also be passed. This is used when creating new nodes in Palmyra.

Examples
--------

Given all columns:

.. code-block:: bash

    python main.py -i 'data/sample.tsv' -d "NOM"

Given only the 'type' and 'label' columns:

.. code-block:: bash

    python main.py -i 'data/sample_without_group_key_columns.tsv' -d "NOM"
