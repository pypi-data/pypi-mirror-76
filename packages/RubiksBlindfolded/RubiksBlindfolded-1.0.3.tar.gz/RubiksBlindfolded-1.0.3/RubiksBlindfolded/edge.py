#!/usr/bin/env python3
# -*- coding: utf-8 -*-

buffer = []
edgeSequence = []

class Edge:

    edgeCount = 0
    edgeIndex = []
    edgeColor = []
    
    def solveEdge(self, sides, edgePriority):
        
        edgeGoal = (sides['U'][1]=='U' and sides['U'][3]=='U' and sides['U'][5]=='U' and sides['U'][7]=='U'
                and sides['F'][1]=='F' and sides['F'][3]=='F' and sides['F'][5]=='F' and sides['F'][7]=='F'
                and sides['R'][1]=='R' and sides['R'][3]=='R' and sides['R'][5]=='R' and sides['R'][7]=='R'
                and sides['D'][1]=='D' and sides['D'][3]=='D' and sides['D'][5]=='D' and sides['D'][7]=='D'
                and sides['B'][1]=='B' and sides['B'][3]=='B' and sides['B'][5]=='B' and sides['B'][7]=='B'
                and sides['L'][1]=='L' and sides['L'][3]=='L' and sides['L'][5]=='L' and sides['L'][7]=='L')

        if (edgeGoal):
            print('Edges are already solved!')
            
        else:
            
            if (sides['U'][5]=='U' and sides['R'][1]=='R') or (sides['U'][5]=='R' and sides['R'][1]=='U'):
                if (sides['U'][5]=='U' and sides['R'][1]=='R'):
                    self.edgeColor.append(['U','R'])
                else:
                    self.edgeColor.append(['R','U'])
                buffer = self.edgeBufferChange(sides,edgePriority)
                self.edgeCount = self.edgeCount + 1
                
            if not (sides['U'][5]=='U' and sides['R'][1]=='R') or (sides['U'][5]=='R' and sides['R'][1]=='U'):
                buffer = [sides['U'][5], sides['R'][1]]
                
                while(1):
                    edgeGoalbuffer =(sides['U'][1]=='U' and sides['U'][3]=='U' and sides['U'][7]=='U'
                                and sides['F'][1]=='F' and sides['F'][3]=='F' and sides['F'][5]=='F' and sides['F'][7]=='F'
                                and sides['R'][3]=='R' and sides['R'][5]=='R' and sides['R'][7]=='R'
                                and sides['D'][1]=='D' and sides['D'][3]=='D' and sides['D'][5]=='D' and sides['D'][7]=='D'
                                and sides['B'][1]=='B' and sides['B'][3]=='B' and sides['B'][5]=='B' and sides['B'][7]=='B'
                                and sides['L'][1]=='L' and sides['L'][3]=='L' and sides['L'][5]=='L' and sides['L'][7]=='L')
                    
                    if (edgeGoalbuffer):
                        sides['U'][5] = 'U'
                        sides['R'][1] = 'R'
                        
                        if not(self.edgeCount%2==0):
                            sidesCopy = sides.copy()
                            parity = [sidesCopy['U'][8], sidesCopy['R'][0], sidesCopy['F'][2],
                                    sidesCopy['U'][2], sidesCopy['B'][0], sidesCopy['R'][2]]
                            sides['U'][2] = parity[0]
                            sides['B'][0] = parity[1]
                            sides['R'][2] = parity[2]
                            
                            sides['U'][8] = parity[3]
                            sides['R'][0] = parity[4]
                            sides['F'][2] = parity[5]
                        
                        #print('Edges are solved!')
                        #print(sides)
                        
                        break
                    
                        
                    face = [buffer[0], buffer[1]]
                    
                    prevBuffer = buffer
                    if (sides['U'][5]=='U' and sides['R'][1]=='R') or (sides['U'][5]=='R' and sides['R'][1]=='U'):
                        
                        self.edgeColor.append(['R','U'])
                        buffer = self.edgeBufferChange(sides,edgePriority)
                        
                    else:
                        edgeSequence.append(buffer)
                        self.edgeColor.append(buffer)
                        
                        index = self.getEdgeIndex(buffer)
                        self.edgeIndex.append([buffer[0],index[0],buffer[1],index[1]])
                        
                        buffer = [sides[buffer[0]][index[0]],sides[buffer[1]][index[1]]] #update buffer
                        
                        sides[prevBuffer[0]][index[0]] = prevBuffer[0]
                        sides[prevBuffer[1]][index[1]] = prevBuffer[1]
                        
                        sides['U'][5] = buffer[0]
                        sides['R'][1] = buffer[1]
                        
                    
                    self.edgeCount = self.edgeCount + 1
                    
                    
        return sides
        
    
    def edgeBufferChange (self,sides,edgePriority):
        sidesCopy = sides.copy()
        a1 = ''
        a2 = 0
        b1 = ''
        b2 = 0
        
        if not (sides[edgePriority[0][0]][edgePriority[0][1]]=='U'
            and sides[edgePriority[0][2]][edgePriority[0][3]]=='B'):
            a1 = 'U'
            a2 = 1
            b1 = 'B'
            b2 = 1
            
            buffer = ['U','B']
            edgeSequence.append(buffer)
            
        elif not (sides[edgePriority[1][0]][edgePriority[1][1]]=='U'
            and sides[edgePriority[1][2]][edgePriority[1][3]]=='L'):
            a1 = 'U'
            a2 = 3
            b1 = 'L'
            b2 = 1
            
            buffer = ['U','L']
            edgeSequence.append(buffer)
        
        elif not (sides[edgePriority[2][0]][edgePriority[2][1]]=='U' 
            and sides[edgePriority[2][2]][edgePriority[2][3]]=='F'):
            a1 = 'U'
            a2 = 7
            b1 = 'F'
            b2 = 1
            
            buffer = ['U','F']
            edgeSequence.append(buffer)
            
        elif not (sides[edgePriority[3][0]][edgePriority[3][1]]=='B' 
            and sides[edgePriority[3][2]][edgePriority[3][3]]=='L'):
            a1 = 'B'
            a2 = 5
            b1 = 'L'
            b2 = 3
            
            buffer = ['B','L']
            edgeSequence.append(buffer)
            
        elif not (sides[edgePriority[4][0]][edgePriority[4][1]]=='L' 
            and sides[edgePriority[4][2]][edgePriority[4][3]]=='F'):
            a1 = 'L'
            a2 = 5
            b1 = 'F'
            b2 = 3
            
            buffer = ['L','F']
            edgeSequence.append(buffer)
        
        elif not (sides[edgePriority[5][0]][edgePriority[5][1]]=='F' 
            and sides[edgePriority[5][2]][edgePriority[5][3]]=='R'):
            a1 = 'F'
            a2 = 5
            b1 = 'R'
            b2 = 3
            
            buffer = ['F','R']
            edgeSequence.append(buffer)
            
        elif not (sides[edgePriority[6][0]][edgePriority[6][1]]=='R' 
            and sides[edgePriority[6][2]][edgePriority[6][3]]=='B'):
            a1 = 'R'
            a2 = 5
            b1 = 'B'
            b2 = 3
            
            buffer = ['R','B']
            edgeSequence.append(buffer)
        
        elif not (sides[edgePriority[7][0]][edgePriority[7][1]]=='D' 
            and sides[edgePriority[7][2]][edgePriority[7][3]]=='F'):
            a1 = 'D'
            a2 = 1
            b1 = 'F'
            b2 = 7
            
            buffer = ['D','F']
            edgeSequence.append(buffer)
        
        elif not (sides[edgePriority[8][0]][edgePriority[8][1]]=='D' 
            and sides[edgePriority[8][2]][edgePriority[8][3]]=='L'):
            a1 = 'D'
            a2 = 3
            b1 = 'L'
            b2 = 7
            
            buffer = ['D','L']
            edgeSequence.append(buffer)
        
        elif not (sides[edgePriority[9][0]][edgePriority[9][1]]=='D' 
            and sides[edgePriority[9][2]][edgePriority[9][3]]=='R'):
            a1 = 'D'
            a2 = 5
            b1 = 'R'
            b2 = 7
            
            buffer = ['D','R']
            edgeSequence.append(buffer)
            
        elif not (sides[edgePriority[10][0]][edgePriority[10][1]]=='D' 
            and sides[edgePriority[10][2]][edgePriority[10][3]]=='B'):
            a1 = 'D'
            a2 = 7
            b1 = 'B'
            b2 = 7
            
            buffer = ['D','B']
            edgeSequence.append(buffer)
        
        
        index = self.getEdgeIndex(buffer)
        self.edgeIndex.append([buffer[0],index[0],buffer[1],index[1]])
        
        swap = [sidesCopy['R'][1], sidesCopy['U'][5], sidesCopy[a1][a2], sidesCopy[b1][b2]]
        
        if (sides['U'][5]=='U' and sides['R'][1]=='R'):
            buffer = [sides[a1][a2],sides[b1][b2]]
            
            sides[b1][b2] = swap[0]
            sides[a1][a2] = swap[1]
            
            sides['U'][5] = swap[2]
            sides['R'][1] = swap[3]
            
        else:
            buffer = [sides[a1][a2],sides[b1][b2]]
            
            sides[b1][b2] = swap[0]
            sides[a1][a2] = swap[1]
            
            sides['U'][5] = swap[2]
            sides['R'][1] = swap[3]
            
        return buffer
    

    def getEdgeIndex(self,buffer):
        if buffer[0]=='U':
            if buffer[1]=='R':
                index = [5,1]
            elif buffer[1]=='F':
                index = [7,1]
            elif buffer[1]=='B':
                index = [1,1]
            elif buffer[1]=='L':
                index = [3,1]
        elif buffer[0]=='F':
            if buffer[1]=='U':
                index = [1,7]
            elif buffer[1]=='R':
                index = [5,3]
            elif buffer[1]=='D':
                index = [7,1]
            elif buffer[1]=='L':
                index = [3,5]
        elif buffer[0]=='R':
            if buffer[1]=='U':
                index = [1,5]
            elif buffer[1]=='F':
                index = [3,5]
            elif buffer[1]=='D':
                index = [7,5]
            elif buffer[1]=='B':
                index = [5,3]
        elif buffer[0]=='D':
            if buffer[1]=='F':
                index = [1,7]
            elif buffer[1]=='R':
                index = [5,7]
            elif buffer[1]=='B':
                index = [7,7]
            elif buffer[1]=='L':
                index = [3,7]
        elif buffer[0]=='B':
            if buffer[1]=='U':
                index = [1,1]
            elif buffer[1]=='R':
                index = [3,5]
            elif buffer[1]=='D':
                index = [7,7]
            elif buffer[1]=='L':
                index = [5,3]
        elif buffer[0]=='L':
            if buffer[1]=='U':
                index = [1,3]
            elif buffer[1]=='F':
                index = [5,3]
            elif buffer[1]=='D':
                index = [7,3]
            elif buffer[1]=='B':
                index = [3,5]
        return index
    
    
    def getEdgeSequence(self):
        return edgeSequence
    
    
    
    
cubeEdges = Edge()