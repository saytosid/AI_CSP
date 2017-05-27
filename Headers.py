import Tkinter as tk
import random

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
        var_name,val = self.worklist.pop()
        var = 0
        for i in self.variables:
            if i.name == var_name:
                var = i
        self.remove_val_from_var(val,var)
        self.refresh_worklist()
        return True
        
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

    def revise(self,d1,d2):
        
        return ret_val
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





class Graphic:
    def __init__(self,canvas_width,canvas_height,algo,timer):
        self.algo = algo
        self.timer = timer
        self.master = tk.Tk()
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.w = tk.Canvas(self.master, 
                width=self.canvas_width,
                height=self.canvas_height)
        self.w.pack()
        self.redraw()
        self.master.mainloop()
    def redraw(self):
        
        self.w.delete("all")
        # Plotting the current variables
        variables = sorted(list(self.algo.variables))
        n = len(variables)
        width_each = self.canvas_width/n
        r = lambda: random.randint(200,255) #light colours
        rd = lambda: random.randint(0,128) #dark colors
        start = 0
        val_locs = {} # Dict of Dicts, locations of all values of all variables
        removed_val_ac4 = 0
        removed_var_ac4 = 0
        for i in xrange(n):
            col = '#%02X%02X%02X' % (r(),r(),r())
            self.w.create_rectangle(start,0,start+width_each,self.canvas_height-50,fill=col)
            if self.algo.name == "ac4":
                if len(self.algo.worklist)!=0:
                    var,val = list(self.algo.worklist)[0]
                    # Printing current Working Queue
                    txt = self.w.create_text(self.canvas_width/2,self.canvas_height-15,fill="darkblue",font="Times 15 bold",
                                    text="Removing value {} from {}".format(val,var))
                    removed_val_ac4 = val
                    removed_var_ac4 = var
                    if var ==variables[i].name:
                        var_color="red"
                    else:
                        var_color="darkblue"
                else:
                    var_color="darkblue"
            
            if self.algo.name == "ac3":
                if len(self.algo.worklist)!=0:
                    var1,var2 = list(self.algo.worklist)[0]
                    # Printing current Working Queue
                    txt = self.w.create_text(self.canvas_width/2,self.canvas_height-15,fill="darkblue",font="Times 15 bold",
                                    text="Revising {} {}".format(var1.name,var2.name))
                    if var1.name ==variables[i].name or var2.name ==variables[i].name:
                        var_color="red"
                    else:
                        var_color="darkblue"
                else:
                    var_color="darkblue"

            self.w.create_text(start+(width_each/2),20,fill=var_color,font="Times 18 bold",text="Var: {}".format(variables[i].name))
            if var_color=="red":
                offset = len(variables[i].name)*32
                self.w.create_oval(start+(width_each/2)-offset,20-12,start+(width_each/2)+offset,20+12,width=4,outline="red")
    
            #plotting domains of each variable
            values = sorted(variables[i].values)
            n_val = len(values)
            height_each = self.canvas_height/n_val
            start_y = 70
            col = '#%02X%02X%02X' % (rd(),rd(),rd())
            locs = {} # Dict to store locations of values of current variable
            for j in range(n_val):
                val = values[j]
                self.w.create_text(start+(width_each/2),start_y,fill = col,font="Times 16 bold underline",text=val)
                if self.algo.name =="ac4":
                    t = self.algo.get_supports_for_var_name(variables[i].name)[val]
                    t = "\n".join([str(x)+"->"+str(y) for x,y in t])
                    self.w.create_text(start+(width_each/2),start_y+35,fill = "red",font="Times 10",text=str(t))
                    if val==removed_val_ac4 and variables[i].name==removed_var_ac4:
                        self.w.create_oval(start+(width_each/2)-12*len(val),start_y-12,

                                    start+(width_each/2)+12*len(val),start_y+12,width=4,outline="red")

                loc = (start+(width_each/2),start_y)
                locs[val] = loc
                start_y += height_each
            val_locs[variables[i].name] = locs
            print variables[i].name,locs
            start += width_each
        
        ## plotting relations between values
        constraints = self.algo.constraints
        for con in constraints:
            var1 = con.d1.name
            var2 = con.d2.name
            relation_list = con.relation_list
            for (x,y) in relation_list:
                coordinates1 = val_locs[var1][x]
                coordinates2 = val_locs[var2][y]
                self.w.create_line(coordinates1[0],coordinates1[1],coordinates2[0],coordinates2[1])

        ########## Algo ##########
        if self.algo.step()==True:
            self.master.after(self.timer,self.redraw)
        else:
            for i in self.algo.variables:
                i.print_stats() 