import random as rng
import numpy  as np
import pdb

VERBOSE = False

def identity(x):
    return x
    
def identityDerivate(x):
    return 1

def binary(x):
    if x>=0:
        return 1
    return -1
    
def sigmoid(x):
    return 1/ (1+np.exp(-x))
    
def sigmoidDerivation(x):
    return x * (1 - x)
        
class Neurode:
    def __init__(self, name,value=0,bias=0,activation=identity):
        self.name = name
        self.value = value
        self.activation = activation
        self.activationDerivate = identityDerivate
        self.bias = bias
        self.synapsesIncoming = []
        self.synapsesLeaving = []
        
    def __str__(self):
        return self.name+": "+str(self.value) +" | bias: "+str(self.bias) +" | act. func.: "+self.activation.__name__
        
    def addSynapse(self,neurode,wheightUperLimit = 1.0,wheightLowerLimit=0.0):
        if(neurode != None):
            synapse = Synapse(rng.uniform(wheightLowerLimit,wheightUperLimit),self,neurode)
            self.synapsesLeaving.append(synapse)
            neurode.synapsesIncoming.append(synapse)
           
class Synapse:
    def __init__(self,value,fromNeurode,toNeurode):
        self.name = "sy"+fromNeurode.name+toNeurode.name
        self.value = value
        self.fromNeurode = fromNeurode
        self.toNeurode = toNeurode
    def __str__(self):
        return self.name+": "+str(self.value)+" ["+self.fromNeurode.name+" -> "+self.toNeurode.name+"]"
        
#get's all the values from it's incoming synapses multiplied by their wheights
#adds the bias to the result
#runs it's activation function and set's it's value as the activation result
def activateNeurode(neurode):        
    sum = 0
    for node in neurode.synapsesIncoming:
        sum += node.fromNeurode.value*node.value
    sum += neurode.bias
    neurode.value = neurode.activation(sum)
    return sum

def _getNextLayer(node):
    nextLayer = []
    for synapse in node.synapsesLeaving:
        nextLayer.append(synapse.toNeurode)
    return nextLayer
    
def _getPriorLayer(node):
    nextLayer = []
    for synapse in node.synapsesIncoming:
        nextLayer.append(synapse.fromNeurode)
    return nextLayer
    
def runNetwork(inputList):
    #getting the 1st layer from the input
    currentNodes = _getNextLayer(inputList[0])
    while len(currentNodes)>0:
        for neurode in currentNodes: 
            neurode.value = 0
            activateNeurode(neurode)
        currentNodes = _getNextLayer(currentNodes[0])

def calculateErrorAndUpdateWheight_AdalineLSM(output_neurode,target,learning_rate,decision_function,decision_parameters = [0]):
    if(decision_function(output_neurode.value,decision_parameters)==target):
        if VERBOSE:
            print("Target hit")
            print("Class: "+str(decision_function(output_neurode.value,decision_parameters)))
        return True
    else:
        for synapse in output_neurode.synapsesIncoming:
                inputValue = synapse.fromNeurode.value
                oldWheight = synapse.value
                newWheight = oldWheight + learning_rate*(target - output_neurode.value)*inputValue
                print("Adjusting wheight: "+str(oldWheight)+"+ "+str(learning_rate)+"*("+str(target)+" - "+str(output_neurode.value)+")*"+str(inputValue))
                synapse.value = newWheight
                print("Wheight Changed: "+str(oldWheight)+" -> "+str(synapse.value))
                print("Difference: "+str(oldWheight - target))
                
                #bias
                output_neurode.bias += learning_rate*(target - output_neurode.value)
        return False

def calculateErrorAndUpdateWheight_AdalineLMS(output_neurode,target,learning_rate,decision_function,decision_parameters = [0]):
    if(decision_function(output_neurode.value,decision_parameters)==target):
        if VERBOSE:
            print("Target hit")
            print("Class: "+str(decision_function(output_neurode.value,decision_parameters)))
        return True
    else:
        for synapse in output_neurode.synapsesIncoming:
                inputValue = synapse.fromNeurode.value
                oldWheight = synapse.value
                newWheight = oldWheight + 2*learning_rate*((target - output_neurode.value)*(target - output_neurode.value))*inputValue
                print("Adjusting wheight: "+str(oldWheight)+"+ "+str(learning_rate)+"*("+str(target)+" - "+str(output_neurode.value)+")*"+str(inputValue))
                synapse.value = newWheight
                print("Wheight Changed: "+str(oldWheight)+" -> "+str(synapse.value))
                print("Difference: "+str(oldWheight - target))
                
                #bias
                output_neurode.bias += learning_rate*(target - output_neurode.value)
        return False

def calculateErrorAndUpdateWheight_MadalineR1_OR(output_neurode,target,learning_rate):
    outputVal = output_neurode.value
    if(outputVal==target):    
        if VERBOSE:
            print("Target hit")
            print("Class: "+str(output_neurode.value))
        return True
    else:
        nextLayerList = []
        if(target == -1):#Update all neurodes with positive input
            if VERBOSE:        
                print("Expected -1, got 1. Updating all Positive output neurodes")
        else:        
            if VERBOSE:
                print("Expected 1, got -1. Updating the node closest to 1")
            
        for synapse in output_neurode.synapsesIncoming:
            if(target == -1):#Update all neurodes with positive input     
                if(synapse.fromNeurode.value >= 0):#If the output is positive, update wheight
                    if(synapse.fromNeurode not in nextLayerList):
                        # print("Neurode "+synapse.fromNeurode.name+" added")
                        nextLayerList.append(synapse.fromNeurode)
            else:#Update the one closest to 1
                if(len(nextLayerList)==0):
                    nextLayerList.append(synapse.fromNeurode)
                else:
                    if(activateNeurode(nextLayerList[0]) < activateNeurode(synapse.fromNeurode)):
                        nextLayerList.clear()
                        nextLayerList.append(synapse.fromNeurode)
        if(target == 1):
            if VERBOSE:
                print("Updating: "+nextLayerList[0].name)
        
        for neurode in nextLayerList:
            for synapse in neurode.synapsesIncoming:
                #synapse wheight update
                synapse.value += learning_rate*(target - activateNeurode(neurode))*synapse.fromNeurode.value
                
                #neurode bias update
                neurode.bias += learning_rate*(target - activateNeurode(neurode))
        return False
       
def generateNextLayer(currentLayer,nextLayer,nextLayerSize,activationFunction,wheightLowerLimit,wheightUperLimit):
    for n in range(nextLayerSize):
        nextLayer.append(Neurode("h"+str(n),0,bias=1,activation=activationFunction))
    for i in range(len(currentLayer)):    
        for j in range(nextLayerSize):
            currentLayer[i].addSynapse(nextLayer[j],wheightUperLimit=wheightUperLimit,wheightLowerLimit=wheightLowerLimit)

        
        
        
        
        
        
        
