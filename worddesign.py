#!/usr/bin/env python
''' A generator of Word design for DNA computing on surfaces problem instances for cnf+
    based off of http://www.csplib.org/ specification, prob033
    Created by Jordyn Maglalang
'''

import argparse

class Generator:
    
    # Word , Position , Letter
    # Letters:
    #  A = 0
    #  T = 1
    #  C = 2
    #  G = 3
    
    # prop_v[(word,position,letter)]
    prop_v={(0,0,0):0}
    # comp_v[(word,position
    comp_b={((0,0,0),(0,0,0)):0}
    comp_c={((0,0,0),(0,0,0)):0}
    num_vars=0
    
    # Problem details
    w=0
    p=8
    l=4
    
    # Constraints
    constrs=[]
    comments=[]
    
    def __init__(self,n):
       self.w = n 
    
    def __genVars(self):
        
        # For each word
        for w in range(self.w):
            
            # For each position
            for p in range(self.p):
                
                # For each letter
                for l in range(self.l):
                    self.num_vars = self.num_vars + 1
                    self.prop_v[(w,p,l)]= self.num_vars
    
    
    # Each word in S has 4 symbols from { C,G };
    def __genConstrsA(self):
        
        # For each word
        for w in range(self.w):
            
            pos_lits=[]
            neg_lits=[]
            
            # Iterate over the positions
            for p in range(self.p):
                
                # Get the vars
                c = self.prop_v[(w,p,2)]
                g = self.prop_v[(w,p,3)]
                
                pos_lits.append(c)
                pos_lits.append(g)
                neg_lits.append(-c)
                neg_lits.append(-g)
            
            self.constrs.append((pos_lits,4))
            self.constrs.append((neg_lits,len(neg_lits)-4))
    
    # Each pair of distinct words in S differ in at least 4 positions
    # Each pair of distinct words in S are the same in at most 4 positions
    def __genConstrsB(self):
        
        # For each pair of words
        for w1 in range(self.w):
            for w2 in range(w1+1,self.w):
                
                # Set of the vars for each comparison
                comps=[]
                # For each position
                for p in range(self.p):
                    
                    # For each letter
                    for l in range(self.l):
                        
                        # Create additional variables for comparison
                        self.num_vars = self.num_vars + 1
                        self.comp_b[((w1,p,l),(w2,p,l))] = self.num_vars
                        comps.append(self.num_vars)
                        
                        # Add a constraint for each comparison
                        lits=[]
                        lits.append(self.prop_v[(w1,p,l)])
                        lits.append(self.prop_v[(w2,p,l)])
                        lits.append(-self.comp_b[((w1,p,l),(w2,p,l))])
                        self.constrs.append((lits,2))
                        
                self.constrs.append((comps,4))
                
    def __genConstrsC(self):
        
        # For each pair of words x and y where x and y may be identical
        for w1 in range(self.w):
            for w2 in range(w1,self.w):
                
                # Set of the vars for each comparison
                comps=[]
                
                # For each position
                for p in range(self.p):
                    # For each letter
                    for l in range(self.l):
                        # Get the reversed position for w1
                        p1 = 7 - p
                        
                        # Get the letter for w2
                        if   l == 0:
                            l2 = 1
                        elif l == 1:
                            l2 = 0
                        elif l == 2:
                            l2 = 3
                        elif l == 3:
                            l2 = 2
                        
                        # Create additional variables for comparison
                        self.num_vars = self.num_vars + 1
                        self.comp_c[((w1,p1,l),(w2,p,l2))] = self.num_vars
                        comps.append(self.num_vars)
                        
                        # Add a constraint for each comparison
                        lits=[]
                        lits.append(self.prop_v[(w1,p1,l)])
                        lits.append(self.prop_v[(w2,p,l2)])
                        lits.append(-self.comp_c[((w1,p1,l),(w2,p,l2))])
                        self.constrs.append((lits,2))
                        
                self.constrs.append((comps,4))
    
    # For each position of each word, only one letter can be assigned
    def __genConstrsD(self):
        
        # For each word
        for w in range(self.w):
            # For each position
            for p in range(self.p):
                pos_lits=[]
                neg_lits=[]
                
                # Generate the constraint on all the letters
                for l in range(self.l):
                    var = self.prop_v[(w,p,l)]
                    pos_lits.append(var)
                    neg_lits.append(-var)
                
                self.constrs.append((pos_lits,1))
                self.constrs.append((neg_lits,len(neg_lits)-1))
            
                
    def __writeComments(self,out):
        for comment in self.comments:
            line = "c " + comment
            out.write(line + '\n')
        
    def __writeDescript(self,out):
        out.write("p cnf+ %d %d\n" % (self.num_vars,len(self.constrs)))
    
    def __writeConstrs(self,out):
       for constr in self.constrs:
            lits = constr[0]
            bound = constr[1]
            line = ''
            for lit in lits:
                line = line + "%d " % lit
            line = line + "<= %d" % bound
            out.write(line + '\n')

##=======================================================##

    def addComment(self,comment):
        self.comments.append(comment)
        
    def genConstrs(self):
        self.__genVars()
        self.__genConstrsA()
        self.__genConstrsB()
        self.__genConstrsC()
        self.__genConstrsD()
        
    def toDimacsP(self,filepath):
        out = open(filepath,'w')
        self.__writeComments(out)
        self.__writeDescript(out)
        self.__writeConstrs(out)
        out.close()
## END OF CLASS DEF
                        
def main():
    argparser = argparse.ArgumentParser(description="a word design generator for CNF+")
    
    argparser.add_argument('size'
                            , type=int
                            , help='Size of the problem: the number of words to search for')
    argparser.add_argument('out'
                            , type=str
                            , help='Outfile location')
                            
    args = argparser.parse_args()
    
    # Setup generator
    gen = Generator(args.size)
    
    # Add comment
    gen.addComment("%d-worddesign" % args.size)
    
    gen.genConstrs()
    
    gen.toDimacsP(args.out)
    
main()
