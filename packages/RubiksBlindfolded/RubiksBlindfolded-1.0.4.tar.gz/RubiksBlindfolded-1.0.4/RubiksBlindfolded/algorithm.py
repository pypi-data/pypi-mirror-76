#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .edge import *
from .corner import *

solvedEdges = []
solvedCorners = []

cube = {}
edgeSequence = []
cornerSequence = []

edgePriority = {0:['U',1,'B',1],
                1:['U',3,'L',1],
                2:['U',7,'F',1],
                3:['B',5,'L',3],
                4:['L',5,'F',3],
                5:['F',5,'R',3],
                6:['R',5,'B',3],
                7:['D',1,'F',7],
                8:['D',3,'L',7],
                9:['D',5,'R',7],
                10:['D',7,'B',7]}
                
cornerPriority = {0:['U',2,'R',2,'B',0],
                    1:['U',6,'L',2,'F',0],
                    2:['U',8,'F',2,'R',0],
                    3:['D',0,'F',6,'L',8],
                    4:['D',2,'R',6,'F',8],
                    5:['D',6,'L',6,'B',8],
                    6:['D',8,'B',6,'R',8]}


def setCube(sides):
    global cube
    cube = sides
    
    
def displayCube():
    return cube
   
    
def updateEdgePriority(inputEdgePriority):
    global edgePriority
    for x in range(11):
        if x in inputEdgePriority.keys(): 
            edgePriority[x] = inputEdgePriority.get(x)
   
   
def displayEdgePriority():
    return edgePriority
    
    
def updateCornerPriority(inputCornerPriority):
    global cornerPriority
    for x in range(7):
        if x in inputCornerPriority.keys(): 
            cornerPriority[x] = inputCornerPriority.get(x)
    
    
def displayCornerPriority():
    return cornerPriority
    

def solveEdges():
    global cube
    global edgeSequence
    cube = cubeEdges.solveEdge(cube,edgePriority)
    edgeSequence = cubeEdges.getEdgeSequence()
    if (len(edgeSequence)>0):
        return edgeSequence
    else:
        return None


def solveCorners():
    global cube
    global cornerSequence
    cube = cubeCorners.solveCorner(cube,cornerPriority)
    cornerSequence = cubeCorners.getCornerSequence()
    if (len(cornerSequence)>0):
        return cornerSequence
    else:
        return None
 

def indexEdgeSequence():
    if (len(edgeSequence)>0):
        return cubeEdges.edgeIndex
    else:
        return None
        

def indexCornerSequence():
    if (len(cornerSequence)>0):
        return cubeCorners.cornerIndex
    else:
        return None
        

def currentEdgeBuffer():
    if (len(edgeSequence)>0):
        return cubeEdges.edgeColor
    else:
        return None


def currentCornerBuffer():
    if (len(cornerSequence)>0):
        return cubeCorners.cornerColor
    else:
        return None
        
        
def parityCheck():
    if (len(edgeSequence)>0 or len(cornerSequence)>0):
        if not(len(edgeSequence)%2==0) or not (len(cornerSequence)%2==0):
            parity = 1
            return parity
        else:
            parity = 0
            return parity
    else:
        return None
        

def parityAlgorithm():
    if not(len(cornerSequence)%2==0) or not (len(edgeSequence)%2==0):
        sidesCopy = cube.copy()
        edgeParity = [sidesCopy['U'][8], sidesCopy['R'][0], sidesCopy['F'][2],
                sidesCopy['U'][2], sidesCopy['B'][0], sidesCopy['R'][2]]
        cube['U'][2] = edgeParity[0]
        cube['B'][0] = edgeParity[1]
        cube['R'][2] = edgeParity[2] 
        
        cube['U'][8] = edgeParity[3]
        cube['R'][0] = edgeParity[4]
        cube['F'][2] = edgeParity[5]
        
        cornerParity = [sidesCopy['U'][3], sidesCopy['L'][1], sidesCopy['U'][1], sidesCopy['B'][1]]
        cube['U'][1] = cornerParity[0]
        cube['B'][1] = cornerParity[1]
        
        cube['U'][3] = cornerParity[2]
        cube['L'][1] = cornerParity[3]
    
    
def getSolvedEdges():
    value = [1,3,5,7]
    for x in range(4):
        if (cube['U'][value[x]]=='U'):
            if (x==0):
                if (cube['B'][1]=='B'):
                    solvedEdges.append(['U',1,'B',1])
            elif (x==1):
                if (cube['L'][1]=='L'):
                    solvedEdges.append(['U',3,'L',1])
            elif (x==2):
                if (cube['R'][1]=='R'):
                    solvedEdges.append(['U',5,'R',1])
            elif (x==3):
                if (cube['F'][1]=='F'):
                    solvedEdges.append(['U',7,'F',1])
        if (cube['F'][value[x]]=='F'):
            if (x==1):
                if (cube['L'][5]=='L'):
                    solvedEdges.append(['F',3,'L',5])
            elif (x==2):
                if (cube['R'][3]=='R'):
                    solvedEdges.append(['F',5,'R',3])
        if (cube['D'][value[x]]=='D'):
            if (x==0):
                if (cube['F'][7]=='F'):
                    solvedEdges.append(['D',1,'F',7])
            elif (x==1):
                if (cube['L'][7]=='L'):
                    solvedEdges.append(['D',3,'L',7])
            elif (x==2):
                if (cube['R'][7]=='R'):
                    solvedEdges.append(['D',5,'R',7])
            elif (x==3):
                if (cube['B'][7]=='B'):
                    solvedEdges.append(['D',7,'B',7])
        if (cube['B'][value[x]]=='B'):
            if (x==1):
                if (cube['R'][5]=='R'):
                    solvedEdges.append(['B',3,'R',5])
            elif (x==2):
                if (cube['L'][3]=='L'):
                    solvedEdges.append(['B',5,'L',3])
                    
    if (len(solvedEdges)>0):                 
        return solvedEdges                
    else:
        return None


def getSolvedCorners():
    value = [0,2,6,8]
    for x in range(4):
        if (cube['U'][value[x]]=='U'):
            if (x==0):
                if cube['L'][0]=='L':
                    if cube['B'][2]=='B':
                        solvedCorners.append(['U',0,'L',0,'B',2])
            elif (x==1):
                if cube['B'][0]=='B':
                    if cube['R'][2]=='R':
                        solvedCorners.append(['U',2,'B',0,'R',2])
            elif (x==2):
                if cube['L'][2]=='L':
                    if cube['F'][0]=='F':
                        solvedCorners.append(['U',6,'L',2,'F',0]) 
            elif (x==3):
                if cube['R'][0]=='R':
                    if cube['F'][2]=='F':
                        solvedCorners.append(['U',8,'R',0,'F',2]) 
        elif (cube['D'][value[x]]=='D'):
            if (x==0):
                if cube['L'][8]=='L':
                    if cube['F'][6]=='F':
                        solvedCorners.append(['D',0,'L',8,'F',6])
            elif (x==1):
                if cube['F'][8]=='F':
                    if cube['R'][6]=='R':
                        solvedCorners.append(['D',2,'F',8,'R',6])
            elif (x==2):
                if cube['L'][6]=='L':
                    if cube['B'][8]=='B':
                        solvedCorners.append(['D',6,'L',6,'B',8])
            elif (x==3):
                if cube['B'][6]=='B':
                    if cube['R'][8]=='R':
                        solvedCorners.append(['D',8,'B',6,'R',8])
                        
    if (len(solvedCorners)>0):                 
        return solvedCorners                
    else:
        return None
            
            
