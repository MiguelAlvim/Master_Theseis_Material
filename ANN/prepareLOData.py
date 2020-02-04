import sys
import re
from enum import IntEnum

FILE_OUTPUT = None
FILE_PATH = None
VERBOSE = False
#Verbose
try:
    sys.argv[sys.argv.index("-v")]
    VERBOSE = True
except:
    pass
    
#Input
try:
    FILE_PATH = sys.argv[sys.argv.index("-p")+1]
except:
    print("No input file given")
    sys.exit()
    
#Output
try:
    FILE_OUTPUT = sys.argv[sys.argv.index("-f")+1]
except:
    print("No output file given, using \"Affinity.txt\" as default")
    FILE_OUTPUT = "Affinity.txt"
    # sys.exit()

#based on Anitha and Deisy 2015: Proposing a novel approach for classification and sequencing of Learning Objects in E-learning systems based on learning style
class LS(IntEnum):#Learning Style 
    #Axis active/reflexive
    ACTIVE     = 0
    REFLECTIVE = 1
    #Axis sensing/intuitive
    SENSING    = 2
    INTUITIVE  = 3
    #Axis visual/verbal
    VISUAL     = 4
    VERBAL     = 5
    #Axis sequential/global
    SEQUENTIAL = 6
    GLOBAL     = 7
    
class IT(IntEnum):#Iteractivity Type 5.1
    ACTIVE     = 0
    MIXED      = 1
    EXPOSITIVE = 2
    
class IL(IntEnum):#Interactivity Level 5.3
    VERY_HIGH = 0
    HIGH      = 1
    MEDIUM    = 2
    LOW       = 3
    VERY_LOW  = 4

class LR(IntEnum):#Learning Resource Type 5.2
    DIAGRAM_FIGURE_GRAPH    = 0
    EXERCISE                = 1
    SIMULATION              = 2
    EXPERIMENT              = 3
    PROBLEM_STATEMENT       = 4
    LECTURE                 = 5
    NARRATIVE_TEXT_LECTURE  = 6
    INDEX                   = 7
    OTHERS                  = 8
    
class TF (IntEnum):#Techinical Format 4.1
    APPLICATION = 0
    IMAGE       = 1
    MODEL       = 2
    VIDEO       = 3
    AUDIO       = 4
    MESSAGE     = 5
    TEXT        = 6
    OTHERS      = 7
    
class Struct(IntEnum):#Structure 1.7
    ATOMIC_LINEAR = 0
    OTHERS        = 1
    
class RK(IntEnum):#Relatioship Kind 7.1
    HAS_PART = 0
    OTHERS   = 1

metadataWeight = [LS.ACTIVE,
                  LS.REFLECTIVE,
                  LS.SENSING,
                  LS.INTUITIVE,
                  LS.VISUAL,
                  LS.VERBAL,
                  LS.SEQUENTIAL,
                  LS.GLOBAL]
metadataWeight[LS.ACTIVE] = {'5.1':{IT.ACTIVE: 0.9,IT.MIXED: 0.5, IT.EXPOSITIVE:0.1}
                            ,'5.3':{IL.VERY_HIGH: 0.9,IL.HIGH: 0.7, IL.MEDIUM:0.5, IL.LOW: 0.3, IL.VERY_LOW: 0.1}}
metadataWeight[LS.REFLECTIVE] = {'5.1':{IT.ACTIVE: 0.1,IT.MIXED: 0.5, IT.EXPOSITIVE:0.9}
                            ,'5.3':{IL.VERY_HIGH: 0.1,IL.HIGH: 0.3, IL.MEDIUM:0.5,IL.LOW:0.7,IL.VERY_LOW:0.9}}
                            
metadataWeight[LS.SENSING] = {'5.2':{LR.DIAGRAM_FIGURE_GRAPH: 0.9,
                                     LR.EXERCISE: 0.5,
                                     LR.SIMULATION: 0.9,
                                     LR.EXPERIMENT: 0.9,
                                     LR.PROBLEM_STATEMENT: 0.5,
                                     LR.LECTURE: 0.6,
                                     LR.OTHERS: 1.0,}}          
                                     
metadataWeight[LS.INTUITIVE] = {'5.2':{LR.DIAGRAM_FIGURE_GRAPH: 0.5,
                                     LR.EXERCISE: 0.9,
                                     LR.SIMULATION: 0.5,
                                     LR.EXPERIMENT: 0.7,
                                     LR.PROBLEM_STATEMENT: 0.9,
                                     LR.LECTURE: 0.9,
                                     LR.OTHERS: 1.0,}}

metadataWeight[LS.VISUAL] = {'4.1':{TF.APPLICATION: 0.9,TF.IMAGE: 0.9, TF.MODEL: 0.9, TF.VIDEO: 0.9,
                                   TF.AUDIO: 0.4, TF.MESSAGE: 0.4, TF.TEXT: 0.5, TF.OTHERS: 1.0}
                            ,'5.2':{LR.DIAGRAM_FIGURE_GRAPH: 0.9, LR.NARRATIVE_TEXT_LECTURE: 0.5, LR.OTHERS: 1.0}}
                            
metadataWeight[LS.VERBAL] = {'4.1':{TF.APPLICATION: 0.5,TF.IMAGE: 0.2, TF.MODEL: 0.3, TF.VIDEO: 0.4,
                                   TF.AUDIO: 0.9, TF.MESSAGE: 0.9, TF.TEXT: 0.9, TF.OTHERS: 1.0}
                            ,'5.2':{LR.DIAGRAM_FIGURE_GRAPH: 0.5, LR.NARRATIVE_TEXT_LECTURE: 0.9, LR.OTHERS: 1.0}}
                            
metadataWeight[LS.SEQUENTIAL] = {'1.7':{Struct.ATOMIC_LINEAR: 0.9, Struct.OTHERS: 0.5}
                                ,'7.1':{RK.HAS_PART: 0.1, RK.OTHERS: 1.0}
                                ,'5.2':{LR.INDEX: 0.2, LR.OTHERS: 1.0}}
                                
metadataWeight[LS.GLOBAL] = {'1.7':{Struct.ATOMIC_LINEAR: 0.8, Struct.OTHERS: 0.9}
                            ,'7.1':{RK.HAS_PART: 0.9, RK.OTHERS: 1.0}
                            ,'5.2':{LR.INDEX: 0.9, LR.OTHERS: 1.0}}
                            

def parseTo1dot7(string):
    val = string.upper().replace(' ','_')
    if(val == "ATOMIC_LINEAR"):
        return Struct.ATOMIC_LINEAR
    return Struct.OTHERS
def parseTo4dot1(string):
    val = string.upper().replace(' ','_')
    if(val == "APPLICATION"):
        return TF.APPLICATION
    if(val == "IMAGE"):
        return TF.IMAGE
    if(val == "MODEL"):
        return TF.MODEL
    if(val == "VIDEO"):
        return TF.VIDEO
    if(val == "AUDIO"):
        return TF.AUDIO
    if(val == "MESSAGE"):
        return TF.MESSAGE
    if(val == "TEXT"):
        return TF.TEXT
    return TF.OTHERS
def parseTo5dot1(string):
    val = string.upper().replace(' ','_')
    if(val == "ACTIVE"):
        return IT.ACTIVE
    if(val == "MIXED"):
        return IT.MIXED
    if(val == "EXPOSITIVE"):
        return IT.EXPOSITIVE
    return None
def parseTo5dot2(string):
    val = string.upper().replace(' ','_')
    if(val == "DIAGRAM_FIGURE_GRAPH"):
        return LR.DIAGRAM_FIGURE_GRAPH
    if(val == "EXERCISE"):
        return LR.EXERCISE
    if(val == "SIMULATION"):
        return LR.SIMULATION
    if(val == "EXPERIMENT"):
        return LR.EXPERIMENT
    if(val == "PROBLEM_STATEMENT"):
        return LR.PROBLEM_STATEMENT
    if(val == "NARRATIVE_TEXT_LECTURE"):
        return LR.NARRATIVE_TEXT_LECTURE
    if(val == "INDEX"):
        return LR.INDEX
    return LR.OTHERS
def parseTo5dot3(string):
    val = string.upper().replace(' ','_')
    if(val == "VERY_HIGH"):
        return IL.VERY_HIGH
    if(val == "HIGH"):
        return IL.HIGH
    if(val == "MEDIUM"):
        return IL.MEDIUM
    if(val == "LOW"):
        return IL.LOW
    if(val == "VERY_LOW"):
        return IL.VERY_LOW
    return None
def parseTo7dot1(string):
    val = string.upper().replace(' ','_')
    if(val == "HAS_PART"):
        return RK.HAS_PART
    return RK.OTHERS
    
def readFile(path,metadataList):
    currentMetadata = -1
    with open(path,'r') as file:
        # aux = True
        line = file.readline()
        # while(line or aux):
        while(line):
            # aux = False
            # print(line, end = '')
            #check for next entry
            name = re.search('(^\[.*\])',line)
            if(name):
                ++currentMetadata
                metadataList.append(dict())
                metadataList[currentMetadata]['name'] = (name.groups()[0].replace('[','')).replace(']','')
                if VERBOSE:
                    print(metadataList[currentMetadata]['name'])
            else:
                m = re.search('(1\.7 : )(.*)',line)
                if(m):
                    metadataList[currentMetadata]['1.7'] = parseTo1dot7(m.groups()[1])
                    # continue
                m = re.search('(4\.1 : )(.*)',line)
                if(m):
                    metadataList[currentMetadata]['4.1'] = parseTo4dot1(m.groups()[1])
                    # continue
                m = re.search('(5\.1 : )(.*)',line)
                if(m):
                    metadataList[currentMetadata]['5.1'] = parseTo5dot1(m.groups()[1])
                    # continue
                m = re.search('(5\.2 : )(.*)',line)
                if(m):
                    metadataList[currentMetadata]['5.2'] = parseTo5dot2(m.groups()[1])
                    # continue
                m = re.search('(5\.3 : )(.*)',line)
                if(m):
                    metadataList[currentMetadata]['5.3'] = parseTo5dot3(m.groups()[1])
                    # continue
                m = re.search('(7\.1 : )(.*)',line)
                if(m):
                    metadataList[currentMetadata]['7.1'] = parseTo7dot1(m.groups()[1])
                    # continue
                m = re.search('(file_size_B \: )([0-9]*)',line)
                if(m):
                    metadataList[currentMetadata]['size'] = m.groups()[1]
                    
                m = re.search('(video_bit_rate_kbps\[v[0-9]*\] \: )(([0-9]| )*)',line)
                if(m):
                    metadataList[currentMetadata]['video_rate'] = m.groups()[1]
                    
                m = re.search('(audio_bit_rate_kbps\[a[0-9]*\] \: )(([0-9]| )*)',line)
                if(m):
                    metadataList[currentMetadata]['audio_rate'] = m.groups()[1]
                    
            line = file.readline()
    if VERBOSE:
        print(len(metadataList))
        for data in metadataList:
            for key, value in data.items():
                print(str(key)+ " = " + str(value))
            print()
def calculateMembership(eixo,object):
    val = 0
    # print(metadataWeight[eixo])
    for axis, values in metadataWeight[eixo].items():
        weight = 1/len(metadataWeight[eixo])
        if VERBOSE:
            print(str(eixo)+' '+str(axis))
            print(metadataWeight[eixo])
            print(metadataWeight[eixo][axis])
            print(weight)
        try:
            val += weight*metadataWeight[eixo][axis][object[axis]]
            if VERBOSE:
                print(str(weight)+"*"+str(metadataWeight[eixo][axis][object[axis]]))
                print()
        except:
            val += weight#If not present, then it's 'others', and those always are 1 point
            if VERBOSE:
                print()
        # if VERBOSE:
            # print(str(object[axis]))
            # print("\t"+axis +" : "+ str(object[axis]))
            # print("\tValue gives : "+ str(metadataWeight[eixo][axis][object[axis]]))
    return val

metadata = []
readFile(FILE_PATH,metadata)        
# if VERBOSE:
    # print("-----|Suitability|-----")
    # LS.ACTIVE     = 0
    # LS.REFLECTIVE = 1
    # LS.SENSING    = 2
    # LS.INTUITIVE  = 3
    # LS.VISUAL     = 4
    # LS.VERBAL     = 5
    # LS.SEQUENTIAL = 6
    # LS.GLOBAL     = 7
open(FILE_OUTPUT,'w').close()
fi = open(FILE_OUTPUT,'a')
    
for lo in metadata:
    activeval = calculateMembership(LS.ACTIVE,lo)
    reflectiveval = calculateMembership(LS.REFLECTIVE,lo)
    sensingval = calculateMembership(LS.SENSING,lo)
    intuitiveval = calculateMembership(LS.INTUITIVE,lo)
    visualval = calculateMembership(LS.VISUAL,lo)
    verbalval = calculateMembership(LS.VERBAL,lo)
    sequentialval = calculateMembership(LS.SEQUENTIAL,lo)
    globalval = calculateMembership(LS.GLOBAL,lo)
    
    # tot = activeval + reflectiveval + sensingval + intuitiveval + visualval + verbalval + sequentialval + globalval
    tot = 1
    activeval = round(activeval/tot,4)
    reflectiveval = round(reflectiveval/tot,4)
    sensingval = round(sensingval/tot,4)
    intuitiveval = round(intuitiveval/tot,4)
    visualval = round(visualval/tot,4)
    verbalval = round(verbalval/tot,4)
    sequentialval = round(sequentialval/tot,4)
    globalval = round(globalval/tot,4)
    try:
        fileSize = lo['size']
    except:
        fileSize = 0
    try:
        bitRateVideo = lo['video_rate']
        bitRateAudio = lo['audio_rate']
    except:
        bitRateVideo = 0
        bitRateAudio = 0

    if VERBOSE:
        print("["+lo['name']+"]")
        # print("--|Final Results|--")
        print("\tACTIVE: "+ str(activeval)+"")
        print("\tREFLECTIVE: "+ str(reflectiveval)+"")
        print("\tSENSING: "+ str(sensingval)+"")
        print("\tINTUITIVE: "+ str(intuitiveval)+"")
        print("\tVISUAL: "+ str(visualval)+"")
        print("\tVERBAL: "+ str(verbalval)+"")
        print("\tSEQUENTIAL: "+ str(sequentialval)+"")
        print("\tGLOBAL: "+ str(globalval)+"")
        print()


    fi.write("["+lo['name']+"]\n")
    fi.write("SIZE: "+ str(fileSize)+"\n")
    fi.write("VIDEO_RATE: "+ str(bitRateVideo)+"\n")
    fi.write("AUDIO_RATE: "+ str(bitRateAudio)+"\n")
    fi.write("ACTIVE: "+ str(activeval)+"\n")
    fi.write("REFLECTIVE: "+ str(reflectiveval)+"\n")
    fi.write("SENSING: "+ str(sensingval)+"\n")
    fi.write("INTUITIVE: "+ str(intuitiveval)+"\n")
    fi.write("VISUAL: "+ str(visualval)+"\n")
    fi.write("VERBAL: "+ str(verbalval)+"\n")
    fi.write("SEQUENTIAL: "+ str(sequentialval)+"\n")
    fi.write("GLOBAL: "+ str(globalval)+"\n")
    fi.write('\n')
fi.close()
    

        
    











