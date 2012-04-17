#!/usr/bin/env python

''' A simple generator for the n-queens problem in CNF+
    Created by Jordyn Maglalang
'''

import argparse

class Generator:
    # Problem Size
    n=0
    
    # Instance details
    num_var=0
    num_constr=0
    
    # Constraints
    Constrs=[]  # a set of tuples: ([list of literals], bound)
    Comments=[]
    
    # Constructor
    def __init__(self,n):
        self.n = n
        self.num_var = n * n
        self.num_constr = (7 * n) - 6

    # Get the variable for a given (row,col)
    def __getVar(self, row, col):
        return row*self.n + col + 1  # 1-based counting for variables

    # Constraint creators
    def __createConstrsQUEENS(self):
        for j in range(self.n):
            # For each column, there must be at least one queen
            # == there must be at most n-1 "not queens" (negated literals)
            lits=[-self.__getVar(i,j) for i in range(self.n)]
            # At most one of these is true
            self.Constrs.append((lits,self.n-1))

    def __createConstrsROW(self):
        for i in range(self.n):
            # For each row, include every cell
            lits=[self.__getVar(i,j) for j in range(self.n)]
            # At most one of these is true
            self.Constrs.append((lits,1))

    def __createConstrsCOL(self):
        for j in range(self.n):
            # For each column, include every cell
            lits=[self.__getVar(i,j) for i in range(self.n)]
            # At most one of these is true
            self.Constrs.append((lits,1))
    
    def __createConstrsDIA(self):
        n = self.n
        
        # Diagonals down to the right from top right corner to top left corner
        # Note, no diagonal will go down to the right from the top right corner
        # So I start at n-1
        front = n-1
        while(front >= 1):
            lits=[]
            current = front
            while(True):
                # Add the current lit
                lits.append(current)
                
                # End of the diagonal
                if((current%n) == 0):
                    self.Constrs.append((lits,1))
                    break
                # Add n+1 (down 1 to the right)
                current = current + n + 1
        
            # Move the start one column to the left
            front = front - 1
        
        
        
        # Diagonals down to the right from the top left corner + n to the bottom
        # left corner. (this will start at n+1 because the down right diagonal from
        # 1 was already added.
        front = 1 + n
        end = ((n-1) * n)+1
        
        while(front < end):
            lits=[]
            current = front
            while(True):
                # Add the current lit
                lits.append(current)
            
                # End of the diagonal
                if(current > end):
                    self.Constrs.append((lits,1))
                    break
                # Add n+1 (down 1 to the right)
                current = current + n + 1
            
            # Move the start one row down
            front = front + n
        
        # Diagonals down to the left from the top left corner + 1 to the top
        # right corner
        front = 2
        while(front <= n):
            lits=[]
            current = front
            while(True):
                # Add the current lit
                lits.append(current)
        
                # End of the diagonal
                if((current%n) == 1):
                    self.Constrs.append((lits,1))
                    break
                
                # Add n-1 (down 1 to the left)
                current = current + n - 1
                
            # Move the start one column to the right
            front = front + 1
            
        # Diagonals down to the left from the top right corner + n to the bottom
        # right corner. Diagonal from the top right corner is already added
        front = n + n
        end = n * (n-1)
        while(front <= end):
            lits=[]
            current = front
            while(True):
                # Add the current lit
                lits.append(current)
                
                # End of the diagonal
                if(current > end):
                    self.Constrs.append((lits,1))
                    break
                    
                # Add n-1 (down 1 to the left)
                current = current + n - 1
            
            #Move the start one row down
            front = front + n

    def __writeComments(self,out):
        for comment in self.Comments:
            line = "c " + comment
            out.write(line + '\n')
        
    def __writeDescript(self,out):
        out.write("p cnf+ %d %d\n" % (self.num_var,self.num_constr))
    
    def __writeConstrs(self,out):
       for constr in self.Constrs:
            lits = constr[0]
            bound = constr[1]
            line = ''
            for lit in lits:
                line = line + "%d " % lit
            line = line + "<= %d" % bound
            out.write(line + '\n')

##=======================================================##

    def addComment(self,comment):
        self.Comments.append(comment)
        
    def genConstrs(self):
        self.__createConstrsQUEENS()
        self.__createConstrsROW()
        self.__createConstrsCOL()
        self.__createConstrsDIA()
        
    def toDimacsP(self,filepath):
        out = open(filepath,'w')
        self.__writeComments(out)
        self.__writeDescript(out)
        self.__writeConstrs(out)
        out.close()
## END OF CLASS DEF

def main():
    
    argparser = argparse.ArgumentParser(description="an n-queens generator for CNF+")

    argparser.add_argument('size' 
                            , type=int
                            , help='Size of the problem i.e n in n-queens')
    argparser.add_argument('out'
                            , type=str
                            , help='Outfile location')
    
    args = argparser.parse_args()
    
    # Setup generator
    gen = Generator(args.size)
    
    # Add comment
    gen.addComment("%d-queens" % args.size)
    #if(args.comment):
        #add extra comment

    gen.genConstrs()
    
    gen.toDimacsP(args.out)
    
main()
