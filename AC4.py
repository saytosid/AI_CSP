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
    

########## AC4 ################
    ac = AC4(variables,constraints)
    gui = Graphic(1000,700,ac,delay) #10000- delay in ms
###############################




class AC4:
    def __init__(self,variables,constraints):
        self.variables = variables
        self.constraints = constraints
        self.worklist = set()
        self.supportlist = {}
        self.name="ac4"
        self.refresh_worklist()
    def refresh_worklist(self):
        for con in self.constraints:
            var1 = con.d1
            var2 = con.d2
            sup_x = self.get_supports_for_var(var1)
            sup_y = self.get_supports_for_var(var2)
            self.supportlist[var1.name] = sup_x
            self.supportlist[var2.name] = sup_y
            # for each edge (X,Y), check if any counter S(X,a,Y) = 0, add it to queue
            for i in sup_x.keys():
                var_flag = {}
                for k in self.variables:
                    if k.name != var1.name:
                        var_flag[k.name] = 0
                for j in sup_x[i]:
                    var_flag[j[0]] = 1

                for j in var_flag.keys():
                    if var_flag[j]==0:
                        self.worklist.add((var1.name,i))
            
            for i in sup_y.keys():
                var_flag = {}
                for k in self.variables:
                    if k.name != var2.name:
                        var_flag[k.name] = 0
                for j in sup_y[i]:
                    var_flag[j[0]] = 1

                for j in var_flag.keys():
                    if var_flag[j]==0:
                        self.worklist.add((var2.name,i))
        print ">>>",self.worklist

    def step(self):
        #remove a variable from queue, delete it from domain, remove its constraints, propagate changes in support list.
        while(len(self.worklist)>0):    
            var_name,val = self.worklist.pop()
            var = 0
            for i in self.variables:
                if i.name == var_name:
                    var = i
            self.remove_val_from_var(val,var)
            self.refresh_worklist()
            return True
        return False
        
    def get_supports_for_var_name(self,var_name):
        for i in self.variables:
            if i.name == var_name:
                return self.get_supports_for_var(i)
    def get_supports_for_var(self,var):
        sup = {}
        values = var.values
        for val in values:
            sup[val] = set()
        for con in self.constraints:
            # print relation_list
            relation_list = con.relation_list
            if con.d1.name == var.name:
                for val in values:
                    val_lst = set([(con.d2.name,y) for x,y in relation_list if x==val])
                    sup[val]=sup[val].union(val_lst)
            if con.d2.name == var.name:
                for val in values:
                    val_lst = set([(con.d1.name,x) for x,y in relation_list if y==val])
                    # print val_lst
                    sup[val]=sup[val].union(val_lst)
        return sup
    def remove_val_from_var(self,val,d1):
        print "Value {} removed from variable {}".format(val,d1.name)
        for i in self.variables:
            if i == d1:
                # self.variables.remove(i)
                i.values.remove(val)
                # self.variables.append(d1)
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