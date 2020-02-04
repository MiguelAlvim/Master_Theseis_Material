import neuralNetwork2 as nn2
import sys
import re
from enum import IntEnum

axis=["ACTIVE","REFLECTIVE","SENSING","INTUITIVE","VISUAL","VERBAL","SEQUENTIAL","GLOBAL"]
intensities=["STRONG","MODERATE","WEAK","NOT_INDICATED"]

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

class CLASSIFICATION(IntEnum):
    STRONG = 0,
    MODERATE = 1,
    WEAK = 2,
    NOT_INDICATED = 3
    
def readLsDatabase(file_path,metric=1):#metric 0 = ILS,1 = MINE
    students = []
    i = -1
    expression = r"(\d\.\d+)  (\d\.\d+)  (\d\.\d+)  (\d\.\d+)  (\d\.\d+)  (\d\.\d+)  (\d\.\d+)  (\d\.\d+)"
    with open(file_path,'r') as file:
        line = file.readline()
        while(line):     
            m = re.search(expression,line)
            if(m):
                students.append(dict())
                i+=1
                
                # students[i]["ACTIVE"]     = float(m.groups()[0])
                # students[i]["REFLECTIVE"] = float(m.groups()[1])
                # students[i]["SENSING"]    = float(m.groups()[2])
                # students[i]["INTUITIVE"]  = float(m.groups()[3])
                # students[i]["VISUAL"]     = float(m.groups()[4])
                # students[i]["VERBAL"]     = float(m.groups()[5])
                # students[i]["SEQUENTIAL"] = float(m.groups()[6])
                # students[i]["GLOBAL"]     = float(m.groups()[7])
                if metric == 1:
                    for axi,j in zip(axis,range(len(axis))):
                        students[i][axi] = []
                        students[i][axi].append(float(m.groups()[j]))
                        if(float(m.groups()[j])>=0.7):
                            students[i][axi].append(CLASSIFICATION.STRONG)
                        elif(float(m.groups()[j])>=0.5):
                            students[i][axi].append(CLASSIFICATION.MODERATE)
                        elif(float(m.groups()[j])>=0.25):
                            students[i][axi].append(CLASSIFICATION.WEAK)
                        else:
                            students[i][axi].append(CLASSIFICATION.NOT_INDICATED)
                elif metric == 0:
                    for axi,j in zip(axis,range(len(axis))):
                        students[i][axi] = []
                        students[i][axi].append(float(m.groups()[j]))
                        if(float(m.groups()[j])>=9.5/11):
                            students[i][axi].append(CLASSIFICATION.STRONG)
                        elif(float(m.groups()[j])>=7.5/11):
                            students[i][axi].append(CLASSIFICATION.MODERATE)
                        else:
                            students[i][axi].append(CLASSIFICATION.WEAK)
                    
                
    
                # User(activeVal,reflectiveVal, sensingVal, intuitiveVal, visualVal, verbalVal, sequentialVal, globalVal,0,0,0)
    
            line = file.readline()
    return students
    
def readLoDatabase(file_path):
    learningObjectBase = []
    currentLO = -1
    with open(file_path,'r') as file:
        line = file.readline()
        while(line):     
            m = re.search('(\[.*\])',line)
            if(m):#New LO found
                ++currentLO
                learningObjectBase.append(dict())
                learningObjectBase[currentLO]['NAME'] = m.groups()[0]
                line = file.readline()
                continue
                
            m = re.search('(SIZE\: )(.*)',line)
            if(m):#Size found
                learningObjectBase[currentLO]['SIZE'] = int(m.groups()[1])
                line = file.readline()
                continue
                
            m = re.search('(VIDEO_RATE\: )(.*)',line)
            if(m):#VIDEO_RATE found
                learningObjectBase[currentLO]['VIDEO_RATE'] = int(m.groups()[1])
                line = file.readline()
                continue
                
            m = re.search('(AUDIO_RATE\: )(.*)',line)
            if(m):#AUDIO_RATE found
                learningObjectBase[currentLO]['AUDIO_RATE'] = int(m.groups()[1])
                line = file.readline()
                continue
                
            m = re.search('(ACTIVE\: )(.*)',line)
            if(m):#ACTIVE found
                learningObjectBase[currentLO]['ACTIVE'] = []
                learningObjectBase[currentLO]['ACTIVE'].append(float(m.groups()[1]))
                if(float(m.groups()[1])>=0.7):
                    learningObjectBase[currentLO]['ACTIVE'].append(CLASSIFICATION.STRONG)
                elif(float(m.groups()[1])>=0.5):
                    learningObjectBase[currentLO]['ACTIVE'].append(CLASSIFICATION.MODERATE)
                elif(float(m.groups()[1])>=0.25):
                    learningObjectBase[currentLO]['ACTIVE'].append(CLASSIFICATION.WEAK)
                else:
                    learningObjectBase[currentLO]['ACTIVE'].append(CLASSIFICATION.NOT_INDICATED)
                    
                line = file.readline()
                continue
                
            m = re.search('(REFLECTIVE\: )(.*)',line)
            if(m):#REFLECTIVE found
                learningObjectBase[currentLO]['REFLECTIVE'] = []
                learningObjectBase[currentLO]['REFLECTIVE'].append(float(m.groups()[1]))
                if(float(m.groups()[1])>=0.7):
                    learningObjectBase[currentLO]['REFLECTIVE'].append(CLASSIFICATION.STRONG)
                elif(float(m.groups()[1])>=0.5):
                    learningObjectBase[currentLO]['REFLECTIVE'].append(CLASSIFICATION.MODERATE)
                elif(float(m.groups()[1])>=0.25):
                    learningObjectBase[currentLO]['REFLECTIVE'].append(CLASSIFICATION.WEAK)
                else:
                    learningObjectBase[currentLO]['REFLECTIVE'].append(CLASSIFICATION.NOT_INDICATED)
                    
                line = file.readline()
                continue
                
            m = re.search('(SENSING\: )(.*)',line)
            if(m):#SENSING found
                learningObjectBase[currentLO]['SENSING'] = []
                learningObjectBase[currentLO]['SENSING'].append(float(m.groups()[1]))
                if(float(m.groups()[1])>=0.7):
                    learningObjectBase[currentLO]['SENSING'].append(CLASSIFICATION.STRONG)
                elif(float(m.groups()[1])>=0.5):
                    learningObjectBase[currentLO]['SENSING'].append(CLASSIFICATION.MODERATE)
                elif(float(m.groups()[1])>=0.25):
                    learningObjectBase[currentLO]['SENSING'].append(CLASSIFICATION.WEAK)
                else:
                    learningObjectBase[currentLO]['SENSING'].append(CLASSIFICATION.NOT_INDICATED)
                    
                line = file.readline()
                continue
                
            m = re.search('(INTUITIVE\: )(.*)',line)
            if(m):#INTUITIVE found
                learningObjectBase[currentLO]['INTUITIVE'] = []
                learningObjectBase[currentLO]['INTUITIVE'].append(float(m.groups()[1]))
                if(float(m.groups()[1])>=0.7):
                    learningObjectBase[currentLO]['INTUITIVE'].append(CLASSIFICATION.STRONG)
                elif(float(m.groups()[1])>=0.5):
                    learningObjectBase[currentLO]['INTUITIVE'].append(CLASSIFICATION.MODERATE)
                elif(float(m.groups()[1])>=0.25):
                    learningObjectBase[currentLO]['INTUITIVE'].append(CLASSIFICATION.WEAK)
                else:
                    learningObjectBase[currentLO]['INTUITIVE'].append(CLASSIFICATION.NOT_INDICATED)
                    
                line = file.readline()
                continue
                
            m = re.search('(VISUAL\: )(.*)',line)
            if(m):#VISUAL found
                learningObjectBase[currentLO]['VISUAL'] = []
                learningObjectBase[currentLO]['VISUAL'].append(float(m.groups()[1]))
                if(float(m.groups()[1])>=0.7):
                    learningObjectBase[currentLO]['VISUAL'].append(CLASSIFICATION.STRONG)
                elif(float(m.groups()[1])>=0.5):
                    learningObjectBase[currentLO]['VISUAL'].append(CLASSIFICATION.MODERATE)
                elif(float(m.groups()[1])>=0.25):
                    learningObjectBase[currentLO]['VISUAL'].append(CLASSIFICATION.WEAK)
                else:
                    learningObjectBase[currentLO]['VISUAL'].append(CLASSIFICATION.NOT_INDICATED)
                    
                line = file.readline()
                continue
                
            m = re.search('(VERBAL\: )(.*)',line)
            if(m):#VERBAL found
                learningObjectBase[currentLO]['VERBAL'] = []
                learningObjectBase[currentLO]['VERBAL'].append(float(m.groups()[1]))
                if(float(m.groups()[1])>=0.7):
                    learningObjectBase[currentLO]['VERBAL'].append(CLASSIFICATION.STRONG)
                elif(float(m.groups()[1])>=0.5):
                    learningObjectBase[currentLO]['VERBAL'].append(CLASSIFICATION.MODERATE)
                elif(float(m.groups()[1])>=0.25):
                    learningObjectBase[currentLO]['VERBAL'].append(CLASSIFICATION.WEAK)
                else:
                    learningObjectBase[currentLO]['VERBAL'].append(CLASSIFICATION.NOT_INDICATED)
                    
                line = file.readline()
                continue
                
            m = re.search('(SEQUENTIAL\: )(.*)',line)
            if(m):#SEQUENTIAL found
                learningObjectBase[currentLO]['SEQUENTIAL'] = []
                learningObjectBase[currentLO]['SEQUENTIAL'].append(float(m.groups()[1]))
                if(float(m.groups()[1])>=0.7):
                    learningObjectBase[currentLO]['SEQUENTIAL'].append(CLASSIFICATION.STRONG)
                elif(float(m.groups()[1])>=0.5):
                    learningObjectBase[currentLO]['SEQUENTIAL'].append(CLASSIFICATION.MODERATE)
                elif(float(m.groups()[1])>=0.25):
                    learningObjectBase[currentLO]['SEQUENTIAL'].append(CLASSIFICATION.WEAK)
                else:
                    learningObjectBase[currentLO]['SEQUENTIAL'].append(CLASSIFICATION.NOT_INDICATED)
                    
                line = file.readline()
                continue
                
            m = re.search('(GLOBAL\: )(.*)',line)
            if(m):#GLOBAL found
                learningObjectBase[currentLO]['GLOBAL'] = []
                learningObjectBase[currentLO]['GLOBAL'].append(float(m.groups()[1]))
                if(float(m.groups()[1])>=0.7):
                    learningObjectBase[currentLO]['GLOBAL'].append(CLASSIFICATION.STRONG)
                elif(float(m.groups()[1])>=0.5):
                    learningObjectBase[currentLO]['GLOBAL'].append(CLASSIFICATION.MODERATE)
                elif(float(m.groups()[1])>=0.25):
                    learningObjectBase[currentLO]['GLOBAL'].append(CLASSIFICATION.WEAK)
                else:
                    learningObjectBase[currentLO]['GLOBAL'].append(CLASSIFICATION.NOT_INDICATED)
                    
                line = file.readline()
                continue
            line = file.readline()
    return learningObjectBase
    
def readNeuralNetworkFile(file,network,input_size,hidden_size):
    with open(file,'r') as f:
        #1st line is always 'Hits: xx.xx%', second is always 'Iteration: xxx'. So we start from the 3rd
        line = f.readline();
        m = re.search("(Hits: )(\d+\.\d+)",line)
        f.readline()
        line = f.readline()
        counter = 0
        entry_node_name = None
        network["inputLayer"] = []
        network["hiddenLayer"] = []
        network["outputLayer"] = []
        network["hit"] = float(m.groups()[1])
        
        #Generating InputLayer - due to how the layers are linked, we need to create the input layer completely first
        while(line and counter<input_size):
            m = re.search(r"^([a-zA-Z]+)",line)
            if(m):
                entry_node_name = m.groups()[0]
                network["inputLayer"].append(nn2.Neurode(entry_node_name,0,bias=1,activation=nn2.binary))
                counter += 1
            line = f.readline()
        
        nn2.generateNextLayer(network["inputLayer"],network["hiddenLayer"],hidden_size,nn2.binary,0,0.3)
        
        f.seek(0)
        counter = 0
        currentInput = 0
        f.readline();f.readline()
        line = f.readline()
        while(line):
            entry_node_name = network["inputLayer"][currentInput].name
            m = re.search(r"(sy"+entry_node_name+r"h.: )(-*\d+\.\d+)",line)
            if(m):
                # print(m.groups()[1])
                value = float(m.groups()[1])
                network["inputLayer"][currentInput].synapsesLeaving[counter].value = value
                counter += 1
            if(counter == hidden_size):
                counter = 0
                currentInput += 1
            if(currentInput == input_size):#end of output
                break
            line = f.readline()
            
        nn2.generateNextLayer(network["hiddenLayer"],network["outputLayer"],1,nn2.binary,(1/5),(1/5))
        network["outputLayer"][0].name = "OUTPUT"
        
        counter = 0
        while(line):
            m = re.search(r"(h\d+:.*\| bias: )(-*\d+\.\d+)",line)
            if(m):
                network["hiddenLayer"][counter].bias = float(m.groups()[1])
                counter += 1
            
            if(counter == hidden_size):
                break
            line = f.readline()
            
def _setInput(network,object):
    network["inputLayer"][0].value = object['ACTIVE'][0]#0
    network["inputLayer"][1].value = object['REFLECTIVE'][0]#1
    network["inputLayer"][2].value = object['SENSING'][0]#2
    network["inputLayer"][3].value = object['INTUITIVE'][0]#3
    network["inputLayer"][4].value = object['VISUAL'][0]#4
    network["inputLayer"][5].value = object['VERBAL'][0]#5
    network["inputLayer"][6].value = object['SEQUENTIAL'][0]#6
    network["inputLayer"][7].value = object['GLOBAL'][0]#7
    
def _clearInput(network):
    network["inputLayer"][0].value = 0
    network["inputLayer"][1].value = 0
    network["inputLayer"][2].value = 0
    network["inputLayer"][3].value = 0
    network["inputLayer"][4].value = 0
    network["inputLayer"][5].value = 0
    network["inputLayer"][6].value = 0
    network["inputLayer"][7].value = 0
        
def runNetworkandGetClassification(object,networks):
    result={axis[0]:'not_applicable',
            axis[1]:'not_applicable',
            axis[2]:'not_applicable',
            axis[3]:'not_applicable',
            axis[4]:'not_applicable',
            axis[5]:'not_applicable',
            axis[6]:'not_applicable',
            axis[7]:'not_applicable'}
    for currentAxis in axis:
        #Testing for Strong
        _setInput(networks["STRONG"][currentAxis],object)        
        nn2.runNetwork(networks["STRONG"][currentAxis]["inputLayer"])
        if(networks["STRONG"][currentAxis]["outputLayer"][0].value==1):
            result[currentAxis] = 'strong'
            _clearInput(networks["STRONG"][currentAxis])
        else:
            #Testing for Moderate
            _setInput(networks["MODERATE"][currentAxis],object)        
            nn2.runNetwork(networks["MODERATE"][currentAxis]["inputLayer"])
            if(networks["MODERATE"][currentAxis]["outputLayer"][0].value==1):
                result[currentAxis] = 'moderate'
                _clearInput(networks["STRONG"][currentAxis])
            else:
                #Testing for Weak
                _setInput(networks["WEAK"][currentAxis],object)        
                nn2.runNetwork(networks["WEAK"][currentAxis]["inputLayer"])
                if(networks["WEAK"][currentAxis]["outputLayer"][0].value==1):
                    result[currentAxis] = 'weak'
                    _clearInput(networks["STRONG"][currentAxis])
                
    return result        

def printNetwork(network):
    for neurode in network["inputLayer"]:
        print(neurode)
        for synapse in neurode.synapsesLeaving:
            print("\t",end='')
            print(synapse)
    for neurode in network["hiddenLayer"]:
        print(neurode)
        for synapse in neurode.synapsesLeaving:
            print("\t",end='')
            print(synapse)
    for neurode in network["outputLayer"]:
        print(neurode)
        for synapse in neurode.synapsesLeaving:
            print("\t",end='')
            print(synapse)