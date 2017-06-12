import json
from Headers import Variable,Constraint,Graphic       
import sys

def main():
    file_name = sys.argv[1]
    delay = sys.argv[2]
    with open(file_name) as data_file:
        data = json.load(data_file)
    variables = []
    constraints = []
    for i in data['variables']:
        var = Variable(i['name'],map(str,i['domain']))
        # var.print_stats()
        variables.append(var)
    for i in data['constraints']:
        d1,d2 = map(str,i['scope'])
        d1 = filter(lambda x: x.name==d1,variables)[0]
        d2 = filter(lambda x: x.name==d2,variables)[0]
        relations = [tuple(map(str,x)) for x in i['relation']]
        con = Constraint(d1,d2,relations)
        constraints.append(con)
    
    
######## AC3 ################
    ac = AC3(variables,constraints)
    gui = Graphic(1000,700,ac,delay) #delay in ms
###############################



class AC3:
    def __init__(self,variables,constraints):
        self.variables = variables
        self.constraints = constraints
        self.worklist = set()
        self.name="ac3"
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


if __name__ == '__main__':
    main()

