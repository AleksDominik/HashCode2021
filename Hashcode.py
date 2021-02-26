import queue
import typing

class Car:
    def __init__(self, Route, priority, status, path):
        self.Route=Route    #routeactuelle
        self.Time_end= 0 # initialisé a la fin
        self.path=path
        self.status= status#'termine', 'start','onroute'
        self.time_spend_on_the_road=0 
        self.priority=priority
    def avancer(self):
        if self.Status=='start': #and self.Route.intersection.schedule[self.Route.name]:
            #self.Route.queue
            pass
    def display(self):
        print(f' This a car with the actual route has given { self.Route} the time of  arrival {self.Time_end}, the path {self.path}, the status {self.status} the priority {self.priority} ')

class Route:
    def __init__(self, K,name, intersection) : 
        self.Longueur=K  #given
        self.queue= queue.Queue()
        self.name=name
        self.intersection=intersection # intersection where route end
    def display(self):
        print(f'the Route is length { self.Longueur} the name {self.name}')



class Intersection :
    def __init__(self,income, outcome, schedule):
        self.income=income
        self.outcome=outcome
        self.schedule=schedule  #((name, int))
        self.internal_time=0
    def which_road_is_green():
        pass
    def display(self):
        print('Intersection: the routes in the income are')
        for route in self.income:
            route.display()
        print('Intersection: the routes in the outcome are')
        for route in self.outcome:
            route.display()

class Reseau:
    def __init__(self, tableau_des_route, tableau_des_intersections,T):


        self.tableau_des_route=tableau_des_route
        self.tableau_des_intersections= tableau_des_intersections
        self.Temps_de_simulation=T


    def initialisation():
     pass 
    def  simuler():
        """
        performance du reseau
        """
        for indice in range(self.Temps_de_simulation-1):
            for cars in self.tableau_des_voitures:
                cars.avancer()
            


    def mutation(self ):
     pass
    
    def reproduction(self, Reseau ):
     pass

if  __name__=='__main__':

    f=open('a.txt', 'r')
    lines= f.readlines()
    lines=[k.replace('\n', '').split(' ') for k in lines]
    first_line=lines[0]
    time_of_simulation,numbers_of_intersection, numbers_of_streets, numbers_of_cars, D=[int(k) for k in first_line]
    print(time_of_simulation,numbers_of_intersection, numbers_of_streets, numbers_of_cars, D )


    list_intersection= [ Intersection( [],[],{}) for _ in range(numbers_of_intersection)]
    list_of_routes=[]
    list_of_cars= []

    for line in lines[1:numbers_of_streets+1]:
        """
        initialise the route and intersection
        """
        #print(line)
        # print(line)
        list_of_routes.append(Route( line[-1], line[2],list_intersection[int(line[1])]) ) 
        list_intersection[ int(line[0])].outcome.append( list_of_routes[-1])
        list_intersection[int(line[1])].income.append(list_of_routes[-1])

    for index, intersection in enumerate( list_intersection):
        print(index)
        intersection.display()
    for priority, line in enumerate(lines[numbers_of_streets+1:]):
        list_of_cars= [ Car(line[0],priority, 'start', line[1:])]
    for car in list_of_cars:
        car.display()
    print(list_intersection, list_of_routes)
    nombre_de_generation=2
    nombre_de_population=4
    # Population=[Reseau()  for k in range(nombre_de_generation)]

    for  indice in range(nombre_de_generation):
        pass
    







