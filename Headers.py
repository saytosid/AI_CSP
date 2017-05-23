class Variable:
    def __init__(self, name,value_list):
        self.name = name
        self.values = value_list
    def print_stats(self):
        print self.name,self.values
    pass

class Constraint:
    def __init__(self,dom_1,dom_2,relation_list):
        self.d1 = dom_1
        self.d2 = dom_2
        self.relation_list = relation_list
    def add_tuple(self,t1):
        self.relation_list.append(t1)
    def print_constraint(self):
        print "Variables: {} , {} ".format(self.d1.name,self.d2.name)
        print "Relations: {}".format(self.relation_list)

class AC3:
    def __init__(self,variables,constraints):
        self.variables = variables
        self.constraints = constraints
        self.worklist = set()
        [self.worklist.add((x.d1,x.d2)) for x in constraints]
        remove_tuples = []
        for d1,d2 in self.worklist:
            if (d2,d1) in self.worklist and (d1,d2) not in remove_tuples:
                remove_tuples.append((d2,d1))
                # print d2.name,d1.name,"removed"
        [self.worklist.remove(x) for x in remove_tuples]
    def print_worklist(self):
        for x,y in self.worklist:
            print "Worklist member: ",x.name,y.name
    def step(self):
        while(len(self.worklist)>0):
            print "CURRENT WORKLIST: {}".format([(str(x.name),str(y.name)) for x,y in self.worklist])
            d1,d2 = self.worklist.pop()
            if self.revise(d1,d2)==True:
                if len(d1.values)==0:
                    return False #Failure
                else:
                    set_added = set()
                    for x in self.constraints:
                        # if x.d1==d1 and x.d2!=d2:
                        if x.d1==d1:
                            set_added.add((x.d2,d1))
                        # if x.d2==d1 and x.d1!=d2:
                        if x.d2==d1:
                            set_added.add((x.d1,d1))
                    self.worklist.update(set_added)
            return True #Algo continues
            break #single step, stepping is handled by Graphic now
        return False # Algo finished
            

    def revise(self,d1,d2):
        print "Revising {} wrt {}".format(d1.name,d2.name)
        ret_val = False
        for val in d1.values:
            print "Checking {} in {}".format(val,d1.name)
            for con in self.constraints:
                if (con.d1==d1 and con.d2==d2):
                    rel = [y for x,y in con.relation_list if x==val ]
                    if(len(rel)==0):
                        self.remove_val_from_var(val,d1)
                        ret_val = True
                    else:
                        print "Found {},{} in {},{}".format(val,rel[0],d1.name,d2.name)
                # in case constraint is in reverse order
                if (con.d1==d2 and con.d2==d1):
                    rel = [x for x,y in con.relation_list if y==val ]
                    if(len(rel)==0):
                        self.remove_val_from_var(val,d1)
                        ret_val = True
                    else:
                        print "Found {},{} in {},{}".format(val,rel[0],d1.name,d2.name)
        return ret_val
    def remove_val_from_var(self,val,d1):
        print "Value {} removed from variable {}".format(val,d1.name)
        for i in self.variables:
            if i == d1:
                self.variables.remove(i)
                d1.values.remove(val)
                self.variables.append(d1)
                # remove constraints that use this variable
                for i in range(len(self.constraints)):
                    con = self.constraints[i]
                    if con.d1==d1:
                        for x,y in con.relation_list:
                            if x==val:
                                self.constraints[i].relation_list.remove((x,y))
                                print "{},{} removed from constraint R({},{})".format(x,y,con.d1.name,con.d2.name)
                    if con.d2==d1:
                        for x,y in con.relation_list:
                            if y==val:
                                self.constraints[i].relation_list.remove((x,y))
                                print "{},{} removed from constraint R({},{})".format(x,y,con.d1.name,con.d2.name)
                break
