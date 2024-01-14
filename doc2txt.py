from docx import Document
from pathlib import Path
import os
import sys

if (args_count := len(sys.argv)<2 ):
    print ("Provide a file name ")
    raise SystemExit(2)
file_name=sys.argv[1]
text=""
text_file_name=file_name.replace(".docx",".txt")      
document = Document (file_name)
all_paras = document.paragraphs
for para in all_paras:
    text+=para.text+"\n"

with open(text_file_name,"w") as f:
    f.write(text)
