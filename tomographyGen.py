#!/usr/bin/env python

''' A generator of Tomography CNF+ instances
    Created by Jordyn Maglalang
'''

import argparse
import random

class Generator:
    
    # Problem size
    n=0
    
    # Cell assignments
    assigns=[]          # A array, storing assignments for each cell
    cols=[]             # An array storing the number 'filled' in each column
    rows=[]             # An array storing the number 'filled' in each row
    
    # Instance
    comments = []       # A collection of comments
    constrs=[]          # An array of tuples ([list of lits],bound)
    
        
    def __init__(self,n):
        self.n = n
        for i in range(n):
            self.cols.append(0)
            self.rows.append(0)
        
    def __genAssigns(self):
        n = self.n
        for i in range(n):
            for j in range(n):
                assign = random.randint(0,1)>0
                self.assigns.append(assign)
                if(assign):
                    self.cols[j] = self.cols[j] + 1
                    self.rows[i] = self.rows[i] + 1
    
    def __addConstr(self,lits,bound):
        # Generate an atmost((lits),#filled) and atmost((-lits),n-#filled))
        # Get the literals
        pos_lits = lits
        neg_lits = []
        for lit in pos_lits:
            neg_lits.append(0-lit)
        # Get the bounds
        pos_bound = bound
        neg_bound = len(pos_lits) - pos_bound
        # Add the constraints
        self.constrs.append((pos_lits,pos_bound))
        self.constrs.append((neg_lits,neg_bound))
    
    def __createConstrsCOL(self):
        n = self.n
        # For each column
        i=1
        while(i<=n):
            lits=[]
            num_filled = self.cols[i-1]
            # Get each variable
            j=0
            while(j < n):
                # Calculate the variable
                var = j*n+i
                # Store it and its negation
                lits.append(var)
                j = j + 1
                
            # Add each constraint
            self.__addConstr(lits,num_filled)
            
            # Increment to the next column
            i = i + 1
    
    def __createConstrsROW(self):
        n = self.n
        # For each row
        i = 0
        while(i<n):
            lits = []
            num_filled = self.rows[i]
            # Get each variable
            j=1
            while(j <= n):
                # Calculate the varaible
                var = n*i+j
                # Store it and its negation
                lits.append(var)
                j = j+1
            
            # Add each constraint
            self.__addConstr(lits,num_filled)
            
            i = i + 1
    
    def __createConstrsDIA(self):
        n = self.n
        
        # Diagonals down to the right from top right corner to top left corner
        # Note, no diagonal will go down to the right from the top right corner
        # So I start at n-1
        front = n-1
        while(front >= 1):
            lits=[]
            current = front
            num_filled = 0
            while(True):
                # Add the current lit
                lits.append(current)
                if(self.assigns[current-1]):
                    num_filled = num_filled + 1 
                # End of the diagonal
                if((current%n) == 0):
                    self.__addConstr(lits,num_filled)
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
            num_filled = 0
            while(True):
                # Add the current lit
                lits.append(current)
                if(self.assigns[current-1]):
                    num_filled = num_filled + 1
                # End of the diagonal
                if(current > end):
                    self.__addConstr(lits,num_filled)
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
            num_filled = 0
            while(True):
                # Add the current lit
                lits.append(current)
                if(self.assigns[current-1]):
                    num_filled = num_filled + 1
                # End of the diagonal
                if((current%n) == 1):
                    self.__addConstr(lits,num_filled)
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
            num_filled = 0
            while(True):
                # Add the current lit
                lits.append(current)
                if(self.assigns[current-1]):
                    num_filled = num_filled + 1
                # End of the diagonal
                if(current > end):
                    self.__addConstr(lits,num_filled)
                    break
                    
                # Add n-1 (down 1 to the left)
                current = current + n - 1
            
            #Move the start one row down
            front = front + n
            
    def __writeComments(self,out):
        for comment in self.comments:
            line = "c " + comment
            out.write(line + '\n')
        
    def __writeDescript(self,out):
        out.write("p cnf+ %d %d\n" % (self.n*self.n,len(self.constrs)))
    
    def __writeConstrs(self,out):
       for i in range(len(self.constrs)):
            constr = self.constrs[i][0]
            bound = self.constrs[i][1]
            line = ''
            for lit in constr:
                line = line + "%d " % lit
            line = line + "<= %d" % bound
            out.write(line + '\n')
    
    def __writeAssigns(self,out):
        pos=0
        for i in range(self.n):
            line=''
            for j in range(self.n):
                if(self.assigns[pos]):
                    line = line + "F "
                else:
                    line = line + "N "
                pos = pos + 1
            out.write(line + '\n')
##===========================================================##
## Public Methods

    def genFormula(self):
        self.__genAssigns()
        self.__createConstrsCOL()
        self.__createConstrsROW()
        self.__createConstrsDIA()
        
    def saveAssigns(self,filepath):
        out = open(filepath,'w')
        self.__writeAssigns(out)
        out.close()

    def addComment(self,comment):
        self.comments.append(comment)

    def toDimacsP(self,filepath):
        out = open(filepath,'w')
        self.__writeComments(out)
        self.__writeDescript(out)
        self.__writeConstrs(out)
        out.close()
## End of class definition

def main():
    
    argparser = argparse.ArgumentParser(description="A tomography generator for CNF+")
    argparser.add_argument('--store','-s'
                            , default=''
                            , type=str
                            , help='Save the random assignment to a file')
    argparser.add_argument('size' 
                            , type=int
                            , help='Size of the grid (N x N')
    argparser.add_argument('out'
                            , type=str
                            , help='Outfile location')
    
    args = argparser.parse_args()
    
    # Setup generator
    gen = Generator(args.size)
    
    # Add comment
    gen.addComment("Tomography instance %d" % args.size)
    # Generate the formula
    gen.genFormula()
    # Save to a file
    gen.toDimacsP(args.out)
    
    if(args.store != ''):
        gen.saveAssigns(args.store)
    
main()