import json
import Tkinter as tk
import random
from Headers import AC3,Variable,Constraint

class AC4:
    def __init__(self,variables,constraints):
        self.variables = variables
        self.constraints = constraints
        self.worklist = set()
        self.supportlist = {}
        for con in constraints:
            var1 = con.d1
            var2 = con.d2
            sup_x = self.get_supports_for_var(var1)
            sup_y = self.get_supports_for_var(var2)
            self.supportlist[var1.name] = sup_x
            self.supportlist[var2.name] = sup_y
            # for each edge (X,Y), check if any counter S(X,a,Y) = 0, add it to queue

    def step(self):
        #remove a variable from queue, delete it from domain, remove its constraints, propagate changes is support list.
        pass
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
    def step(self):
        
        return false

    def revise(self,d1,d2):
        
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
        # Printing current Working Queue
        txt = self.w.create_text(self.canvas_width/2,self.canvas_height-15,fill="darkblue",font="Times 15 bold",
                        text="Current Work Queue: {}".format([(str(x.name),str(y.name)) for x,y in self.algo.worklist]))
        # Plotting the current variables
        variables = sorted(list(self.algo.variables))
        n = len(variables)
        width_each = self.canvas_width/n
        r = lambda: random.randint(200,255) #light colours
        rd = lambda: random.randint(0,128) #dark colors
        start = 0
        val_locs = {} # Dict of Dicts, locations of all values of all variables
        for i in xrange(n):
            col = '#%02X%02X%02X' % (r(),r(),r())
            self.w.create_rectangle(start,0,start+width_each,self.canvas_height-50,fill=col)
            self.w.create_text(start+(width_each/2),20,fill="darkblue",font="Times 18 bold",text="Var: {}".format(variables[i].name))
    
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
                

        
        

def main():
    with open("csp2.json") as data_file:
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
    
    
########## AC3 ################
    ac = AC3(variables,constraints)
    gui = Graphic(1000,700,ac,300) #10000- delay in ms
###############################

########## AC4 ################
    # ac = AC4(variables,constraints)
    # print ac.get_supports_for_var(variables[0])
###############################
    


if __name__ == '__main__':
    main()