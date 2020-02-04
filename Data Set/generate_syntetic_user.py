import random as rng
import sys
import time

runningTime = time.time();
#constants
STRONG = 8
MODERATE = 4
BALANCED = 0
LEFT = -1
RIGHT = 1

# -s <seed> | int
# -p <file path> | str
# -a <amount of persons> | unsigned int | A multiple of 12500 or a substantialy larger number is recomended
# -A a variation of -a, instead of the total number, the user inputs how many members of each permutation he wants; It's overrides the -a value
# -v verbose creation, printing on the terminal all the generated entries

seed   = 0
path   = "syntetic_user.txt"
amount = 12500
verbose = False
# for n in range(len(sys.argv)):
    # print(str(n)+" = "+sys.argv[n])
# print()

#Seed
try:
    seed = int(sys.argv[sys.argv.index("-s")+1])
    rng.seed(seed)
except:
    print("No seed given, using default <current sysetm time>")
    # pass
    
#Path
try:
    path = sys.argv[sys.argv.index("-p")+1]
except:
    print("No path given, using default \"\syntetic.txt\"")
    # pass
    
#Amount
try:
    amount = int(sys.argv[sys.argv.index("-a")+1])
except:
    # print("No amount given, using default 12500 / 1 entry per permutation")
    #Amount 2
    try:
        amount = 12500*int(sys.argv[sys.argv.index("-A")+1])
    except:
        print("No amount given, using default 12500 = 1 entry per permutation")
    # pass
    # pass
    

#Verbose
try:
    sys.argv[sys.argv.index("-v")]
    verbose = True
except:
    # print("Not verbose")
    pass
    
#Auxiliary class for quickly creating and printing users
class User:
    def __init__(self,activeVal =0.5,reflectiveVal =0.5, sensingVal=0.5, intuitiveVal =0.5, visualVal=0.5, verbalVal =0.5, sequentialVal =0.5, globalVal =0.5, connectionType= 0, connectionSpeed = 30, deviceType = 0):
        self.activeVal = activeVal
        self.reflectiveVal = reflectiveVal
        self.sensingVal = sensingVal
        self.intuitiveVal = intuitiveVal
        self.visualVal = visualVal
        self.verbalVal = verbalVal
        self.sequentialVal = sequentialVal
        self.globalVal = globalVal
        self.connectionType = connectionType
        self.connectionSpeed = connectionSpeed
        self.deviceType = deviceType
    def __str__(self):
        return "Active: "+str(self.activeVal)+"\n"+\
               "Reflective: "+str(self.reflectiveVal)+"\n"+\
               "Sensing: "+str(self.sensingVal)+"\n"+\
               "Intuitive: "+str(self.intuitiveVal)+"\n"+\
               "Visual: "+str(self.visualVal)+"\n"+\
               "Verbal: "+str(self.verbalVal)+"\n"+\
               "Sequential: "+str(self.sequentialVal)+"\n"+\
               "Global: "+str(self.globalVal)+"\n"+\
               "ConnectionType: "+str(self.connectionType)+"\n"+\
               "ConnectionSpeed: "+str(self.connectionSpeed)+"\n"+\
               "DeviceType: "+str(self.deviceType)
    def singleLineToStr(self):
        return "Active: "+str(self.activeVal)+"  "+\
               "Reflective: "+str(self.reflectiveVal)+"  "+\
               "Sensing: "+str(self.sensingVal)+"  "+\
               "Intuitive: "+str(self.intuitiveVal)+"  "+\
               "Visual: "+str(self.visualVal)+"  "+\
               "Verbal: "+str(self.verbalVal)+"  "+\
               "Sequential: "+str(self.sequentialVal)+"  "+\
               "Global: "+str(self.globalVal)+"  "+\
               "ConnectionType: "+str(self.connectionType)+"  "+\
               "ConnectionSpeed: "+str(self.connectionSpeed)+"  "+\
               "DeviceType: "+str(self.deviceType)
    def singleLineToStrOnlyValues(self):
        return str(self.activeVal)+"  "+\
               str(self.reflectiveVal)+"  "+\
               str(self.sensingVal)+"  "+\
               str(self.intuitiveVal)+"  "+\
               str(self.visualVal)+"  "+\
               str(self.verbalVal)+"  "+\
               str(self.sequentialVal)+"  "+\
               str(self.globalVal)+"  "+\
               str(self.connectionType)+"  "+\
               str(self.connectionSpeed)+"  "+\
               str(self.deviceType)
'''
The FSLSM subdivides the affinity of users into further 3 categories: Balanced, Moderate Preference and Strong Preference
According to the ILS (the oficial FSLSM test created by Felder and Soloman), a score of 1 or 3 in 11 is Balanced, 5 or 7 in 11 is Moderate and 9 or 11 in 11 is Strong
To generate the base, the total amount is divided into target groups, with each target group focusing on having a representation of a dimension.
If we were to create groups for each possible scenario:
5 possibilites per axis (1 balanced, 2 moderate per side, 2 strong per side)
4 different axis
Total: 5*5*5*5 -> 5^4 -> 625 possibilities

For the list that keeps track of the groups we have the following convention
Each axis of the FSLSM has an identifier: active/reflective =0, sensing/intuitive =1, visual/verbal =2, sequential/global =3
The list is constructed following this order: balanced Axis 4 + all permutations following this order; once one is completed, go for moderate right, moderate left, strong right, strong left
One of each possibility is build; once all 625 are done, restart. The building stops when the target amount is achieved
A value from 1 or 3(or -1 or 3) is randomly created for a balanced amount (note a -1 or -3 and a 1 or 3 is considered balanced by the ILS. In this case we simply decide randomly the sign); same idea for moderate and strong, with a moderate being (1 or 3) +4 and a strong (1 or 3) + 8

Beyond that, we also have another 3 values to consider: connectionType (0 for physical or 1 for mobile), connectionSpeed (no limit, but we can divide it in 5 groups acoding to the ANATEL[brazilian national agency of telecomunications] 2018 report: 1.3% in 0~512kbps, 15.1% in 0.512~2Mbps,26.0% in 12~34Mbps, 26.1% in >34Mbps and 31.5% in 2~12Mbps) and connection type (cable = 0 and mobile =1; in Brazil, approxim); on mobile we have different speeds! The availble report by ANATEL gives 4G with ~125.000 recorded accesses, 3G with ~60.000 accesses and 2G with ~25.000 accesses
This gives around 210.000 accesses: we can estimate that 4G has ~59.52% ,3G has ~28.57% of usage and 2G has ~11.90%

That brings the total of unique entries to: 625*5(cable speed)*2(device type)*2(connection type) = 12500
To make it simpler, no consideration to the distribution of speed types were taken; also we can consider 2G to be ~64kbps (group 1), 3G to be ~144kbps to 2Mbps(mostly group 2) and 4G to be ~100Mbps ~ 1Gbps (group4), and since we are not considering the distribution percentages, the difference into connection type speed does not mater
'''
#Auxiliary functions
def createUserTuple(axis0,axis1,axis2,axis3,speed,type,device):
    return (axis0,axis1,axis2,axis3,speed,type,device)
    
def createUser(axisTuple,connectionSpeed,connectionType,deviceType):
    activeVal = 0
    reflectiveVal = 0
    sensingVal = 0
    intuitiveVal = 0
    visualVal = 0
    verbalVal = 0
    sequentialVal = 0
    globalVal = 0

    axi0 = axisTuple[0]/11
    axi1 = axisTuple[1]/11
    axi2 = axisTuple[2]/11
    axi3 = axisTuple[3]/11
    # if(axi0 > 0):
        
    # return User(activeVal = axisTuple[0]
    pass
    
def generateILSValue(intensity,side):
    seq = (1,3)
    sign = side
    if(intensity == BALANCED):
        sign = rng.choice((-1,1))
    return (rng.choice(seq)+intensity)*sign

def generateBazilianSpeedValue(group):
    #The values are in kbps
    groups =((64,512),
            (513,2048),
            (2049,12000),
            (12001,34000),
            (34000,500000))
    return rng.randint(groups[group][0],groups[group][1])

order = ((BALANCED,RIGHT),
         (MODERATE,RIGHT),
         (MODERATE,LEFT),
         (STRONG,RIGHT),
         (STRONG,LEFT))
axisSpot = [0,0,0,0]
connectionDeviceSpot = [0,0,0]#[speed,connection type, device type]
users = []
fullLoop = 0
file = open(path,"w").close()
file = open(path,"a")

print("Seed: "+str(seed))
print("Path: "+str(path))
print("Amount: "+str(amount))

for n in range(amount):
    user = createUserTuple(generateILSValue(order[axisSpot[0]][0],order[axisSpot[0]][1]),
                      generateILSValue(order[axisSpot[1]][0],order[axisSpot[1]][1]),
                      generateILSValue(order[axisSpot[2]][0],order[axisSpot[2]][1]),
                      generateILSValue(order[axisSpot[3]][0],order[axisSpot[3]][1]),
                      generateBazilianSpeedValue(connectionDeviceSpot[0]),
                      (connectionDeviceSpot[1]),
                      (connectionDeviceSpot[2]))
    currentAxis = str(axisSpot)+str(connectionDeviceSpot)
    axisSpot[0] = (axisSpot[0]+1)%5
    if(axisSpot[0] == 0):
        axisSpot[1] = (axisSpot[1]+1)%5
        if(axisSpot[1] == 0):
            axisSpot[2] = (axisSpot[2]+1)%5
            if(axisSpot[2] == 0):
                axisSpot[3] = (axisSpot[3]+1)%5
                if(axisSpot[3] == 0):
                    connectionDeviceSpot[0] = (connectionDeviceSpot[0]+1)%5
                    if(connectionDeviceSpot[0] == 0):
                        connectionDeviceSpot[1] = (connectionDeviceSpot[1]+1)%2
                        if(connectionDeviceSpot[1] == 0):
                            connectionDeviceSpot[2] = (connectionDeviceSpot[2]+1)%2
                            if(connectionDeviceSpot[2] == 0):
                                fullLoop +=1
                    
    if(verbose):               
        print(str(n+1)+" "+currentAxis+":"+str(user))
    # file.write(str(n+1)+" "+currentAxis+":"+str(user)+"\n")
    precision = 4
    activeVal     = round(0.5+ user[0]/22, precision)
    reflectiveVal = round(0.5- user[0]/22, precision)
    sensingVal    = round(0.5+ user[1]/22, precision)
    intuitiveVal  = round(0.5- user[1]/22, precision)
    visualVal     = round(0.5+ user[2]/22, precision)
    verbalVal     = round(0.5- user[2]/22, precision)
    sequentialVal = round(0.5+ user[3]/22, precision)
    globalVal     = round(0.5- user[3]/22, precision)
    
    final = User(activeVal,reflectiveVal, sensingVal, intuitiveVal, visualVal, verbalVal, sequentialVal, globalVal,user[4], user[5], user[6])
    file.write(final.singleLineToStrOnlyValues()+"\n")
    
file.close()
runningTime =  time.time() - runningTime
print("Total de Loops: "+str(fullLoop))
print("Tempo Gasto: ~"+str("{0:.2f}".format(runningTime))+"s")