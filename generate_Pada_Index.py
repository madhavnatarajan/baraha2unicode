import json
from pathlib import Path


ts_string = '''\
{
    "TS": {
        "Kanda": [{"id": "1","Prasna": [{"Id": "1","Anuvakkam": [{"Id": "1","Panchasat": [{"Id": "1","Content": "x"}]}]}]}]
    }
}
'''
padaIndex={}
padaTerms=[]
ts_string = Path("TS_withPada.json").read_text(encoding="utf-8")
parseTree = json.loads(ts_string)
for kanda in parseTree['TS']['Kanda']:
    #print(kanda['id'])
    for prasna in kanda['Prasna']:
        #print(prasna['id'])
        for anuvakkam in prasna['Anuvakkam']:
            #print(anuvakkam['id'])
            for panchasat in anuvakkam['Panchasat']:
                value=panchasat['header'].replace("TS ","")
                #print(panchasat['PadaPaata'],panchasat['header'])
                tokens=panchasat['PadaPaata'].split("।")
                for t in tokens:
                    key=t.strip()
                    key=key.replace("['']","")
                    key=key.replace("(","")
                    key=key.replace(")","")
                    key=key.replace(" - ","-")
                    key=key.strip()
                    if padaIndex.get(key) is None:
                        padaIndex[key]=[]
                    
                    padaIndex[key].append(value)
                    #print(key,value)
                #padaOccurence=panchasat['header'].replace("TS ","")
                # print(panchasat['Content']
for key in padaIndex.keys():
    padaIndex[key]=sorted(set(padaIndex[key]))

sortedPadaIndex = dict(sorted(padaIndex.items()))
for key in sortedPadaIndex.keys():
    #print("key",key)
    value = ', '.join(sortedPadaIndex[key][:10])
    totalItems = len(sortedPadaIndex[key])
    if totalItems > 10:
        moreitems=str(totalItems-10)
        text= " ...+ "+moreitems+" more"
        value+=text
    print("key",key,value)
#sortedPadaIndex=sorted(padaIndex.items(), key=lambda x: len(x[1]), reverse=True)
#for item in sortedPadaIndex:
#    print(item[0],len(item[1]))    #
#print(padaIndex)
    

