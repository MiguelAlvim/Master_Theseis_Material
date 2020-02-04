import random as rng
import sys
import time
from enum import IntEnum

runningTime = time.time();

# -s <SEED> | int
# -p <file PATH> | str
# -a <AMOUNT of persons> | unsigned int | A multiple of 12500 or a substantialy larger number is recomended
# -A a variation of -a, instead of the total number, the user inputs how many members of each permutation he wants; It's overrides the -a value
# -v VERBOSE creation, printing on the terminal all the generated entries

SEED   = 0
PATH   = "syntetic_lo.txt"
AMOUNT = 4320
VERBOSE = False
FORTRAINING = False
# for n in range(len(sys.argv)):
    # print(str(n)+" = "+sys.argv[n])
# print()

#Seed
try:
    SEED = int(sys.argv[sys.argv.index("-s")+1])
    rng.seed(SEED)
except:
    rng.seed(0)
    print("No SEED given, using default 0")
    # pass
    
#Path
try:
    PATH = sys.argv[sys.argv.index("-p")+1]
except:
    print("No PATH given, using default \"\syntetic.txt\"")
    # pass
    
#Amount
try:
    AMOUNT = int(sys.argv[sys.argv.index("-a")+1])
except:
    # print("No AMOUNT given, using default 4320 / 1 entry per permutation")
    #Amount 2
    try:
        AMOUNT = 4320*int(sys.argv[sys.argv.index("-A")+1])
    except:
        print("No AMOUNT given, using default 4320 / 1 entry per permutation")
    # pass
    # pass
    
#Verbose
try:
    sys.argv[sys.argv.index("-v")]
    VERBOSE = True
except:
    # print("Not VERBOSE")
    pass

class Struct(IntEnum):#Structure 1.7
    ATOMIC_LINEAR = 0
    OTHERS        = 1

def structToSTR(struct):
    if struct == Struct.ATOMIC_LINEAR:
        return "ATOMIC_LINEAR"
    return "OTHERS"
    
class TF (IntEnum):#Techinical Format 4.1
    APPLICATION = 0
    IMAGE       = 1
    MODEL       = 2
    VIDEO       = 3
    AUDIO       = 4
    MESSAGE     = 5
    TEXT        = 6
    OTHERS      = 7
    
def tfToSTR(struct):
    if struct == TF.APPLICATION:
        return "APPLICATION"
    if struct == TF.IMAGE:
        return "IMAGE"
    if struct == TF.MODEL:
        return "MODEL"
    if struct == TF.VIDEO:
        return "VIDEO"
    if struct == TF.AUDIO:
        return "AUDIO"
    if struct == TF.MESSAGE:
        return "MESSAGE"
    if struct == TF.TEXT:
        return "TEXT"
    return "OTHERS"
    
class IT(IntEnum):#Iteractivity Type 5.1
    ACTIVE     = 0
    MIXED      = 1
    EXPOSITIVE = 2
    
def itToSTR(struct):
    if struct == IT.ACTIVE:
        return "ACTIVE"
    if struct == IT.MIXED:
        return "MIXED"
    if struct == IT.EXPOSITIVE:
        return "EXPOSITIVE"
        
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

def lrToSTR(struct):
    if struct == LR.DIAGRAM_FIGURE_GRAPH:
        return "DIAGRAM_FIGURE_GRAPH"
    if struct == LR.EXERCISE:
        return "EXERCISE"
    if struct == LR.SIMULATION:
        return "SIMULATION"
    if struct == LR.EXPERIMENT:
        return "EXPERIMENT"
    if struct == LR.PROBLEM_STATEMENT:
        return "PROBLEM_STATEMENT"
    if struct == LR.LECTURE:
        return "LECTURE"
    if struct == LR.NARRATIVE_TEXT_LECTURE:
        return "NARRATIVE_TEXT_LECTURE"
    if struct == LR.INDEX:
        return "INDEX"
    return "OTHERS"
    
class IL(IntEnum):#Interactivity Level 5.3
    VERY_HIGH = 0
    HIGH      = 1
    MEDIUM    = 2
    LOW       = 3
    VERY_LOW  = 4
    
def ilToSTR(struct):
    if struct == IL.VERY_HIGH:
        return "VERY_HIGH"
    if struct == IL.HIGH:
        return "HIGH"
    if struct == IL.MEDIUM:
        return "MEDIUM"
    if struct == IL.LOW:
        return "LOW"
    if struct == IL.VERY_LOW:
        return "VERY_LOW"
        
    
class RK(IntEnum):#Relatioship Kind 7.1
    HAS_PART = 0
    OTHERS   = 1

def rkToSTR(struct):
    if struct == RK.HAS_PART:
        return "HAS_PART"
    return "OTHERS"
    
class LO:
    def __init__(self,name="placeholder",it=IT.ACTIVE,il=IL.VERY_LOW,lr=LR.OTHERS,tf=TF.OTHERS,struct=Struct.OTHERS,rk=RK.OTHERS,size=100,audioRate=100,videoRate=200):
        self.it = it
        self.il = il
        self.lr = lr
        self.tf = tf
        self.struct = struct
        self.rk = rk
        self.size = size
        self.audioRate = audioRate
        self.videoRate = videoRate
        self.name = name
    def __str__(self):
        return "["+self.name+"]\n"+\
               "file_size_B : "+str(self.size)+"\n"+\
               "video_bit_rate_kbps[v0] : "+str(self.videoRate)+"\n"+\
               "audio_bit_rate_kbps[a0] : "+str(self.audioRate)+"\n"+\
               "1.7 : "+str(self.struct)+"\n"+\
               "4.1 : "+str(self.tf)+"\n"+\
               "5.1 : "+str(self.it)+"\n"+\
               "5.2 : "+str(self.lr)+"\n"+\
               "5.3 : "+str(self.il)+"\n"+\
               "7.1 : "+str(self.rk)
    def toStrOnlyLOM(self):
        return "["+str(self.struct)+","+\
               str(self.tf)+","+\
               str(self.it)+","+\
               str(self.lr)+","+\
               str(self.il)+","+\
               str(self.rk)+"]"
    def singleLineToStr(self):
        return "["+self.name+"]  "+\
               "file_size_B : "+str(self.size)+"  "+\
               "video_bit_rate_kbps[v0] : "+str(self.videoRate)+"  "+\
               "audio_bit_rate_kbps[a0] : "+str(self.audioRate)+"  "+\
               "1.7 : "+str(self.struct)+"  "+\
               "4.1 : "+str(self.tf)+"  "+\
               "5.1 : "+str(self.it)+"  "+\
               "5.2 : "+str(self.lr)+"  "+\
               "5.3 : "+str(self.il)+"  "+\
               "7.1 : "+str(self.rk)
    def singleLineToStrOnlyValues(self):
        return "["+self.name+"]  "+\
               str(self.size)+"  "+\
               str(self.videoRate)+"  "+\
               str(self.audioRate)+"  "+\
               str(self.struct)+"  "+\
               str(self.tf)+"  "+\
               str(self.it)+"  "+\
               str(self.lr)+"  "+\
               str(self.il)+"  "+\
               str(self.rk)

axisSpot = [0,0,0,0,0,0]
fullLoop = 0
file = open(PATH,"w").close()
file = open(PATH,"a")
for n in range(AMOUNT):
    lo =      LO(name= "__"+str(n)+"__",
            audioRate= rng.randrange(8,512),
            videoRate= rng.randrange(124,4096),
                 size= rng.randrange(3000,2000000),
               struct= (axisSpot[0]),
                   tf= (axisSpot[1]),
                   it= (axisSpot[2]),
                   lr= (axisSpot[3]),
                   il= (axisSpot[4]),
                   rk= (axisSpot[5]))
    print(lo.toStrOnlyLOM())
    axisSpot[0] = (axisSpot[0]+1)%len(Struct)
    if(axisSpot[0] == 0):
        axisSpot[1] = (axisSpot[1]+1)%len(TF)
        if(axisSpot[1] == 0):
            axisSpot[2] = (axisSpot[2]+1)%len(IT)
            if(axisSpot[2] == 0):
                axisSpot[3] = (axisSpot[3]+1)%len(LR)
                if(axisSpot[3] == 0):
                    axisSpot[4] = (axisSpot[4]+1)%len(IL)
                    if(axisSpot[4] == 0):
                        axisSpot[5] = (axisSpot[5]+1)%len(RK)
                        if(axisSpot[5] == 0):
                            fullLoop +=1
                                
runningTime =  time.time() - runningTime
print("Tempo Gasto: ~"+str("{0:.2f}".format(runningTime))+"s")
