# un-code-mixed-mt
Machine Translation of Code-Mixed data.

This repo contains:
1. unique_mapping.py - Python code to generate code-mixed data.
2. Three subdirectories (Hindi-English, German-English, French-English) which contains testsets used to report models performance.
 
Generating code-mixed data:
In our experiments, we are always keeping English as target language and only source language (Hindi, German, French) will be changed. We have generated alignments in this way only (keeping English as target). But the code will work in any direction and based on the direction, the alignments needs to be generated.

The python file (unique_mapping.py) takes three inputs:
  1. source side of given parallel corpus (Hindi/German/French in this case)
  2. target side of given parallel corpus (English in this case)
  3. alignment file between the source-target (Hindi/German/French to English in this case)
  
 The alignment file can be obtained from fast_align (https://github.com/clab/fast_align/)
 
 The parallel corpora can be obtained from following links:
 
 Hindi-English corpus: https://www.cfilt.iitb.ac.in/~parallelcorp/iitb_en_hi_parallel/
 
 German-English and French-English corpus: http://www.statmt.org/wmt14/translation-task.html
