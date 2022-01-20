import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '4,40'

import pygame, sys, math
from pygame.locals import *

WINDOWWIDTH = 1360                         # size of window's width in pixels
WINDOWHEIGHT = 720                         # size of windows' height in pixels
corners = [(0,0),(0,WINDOWHEIGHT),(WINDOWWIDTH,WINDOWHEIGHT),(WINDOWWIDTH,0)] 

BLACK    = (  0,   0,   0)
DARK     = ( 50,  50,  50)
GRAY     = (100, 100, 100)
WHITE    = (255, 255, 255)
YELLOW   = (255, 255,   0)
BLUE     = (  0,   0, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)

points = []        

def main():
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.fill(GRAY)
    pygame.display.set_caption('DIAGRAM')
    
    
    
    while True:                                # main loop
        for event in pygame.event.get():       # event handling loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                points.append(pos)

            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos     
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    DISPLAYSURF.fill(GRAY)
                    for p in points:
                        pygame.draw.circle(DISPLAYSURF, YELLOW, p, 5, 0)
    
                    if len(points) > 1:
                        l = len(points)
                        for r in range(l): 
                            po = polygon(points[:r] + points[r+1:], points[r])  
                            pygame.draw.polygon(DISPLAYSURF, GREEN, po, 6)
                        for n in neighbors(points[1:], points[0]):
                            pygame.draw.circle(DISPLAYSURF, BLUE, n, 8, 0)
                    if points: pygame.draw.circle(DISPLAYSURF, RED, points[0], 8, 0)

        for p in points:
            pygame.draw.circle(DISPLAYSURF, YELLOW, p, 5, 0)
            
        pygame.display.update()
        

def add(a,b):
    return (a[0]+b[0],a[1]+b[1])

def subtract(a,b):
    return (a[0]-b[0],a[1]-b[1])

def bisectorLine(p1,p2):             # returns 2 points representing the line that is 
    mid = divide(add(p1,p2),2)       # the perpendicular bisector of the line segment [p1,p2]  
    vec = subtract(p2,p1)
    normalVec = (2*vec[1],-2*vec[0])
    result1 = add(mid,normalVec)
    result2 = subtract(mid,normalVec) 
    return [result1,result2]

def closest(points,point):           # the closest element of points to point
    dist = distance(point, points[0])
    result = points[0]
    for p in points:
        newDist = distance(p, point)
        if  newDist < dist:
            result = p
            dist = newDist
    return result


def cross(p1,p2,p3):     
    # finds the sign of cross product: (point1,point2) x (point1,point3)
    vector0 = (p2[0]-p1[0],p2[1]-p1[1])
    vector1 = (p3[0]-p1[0],p3[1]-p1[1])
    determinant = vector0[0]*vector1[1] - vector0[1]*vector1[0]
    if determinant == 0: return 0     # the points are linear
    if determinant > 0: return 1      # point3 is on the right side of (point1,point2)
    if determinant < 0: return -1     # point3 is on the left side of (point1,point2)


def divide(point,n):
    return [point[0]//n,point[1]//n]

def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
'''
def enumerate(points):
    result = {p:None for p in points}
    N = neighbDict(points)
    nums = {r for r in range(168)}
    for p in points:
        result[p] =   list(nums - {result[n] for n in N[p]})[0]
    return result 
'''

def listDistance(list1,list2):
    inf = math.inf
    result = inf
    for l in list1:
        for k in list2:
            dist = abs(l[0]-k[0]) + abs(l[1]-k[1])
            if dist < result: result = dist
    return result         

def lineIntersection(line1,line2):
    vector0 = (line1[1][0]-line1[0][0],line1[1][1]-line1[0][1])
    vector1 = (line2[1][0]-line2[0][0],line2[1][1]-line2[0][1])
    determinant = vector0[0]*vector1[1] - vector0[1]*vector1[0]
    if determinant == 0: return None
    result0 = (line1[0][0]*line1[1][1] - line1[0][1]*line1[1][0])*(line2[0][0] - line2[1][0]) - (line2[0][0]*line2[1][1] - line2[0][1]*line2[1][0])*(line1[0][0] - line1[1][0])
    result1 = (line1[0][0]*line1[1][1] - line1[0][1]*line1[1][0])*(line2[0][1] - line2[1][1]) - (line2[0][0]*line2[1][1] - line2[0][1]*line2[1][0])*(line1[0][1] - line1[1][1])
    result0 = result0 / determinant
    result1 = result1 / determinant
    
    return (result0,result1)   

def neighbors(points,point):   # points does not contain point
    result = set()
    n = len(points)
    for r in range(n):
        rest = points[:r] + points[r+1:] + [point]
        if listDistance(polygon(points,point),polygon(rest,points[r])) < 5:
            result.add(points[r])

    return result

def neighbDict(points):   # points: A list of points
    result = {}
    n = len(points)
    for r in range(n):
        rest = points[:r] + points[r+1:]
        result[points[r]] = neighbors(rest,points[r])

    return result




def polygon(points,point):     # points does not contain point
    result = []
    c = closest(points,point)
    mid = divide(add(c,point),2) 
    closestLine = bisectorLine(c,point)
    lines = [bisectorLine(p,point) for p in points]
    distLines = [distance(p,point)/2 for p in points]
    borderLines = [corners[:2],corners[1:3],corners[2:],[corners[0],corners[3]]]
    distBorderLines = [point[0],WINDOWHEIGHT-point[1],WINDOWWIDTH-point[0],point[1]]
    lines += borderLines
    distLines += distBorderLines

    n = len(lines)
    nextLine = None
    nextLineDist = None
    startPoint = None
    li = None
    dist = None
    for r in range(n):
        li = lineIntersection(closestLine,lines[r])
        if li and cross(point,c,li) == 1:
            newDist = distance(mid,li)
            if not dist:
                dist = newDist
                startPoint = li
                nextLine = lines[r]
                nextLineDist = distLines[r]
            elif newDist < dist:
                dist = newDist
                startPoint = li
                nextLine = lines[r]
                nextLineDist = distLines[r]
            elif newDist == dist and distLines[r] < nextLineDist:
                startPoint = li
                nextLine = lines[r]
                nextLineDist = distLines[r]
    
    result.append(startPoint)
    closestLine = nextLine
    c = startPoint

    while (len(result) == 1 or result[0] != result[-1]):        # and len(result) < 5:
        li = None
        dist = None
        for r in range(n):
            li = lineIntersection(closestLine,lines[r])
            if li and cross(point,c,li) == 1:
                newDist = distance(c,li)
                if not dist:
                    dist = newDist
                    startPoint = li
                    nextLine = lines[r]
                    nextLineDist = distLines[r]
                elif newDist < dist:
                    dist = newDist
                    startPoint = li
                    nextLine = lines[r]
                    nextLineDist = distLines[r]
                elif newDist == dist and distLines[r] < nextLineDist:
                    startPoint = li
                    nextLine = lines[r]
                    nextLineDist = distLines[r]
        result.append(startPoint)
        closestLine = nextLine
        c = startPoint


    return result[:-1]

main()