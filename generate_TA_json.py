import pyparsing as pp
import sys
from pathlib import Path
import re
from indic_transliteration import sanscript
from pathlib import Path
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
import json
from docx import Document
parseTree =  {"TA": {"Prapaataka":[]}}
sectionTitle_temp = ""
invocation_temp = ""
global_identifier = {}
global_identifier["Prapaataka"]  = global_identifier["Anuvakkam"] = global_identifier["Panchasat"] =0

def updateTree(panchasatCollection,anuvakkamCollection,specialKorvaiCollection):
    global parseTree
    for (prapaataka_id,anuvakkam_id,panchasat,panchasat_id,panchasat_sloka) in panchasatCollection:
        #print("Panchasat ",prapaataka_id,anuvakkam_id,panchasat,panchasat_id,panchasat_sloka)
        id=prapaataka_id.strip()+"."+anuvakkam_id.strip()+"."+panchasat.strip()
        header="T.A."+prapaataka_id.strip()+"."+anuvakkam_id.strip()+"."+panchasat.strip()
        outputString=transliterate(panchasat_sloka,sanscript.BARAHA, sanscript.DEVANAGARI)

        #print(id)
        prapaatakaInfo = int(prapaataka_id)
        anuvakkamInfo = int(anuvakkam_id)
        if ("-") in panchasat:
            mainPanchasatInfo,upaPanchasatInfo = panchasat_id.split("-")
            mainPanchasatInfo = int(mainPanchasatInfo)
            upaPanchasatInfo = int(upaPanchasatInfo)
            parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][mainPanchasatInfo-1]["UpaPanchasat"][upaPanchasatInfo-1]["header"]=header
            parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][mainPanchasatInfo-1]["id"]=panchasat
            parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][mainPanchasatInfo-1]["UpaPanchasat"][upaPanchasatInfo-1]["SamhitaPaata"]=outputString


        else:
            mainPanchasatInfo = int(panchasat)
            upaPanchasatInfo = 0
            parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][mainPanchasatInfo-1]["header"]=header
            parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][mainPanchasatInfo-1]["id"]=panchasat_id
            parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][mainPanchasatInfo-1]["SamhitaPaata"]=outputString
        prapaatakaTreeLength=len(parseTree["TA"]["Prapaataka"])
        anuvaakaTreeLength = len(parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"])
        panchasatTreeLength = len(parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"])
        if panchasatTreeLength < mainPanchasatInfo or anuvaakaTreeLength < anuvakkamInfo or prapaatakaTreeLength < prapaatakaInfo:
            print("ERROR ")
            print(prapaatakaTreeLength,anuvaakaTreeLength,panchasatTreeLength)
        
    for prapaataka_id,x_anuvakkam_id,panchasat_id,anuvakkam_id,anuvakkamKorvai in anuvakkamCollection:
        prapaatakaInfo = int(prapaataka_id)
        anuvakkamInfo = int(anuvakkam_id)
        if "no korvai" in anuvakkamKorvai:
            pass
        else:
            outputString=transliterate(anuvakkamKorvai,sanscript.BARAHA, sanscript.DEVANAGARI)
            parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Korvai"]=outputString
            parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["anuvakkam_id"]=anuvakkam_id

    
    for prapaataka_id,anuvakkam_id,panchasat_id,specialKorvai in specialKorvaiCollection:
        prapaatakaInfo = int(prapaataka_id)
        anuvakkamInfo = int(anuvakkam_id)
        panchasatInfo=int(panchasat_id)
        compiled = re.compile("special korvai", re.IGNORECASE)
        res = compiled.sub("", specialKorvai)
        outputString=transliterate(res,sanscript.BARAHA, sanscript.DEVANAGARI)
        try:
            parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][panchasatInfo-1]["specialKorvai"]=outputString
        except Exception as e:
            print("Info passed " , prapaatakaInfo,anuvakkamInfo,panchasatInfo,specialKorvai)
            print("Length of Prapaataka array ",len(parseTree["TA"]["Prapaataka"]))
            print("Length of anuvakka array ",len(parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"]))
            print("Length of Panchasat array ",len(parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"]))

            print("Exception ",e)





 
        
    
def createPrapaatakaNodes(prapaatakaInfo):
    global global_identifier
    prapaatakaInfo = int(prapaatakaInfo)
    currentPrapaatakaLength = 0
    if parseTree["TA"].get("Prapaataka") == None:
        currentPrapaatakaLength = 0
    else: 
        currentPrapaatakaLength = len(parseTree["TA"]["Prapaataka"])
    while (prapaatakaInfo - currentPrapaatakaLength) > 0:
        PanchasatNode={"id":0,"SamhitaPaata":"","header":""}
        AnuvakkamNode={"id":0,"Panchasat":[],"Korvai":""}
        AnuvakkamNode["Panchasat"].append(PanchasatNode)
        PrapaatakaNode={"id":0,"Anuvakkam":[]}
        PrapaatakaNode["Anuvakkam"].append(AnuvakkamNode)
        parseTree["TA"]["Prapaataka"].append(PrapaatakaNode)

        #parseTree["TA"]["Prapaataka"][currentPrapaatakaLength]["Anuvakkam"].append(AnuvakkamNode)
        #print("After appending Prapaataka",parseTree)
        currentPrapaatakaLength += 1

def createAnuvakkamNodes(prapaatakaInfo,anuvakkamInfo):
    global global_identifier
    prapaatakaInfo = int(prapaatakaInfo)
    anuvakkamInfo = int(anuvakkamInfo)
    currentAnuvakkamLength = 0
    if parseTree["TA"]["Prapaataka"][prapaatakaInfo-1].get("Anuvakkam") == None:
        currentAnuvakkamLength = 0
    else:
        currentAnuvakkamLength = len(parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"])
    while (anuvakkamInfo - currentAnuvakkamLength) > 0:
        PanchasatNode={"id":0,"SamhitaPaata":"","header":""}
        AnuvakkamNode={"id":0,"Panchasat":[],"Korvai":""}
        AnuvakkamNode["Panchasat"].append(PanchasatNode)
        
        parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"].append(AnuvakkamNode) 
        currentAnuvakkamLength += 1

def createPanchasatNodes(prapaatakaInfo,anuvakkamInfo,panchasatInfo):
    global global_identifier
    #print("createPanchasatNodes : Invoked with ",prapaatakaInfo,anuvakkamInfo,panchasatInfo)
    prapaatakaInfo = int(prapaatakaInfo)
    anuvakkamInfo = int(anuvakkamInfo)
    try:
        panchasatInfo = int(panchasatInfo)
    

        currentPanchasatLength = 0
        #print(prapaatakaInfo,anuvakkamInfo,panchasatInfo)
        #print(parseTree)
        if parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1].get("Panchasat") == None:
            currentPanchasatLength = 0
        else:
            currentPanchasatLength = len(parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"])
        while (panchasatInfo - currentPanchasatLength) > 0:
            PanchasatNode={"id":0,"SamhitaPaata":"","header":""}
            #parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"]=[]

            parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"].append(PanchasatNode)
            currentPanchasatLength += 1
    except:
        #print("In exception ",panchasatInfo)
        subpanchasat=panchasatInfo.split("-")
        
        
        mainPanchasatInfo=int(subpanchasat[0])
        upaPanchasatInfo = int(subpanchasat[1])
        
        if parseTree["TA"]["Prapaataka"][prapaatakaInfo-1].get("Anuvakkam"):
            #print("Anuvakkam exists",anuvakkamInfo) 
            if parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1].get("Panchasat") == None:
                #print(" The previous subtree does not exist ",prapaatakaInfo,anuvakkamInfo,panchasatInfo)
                pass
            else:
                #print("Panchasat exists ",panchasatInfo,mainPanchasatInfo)
                try:
                    x=len(parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][mainPanchasatInfo-1])
                except Exception as e:
                    print("Create PanchasatNodes Exception in getting length ",prapaatakaInfo,anuvakkamInfo,panchasatInfo)
                    print("Info passed " , prapaatakaInfo,anuvakkamInfo,panchasatInfo)
                    print("Length of Prapaataka array ",len(parseTree["TA"]["Prapaataka"]))
                    print("Length of anuvakka array ",len(parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"]))
                    print("Length of Panchasat array ",len(parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"]))
        if parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][mainPanchasatInfo-1].get("UpaPanchasat") == None:
            #print("No UpaPanchasat yet ",panchasatInfo)
            parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][mainPanchasatInfo-1]["UpaPanchasat"]=[]
            currentupaPanchasatLength = 0
        else:
            #print("not none")
            currentupaPanchasatLength = len(parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][mainPanchasatInfo-1]["UpaPanchasat"])
        #print(" upaPanchasatInfo : ",upaPanchasatInfo, " currentupaPanchasatLength ",currentupaPanchasatLength)
        while (upaPanchasatInfo - currentupaPanchasatLength) > 0:
            PanchasatNode={"id":0,"SamhitaPaata":"","header":""}
            #parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"]=[]

            parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][mainPanchasatInfo-1]["UpaPanchasat"].append(PanchasatNode)
            currentupaPanchasatLength += 1

def corePrasnaAction(tokens):
    #print("corePrasnaAction ",tokens)
    prapaatakaInfo=int(global_identifier.get("Prapaataka"))
    prapaatakaInfo=int(prapaatakaInfo)
    anuvakkamInfo=int(global_identifier.get("Anuvakkam"))
    panchasatInfo=int(global_identifier.get("Panchasat"))
    parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["title"]=global_identifier.get("title_temp")
    title_array=global_identifier.get("title_temp").split(" ")
    prapaatakaId=int(title_array[0])
    parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["title"]=' '.join(title_array[1:])
    parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["id"]=prapaatakaId
    parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["sectionTitle"]=global_identifier.get("sectionTitle_temp")
    parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["invocation"]=global_identifier.get("invocation_temp")

def sectiontitleLine_Action(tokens):
    #print("sectiontitleLine_Action ",tokens)
    lines=""
    outputString=""
    for t in tokens:
        lines +=(str)(t)
    outputString=transliterate(lines,sanscript.BARAHA, sanscript.DEVANAGARI)
    #outputString=transliterate(lines,sanscript.BARAHA, sanscript.TAMIL)
    #print("##",outputString,"##")
    global_identifier["sectionTitle_temp"]=outputString
    return outputString

def titleLine_Action(tokens):
    #print("titleLine_Action ",tokens)
    lines=""
    outputString=""
    for t in tokens:
        lines +=(str)(t)
    outputString=transliterate(lines,sanscript.BARAHA, sanscript.DEVANAGARI)
    #outputString=transliterate(lines,sanscript.BARAHA, sanscript.TAMIL)

    global_identifier["title_temp"]=outputString
    #print("title Section")
    #MYGLOBAL.append("Title")
    return outputString

def invocationLine_Action(tokens):
    #print("invocationLine_Action ",tokens)
    lines=""
    outputString=""
    for t in tokens:
        lines +=(str)(t)
    outputString=transliterate(lines,sanscript.BARAHA, sanscript.DEVANAGARI)
    #outputString=transliterate(lines,sanscript.BARAHA, sanscript.TAMIL)

    global_identifier["invocation_temp"] = outputString
    return outputString

def remainingLinesAction(tokens):
    print("In remainingLinesAction")
    x= len(tokens)-1
    outputString=""
    #print("0: ", tokens[0])
    #print("1: ",tokens[1])
    #print("2: ",tokens[2])
    #lines=str(tokens[x]).split("\n")
    #y = lines[0].split("\n")
    englishPattern1=r"appearing"
    englishPattern2=r"appendix"
    for line in tokens[x]:
        englishResult1 = re.search(englishPattern1,line,re.IGNORECASE)
        englishResult2 = re.search(englishPattern2,line,re.IGNORECASE)
        if englishResult1 or englishResult2:
            outputString+=line
            print("no transliteration",line)
        else:
            if len(line) >1:
                x = transliterate(line, sanscript.BARAHA, sanscript.DEVANAGARI)
                outputString+=x

                #print(x)
            else :
                outputString+=line
                #print(line)
    prapaatakaInfo=int(global_identifier.get("Prapaataka"))
    prapaatakaInfo=int(prapaatakaInfo)
    parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["ending"]=outputString
    return outputString
    #print("End of remainingLinesAction")

def firstLastPadamLinesAction(tokens):
    prapaatakaInfo=int(global_identifier.get("Prapaataka"))
    prapaatakaInfo=int(prapaatakaInfo)
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
        #x = transliterate(lines, sanscript.BARAHA, sanscript.TAMIL)

        outputString=header + "\n" + x
        parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["firstLastPadams_Sloka"] = x
        parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["firstLastPadams_header"] = header
    elif tokenLength <2 :
        print(" firstandLastPadams : Check the token returned. Seems to be a problem")
        SystemExit(-1)
    if (tokenLength >2 ):
        print(" firstandLastPadams : Check the parser. This is just a warning  ");
    return outputString

def korvaiLinesAction(tokens):
    #print("In korvaiLinesAction")
    prapaatakaInfo=global_identifier.get("Prapaataka")
    prapaatakaInfo=int(prapaatakaInfo)
    
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
        #x = transliterate(lines, sanscript.BARAHA, sanscript.TAMIL)

        outputString=header + "\n" + x
        parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Korvai_Sloka"] = x
        parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["Korvai_header"] = header
    elif tokenLength <2 :
        print(" korvaiLines : Check the token returned. Seems to be a problem")
        SystemExit(-1)
    if (tokenLength >2 ):
        print(" korvaiLines : Check the parser. This is just a warning  ");
    return outputString
    print("End of korvaiLinesAction")

def prasnaKorvaiLinesAction(tokens):
    #print("In prasnaKorvaiLinesAction")
    prapaatakaInfo=global_identifier.get("Prapaataka")
    prapaatakaInfo=int(prapaatakaInfo)
    
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
        #x = transliterate(lines, sanscript.BARAHA, sanscript.TAMIL)

        outputString=header + "\n" + x
        parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["PrasnaKorvai_Sloka"] = x
        parseTree["TA"]["Prapaataka"][prapaatakaInfo-1]["PrasnaKorvai_header"] = header
    elif tokenLength <2 :
        print(" prasnaKorvaiLines : Check the token returned. Seems to be a problem")
        SystemExit(-1)
    if (tokenLength >2 ):
        print(" prasnaKorvaiLines : Check the parser. This is just a warning  ");
    return outputString
    

def prasnaLinesAction(tokens):
    #| 1 (10)
    prevPanchasat=0
    prevAnuvakkam=0
    #print("In prasnaLinesAction")
    panchasatEndPattern = r"(.*)\|+(\s)*(\d+)(\s)*\((\d+)\)(\s)*$"
    panchasatEndPattern_2 = r"(.*)\|+(\s)*(\d+-\d+)(\s)*\((\d+)\)(\s)*$"

    anuvakkamEndPattern = r"(\(.*\))\s*\(A(\d+)\)(\s|$)"
    panchasatTitlePattern_1 = r"([\d]+[.][\d]+[.][\d]+)(\s*)(.*)-\s*(\d+)(.*)$"
    panchasatTitlePattern_2 = r"^T.A.\s*([\d]+)[.]([\d]+)[.]([\d]+)(.*)"
    #panchasatTitlePattern_3 = r"^T.A. ([\d]+)[.]([\d]+)[.]([\d]+)(.*)"


    specialPattern = r"special korvai"

    IN_PANCHASAT_STATE=IN_PANCHASAT_END_STATE=IN_ANUVAKKAM_END_STATE=IN_TITLE_STATE=IN_SPECIAL_KORVAI=False
    x= len(tokens)-1
    lines=tokens[x].split("\n")
    panchasat_id_list = []
    anuvakkam_id_list = []
    anuvakkam_title_list = []
    anuvakkam_meta_list = []
    currentPanchasat = []
    currentSpecialKorval =[]
    panchasatCollection = []
    anuvakkamCollection = []
    specialKorvaiCollection = []
    currentAnuvakkamKorvai = ""
    for line in lines:
        
        panchasatEndResult = re.search(panchasatEndPattern,line)
        panchasatEndResult_2 = re.search(panchasatEndPattern_2,line)
        anuvakkamEndResult = re.search(anuvakkamEndPattern,line)
        panchasatTitleResult_1 = re.search(panchasatTitlePattern_1,line,re.IGNORECASE)
        panchasatTitleResult_2 = re.search(panchasatTitlePattern_2,line,re.IGNORECASE)
        #panchasatTitleResult_3 = re.search(panchasatTitlePattern_3,line,re.IGNORECASE)

        specialKorvaiResult = re.search(specialPattern,line,re.IGNORECASE)
        #print(line,panchasatEndResult,anuvakkamEndResult,panchasatTitleResult_1,panchasatTitleResult_2,specialKorvaiResult)
        if panchasatEndResult:
            #print("PanchasatEnd ",line)
            if anuvakkamEndResult:
                print(line," Matched both Panchasat and Anuvakkam")
            #print("1",panchasatResult.group(1))
            #print("2",panchasatResult.group(2))
            #print("3",panchasatResult.group(3))
            #print("4",panchasatResult.group(4))
            #print("5",panchasatResult.group(5))
            sloka = panchasatEndResult.group(1)
            currentPanchasat.append(sloka)
            panchasat_id = panchasatEndResult.group(3)
            panchasat_id_list.append(panchasat_id)
            panchasat = ' '.join(currentPanchasat)
            panchasatTuple = (global_identifier["Prapaataka"],global_identifier["Anuvakkam"],global_identifier["Panchasat"],panchasat_id,panchasat)
            panchasatCollection.append(panchasatTuple)
            currentPanchasat = []
            IN_PANCHASAT_END_STATE = True
            #print(line)
        elif panchasatEndResult_2:
            #print("Matched Panchasat End 2",line)
            
            sloka = panchasatEndResult_2.group(1)
            currentPanchasat.append(sloka)
            panchasat_id = panchasatEndResult_2.group(3)
            panchasat_id_list.append(panchasat_id)
            sloka = ' '.join(currentPanchasat)
            panchasatTuple = (global_identifier["Prapaataka"],global_identifier["Anuvakkam"],panchasat_id,panchasat_id,sloka)
            createPanchasatNodes(global_identifier["Prapaataka"],global_identifier["Anuvakkam"],panchasat_id)
            panchasatCollection.append(panchasatTuple)
            currentPanchasat = []
        elif anuvakkamEndResult:
            #print("Anuvakkam")
            #print("2",anuvakkamResult.group(2))
            anuvakkam_id = anuvakkamEndResult.group(2)
            currentAnuvakkamKorvai = anuvakkamEndResult.group(1)
            anuvakkamKorvaiTuple = (global_identifier["Prapaataka"],global_identifier["Anuvakkam"],global_identifier["Panchasat"],anuvakkam_id,currentAnuvakkamKorvai)
            anuvakkamCollection.append(anuvakkamKorvaiTuple)
            anuvakkam_id_list.append(anuvakkam_id)
            currentAnuvakkamKorvai = ""
            IN_ANUVAKKAM_END_STATE = True
        elif specialKorvaiResult:
            IN_SPECIAL_KORVAI = True
            currentSpecialKorval.append(line)
            #print("Special Korvai",line)
        elif panchasatTitleResult_1:
            #print("Meta Information-",line)
            #print("1",metaInformationResult.group(1))
            #print("4",metaInformationResult.group(4))
            anuvakkam_title_list.append(panchasatTitleResult_1.group(4)) 
            IN_TITLE_STATE = True
        elif panchasatTitleResult_2: #or panchasatTitleResult_3:
            '''
                At this point ideally 
                     - the previous panchasat should be added to the collection
                          -- which implies  the variable currentPanchast should be an empty list
                     -- if this is a new anuvakkam should be added to the collection
                          -- which implies the variable currentAnuvakkamKorvai should be an empty string
                    

            '''
            #if panchasatTitleResult_3:
                #panchasatTitleResult_2 = panchasatTitleResult_3
            if IN_SPECIAL_KORVAI:
                #print("end of special korvai ")
                IN_SPECIAL_KORVAI = False
                newstuff = ' '.join(currentSpecialKorval)
                korvaiTuple=(global_identifier["Prapaataka"],global_identifier["Anuvakkam"],global_identifier["Panchasat"],newstuff)
                #print("Adding to specialKorvaiCollection ",korvaiTuple)
                specialKorvaiCollection.append(korvaiTuple)
                currentSpecialKorval = []
            IN_TITLE_STATE = True
            
            prapaatakaInfo = panchasatTitleResult_2.group(1)
            anuvakkamInfo = panchasatTitleResult_2.group(2)
            panchasatInfo = panchasatTitleResult_2.group(3)
            if (any(currentPanchasat)):
                #print("This should have been part of something else Current identifiers are ", prapaatakaInfo,anuvakkamInfo,panchasatInfo,currentPanchasat)
                newstuff = ' '.join(currentPanchasat)
                t1 = re.search(panchasatEndPattern,newstuff)
                t2 = re.search(anuvakkamEndPattern,newstuff)
                if t1:
                    #print("Panchasat -- Need to add into tuple ",t1.group(3))
                    pass
                elif t2:
                    #print("Matched Anuvakkam Korvai id. Adding to it ",t2.group(2),newstuff)
                    anuvakkam_id = t2.group(2)
                    currentAnuvakkamKorvai = t2.group(1)
                    anuvakkamKorvaiTuple = (global_identifier["Prapaataka"],global_identifier["Anuvakkam"],global_identifier["Panchasat"],anuvakkam_id,currentAnuvakkamKorvai)

                    anuvakkamCollection.append(anuvakkamKorvaiTuple)
                    anuvakkam_id_list.append(anuvakkam_id)
                    currentAnuvakkamKorvai = ""
                    currentPanchasat = []
                else:
                    print("Ignoring this line",newstuff)
                    newstuff=""
                    currentPanchasat = []
            createPrapaatakaNodes(prapaatakaInfo)
            createAnuvakkamNodes(prapaatakaInfo,anuvakkamInfo)
            createPanchasatNodes(prapaatakaInfo,anuvakkamInfo,panchasatInfo)
            global_identifier["Prapaataka"]=prapaatakaInfo
            
            global_identifier["Anuvakkam"]=anuvakkamInfo
            global_identifier["Panchasat"]=panchasatInfo
            #print("Meta Information-",line)
            #print("1",metaInformationResult.group(1))
            #print("4",metaInformationResult.group(4))
            anuvakkam_meta_list.append(panchasatTitleResult_2.group(2))
        else:
            #print("Alternative",line)
            if IN_SPECIAL_KORVAI:
                currentSpecialKorval.append(line)

            elif IN_TITLE_STATE:
                currentPanchasat.append(line)

        

    

    #print("Panchasat")
    prevAnuvakkam_id = prevPrapaataka_id = prevPanchasat_id = prevPanchasat_number =0
    for (prapaataka_id,anuvakkam_id,panchasat_id,panchasat_number,sloka) in panchasatCollection:
        #prapaataka_id = int(prapaataka_id)
        #anuvakkam_id = int(anuvakkam_id)
        #panchasat_id = int(panchasat_id)
        #panchasat_number = int(panchasat_number)
        #print("T.A.",prapaataka_id.strip(),".",anuvakkam_id.strip(),".",panchasat_id.strip())
        #print(sloka,panchasat_number)
        prevAnuvakkam_id = anuvakkam_id
        prevPanchasat_id = panchasat_id
        prevPanchasat_number = panchasat_number

    #print("Anuvakkam",anuvakkamCollection)
    #print("Special Korvai",specialKorvaiCollection)
    updateTree(panchasatCollection,anuvakkamCollection,specialKorvaiCollection)
    #print("End of prasnaLinesAction")


#parseTree = json.loads(ts_string)





  
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

prasnaKorvai_Starting = pp.CaselessKeyword("Prapaataka Korvai with starting Padams")
korvai_Starting = pp.CaselessKeyword("korvai with starting padams of")
firstLastPadam_Starting = pp.CaselessKeyword("first and last padam")
prapaatakaKorvai_Starting = pp.CaselessKeyword("Prapaataka Korvai with starting Padams of")
samhitaKorvai_Starting = pp.CaselessKeyword("samhita korvai with starting padams of")
specialKorvai_Starting = pp.CaselessKeyword("special korvai")

prasnaEnding_Starting_1 = pp.CaselessKeyword("|| hari#H OM ||")
prasnaEnding_Starting_2 = pp.CaselessKeyword("|| hariH# OM ||")
prasnaEnding_Starting_3 = pp.CaselessKeyword("|| hari# OM ||")

prasnaEnding_Starting = prasnaEnding_Starting_1 | prasnaEnding_Starting_2 | prasnaEnding_Starting_3

prasnaLines = pp.Optional(EOL) + pp.Combine(
    pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=prasnaKorvai_Starting)
).setResultsName("prasna_Lines*")

prasnaLines.setParseAction(prasnaLinesAction)
prasnaKorvaiLines = (
    prasnaKorvai_Starting
    + pp.Optional(EOL)
    + pp.Group(pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=korvai_Starting | specialKorvai_Starting))
)
prasnaKorvaiLines.setParseAction(prasnaKorvaiLinesAction)
korvaiLines = (
    korvai_Starting
    + pp.Optional(EOL)
    + pp.Group(
        pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=firstLastPadam_Starting)
    )
)
korvaiLines.setParseAction(korvaiLinesAction)
prapaatakaKorvaiLines = (
    prapaatakaKorvai_Starting
    + pp.Optional(EOL)
    + pp.Group(pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=EmptyLine))
)
specialKorvaiLines = (
    specialKorvai_Starting
    + pp.Optional(EOL)
    + pp.Group(pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=EmptyLine))
)

samhitaKorvaiLines = (
    samhitaKorvai_Starting
    + pp.Optional(EOL)
    + pp.Group(pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=EmptyLine))
)
firstLastPadamLines = (
    firstLastPadam_Starting
    + pp.Optional(EOL)
    + pp.Group(pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=EmptyLine))
)
firstLastPadamLines.setParseAction(firstLastPadamLinesAction)
Separator1 = pp.Keyword("*************")
prasna_Separator_1 = pp.Keyword("==========================================").suppress()
prasna_Separator_2 = pp.Keyword("------------------------------------------").suppress()

prasna_Separator = prasna_Separator_1 | prasna_Separator_2
annexureStartingLine_1 = pp.LineStart() + pp.CaselessLiteral("Annexure")
annexureStartingLine_2 = (
    pp.LineStart()  + pp.CaselessLiteral("Appendix")
)
annexureStartingLine = annexureStartingLine_1 | annexureStartingLine_2

annexureLines = (
    pp.Combine(annexureStartingLine + pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL)
    + pp.Optional(pp.OneOrMore(EmptyLine))
    + pp.Combine(pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=prasna_Separator)))
)



remainingLines = (
    
    prasnaEnding_Starting
    + pp.Optional(EOL)
    + pp.Group(
        pp.OneOrMore(
            ~invocation + pp.SkipTo(pp.LineEnd()) + EOL, stopOn=prasna_Separator
        )
    ).setResultsName("RemainingLines")
)
remainingLines.setParseAction(remainingLinesAction) # This is not working


#remainingLines = remainingLines_WithoutAppendix  # This seems like a hack but this is the best I can do now
# Otherwise a greedy match happens
corePrasna = (
    sectiontitleLine
    + prasnaLines
    + prasnaKorvaiLines
    #+ pp.ZeroOrMore(specialKorvaiLines)
    + korvaiLines
    + firstLastPadamLines
    #+ pp.ZeroOrMore(prapaatakaKorvaiLines)
    #+ pp.ZeroOrMore(samhitaKorvaiLines)
    + remainingLines
)

corePrasna.setParseAction(corePrasnaAction)
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
     pp.Optional((prasna_Separator + pp.SkipTo(EOL))).suppress() + invocation + titleLine + corePrasna
)
prasna_Section = (prasna_Section_2 | prasna_Section_1).setResultsName("prasna_Section*")
#prasna_Section = (prasna_Section_2 ).setResultsName("prasna_Section*")



'''prasnaLines.setName("prasnaLine")
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
prapaatakaKorvaiLines.setName("KKorvai")
remainingLines.setName("rem")'''

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
json_file_name = "TA.json"

my_json = json.dumps(parseTree,indent=3,ensure_ascii=False, sort_keys=True)
my_json = my_json.replace("\uA8E3","\u1CDA")
with open(json_file_name, "w") as f:
    f.write(my_json)

