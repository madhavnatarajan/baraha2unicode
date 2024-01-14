
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

def cleanupText(text):
    #pattern1=r"[\d]+"
    pattern2=r"\([\d]+/[\d]+\)"
    pattern3=r"\(A[\d]+\)"
    #print ("Entering cleanup for ")
    anuvakkamEndPattern = r"[\d]+[\s]\([\d]+/[\d]+\)(.*)[\s]*(\(A[\d]+\)$)"
    panchasatEndPattern = r"[\d]+[\s]\([\d]+/[\d]+\)$"

    anuvakkamEndResult=re.search(anuvakkamEndPattern,text)
    panchasatEndResult=re.search(panchasatEndPattern,text)
    text1=text
    if anuvakkamEndResult:
        #text1=re.sub(anuvakkamEndResult.group(),"",text)
        text1=text.replace(anuvakkamEndResult.group(),"")
        #print("Also matched the anuvakkam pattern ",anuvakkamEndResult.group(1),anuvakkamEndResult.group(2))
    elif panchasatEndResult:
        #text1=re.sub(panchasatEndResult.group(),"",text)
        text1=text.replace(panchasatEndResult.group(),"")
        #print("Also matched the panchasat pattern ",panchasatEndResult.group())
    
    #print(result1)
    return text1
def updateMarkupFile(text,metaInformation,outputdir):
    '''
        Get the text . 
        Get the metadata . 
        Create hashmap with keys and values
        If file exists :
             Read existing contents into a hashmap
             update hashmap with extrakeys if found
        
        Replace contents of hashmap with new text 
        Write file 
    '''
    myhash={}
    outfile=f"{outputdir}/{metaInformation}.json"
    p1 = Path(outfile)
    if p1.is_file():
        with open(outfile,"r") as existingFile:
            myhash=json.load(existingFile)
            #myhash=json.loads(myhash_str)
            myhash.update({documentType:text})  # File already existed either from Pada / Samhita / Krama

    else:
        myhash={}
        metaInfoSplit=metaInformation.split(".")
        kandaInfo = prasnaInfo = anuvakkamInfo = panchasatInfo =""
        if len(metaInfoSplit) >=4:
            kandaInfo=metaInfoSplit[0]
            prasnaInfo=metaInfoSplit[1]
            anuvakkamInfo=metaInfoSplit[2]
            panchasatInfo=metaInfoSplit[3]
            myhash["id"]=metaInformation
            newobj={}
            
            newobj["kanda"]=kandaInfo
            newobj["prasna"]=prasnaInfo
            newobj["anuvakkam"]=anuvakkamInfo
            newobj["panchasat"]=panchasatInfo
            myhash["classification"]=newobj
            myhash.update({documentType:text})
    #print(documentType," is the type an file is ",outfile)
    
    with open(outfile,"w") as f:
        #json_data = json.dumps(myhash, ensure_ascii=False) 
        #print(myhash)
        json.dump(myhash,f,ensure_ascii=False)
    return 0

def generatePdf (document, DocfamilyName): 
    exit_code=0
    mainTemplateFile=f"templates/{DocfamilyName}_main.tex"
    beginningTemplateFile=f"templates/{DocfamilyName}_title.tex"
    endingTemplateFile=f"templates/{DocfamilyName}_end.tex"
    TexFileName=f"{DocfamilyName}.tex"
    PdfFileName=f"{DocfamilyName}.pdf"
    TocFileName=f"{DocfamilyName}.toc"
    LogFileName=f"{DocfamilyName}.log"
    outputdir="outputs"
    logdir="logs"

    beginningText=""
    endingText=""
    titlepath=Path(beginningTemplateFile)
    if titlepath.is_file():
        beginningText=titlepath.read_text()
    endpath=Path(endingTemplateFile)
    if endpath.is_file():
        endingText=endpath.read_text()

    text=""
    TS_STATE=False
    TS_TEXT=""
    all_paras = document.paragraphs
    for para in all_paras:
        data=para.text
        words=data.split()
         
        
        
        if (len(words) >0):
            #print(data)
            pageSeparatorResult = re.match(pageSeparatorPattern,words[0])
            titleResult = re.match(titlePattern,words[0])
            boldResult1 = re.match(boldPattern1,words[0])
            boldResult2 = re.match(boldPattern2,words[0])
            tsseparatorresult = re.match(tspattern,data)
            metaPatternResult=re.search(metaPattern,data)
            tsseparatorresult1=re.search(tspattern1,data)
            text = text.replace("\uA8E3","\u1CDA") # This ideally would have been in baraha.toml . But

            if pageSeparatorResult or titleResult or boldResult1 or boldResult2 or tsseparatorresult or tsseparatorresult1:
                if TS_STATE:
                    TS_STATE=False
                    TS_TEXT=cleanupText(TS_TEXT)
                    #print("TS_TEXT_START_1",TS_TEXT,"TS_TEXT_END_1")
                    #text+=transliterate(TS_TEXT, sanscript.BARAHA, sanscript.DEVANAGARI)+"\\par \n"
                    if documentType == "Krama":
                        t3=transliterate(TS_TEXT, sanscript.BARAHA, sanscript.DEVANAGARI)+"\\par \n"
                        t=t3.replace("।","\\switchcolumn")
                    #print(t)
                        t1="\\begin{paracol}{2}"
                        t2="\\end{paracol}"
                    
                        text+=t1+t+t2
                    else:
                        text+=transliterate(TS_TEXT, sanscript.BARAHA, sanscript.DEVANAGARI)+"\\par \n"
                    TS_TEXT="" 
            
            if pageSeparatorResult:
                #print("Matched Separator ",pageSeparatorResult.group() )
                text+= "\\pagebreak \n"
                
            elif titleResult:
                #print("Matched Title ",titleResult.group())
                data=data.replace(words[0],"")
                if ("___no___" not in data):
                    text+="\\addcontentsline{toc}{section}{"+transliterate(data, sanscript.BARAHA, sanscript.DEVANAGARI) +"}\n"
                    text+="\\markright{"+transliterate(data, sanscript.BARAHA, sanscript.DEVANAGARI)+"\\hfill www.vedavms.in\\hfill}\n"
                    text+="\\section*{"+transliterate(data, sanscript.BARAHA, sanscript.DEVANAGARI)+"}\n"
                else:
                    data=data.replace("___no___","")
                    text+="\\textbf{"+transliterate(data, sanscript.BARAHA, sanscript.DEVANAGARI)+"}\\par\n"

            elif boldResult1 or boldResult2:
                #print("Matched bold " ,data)
                text+="\\textbf{"+transliterate(data, sanscript.BARAHA, sanscript.DEVANAGARI)+"}\\par\n"

            elif tsseparatorresult1:
                #print("matched tsseparator1",data)
                data=data.replace(words[0],"")
                text+="\\textbf{"+data+"}\\par\n"
                TS_STATE=True

            elif tsseparatorresult:
                #print("Matched tsseparator",data)
                data=data.replace(words[0],"")
                text+="\\textbf{"+data+"}\\par\n"
            
            else:
                '''if documentType == "Krama":
                    t3=transliterate(data, sanscript.BARAHA, sanscript.DEVANAGARI)
                    t=t3.replace("।","\\switchcolumn")
                    #print(t)
                    t1="\\begin{paracol}{2}"
                    t2="\\end{paracol}"
                    
                    text+=t1+t+t2
                else:'''
                if  TS_STATE:
                    TS_TEXT+=data
                else:
                    #print("matched nothing")
                    text+=transliterate(data, sanscript.BARAHA, sanscript.DEVANAGARI)+"\\par \n"
        else:
            if TS_STATE:
                TS_STATE=False
                TS_TEXT=cleanupText(TS_TEXT)
                #print("TS_TEXT_START",TS_TEXT,"TS_TEXT_END")
                
                #text+=transliterate(TS_TEXT, sanscript.BARAHA, sanscript.DEVANAGARI)+"\\par \n"
                ''' has to be coded better. There is a text in the anuvakka that needs to come after the
                switch column. We are just deleting it for now . But that has to be returned and put after this
                '''
                if documentType == "Krama":
                        t3=transliterate(TS_TEXT, sanscript.BARAHA, sanscript.DEVANAGARI)+"\\par \n"
                        t=t3.replace("।","\\switchcolumn")
                    #print(t)
                        t1="\\begin{paracol}{2}"
                        t2="\\end{paracol}"
                    
                        text+=t1+t+t2
                else:
                    text+=transliterate(TS_TEXT, sanscript.BARAHA, sanscript.DEVANAGARI)+"\\par \n"
                TS_TEXT=""
            #print("paragraph has zero words ")            

    #return 0 # Temporary fix to prevent commenting code
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

    print("running xelatex with ",mainTemplateFile)
    template = latex_jinja_env.get_template(mainTemplateFile)
    document = template.render(beginningText=beginningText,text=text,endingText=endingText)
    
    tmpdirname="."
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpfilename=f"{tmpdirname}/{TexFileName}"
        
        with open(tmpfilename,"w") as f:
            f.write(document)
        result = subprocess.Popen(["latexmk","-xelatex", "--interaction=nonstopmode", "--silent",tmpfilename],cwd=tmpdirname)
        result.wait()
        src_pdf_file=Path(f"{tmpdirname}/{PdfFileName}")
        dst_pdf_file=Path(f"{outputdir}/{PdfFileName}")
        src_log_file=Path(f"{tmpdirname}/{LogFileName}")
        dst_log_file=Path(f"{logdir}/{LogFileName}")
        src_toc_file=Path(f"{tmpdirname}/{TocFileName}")
        dst_toc_file=Path(f"{outputdir}/{TocFileName}")
        src_tex_file=Path(f"{tmpdirname}/{TexFileName}")
        dst_tex_file=Path(f"{outputdir}/{TexFileName}")
            
        if result.returncode != 0:
            print('Exit-code not 0  check Code!')
            exit_code=1

        src_tex_file.rename(dst_tex_file)        
        src_pdf_file.rename(dst_pdf_file)
        src_log_file.rename(dst_log_file)
        #src_toc_file.rename(dst_toc_file)
        
        return exit_code

def generateMarkup (document, DocfamilyName,documentType): 
    
    exit_code=0
    
    outputdir="outputs/json"
    logdir="logs"

    
    text=""
    outfile=""
    
    TS_STATE=False
    TS_TEXT=""
    text=""
    TS_STATE=False
    TS_TEXT=""
    all_paras = document.paragraphs
    for para in all_paras:
        data=para.text
        words=data.split()
         
        
        
        if (len(words) >0):
            #print(data)
            pageSeparatorResult = re.match(pageSeparatorPattern,words[0])
            titleResult = re.match(titlePattern,words[0])
            boldResult1 = re.match(boldPattern1,words[0])
            boldResult2 = re.match(boldPattern2,words[0])
            tsseparatorresult = re.match(tspattern,data)
            metaPatternResult=re.search(metaPattern,data)
            tsseparatorresult1=re.search(tspattern1,data)
            text = text.replace("\uA8E3","\u1CDA") # This ideally would have been in baraha.toml . But

            if pageSeparatorResult or titleResult or boldResult1 or boldResult2 or tsseparatorresult or tsseparatorresult1 or metaPatternResult:
                if TS_STATE:
                    TS_STATE=False
                    TS_TEXT=cleanupText(TS_TEXT)
                    #print("TS_TEXT_START_1",TS_TEXT,"TS_TEXT_END_1")
                    text=transliterate(TS_TEXT, sanscript.BARAHA, sanscript.DEVANAGARI)+"\n"
                    updateMarkupFile(text,metaInformation,outputdir)
                    TS_TEXT="" 
            
            if pageSeparatorResult:
                continue
                
            elif titleResult:
                continue
            elif boldResult1 or boldResult2:
                continue
            elif tsseparatorresult1:
                #print("matched tsseparator1",data)
                metaInformation=tsseparatorresult1.group(1)
                TS_STATE=True
            elif metaPatternResult:
                #print("matched metapattern",data)
                TS_STATE=True
                metaInformation=metaPatternResult.group(1)

            elif tsseparatorresult:
                continue
            
            else:
                
                if  TS_STATE:
                    TS_TEXT+=data
                else:
                    continue
        else:
            if TS_STATE:
                TS_STATE=False
                TS_TEXT=cleanupText(TS_TEXT)
                #print("TS_TEXT_START",TS_TEXT,"TS_TEXT_END")
                text=transliterate(TS_TEXT, sanscript.BARAHA, sanscript.DEVANAGARI)+"\n"
                updateMarkupFile(text,metaInformation,outputdir)
                TS_TEXT=""
            #print("paragraph has zero words ")            

## Main Program starts here     


# CORE LOGIC 
# If the line is a ========  this is a page separator
# If the line begins with a [0-9]^.[0-9]^ 1.0 , 10.0  etc. this line is a title
# If the line beings with a [0-9]^ this line is in bold 

pageSeparatorPattern = r"======="
titlePattern = r"([\d]+[.][\d]+)"
boldPattern1 = r"[\d]+[.]"
boldPattern2 = r"[\d]+"
tspattern=r"^TS [\d]+[.][\s](.*)"
tspattern1=r"^TS ([\d]+[.][\d]+[.][\d]+[.][\d]+)(.*)"
metaPattern = r"^([\d]+[.][\d]+[.][\d]+[.][\d]+)(.*)"

if (args_count := len(sys.argv)<2 ):
    print ("Provide a file name and type of document (e.g.) Pada / Samhita / Krama ")
    raise SystemExit(2)
file_name=sys.argv[1]
if "Pada" in file_name:
    documentType="Pada"
elif "Krama" in file_name:
    documentType="Krama"
else:
    documentType="Samhita"
if len(sys.argv) >2 :
    documentType = sys.argv[2]      
document = Document (file_name)
# Define the sets of files being operated and the directories
baseName = os.path.basename(file_name)
# Replace space and strip and take the first part before dot
DocfamilyName=baseName.strip().replace(" ","_").split(".")[0]
print(DocfamilyName,documentType)
generatePdf(document,DocfamilyName)
generateMarkup(document,DocfamilyName,documentType)

