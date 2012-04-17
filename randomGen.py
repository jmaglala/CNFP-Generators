#!/usr/bin/env python

''' A generator of random CNF+ instances
    Created by Jordyn Maglalang
'''

import random
import math
import argparse
import sys

class Generator:
    ''' A tunable generator for creating random instances in the DIMACS+ format'''
    
    # Instance stats
    num_var=0
    num_constr=0
    size_constr=0
    ratio=0.0
    known='UNKNOWN'
    
    # Instance
    available = []      # A list of available literals (for random.sample())
    comments = []       # A list of comments
    constrs = []        # A liset of tuples ([list of lits], bound)
    assignment = []     # A full assignment chosen
    
    # Methods
    def __init__(self, n, r, k):
        self.num_var = n
        self.ratio = r
        self.size_constr = k
        self.num_constr=int(n*r)
        self.available = range(1,n+1)# + range(-1,-(n+1),-1)

    def __genConstraint(self):
        lits = random.sample(self.available, self.size_constr)
        lits = [x*random.choice([1,-1]) for x in lits]  # randomly swap polarities
        bound = random.randint(1,self.size_constr-1)
        return lits,bound
    
    def __writeComments(self,out):
        for comment in self.comments:
            line = "c " + comment
            out.write(line + '\n')
        
    def __writeDescript(self,out):
        out.write("p cnf+ %d %d\n" % (self.num_var,self.num_constr))
    
    def __writeConstrs(self,out):
       for i in range(len(self.constrs)):
            constr = self.constrs[i][0]
            bound = self.constrs[i][1]
            line = ''
            for lit in constr:
                line = line + "%d " % lit
            line = line + "<= %d" % bound
            out.write(line + '\n')

    def __genAssign(self):
        for i in range(self.num_var):
            self.assignment.append(random.randint(0,1)>0)
    
    def __covers(self,constr):
        lits = constr[0]
        bound = constr[1]
        counter=0
        for lit in lits:
            # Get the variable\
            var = int(math.fabs(lit))
            # The current lit from the constraint matches the assignment
            if(self.assignment[var-1] == (lit > 0)):
                # Exceeded the atmost
                if(counter > bound):
                    return False
                # Increment the counter
                counter = counter + 1
        return True
        
    def __addConstr(self,constr):
        self.constrs.append(constr)
        
##===========================================================##
## Public Methods

    def addComment(self,comment):
        self.comments.append(comment)

    def toDimacsP(self,filepath):
        if filepath != '':
            out = open(filepath,'w')
        else:
            out = sys.stdout
        self.__writeComments(out)
        self.__writeDescript(out)
        self.__writeConstrs(out)
        if filepath != '':
            out.close()
    
    def genFormula(self, forceTrue):
        if forceTrue:
            self.__genAssign()
            #TODO: add flag to print out the assignment
            
        # Generate the constraints
        for i in range(self.num_constr):
            constr = self.__genConstraint()
            while forceTrue and not self.__covers(constr):
                constr = self.__genConstraint()
            self.__addConstr(constr)


## END OF CLASS DEF            
##============================================================##

def main():
    # Parse command line arguments
    argparser = argparse.ArgumentParser(description="A tunable random generator for CNF+")
    argparser.add_argument('--sat','-s'
                            , action='store_true'
                            , default=False
                            , help='Generate a known satisfiable instance')
    argparser.add_argument('n'
                            , type=int
                            , help='Number of variables')
    argparser.add_argument('r'
                            , type=float
                            , help='Ratio of constraints to variables')                
    argparser.add_argument('k' 
                            , type=int
                            , help='Size of the constraints')
    argparser.add_argument('out'
                            , nargs='?'
                            , type=str
                            , default=''
                            , help='Output file [default: output to stdout]')
    args = argparser.parse_args()
    
    # Setup Generator
    gen = Generator(args.n,args.r,args.k)
    if (args.sat):
        gen.known='SAT'
    
    # Add comments
    gen.addComment('Randomly generated %s cnf+ instance' % gen.known )
    gen.addComment('n:%d r:%f k:%d' % (args.n, args.r, args.k) )
    if args.out != '':
        gen.addComment(args.out)
    
    # Generate constraints
    gen.genFormula(args.sat)
    
    # Write to outfile
    gen.toDimacsP(args.out)
    
main()

