from docx import Document
from indic_transliteration import sanscript
from pathlib import Path
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
import re
import sys
#from doc_utils import escape_for_latex
import jinja2
import subprocess
import tempfile
import os
import json
'''
Bug : Need to add the english prefix into the json tree
'''

def CreatePdf (templateFileName,name,DocfamilyName,data):
    outputdir="outputs"
    logdir="logs"
    latex_jinja_env = jinja2.Environment(
        block_start_string = '\BLOCK{',
        block_end_string = '}',
        variable_start_string = '\VAR{',
        variable_end_string = '}',
        comment_start_string = '\#{',
        comment_end_string = '}',
        line_statement_prefix = '%-',
        line_comment_prefix = '%#',
        trim_blocks = True,
        autoescape = False,
        loader = jinja2.FileSystemLoader(os.path.abspath('.'))
    )
    TexFileName=f"{name}_{DocfamilyName}_Unicode.tex"
    PdfFileName=f"{name}_{DocfamilyName}_Unicode.pdf"
    TocFileName=f"{name}_{DocfamilyName}_Unicode.toc"
    LogFileName=f"{name}_{DocfamilyName}_Unicode.log"
    template = latex_jinja_env.get_template(templateFileName)
    if DocfamilyName == "Samhita":
        document = template.render(kanda=data,invocation=invocation,title=title)
    elif DocfamilyName == "Pada":
        document = template.render(prasna=data,invocation=invocation,title=title)
    tmpdirname="."
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpfilename=f"{tmpdirname}/{TexFileName}"

        with open(tmpfilename,"w") as f:
            f.write(document)
        result = subprocess.Popen(["latexmk","-xelatex", "--interaction=nonstopmode","--silent",tmpfilename],cwd=tmpdirname)
        result.wait()
        src_pdf_file=Path(f"{tmpdirname}/{PdfFileName}")
        dst_pdf_file=Path(f"{outputdir}/{PdfFileName}")
        src_log_file=Path(f"{tmpdirname}/{LogFileName}")
        dst_log_file=Path(f"{logdir}/{LogFileName}")
        #src_toc_file=Path(f"{tmpdirname}/{TocFileName}")
        #dst_toc_file=Path(f"{outputdir}/{TocFileName}")
        src_tex_file=Path(f"{tmpdirname}/{TexFileName}")
        dst_tex_file=Path(f"{outputdir}/{TexFileName}")
        
        if result.returncode != 0:
            print('Exit-code not 0  check Code!')
            exit_code=1
        path = Path(src_tex_file)
        if path.is_file():
            src_tex_file.rename(dst_tex_file)  
        path = Path(src_pdf_file)
        if path.is_file():      
            src_pdf_file.rename(dst_pdf_file)
        path = Path(src_log_file)
        if path.is_file():
            src_log_file.rename(dst_log_file)
        #src_toc_file.rename(dst_toc_file)



def escape_for_latex(data):
    if isinstance(data, dict):
        new_data = {}
        for key in data.keys():
            new_data[key] = escape_for_latex(data[key])
        return new_data
    elif isinstance(data, list):
        return [escape_for_latex(item) for item in data]
    elif isinstance(data, str):
        # Adapted from https://stackoverflow.com/q/16259923
        latex_special_chars = {
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\^{}",
            "\\": r"\textbackslash{}",
            "\n": "\\newline%\n",
            "-": r"{-}",
            "\xA0": "~",  # Non-breaking space
            "[": r"{[}",
            "]": r"{]}",
        }
        return "".join([latex_special_chars.get(c, c) for c in data])

    return data
ts_string = Path("TS_withPada.json").read_text(encoding="utf-8")
parseTree = json.loads(ts_string)

DocfamilyName="Samhita"
samhitaTemplateFile=f"templates/{DocfamilyName}_main.tex"
padaTemplateFile="templates/Pada_main.tex"
beginningTemplateFile=f"templates/{DocfamilyName}_title.tex"
endingTemplateFile=f"templates/{DocfamilyName}_end.tex"

outputdir="outputs"
logdir="logs"
latex_jinja_env = jinja2.Environment(
block_start_string = '\BLOCK{',
block_end_string = '}',
variable_start_string = '\VAR{',
variable_end_string = '}',
comment_start_string = '\#{',
comment_end_string = '}',
line_statement_prefix = '%-',
line_comment_prefix = '%#',
trim_blocks = True,
autoescape = False,
loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)

print("running xelatex with ",samhitaTemplateFile)
template = latex_jinja_env.get_template(samhitaTemplateFile)
kandaInfo=1
kanda=parseTree['TS']['Kanda'][kandaInfo-1]
for kanda in parseTree['TS']['Kanda']:
    invocation=kanda['Prasna'][0]['invocation'].strip()
    #invocation=invocation.replace("\n","\\\\")
    kandaInfo=kanda['id']
    title=kanda['title']
    
    for prasna in kanda['Prasna']:
        prasnaInfo=prasna['id']
        CreatePdf(padaTemplateFile,f"TS_{kandaInfo}_{prasnaInfo}","Pada",prasna)
        for anuvakkam in prasna['Anuvakkam']:
            for panchasat in anuvakkam['Panchasat']:
                #print("Panchasat ",panchasat)
                pass

    #document = template.render(kanda=kanda,invocation=invocation,title=title)
    CreatePdf(samhitaTemplateFile,f"TS_{kandaInfo}",DocfamilyName,kanda)

    

#return exit_code
