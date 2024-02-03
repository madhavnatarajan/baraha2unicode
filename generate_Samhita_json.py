import pyparsing as pp
import sys
from pathlib import Path
import re
from indic_transliteration import sanscript
from pathlib import Path
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
import json
from docx import Document
'''
Bug 1: The last line of the prasna is not getting parsed properly. The last number in 2 digits seems to be missing the last digit
-- Fixed had to add a space to understand the Panchasat number. Else it was getting processed as part of the previous group
Bug 2: The last Prasna is not getting processed . 
Fixed was a bug in the input file
Bug 3: Additional korvai information needs to get into the Tree
Fixed 
Bug 4 : Kanda 4 has additional Korvai's in middle of the prasnaLines section. this needs to be added as an additional node in the tree
Fixed 
'''

#kandaInfo = prasnaInfo = anuvakkamInfo = panchasatInfo =""
ts_string = '''\
{
    "TS": {
        "Kanda": [{"id": "1","Prasna": [{"Id": "1","Anuvakkam": [{"Id": "1","Panchasat": [{"Id": "1","SamhitaPaata": "x"}]}]}]}]
    }
}
'''

kandaNode={"id":"x","Prasna":[]}
prasnaNode={"id":"x","Anuvakkam":[]}
AnuvakkamNode={"id":"x","Panchasat":[]}
PanchasatNode={"id":"x","SamhitaPaata":"x"}

#parseTree = json.loads(ts_string)
parseTree =  {"TS": {"Kanda":[]}}
#print(parseTree["TS"]["Kanda"][0]["Prasna"][0]["Anuvakkam"][0]["Panchasat"][0]['SamhitaPaata'])
sectionTitle_temp = ""
invocation_temp = ""
global_identifier = {}
global_identifier["Kanda"] = global_identifier["Prasna"] = global_identifier["Anuvakkam"] = global_identifier["Panchasat"] =0
MYGLOBAL = ["test 1"]



def prasnaSection_Action(tokens):
    #print("prasnaSection_Action ",tokens,file=sys.stderr)
    kandaInfo=global_identifier.get("Kanda")
    prasnaInfo=global_identifier.get("Prasna")
    anuvakkamInfo=global_identifier.get("Anuvakkam")
    panchasatInfo=global_identifier.get("Panchasat")
    sectionTitle_temp = global_identifier.get("sectionTitle_temp")
    title_temp=global_identifier.get("title_temp")
    invocation_temp = global_identifier.get("invocation_temp")
    #parseTree["section"]=sectionTitle_temp
    parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["section"] = sectionTitle_temp
    parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["invocation"] = invocation_temp
    parseTree["TS"]["Kanda"][kandaInfo-1]["title"] = title_temp
    #x="title"
    #print(parseTree)

def titleLine_Action(tokens):
    print("titleLine_Action ",tokens,file=sys.stderr)
    lines=""
    outputString=""
    for t in tokens:
        lines +=(str)(t)
    outputString=transliterate(lines,sanscript.BARAHA, sanscript.DEVANAGARI)
    global_identifier["title_temp"]=outputString
    #print("title Section")
    #MYGLOBAL.append("Title")
    return outputString

def sectiontitleLine_Action(tokens):
    print("sectiontitleLine_Action ",tokens,file=sys.stderr)
    lines=""
    outputString=""
    for t in tokens:
        lines +=(str)(t)
    outputString=transliterate(lines,sanscript.BARAHA, sanscript.DEVANAGARI)
    #print("##",outputString,"##")
    global_identifier["sectionTitle_temp"]=outputString
    return outputString

def invocationLine_Action(tokens):
    print("invocationLine_Action ",tokens,file=sys.stderr)
    lines=""
    outputString=""
    for t in tokens:
        lines +=(str)(t)
    outputString=transliterate(lines,sanscript.BARAHA, sanscript.DEVANAGARI)
    global_identifier["invocation_temp"] = outputString
    return outputString


def remainingLines_Action(tokens):
    print("remainingLines_Action ",tokens,file=sys.stderr)
    # With this implementation it is not possible to mark the Appendix section in the tree . Need to fix
    outputString=""
    lines=""
    lines1=""
    EnglishPattern1 = r"Annexure for "
    EnglishPattern2 = r"(.*)(Appearing in TS)(.*)$"
    EnglishPattern3=  r"Appendix"
    kandaInfo=global_identifier.get("Kanda")
    prasnaInfo=global_identifier.get("Prasna")
    anuvakkamInfo=global_identifier.get("Anuvakkam")
    panchasatInfo=global_identifier.get("Panchasat")
    tokenLength = len(tokens)
    foundAnnexure=False
    parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Appendix"]=""
    if (len(tokens) >=3):
        lines += transliterate((str)(tokens[0]),sanscript.BARAHA, sanscript.DEVANAGARI)
        #lines += transliterate((str)(tokens[1]),sanscript.BARAHA, sanscript.DEVANAGARI)
        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["ending"] = lines
        for t in tokens[2]:
            mystr = (str)(t)
            EnglishPattern1Result = re.search(EnglishPattern1,mystr,re.IGNORECASE)
            EnglishPattern2Result = re.search(EnglishPattern2,mystr,re.IGNORECASE)
            EnglishPattern3Result = re.search(EnglishPattern3,mystr,re.IGNORECASE)
            if   EnglishPattern1Result or  EnglishPattern2Result or EnglishPattern3Result:
                #print(AnnexurePatternResult)
                #print("Found Annexure")
                foundAnnexure=True
                if EnglishPattern2Result:
                    mystr1 = transliterate(EnglishPattern2Result.group(1),sanscript.BARAHA, sanscript.DEVANAGARI)
                    #print(mystr1,file=sys.stderr)
                    mystr2=EnglishPattern2Result.group(2)
                    mystr3 = transliterate(EnglishPattern2Result.group(3),sanscript.BARAHA, sanscript.DEVANAGARI)
                    mystr = mystr1 + mystr2 + mystr3
                    #print ("###",mystr,"###",file=sys.stderr)
                parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Appendix"]+=mystr
                lines1 +=mystr
            else:
                
                x =transliterate(mystr, sanscript.BARAHA, sanscript.DEVANAGARI)
                lines1+=x
                if foundAnnexure:
                    parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Appendix"] += x
                else:
                    parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["ending"] += x
    #x = transliterate(lines, sanscript.BARAHA, sanscript.DEVANAGARI)
    #parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Appendix"] = lines1
    outputString=lines +lines1
    return outputString
def kandaKorvaiLines_Action(tokens):
    print("kandaKorvaiLines_Action ",tokens,file=sys.stderr)
    kandaInfo=global_identifier.get("Kanda")
    prasnaInfo=global_identifier.get("Prasna")
    anuvakkamInfo=global_identifier.get("Anuvakkam")
    panchasatInfo=global_identifier.get("Panchasat")
    outputString=""
    tokenLength = len(tokens)
    if tokenLength >= 2 :
        header = tokens[0] + " " + tokens[1][0]
        lines=""
        for s in tokens[1][1:]:
            lines+=s+"\n"
        x = transliterate(lines, sanscript.BARAHA, sanscript.DEVANAGARI)
        outputString=header + "\n" + x
        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["kandaKorvai_Sloka"] = x
        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["kandaKorvai_header"] = header
    elif tokenLength <2 :
        print(" kandaKorvaiLines : Check the token returned. Seems to be a problem")
        SystemExit(-1)
    if (tokenLength >2 ):
        print(" kandaKorvaiLines : Check the parser. This is just a warning  ");
    return outputString

def samhitaKorvaiLines_Action(tokens):
    print("samhitaKorvaiLines_Action ",tokens,file=sys.stderr)
    kandaInfo=global_identifier.get("Kanda")
    prasnaInfo=global_identifier.get("Prasna")
    anuvakkamInfo=global_identifier.get("Anuvakkam")
    panchasatInfo=global_identifier.get("Panchasat")
    outputString=""
    tokenLength = len(tokens)
    if tokenLength >= 2 :
        header = tokens[0] + " " + tokens[1][0]
        lines=""
        for s in tokens[1][1:]:
            lines+=s+"\n"
        x = transliterate(lines, sanscript.BARAHA, sanscript.DEVANAGARI)
        outputString=header + "\n" + x
        parseTree["TS"]["Kanda"][kandaInfo-1]["samhitaKorvai_Sloka"] = x
        parseTree["TS"]["Kanda"][kandaInfo-1]["samhitaKorvai_header"] = header
    elif tokenLength <2 :
        print(" samhitaKorvaiLines : Check the token returned. Seems to be a problem")
        SystemExit(-1)
    if (tokenLength >2 ):
        print(" samhitaKorvaiLines : Check the parser. This is just a warning  ");
    return outputString

def specialKorvaiLines_Action(tokens):
    print("specialKorvaiLines_Action ",tokens,file=sys.stderr)
    kandaInfo=global_identifier.get("Kanda")
    prasnaInfo=global_identifier.get("Prasna")
    anuvakkamInfo=global_identifier.get("Anuvakkam")
    panchasatInfo=global_identifier.get("Panchasat")
    outputString=""
    tokenLength = len(tokens)
    if tokenLength >= 2 :
        header = tokens[0] + " " + tokens[1][0]
        lines=""
        for s in tokens[1][1:]:
            lines+=s+"\n"
        x = transliterate(lines, sanscript.BARAHA, sanscript.DEVANAGARI)
        outputString=header + "\n" + x
        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["specialKorvai_Sloka"] = x
        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["specialKorvai_header"] = header
    elif tokenLength <2 :
        print(" specialKorvaiLines : Check the token returned. Seems to be a problem")
        SystemExit(-1)
    if (tokenLength >2 ):
        print(" specialKorvaiLines : Check the parser. This is just a warning  ");
    return outputString


def firstLastPadamsLines_Action(tokens):
    print("firstLastPadamsLines_Action ",tokens,file=sys.stderr)
    kandaInfo=global_identifier.get("Kanda")
    prasnaInfo=global_identifier.get("Prasna")
    anuvakkamInfo=global_identifier.get("Anuvakkam")
    panchasatInfo=global_identifier.get("Panchasat")
    outputString=""
    tokenLength = len(tokens)
    if tokenLength >= 2 :
        header = tokens[0] + " " + tokens[1][0]
        lines=""
        for s in tokens[1][1:]:
            lines+=s
            
        x = transliterate(lines, sanscript.BARAHA, sanscript.DEVANAGARI)
        outputString=header + "\n" + x
        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["firstLastPadams_Sloka"] = x
        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["firstLastPadams_header"] = header
    elif tokenLength <2 :
        print(" firstandLastPadams : Check the token returned. Seems to be a problem")
        SystemExit(-1)
    if (tokenLength >2 ):
        print(" firstandLastPadams : Check the parser. This is just a warning  ");
    return outputString

def korvaiLines_Action(tokens):
    # The first token and the first line of the second token is the heading 
    print("korvaiLines_Action ",tokens,file=sys.stderr)
    kandaInfo=global_identifier.get("Kanda")
    prasnaInfo=global_identifier.get("Prasna")
    anuvakkamInfo=global_identifier.get("Anuvakkam")
    panchasatInfo=global_identifier.get("Panchasat")
    outputString=""
    tokenLength = len(tokens)
    if tokenLength >= 2 :
        header = tokens[0] + tokens[1][0]
        lines=""
        for s in tokens[1][1:]:
            lines+=s+"\n"
        x = transliterate(lines, sanscript.BARAHA, sanscript.DEVANAGARI)
        outputString=header + "\n" + x
        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Korvai_Sloka"] = x
        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Korvai_header"] = header
    elif tokenLength <2 :
        print(" korvaiLines : Check the token returned. Seems to be a problem")
        SystemExit(-1)
    if (tokenLength >2 ):
        print(" korvaiLines : Check the parser. This is just a warning  ");
    return outputString

def prasnaKorvaiLines_Action(tokens):
    # The first token and the first line of the second token is the heading 
    print("prasnaKorvaiLines_Action ",tokens,file=sys.stderr)
    kandaInfo=global_identifier.get("Kanda")
    prasnaInfo=global_identifier.get("Prasna")
    anuvakkamInfo=global_identifier.get("Anuvakkam")
    panchasatInfo=global_identifier.get("Panchasat")
    outputString=""
    tokenLength = len(tokens)
    if tokenLength >= 2 :
        header = tokens[0] + " " + tokens[1][0]
        lines=""
        for s in tokens[1][1:]:
            lines+=s+"\n"
        x = transliterate(lines, sanscript.BARAHA, sanscript.DEVANAGARI)
        outputString=header + "\n" + x
        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["PrasnaKorvai_Sloka"] = x
        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["PrasnaKorvai_header"] = header
    elif tokenLength <2 :
        print(" prasnaKorvaiLines : Check the token returned. Seems to be a problem")
        SystemExit(-1)
    if (tokenLength >2 ):
        print(" prasnaKorvaiLines : Check the parser. This is just a warning  ");
    return outputString

def prasnaLines_Action(tokens):
    print("prasnaLines_Action ",tokens,file=sys.stderr)
    panchasatPattern = r"(.*)(\s\d+)(\s|$)"
    anuvakkamPattern = r"(.*)(\(A(\d+)\))(\s|$)"
    metaInformationPattern = r"^TS ([\d]+[.][\d]+[.][\d]+[.][\d]+)(.*)"
    specialPattern = r"special "

    #print("Tokens :", len(tokens[0]))
    
    outputString=""
    inSpecialKorvai=False
    specialKorvai_header=""
    specialKorvai_Sloka=""
    kandaInfo = prasnaInfo = anuvakkamInfo = panchasatInfo =0
    for t in tokens:
        mystr=(str)(t)
        lines=mystr.split("\n")
        
        for line in lines:
            
            panchasatResult = re.search(panchasatPattern, line)
            anuvakkamResult = re.search(anuvakkamPattern, line)
            metaInformationResult = re.search(metaInformationPattern, line)
            specialResult = re.search(specialPattern, line,re.IGNORECASE)
            #print("Processing ",line,specialResult,panchasatResult,anuvakkamResult,metaInformationResult,file=sys.stderr)
            if metaInformationResult:
                if inSpecialKorvai:
                        #print("Adding-3",specialKorvai_header,specialKorvai_Sloka,file=sys.stderr)
                        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][panchasatInfo-1]["specialKorvai_Sloka"]=specialKorvai_Sloka
                        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][panchasatInfo-1]["specialKorvai_header"]=specialKorvai_header
                        inSpecialKorvai=False
                        specialKorvai_header=""
                        specialKorvai_Sloka=""
                metaInformation=metaInformationResult.group(1)
                metaInfoSplit=metaInformation.split(".")                
                if len(metaInfoSplit) >=4:
                    kandaInfo=int(metaInfoSplit[0])
                    prasnaInfo=int(metaInfoSplit[1])
                    anuvakkamInfo=int(metaInfoSplit[2])
                    panchasatInfo=int(metaInfoSplit[3])
                    
                    #print("Splitting metaInfo ",global_identifier,metaInformation)
                    #print("Debug_1",global_identifier.get("Anuvakkam"),anuvakkamInfo)
                    if global_identifier.get("Kanda") is None or global_identifier.get("Kanda") != kandaInfo:
                        
                        #print("In condition 1")
                        PanchasatNode={"id":panchasatInfo,"SamhitaPaata":"","header":line}
                        AnuvakkamNode={"id":anuvakkamInfo,"Panchasat":[]}
                        AnuvakkamNode["Panchasat"].append(PanchasatNode)
                        PrasnaNode={"id":prasnaInfo,"Anuvakkam":[]}
                        PrasnaNode["Anuvakkam"].append(AnuvakkamNode)
                        KandaNode={"id":kandaInfo,"Prasna":[]}
                        KandaNode["Prasna"].append(PrasnaNode)
                        parseTree["TS"]["Kanda"].append(KandaNode)
                        global_identifier["Kanda"]=kandaInfo
                        global_identifier["Prasna"]=prasnaInfo
                        global_identifier["Anuvakkam"]=anuvakkamInfo
                        global_identifier["Panchasat"]=panchasatInfo


                    elif global_identifier.get("Prasna") !=prasnaInfo:
                        #print("In condition 2")

                        PanchasatNode={"id":panchasatInfo,"SamhitaPaata":"","header":line}
                        AnuvakkamNode={"id":anuvakkamInfo,"Panchasat":[]}
                        AnuvakkamNode["Panchasat"].append(PanchasatNode)
                        PrasnaNode={"id":prasnaInfo,"Anuvakkam":[]}
                        PrasnaNode["Anuvakkam"].append(AnuvakkamNode)
                        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"].append(PrasnaNode)
                        global_identifier["Kanda"]=kandaInfo
                        global_identifier["Prasna"]=prasnaInfo
                        global_identifier["Anuvakkam"]=anuvakkamInfo
                        global_identifier["Panchasat"]=panchasatInfo

                    elif global_identifier.get("Anuvakkam") != anuvakkamInfo:
                        #print("Adding a new Anuvakkam node")
                        PanchasatNode={"id":panchasatInfo,"SamhitaPaata":"","header":line}
                        AnuvakkamNode={"id":anuvakkamInfo,"Panchasat":[]}
                        AnuvakkamNode["Panchasat"].append(PanchasatNode)
                        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Anuvakkam"].append(AnuvakkamNode)
                        global_identifier["Kanda"]=kandaInfo
                        global_identifier["Prasna"]=prasnaInfo
                        global_identifier["Anuvakkam"]=anuvakkamInfo
                        global_identifier["Panchasat"]=panchasatInfo
                    
                    elif global_identifier.get("Panchasat") != panchasatInfo :
                        #print("Processing different Panchasat ",panchasatInfo)
                        PanchasatNode={"id":panchasatInfo,"SamhitaPaata":"","header":line}
                        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"].append(PanchasatNode)
                        global_identifier["Kanda"]=kandaInfo
                        global_identifier["Prasna"]=prasnaInfo
                        global_identifier["Anuvakkam"]=anuvakkamInfo
                        global_identifier["Panchasat"]=panchasatInfo
                    
                    

                        

                
                outputString+=line+"\n"
                
                
            elif anuvakkamResult:
                #print("new Anuvaka",anuvakkamResult.group(1))
                x = transliterate(anuvakkamResult.group(1), sanscript.BARAHA, sanscript.DEVANAGARI)
                parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["KorvaiInfo"]=x
                
                outputString+=x 
                outputString+="  " + anuvakkamResult.group(2)+"\n"
                parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Anuvakkam"][anuvakkamInfo-1]['anuvakkamInfo']=anuvakkamResult.group(2)
                
            elif panchasatResult:
                #print("Panchasat-1","2- ",panchasatResult.group(2), " 3- ",panchasatResult.group(3),file=sys.stderr)
                x = transliterate(panchasatResult.group(1), sanscript.BARAHA, sanscript.DEVANAGARI)
                #print(x)
                #print("kandaInfo: ",kandaInfo, " prasnaInfo: ",prasnaInfo," anuvakkamInfo: ",anuvakkamInfo," panchasatInfo: ",panchasatInfo) 
                      
                #print(" X ",parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][panchasatInfo-1]["SamhitaPaata"])

                parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][panchasatInfo-1]["SamhitaPaata"]+=x

                outputString+=x 
                outputString+="  " + panchasatResult.group(2)+"\n"
                parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][panchasatInfo-1]["panchasatInfo"]=panchasatResult.group(2)+panchasatResult.group(3)

            elif specialResult:
                inSpecialKorvai=True
                #print("Special Korvai-1",line,global_identifier,file=sys.stderr)
                specialKorvai_header=line
            else:
                #words=line.split(" ")
                #maxlen=len(words)-1
                #print("###",line,len(line),"###")
                #print("Panchasat-2",panchasatResult, line,file=sys.stderr)
                if (len(line) >0):
                    x = transliterate(line, sanscript.BARAHA, sanscript.DEVANAGARI)
                    if (inSpecialKorvai):
                        #print("Special Korvai-2",line,global_identifier,file=sys.stderr)
                        specialKorvai_Sloka+=x
                    else:
                        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][panchasatInfo-1]["SamhitaPaata"]+=x

                    outputString+=x 
                #outputString+=line
                outputString+="\n"
            
    
    #print(outputString)
    #MYGLOBAL ="In parseLineActions"
    if inSpecialKorvai:
        #print("Special Korvai at end ",line,global_identifier,file=sys.stderr)
        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][panchasatInfo-1]["specialKorvai_Sloka"]=specialKorvai_Sloka
        parseTree["TS"]["Kanda"][kandaInfo-1]["Prasna"][prasnaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][panchasatInfo-1]["specialKorvai_header"]=specialKorvai_header
        inSpecialKorvai=False
        specialKorvai_header=""
        specialKorvai_Sloka=""
    return outputString
    
# Largely built following the example and comments in
# https://stackoverflow.com/questions/55909620/capturing-block-over-multiple-lines-using-pyparsing
# and
# https://stackoverflow.com/questions/15938540/how-can-i-do-a-non-greedy-backtracking-match-with-oneormore-etc-in-pyparsing
pp.enable_diag(pp.Diagnostics.enable_debug_on_named_expressions)

EOL = pp.LineEnd()
EmptyLine = pp.Suppress(pp.LineStart() + EOL)

englishLine_StopSeparator = pp.LineStart() + "OM"

englishLines = pp.Optional(EOL) + pp.Group(
    pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=englishLine_StopSeparator)
)
englishPreface = pp.Combine(pp.CaselessKeyword("Notes") + englishLines).setResultsName(
    "englishPreface_Section"
)
sectiontitleLine = pp.Combine(
    pp.Word(pp.nums) + pp.Literal(".") + pp.Word(pp.nums) + (pp.SkipTo(EOL)) + EOL
).setResultsName("sectiontitleLine_Section*")
sectiontitleLine.setParseAction(sectiontitleLine_Action)


titleLine = pp.Combine(
    ~sectiontitleLine + pp.Word(pp.nums) + (pp.SkipTo(EOL)) + pp.Suppress(EOL)
).setResultsName("titleLine_Section")
titleLine.setParseAction(titleLine_Action)


invocationLine_StopSeparator = pp.LineStart() + ( titleLine | sectiontitleLine )

invocationLines = pp.Optional(EOL) + pp.Group(
    pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=invocationLine_StopSeparator)
)
invocation = pp.Combine(pp.Keyword("OM") + invocationLines).setResultsName(
    "invocation_Section*"
)
invocation.setParseAction(invocationLine_Action)

prasnaKorvai_Starting = pp.CaselessKeyword("praSna korvai with starting padams")
korvai_Starting = pp.CaselessKeyword("korvai with starting padams of")
firstLastPadam_Starting = pp.CaselessKeyword("first and last padam of")
kandaKorvai_Starting = pp.CaselessKeyword("kAnda korvai with starting padams of")
samhitaKorvai_Starting = pp.CaselessKeyword("samhita korvai with starting padams of")
specialKorvai_Starting = pp.CaselessKeyword("special korvai")

prasnaEnding_Starting_1 = pp.CaselessKeyword("|| hari#H OM ||")
prasnaEnding_Starting_2 = pp.CaselessKeyword("|| hariH# OM ||")
prasnaEnding_Starting_3 = pp.CaselessKeyword("|| hari# OM ||")

prasnaEnding_Starting = prasnaEnding_Starting_1 | prasnaEnding_Starting_2 | prasnaEnding_Starting_3

prasnaLines = pp.Optional(EOL) + pp.Combine(
    pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=prasnaKorvai_Starting)
).setResultsName("prasna_Lines*")
prasnaLines.setParseAction(prasnaLines_Action)

prasnaKorvaiLines = (
    prasnaKorvai_Starting
    + pp.Optional(EOL)
    + pp.Group(pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=korvai_Starting | specialKorvai_Starting))
)
prasnaKorvaiLines.setParseAction(prasnaKorvaiLines_Action)

korvaiLines = (
    korvai_Starting
    + pp.Optional(EOL)
    + pp.Group(
        pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=firstLastPadam_Starting)
    )
)
korvaiLines.setParseAction(korvaiLines_Action)
kandaKorvaiLines = (
    kandaKorvai_Starting
    + pp.Optional(EOL)
    + pp.Group(pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=EmptyLine))
)
kandaKorvaiLines.setParseAction(kandaKorvaiLines_Action)
specialKorvaiLines = (
    specialKorvai_Starting
    + pp.Optional(EOL)
    + pp.Group(pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=EmptyLine))
)
specialKorvaiLines.setParseAction(specialKorvaiLines_Action)

samhitaKorvaiLines = (
    samhitaKorvai_Starting
    + pp.Optional(EOL)
    + pp.Group(pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=EmptyLine))
)
samhitaKorvaiLines.setParseAction(samhitaKorvaiLines_Action)
firstLastPadamLines = (
    firstLastPadam_Starting
    + pp.Optional(EOL)
    + pp.Group(pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=EmptyLine))
)
firstLastPadamLines.setParseAction(firstLastPadamsLines_Action)

Separator1 = pp.Keyword("*************")
prasna_Separator_1 = pp.Keyword("==========================================").suppress()
prasna_Separator_2 = pp.Keyword("------------------------------------------").suppress()

prasna_Separator = prasna_Separator_1 | prasna_Separator_2
annexureStartingLine_1 = pp.LineStart() + pp.CaselessLiteral("Annexure")
annexureStartingLine_2 = (
    pp.LineStart() + pp.Word(pp.printables) + pp.CaselessLiteral("Appendix")
)
annexureStartingLine = annexureStartingLine_1 | annexureStartingLine_2

annexureLines = (
    annexureStartingLine
    + pp.Optional(EOL)
    + pp.Combine(pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=prasna_Separator))
)


remainingLines_WithAppendix = pp.Group(
    prasnaEnding_Starting
    + pp.Optional(EOL)
    + pp.Combine(
        pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=annexureStartingLine)
    )
    + annexureLines
).setResultsName("WithAppendix")

remainingLines = (
    prasnaEnding_Starting
    + pp.Optional(EOL)
    + pp.Group(
        pp.OneOrMore(
            ~invocation + pp.SkipTo(pp.LineEnd()) + EOL, stopOn=prasna_Separator
        )
    ).setResultsName("RemainingLines")
)
remainingLines.setParseAction(remainingLines_Action)

#remainingLines = remainingLines_WithoutAppendix  # This seems like a hack but this is the best I can do now
# Otherwise a greedy match happens
corePrasna = (
    sectiontitleLine
    + prasnaLines
    + prasnaKorvaiLines
    + pp.ZeroOrMore(specialKorvaiLines)
    + korvaiLines
    + firstLastPadamLines
    + pp.ZeroOrMore(kandaKorvaiLines)
    + pp.ZeroOrMore(samhitaKorvaiLines)
    + remainingLines
)


#firstLastPadamLines.setName("firstLast")
#remainingLines_WithoutAppendix.setName("remainingLinesWithoutAppendix")
#remainingLines_WithAppendix.setName("remainingLines_WithAppendix")
'''prasna_Section_1 = (
    pp.Optional(prasna_Separator + pp.SkipTo(EOL)).suppress()  + corePrasna
)
prasna_Section_2 = (
    pp.Optional(prasna_Separator + pp.SkipTo(EOL)).suppress() + invocation + corePrasna
)'''
prasna_Section_1 = (
    pp.Optional((prasna_Separator + pp.SkipTo(EOL))).suppress()  + corePrasna
)
prasna_Section_2 = (
     pp.Optional((prasna_Separator + pp.SkipTo(EOL))).suppress() + invocation + corePrasna
)
prasna_Section = (prasna_Section_2 | prasna_Section_1).setResultsName("prasna_Section*")
prasna_Section.setParseAction(prasnaSection_Action)

'''
prasnaLines.setName("prasnaLine")
corePrasna.setName("core")
prasna_Section_1.setName("P1")
prasna_Section_2.setName("P2")
prasna_Section.setName("PS")
specialKorvaiLines.setName("SK")
korvaiLines.setName("Korvai")
sectiontitleLine.setName("sectiontitleLine")
titleLine.setName("titleLine")
invocation.setName("invocation")
prasnaKorvaiLines.setName("PSK")
firstLastPadamLines.setName("firstLast")
kandaKorvaiLines.setName("KKorvai")
remainingLines.setName("rem")
'''
parser = englishPreface + invocation + titleLine + pp.OneOrMore(prasna_Section)
#parser = englishPreface + invocation + titleLine + sectiontitleLine + prasnaLines + prasnaKorvaiLines + pp.ZeroOrMore(specialKorvaiLines)+ korvaiLines+ firstLastPadamLines+ pp.ZeroOrMore(kandaKorvaiLines)+ pp.ZeroOrMore(samhitaKorvaiLines)+ remainingLines
# parser = prasnaLines
if args_count := len(sys.argv) < 2:
    print("Provide a file name ")
    raise SystemExit(2)
for file_name in sys.argv[1:]:
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
json_file_name = "TS.json"

my_json = json.dumps(parseTree,indent=3,ensure_ascii=False, sort_keys=True)
my_json = my_json.replace("\uA8E3","\u1CDA")
with open(json_file_name, "w") as f:
    f.write(my_json)

