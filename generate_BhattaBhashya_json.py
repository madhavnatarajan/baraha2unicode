import pyparsing as pp
import sys
from pathlib import Path
import re
from indic_transliteration import sanscript
from pathlib import Path
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
import json
from docx import Document

def bhashyaLinesAction(tokens):
    print ("header:", tokens[0:1])
    if len(tokens) <=2:
        print("No Bhashya")
    else:
        ids = tokens[0].split(" ")
        kandaInfo,prasnaInfo,anuvakaInfo = ids[0].split(".")
        kandaInfo = int(kandaInfo)
        prasnaInfo = int(prasnaInfo)
        anuvakaInfo = int(anuvakaInfo)
        print("Kanda:",kandaInfo,"Prasna:",prasnaInfo,"Anuvaka:",anuvakaInfo)  
        if (int(anuvakaInfo) == 0):
            parseTree['TS']['BhattaBhashya']={}
            parseTree['TS']['BhattaBhashya']['Sloka']=tokens[2:]
            parseTree['TS']['BhattaBhashya']['header']=tokens[0:1]
        else:
            parseTree['TS']["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Anuvakkam"][anuvakaInfo-1]['BhattaBhashya']={}

            parseTree['TS']["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Anuvakkam"][anuvakaInfo-1]['BhattaBhashya']["Sloka"]=tokens[2:]
            parseTree['TS']["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Anuvakkam"][anuvakaInfo-1]['BhattaBhashya']["header"]=tokens[0:1]
        
    
    
EOL = pp.LineEnd()
EmptyLine = pp.Suppress(pp.LineStart() + EOL)
bhashyaTitleLine = (
        pp.Combine(
            pp.Word(pp.nums)
            + pp.Literal(".")
            + pp.Word(pp.nums)
            + pp.Literal(".")
            + pp.Word(pp.nums)
            
            + pp.Group(pp.SkipTo(EOL))
        )
        
        + pp.Suppress(EOL)
)
bhashyaLines = bhashyaTitleLine + pp.Optional (pp.SkipTo(pp.LineEnd())) + EOL + pp.Optional(pp.Combine(
    pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=bhashyaTitleLine))
)
bhashyaLines.setParseAction(bhashyaLinesAction)
parser = pp.OneOrMore(bhashyaLines)

ts_string = Path("TS_withSayanaBhashya.json").read_text(encoding="utf-8")
parseTree = json.loads(ts_string)
if args_count := len(sys.argv) < 2:
    print("Provide a file name ")
    raise SystemExit(2)
for file_name in sys.argv[1:]:
    print(file_name)
    #file_name = sys.argv[1]
    text=""
    document = Document(file_name)

    all_paras = document.paragraphs
    for para in all_paras:
        text += para.text + "\n"
    #text = Path(file_name).read_text(encoding="utf-8")
    text_file_name = file_name.replace(".docx", ".txt")
    with open(text_file_name, "w") as f:
        f.write(text)

    results = parser.parseString(text)
    #print(results)
json_file_name = "TS_withBhattaBhashya.json"
my_json = json.dumps(parseTree,indent=3,ensure_ascii=False, sort_keys=True)
my_json = my_json.replace("\uA8E3","\u1CDA")
with open(json_file_name, "w") as f:
    f.write(my_json)
#print(my_json)
