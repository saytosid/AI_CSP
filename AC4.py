import json
from Headers import Variable,Constraint,AC4,Graphic       

def main():
    with open("csp.json") as data_file:
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
    gui = Graphic(1000,700,ac,1000) #10000- delay in ms
###############################
    


if __name__ == '__main__':
    main()