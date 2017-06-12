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


class Graphic:
    def __init__(self,canvas_width,canvas_height,algo,timer):
        self.val_locs = {}
        self.firsttime = True
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
        rd = lambda: random.randint(0,90) #dark colors
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
            for val in sorted(values):
                # val = values[j]
                if self.firsttime == False:
                    loc = self.val_locs[variables[i].name][val]
                else:
                    loc = (start+(width_each/2),start_y)
                self.w.create_text(loc[0],loc[1],fill = col,font="Times 25 bold underline",text=val)
                if self.algo.name =="ac4":
                    if val==removed_val_ac4 and variables[i].name==removed_var_ac4:
                        self.w.create_oval(loc[0]-12*len(val),loc[1]-12,
                                    loc[0]+12*len(val),loc[1]+12,width=4,outline="red")
                
                
                locs[val] = loc
                start_y += height_each
            if self.firsttime:
                self.val_locs[variables[i].name] = locs
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
                y_shift = random.randint(-20,20)
                col = '#%02X%02X%02X' % (rd(),rd(),rd())
                self.w.create_line(coordinates1[0],coordinates1[1]+y_shift,coordinates2[0],coordinates2[1]+y_shift,fill=col,dash=(10,5))
        self.firsttime = False
        ########## Algo ##########
        if self.algo.step()==True:
            self.master.after(self.timer,self.redraw)
        else:
            self.w.create_text(self.canvas_width/2,self.canvas_height/2,fill="green",font="Times 35 bold",
                                    text="DONE")
            for i in self.algo.variables:
                i.print_stats() 