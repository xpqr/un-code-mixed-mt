# code-mixed-mt
Machine Translation of Code-Mixed data.

This repo contains:
1. unique_mapping.py - Python code to generate code-mixed data.
2. Three subdirectories (Hindi-English, German-English, French-English) which contains testsets used to report models performance.

Generating code-mixed data:
The python file (unique_mapping.py) takes three inputs:
  1. source side of given parallel corpus
  2. target side of given parallel corpus
  3. alignment file between the source-target
  
 The alignment file can be obtained from fast_align (https://github.com/clab/fast_align/)
 
 The parallel corpora can be obtained from following links:
 
 Hindi-English corpus: https://www.cfilt.iitb.ac.in/~parallelcorp/iitb_en_hi_parallel/
 
 German-English and French-English corpus: http://www.statmt.org/wmt14/translation-task.html
