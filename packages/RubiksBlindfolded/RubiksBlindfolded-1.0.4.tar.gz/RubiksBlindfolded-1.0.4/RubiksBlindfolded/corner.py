#!/usr/bin/env python3
# -*- coding: utf-8 -*-

cornerBuffer = []
cornerSequence = []

class Corner:

    cornerCount = 0
    cornerIndex = []
    cornerColor = []
    
    def solveCorner(self,sides,cornerPriority):
        
        cornerGoal = (sides['U'][0]=='U' and sides['U'][2]=='U' and sides['U'][6]=='U' and sides['U'][8]=='U'
                and sides['F'][0]=='F' and sides['F'][2]=='F' and sides['F'][6]=='F' and sides['F'][8]=='F'
                and sides['R'][0]=='R' and sides['R'][2]=='R' and sides['R'][6]=='R' and sides['R'][8]=='R'
                and sides['D'][0]=='D' and sides['D'][2]=='D' and sides['D'][6]=='D' and sides['D'][8]=='D'
                and sides['B'][0]=='B' and sides['B'][2]=='B' and sides['B'][6]=='B' and sides['B'][8]=='B'
                and sides['L'][0]=='L' and sides['L'][2]=='L' and sides['L'][6]=='L' and sides['L'][8]=='L')

        if (cornerGoal):
            print('Corners are already solved!')
            
        else:
            
            if ((sides['L'][0]=='L' and sides['U'][0]=='U' and sides['B'][2]=='B') or 
                (sides['L'][0]=='U' and sides['U'][0]=='B' and sides['B'][2]=='L') or
                (sides['L'][0]=='B' and sides['U'][0]=='L' and sides['B'][2]=='U')):
                cornerBuffer = self.cornerBufferChange(sides,cornerPriority)
                self.cornerCount = self.cornerCount + 1
                
            if not ((sides['L'][0]=='L' and sides['U'][0]=='U' and sides['B'][2]=='B') or 
                (sides['L'][0]=='U' and sides['U'][0]=='B' and sides['B'][2]=='L') or
                (sides['L'][0]=='B' and sides['U'][0]=='L' and sides['B'][2]=='U')):
                cornerBuffer = [sides['L'][0], sides['U'][0], sides['B'][2]]
                
                
                while(1):
                    cornerGoalbuffer = (sides['U'][2]=='U' and sides['U'][6]=='U' and sides['U'][8]=='U'
                                    and sides['F'][0]=='F' and sides['F'][2]=='F' and sides['F'][6]=='F' and sides['F'][8]=='F'
                                    and sides['R'][0]=='R' and sides['R'][2]=='R' and sides['R'][6]=='R' and sides['R'][8]=='R'
                                    and sides['D'][0]=='D' and sides['D'][2]=='D' and sides['D'][6]=='D' and sides['D'][8]=='D'
                                    and sides['B'][0]=='B' and sides['B'][6]=='B' and sides['B'][8]=='B'
                                    and sides['L'][2]=='L' and sides['L'][6]=='L' and sides['L'][8]=='L')
                    
                    if (cornerGoalbuffer):
                        sides['L'][0] = 'L'
                        sides['U'][0] = 'U'
                        sides['B'][2] = 'B'
                        
                        if not(self.cornerCount%2==0):
                            sidesCopy = sides.copy()
                            parity = [sidesCopy['U'][3], sidesCopy['L'][1], sidesCopy['U'][1], sidesCopy['B'][1]]
                            sides['U'][1] = parity[0]
                            sides['B'][1] = parity[1]
                            
                            sides['U'][3] = parity[2]
                            sides['L'][1] = parity[3]
                        
                        #print('Corners are solved!')
                        #print(sides)
                        
                        break
                    
                        
                    face = [cornerBuffer[0], cornerBuffer[1], cornerBuffer[2]]
                    
                    prevBuffer = cornerBuffer
                    if ((sides['L'][0]=='L' and sides['U'][0]=='U' and sides['B'][2]=='B') or 
                        (sides['L'][0]=='U' and sides['U'][0]=='B' and sides['B'][2]=='L') or
                        (sides['L'][0]=='B' and sides['U'][0]=='L' and sides['B'][2]=='U')):
                        cornerBuffer = self.cornerBufferChange(sides,cornerPriority)
                        
                    else:
                        cornerSequence.append(cornerBuffer)
                        self.cornerColor.append(cornerBuffer)
                        
                        index = self.getCornerIndex(cornerBuffer)
                        self.cornerIndex.append([cornerBuffer[0],index[0],cornerBuffer[1],index[1],cornerBuffer[2],index[2]])
                        

                        cornerBuffer = [sides[cornerBuffer[0]][index[0]],sides[cornerBuffer[1]][index[1]],sides[cornerBuffer[2]][index[2]]] #update buffer
                        
                        sides[prevBuffer[0]][index[0]] = prevBuffer[0]
                        sides[prevBuffer[1]][index[1]] = prevBuffer[1]
                        sides[prevBuffer[2]][index[2]] = prevBuffer[2]
                        
                        sides['L'][0] = cornerBuffer[0]
                        sides['U'][0] = cornerBuffer[1]
                        sides['B'][2] = cornerBuffer[2]
                        
                    self.cornerCount = self.cornerCount + 1
                    
        
        return sides
    
    
    def cornerBufferChange(self,sides,cornerPriority):
        sidesCopy = sides.copy()
        a1 = ''
        a2 = 0
        b1 = ''
        b2 = 0
        c1 = ''
        c2 = 0
        
        if not (sides[cornerPriority[0][0]][cornerPriority[0][1]]=='U' 
            and sides[cornerPriority[0][2]][cornerPriority[0][3]]=='R' 
            and sides[cornerPriority[0][4]][cornerPriority[0][5]]=='B'):
            a1 = 'U'
            a2 = 2
            b1 = 'R'
            b2 = 2
            c1 = 'B'
            c2 = 0
            
            cornerBuffer = ['U','R','B']
            cornerSequence.append(cornerBuffer)
            
        elif not (sides[cornerPriority[1][0]][cornerPriority[1][1]]=='U' 
            and sides[cornerPriority[1][2]][cornerPriority[1][3]]=='L' 
            and sides[cornerPriority[1][4]][cornerPriority[1][5]]=='F'):
            a1 = 'U'
            a2 = 6
            b1 = 'L'
            b2 = 2
            c1 = 'F'
            c2 = 0
            
            cornerBuffer = ['U','L','F']
            cornerSequence.append(cornerBuffer)
        
        elif not (sides[cornerPriority[2][0]][cornerPriority[2][1]]=='U' 
            and sides[cornerPriority[2][2]][cornerPriority[2][3]]=='F' 
            and sides[cornerPriority[2][4]][cornerPriority[2][5]]=='R'):
            a1 = 'U'
            a2 = 8
            b1 = 'F'
            b2 = 2
            c1 = 'R'
            c2 = 0
            
            cornerBuffer = ['U','F','R']
            cornerSequence.append(cornerBuffer)
            
        elif not (sides[cornerPriority[3][0]][cornerPriority[3][1]]=='D' 
            and sides[cornerPriority[3][2]][cornerPriority[3][3]]=='F' 
            and sides[cornerPriority[3][4]][cornerPriority[3][5]]=='L'):
            a1 = 'D'
            a2 = 0
            b1 = 'F'
            b2 = 6
            c1 = 'L'
            c2 = 8
            
            cornerBuffer = ['D','F','L']
            cornerSequence.append(cornerBuffer)
            
        elif not (sides[cornerPriority[4][0]][cornerPriority[4][1]]=='D' 
            and sides[cornerPriority[4][2]][cornerPriority[4][3]]=='R' 
            and sides[cornerPriority[4][4]][cornerPriority[4][5]]=='F'):
            a1 = 'D'
            a2 = 2
            b1 = 'R'
            b2 = 6
            c1 = 'F'
            c2 = 8
            
            cornerBuffer = ['D','R','F']
            cornerSequence.append(cornerBuffer)
        
        elif not (sides[cornerPriority[5][0]][cornerPriority[5][1]]=='D' 
            and sides[cornerPriority[5][2]][cornerPriority[5][3]]=='L' 
            and sides[cornerPriority[5][4]][cornerPriority[5][5]]=='B'):
            a1 = 'D'
            a2 = 6
            b1 = 'L'
            b2 = 6
            c1 = 'B'
            c2 = 8
            
            cornerBuffer = ['D','L','B']
            cornerSequence.append(cornerBuffer)
            
        elif not (sides[cornerPriority[6][0]][cornerPriority[6][1]]=='D' 
            and sides[cornerPriority[6][2]][cornerPriority[6][3]]=='B' 
            and sides[cornerPriority[6][4]][cornerPriority[6][5]]=='R'):
            a1 = 'D'
            a2 = 8
            b1 = 'B'
            b2 = 6
            c1 = 'R'
            c2 = 8
            
            cornerBuffer = ['D','B','R']
            cornerSequence.append(cornerBuffer)
        
        
        index = self.getCornerIndex(cornerBuffer)
        self.cornerIndex.append([cornerBuffer[0],index[0],cornerBuffer[1],index[1],cornerBuffer[2],index[2]])
        
        swap = [sidesCopy['L'][0], sidesCopy['U'][0], sidesCopy['B'][2],
                sidesCopy[a1][a2], sidesCopy[b1][b2], sidesCopy[c1][c2]]
        
        cornerBuffer = [sides[a1][a2],sides[b1][b2],sides[c1][c2]]
        
        
        if (sides['L'][0]=='L' and sides['U'][0]=='U' and sides['B'][2]=='B'):
            self.cornerColor.append(['L','U','B'])
            
        elif (sides['L'][0]=='U' and sides['U'][0]=='B' and sides['B'][2]=='L'):
            self.cornerColor.append(['U','B','L'])
            
        elif (sides['L'][0]=='B' and sides['U'][0]=='L' and sides['B'][2]=='U'):
            self.cornerColor.append(['B','L','U'])
        
        sides[a1][a2] = swap[0]
        sides[b1][b2] = swap[1]
        sides[c1][c2] = swap[2]
        
        sides['L'][0] = swap[3]
        sides['U'][0] = swap[4]
        sides['B'][2] = swap[5]
        
            
        return cornerBuffer
        
    
    def getCornerIndex(self,cornerBuffer):
        if cornerBuffer[0]=='U':
            if cornerBuffer[1]=='R':
                if cornerBuffer[2]=='F':
                    index = [8,0,2]
                elif cornerBuffer[2]=='B':
                    index = [2,2,0]
            elif cornerBuffer[1]=='F':
                if cornerBuffer[2]=='R':
                    index = [8,2,0]
                elif cornerBuffer[2]=='L':
                    index = [6,0,2]
            elif cornerBuffer[1]=='B':
                if cornerBuffer[2]=='R':
                    index = [2,0,2]
                elif cornerBuffer[2]=='L':
                    index = [0,2,0]
            elif cornerBuffer[1]=='L':
                if cornerBuffer[2]=='F':
                    index = [6,2,0]
                elif cornerBuffer[2]=='B':
                    index = [0,0,2]
        elif cornerBuffer[0]=='F':
            if cornerBuffer[1]=='U':
                if cornerBuffer[2]=='R':
                    index = [2,8,0]
                elif cornerBuffer[2]=='L':
                    index = [0,6,2]
            elif cornerBuffer[1]=='R':
                if cornerBuffer[2]=='U':
                    index = [2,0,8]
                elif cornerBuffer[2]=='D':
                    index = [8,6,2]
            elif cornerBuffer[1]=='D':
                if cornerBuffer[2]=='R':
                    index = [8,2,6]
                elif cornerBuffer[2]=='L':
                    index = [6,0,8]
            elif cornerBuffer[1]=='L':
                if cornerBuffer[2]=='U':
                    index = [0,2,6]
                elif cornerBuffer[2]=='D':
                    index = [6,8,0]
        elif cornerBuffer[0]=='R':
            if cornerBuffer[1]=='U':
                if cornerBuffer[2]=='F':
                    index = [0,8,2]
                elif cornerBuffer[2]=='B':
                    index = [2,2,0]
            elif cornerBuffer[1]=='F':
                if cornerBuffer[2]=='U':
                    index = [0,2,8]
                elif cornerBuffer[2]=='D':
                    index = [6,8,2]
            elif cornerBuffer[1]=='D':
                if cornerBuffer[2]=='F':
                    index = [6,2,8]
                elif cornerBuffer[2]=='B':
                    index = [8,8,6]
            elif cornerBuffer[1]=='B':
                if cornerBuffer[2]=='U':
                    index = [2,0,2]
                elif cornerBuffer[2]=='D':
                    index = [8,6,8]
        elif cornerBuffer[0]=='D':
            if cornerBuffer[1]=='F':
                if cornerBuffer[2]=='R':
                    index = [2,8,6]
                elif cornerBuffer[2]=='L':
                    index = [0,6,8]
            elif cornerBuffer[1]=='R':
                if cornerBuffer[2]=='F':
                    index = [2,6,8]
                elif cornerBuffer[2]=='B':
                    index = [8,8,6]
            elif cornerBuffer[1]=='B':
                if cornerBuffer[2]=='R':
                    index = [8,6,8]
                elif cornerBuffer[2]=='L':
                    index = [6,8,6]
            elif cornerBuffer[1]=='L':
                if cornerBuffer[2]=='F':
                    index = [0,8,6]
                elif cornerBuffer[2]=='B':
                    index = [6,6,8]
        elif cornerBuffer[0]=='B':
            if cornerBuffer[1]=='U':
                if cornerBuffer[2]=='R':
                    index = [0,2,2]
                elif cornerBuffer[2]=='L':
                    index = [2,0,0]
            elif cornerBuffer[1]=='R':
                if cornerBuffer[2]=='U':
                    index = [0,2,2]
                elif cornerBuffer[2]=='D':
                    index = [6,8,8]
            elif cornerBuffer[1]=='D':
                if cornerBuffer[2]=='R':
                    index = [6,8,8]
                elif cornerBuffer[2]=='L':
                    index = [8,6,6]
            elif cornerBuffer[1]=='L':
                if cornerBuffer[2]=='U':
                    index = [2,0,0]
                elif cornerBuffer[2]=='D':
                    index = [8,6,6]
        elif cornerBuffer[0]=='L':
            if cornerBuffer[1]=='U':
                if cornerBuffer[2]=='F':
                    index = [2,6,0]
                elif cornerBuffer[2]=='B':
                    index = [0,0,2]
            elif cornerBuffer[1]=='F':
                if cornerBuffer[2]=='U':
                    index = [2,0,6]
                elif cornerBuffer[2]=='D':
                    index = [8,6,0]
            elif cornerBuffer[1]=='D':
                if cornerBuffer[2]=='F':
                    index = [8,0,6]
                elif cornerBuffer[2]=='B':
                    index = [6,6,8]
            elif cornerBuffer[1]=='B':
                if cornerBuffer[2]=='U':
                    index = [0,2,0]
                elif cornerBuffer[2]=='D':
                    index = [6,8,6]
        return index
    
    
    def getCornerSequence(self):
        return cornerSequence
        
        
cubeCorners = Corner()