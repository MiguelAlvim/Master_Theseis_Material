import neuralNetwork2 as nn2
import stuff_for_neural_and_ls as aux
import operator
import re
from enum import IntEnum

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

def runNetworkandGetClassification(object):
    result={aux.axis[0]:'not_applicable',
            aux.axis[1]:'not_applicable',
            aux.axis[2]:'not_applicable',
            aux.axis[3]:'not_applicable',
            aux.axis[4]:'not_applicable',
            aux.axis[5]:'not_applicable',
            aux.axis[6]:'not_applicable',
            aux.axis[7]:'not_applicable'}
    for currentAxis in aux.axis:
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
        
        # print("F1")
        #Generating InputLayer - due to how the layers are linked, we need to create the input layer completely first
        while(line and counter<input_size):
            m = re.search(r"^([a-zA-Z]+)",line)
            if(m):
                # print(m.groups()[0])
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
        # print("\nF2")
        while(line):
            entry_node_name = network["inputLayer"][currentInput].name
            # print(entry_node_name)
            m = re.search(r"(sy"+entry_node_name+r"h.: )(-*\d+\.\d+)",line)
            if(m):
                # print(m.groups()[1])
                value = float(m.groups()[1])
                network["inputLayer"][currentInput].synapsesLeaving[counter].value = value
                counter += 1
            if(counter == hidden_size):
                counter = 0
                currentInput += 1
                # print()
            if(currentInput == input_size):#end of output
                break
            line = f.readline()
            
        nn2.generateNextLayer(network["hiddenLayer"],network["outputLayer"],1,nn2.binary,(1/5),(1/5))
        network["outputLayer"][0].name = "OUTPUT"
        
        # print("\nF3")
        counter = 0
        while(line):
            m = re.search(r"(h\d+:.*\| bias: )(-*\d+\.\d+)",line)
            if(m):
                # print(m.groups()[1])
                network["hiddenLayer"][counter].bias = float(m.groups()[1])
                counter += 1
            
            if(counter == hidden_size):
                break
            line = f.readline()
            
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
  
def printResultsFromClassification(object):
    for key,value in zip(object,object.values()):
        print(str(key)+": "+str(value))
 
def getValueFromClassification(object):
    result = []
    for key,value in zip(object,object.values()):
        if value == 'strong':
            result.append(2)
        elif value == 'moderate':
            result.append(1)            
        elif value == 'weak':
            result.append(0.5)
        else:
            result.append(0)
    return result
    
def recommend(user,object):
    score = 0
    for characteristic,i in zip(user.values(),range(len(object))):
        score += characteristic[0]*object[i]
    
    return score
    
def groupSameValue(object):
    result = {}
    for stuff in object:
        if stuff[1] in result:
            result[stuff[1]].append(stuff[0])
        else:
            result[stuff[1]] = []
            result[stuff[1]].append(stuff[0])
    return result
 
students = aux.readLsDatabase("marcelo_students.txt",0)
syntLO = aux.readLoDatabase("affsyno1.txt")
realLO = aux.readLoDatabase("affmarcelo300.txt")  
  
networks = dict()
for intensity in aux.intensities:
    networks[intensity] = dict()
    for axi in aux.axis:
        networks[intensity][axi] = dict()

networkPath = "neural_results_syn/"

readNeuralNetworkFile(networkPath+"active_strong.txt",networks["STRONG"]["ACTIVE"],8,6)
readNeuralNetworkFile(networkPath+"active_moderate.txt",networks["MODERATE"]["ACTIVE"],8,6)
readNeuralNetworkFile(networkPath+"active_weak.txt",networks["WEAK"]["ACTIVE"],8,6)
readNeuralNetworkFile(networkPath+"active_not_indicated.txt",networks["NOT_INDICATED"]["ACTIVE"],8,6)

readNeuralNetworkFile(networkPath+"reflective_strong.txt",networks["STRONG"]["REFLECTIVE"],8,6)
readNeuralNetworkFile(networkPath+"reflective_moderate.txt",networks["MODERATE"]["REFLECTIVE"],8,6)
readNeuralNetworkFile(networkPath+"reflective_weak.txt",networks["WEAK"]["REFLECTIVE"],8,6)
readNeuralNetworkFile(networkPath+"reflective_not_indicated.txt",networks["NOT_INDICATED"]["REFLECTIVE"],8,6)

readNeuralNetworkFile(networkPath+"sensing_strong.txt",networks["STRONG"]["SENSING"],8,6)
readNeuralNetworkFile(networkPath+"sensing_moderate.txt",networks["MODERATE"]["SENSING"],8,6)
readNeuralNetworkFile(networkPath+"sensing_weak.txt",networks["WEAK"]["SENSING"],8,6)
readNeuralNetworkFile(networkPath+"sensing_not_indicated.txt",networks["NOT_INDICATED"]["SENSING"],8,6)

readNeuralNetworkFile(networkPath+"intuitive_strong.txt",networks["STRONG"]["INTUITIVE"],8,6)
readNeuralNetworkFile(networkPath+"intuitive_moderate.txt",networks["MODERATE"]["INTUITIVE"],8,6)
readNeuralNetworkFile(networkPath+"intuitive_weak.txt",networks["WEAK"]["INTUITIVE"],8,6)
readNeuralNetworkFile(networkPath+"intuitive_not_indicated.txt",networks["NOT_INDICATED"]["INTUITIVE"],8,6)

readNeuralNetworkFile(networkPath+"visual_strong.txt",networks["STRONG"]["VISUAL"],8,6)
readNeuralNetworkFile(networkPath+"visual_moderate.txt",networks["MODERATE"]["VISUAL"],8,6)
readNeuralNetworkFile(networkPath+"visual_weak.txt",networks["WEAK"]["VISUAL"],8,6)
readNeuralNetworkFile(networkPath+"visual_not_indicated.txt",networks["NOT_INDICATED"]["VISUAL"],8,6)

readNeuralNetworkFile(networkPath+"verbal_strong.txt",networks["STRONG"]["VERBAL"],8,6)
readNeuralNetworkFile(networkPath+"verbal_moderate.txt",networks["MODERATE"]["VERBAL"],8,6)
readNeuralNetworkFile(networkPath+"verbal_weak.txt",networks["WEAK"]["VERBAL"],8,6)
readNeuralNetworkFile(networkPath+"verbal_not_indicated.txt",networks["NOT_INDICATED"]["VERBAL"],8,6)

readNeuralNetworkFile(networkPath+"sequential_strong.txt",networks["STRONG"]["SEQUENTIAL"],8,6)
readNeuralNetworkFile(networkPath+"sequential_moderate.txt",networks["MODERATE"]["SEQUENTIAL"],8,6)
readNeuralNetworkFile(networkPath+"sequential_weak.txt",networks["WEAK"]["SEQUENTIAL"],8,6)
readNeuralNetworkFile(networkPath+"sequential_not_indicated.txt",networks["NOT_INDICATED"]["SEQUENTIAL"],8,6)

readNeuralNetworkFile(networkPath+"global_strong.txt",networks["STRONG"]["GLOBAL"],8,6)
readNeuralNetworkFile(networkPath+"global_moderate.txt",networks["MODERATE"]["GLOBAL"],8,6)
readNeuralNetworkFile(networkPath+"global_weak.txt",networks["WEAK"]["GLOBAL"],8,6)
readNeuralNetworkFile(networkPath+"global_not_indicated.txt",networks["NOT_INDICATED"]["GLOBAL"],8,6)

users = (26,48)
for u in users:
    objects = []
    for object,i in zip(syntLO,range(len(syntLO))):
        obj = runNetworkandGetClassification(object)
        rec = getValueFromClassification(obj)
        res = recommend(students[u],rec)
        # printResultsFromClassification(obj)
        objects.append((i,res))
        
        # print(object["NAME"])
        # print(rec)
        # print(res)
        # print()

    objects = sorted(objects,key = operator.itemgetter(1),reverse = True)
    re = groupSameValue(objects)
    # for stuff in objects:
        # print(stuff)
    print("User: "+str(u))
    for key,value in zip(re,re.values()):
        print(str(key)+": "+str(value))
        
    print()
    

