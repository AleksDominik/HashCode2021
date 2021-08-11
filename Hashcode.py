import queue
import typing
from itertools import accumulate
import math, random, itertools

class Car:
    """
    Car class
    """
    def __init__(self, Route, priority, status, path):
        self.Route=Route    #routeactuelle( only the name)
        self.Time_end= 0 # initialisé a la fin
        self.path=path # array of name of route
        self.status= status#'termine', 'start','onroute','onqueue'
        self.time_spend_on_the_road=0
        self.priority=priority
        self.path_queue=queue.Queue()
        for path_ in self.path:
            self.path_queue.put(path_)

    def display(self):
        print(f' This is a car with the actual route has given { self.Route} the time of  arrival {self.Time_end}, the path {self.path}, the status {self.status} the priority {self.priority}, the time spend on route is {self.time_spend_on_the_road}')

class Route:
    """
    Route classe
    """
    def __init__(self, K,name, intersection) :
        self.Longueur=int(K)  #given
        self.queue= queue.Queue()
        self.name=name
        self.intersection=intersection # intersection where route end
    def display(self):
        print(f'the Route is length { self.Longueur} the name {self.name}')



class Intersection :
    """
    Class for intersection

    """
    def __init__(self,income, outcome, schedule, index_of_intersection):
        self.income=income
        self.outcome=outcome
        self.schedule=schedule  #((name, int))
        self.index_time= list(accumulate([k[1] for k in self.schedule]))
        # print(sum( [[k[1] for k in self.schedule]]))
        self.sum_time=sum(  [int(k[1]) for k in self.schedule] )
        self.internal_time=0 #
        self.index_of_intersection=index_of_intersection
        self.can_go_through=True

    def initialize_schedule(self,top_time):
        """
        initialize self.schedule to a list of list
        (
            (name of the street, temp of green ligth)
        )
        the order matter
        # TODO in mutation think at a swaping operation to change the order of the street in the schedule.
        """
        self.sum_time=0
        while self.sum_time==0:
            self.schedule=[]
            for name in [k.name for k in self.income]:
                self.schedule.append((name, random.randint(0,top_time)))
            print(f' the schedule is {self.schedule} ')
            self.sum_time=sum(  [int(k[1]) for k in self.schedule] )

        self.index_time= list(accumulate([k[1] for k in self.schedule]))



    def which_road_is_green(self,TIME):
        """
        function that manage the schedule for infor management
        """
        mod= TIME%self.sum_time
        # print(self.sum_time)
        # print(f'the modulo is {mod}')
        # print(self.index_time)
        # print({f'the index time is {self.index_time}'})
        l= [k for k in self.schedule if k[1]!=0]
        index=list(accumulate([k[1] for k in l]))
        print(self.index_time)
        for k in range(len(index)):
            if mod <index[0]:
                return l[0]

            elif index[k]<=mod<index[k+1]:
                return l[k+1]

    def display(self):
        print('Intersection: the routes in the income are')
        for route in self.income:
            route.display()
        print('Intersection: the routes in the outcome are')
        for route in self.outcome:
            route.display()
        print( "the schedule is ")
        print(self.schedule)

class Reseau:
    """
    Network classes handle the env for simulation 
    """
    def __init__(self,file):
        f=file

        lines= f.readlines()
        # print(lines)
        lines=[k.replace('\n', '').split(' ') for k in lines]
        self.lines=lines
        first_line=lines[0]
        time_of_simulation,numbers_of_intersection, numbers_of_streets, numbers_of_cars, D=[int(k) for k in first_line]
        self.numbers_of_streets=numbers_of_streets
        # print(time_of_simulation,numbers_of_intersection, numbers_of_streets, numbers_of_cars, D )

        list_intersection= [ Intersection( [],[],[], i) for i in range(numbers_of_intersection)]
        table_of_routes={}
        list_of_cars= []

        for index_inter, line in enumerate(lines[1:numbers_of_streets+1]):
            """
            initialise the route and intersection
            """
            # print(line)
            table_of_routes[line[2]]=Route( line[-1], line[2],list_intersection[int(line[1])],)
            list_intersection[ int(line[1])  ].outcome.append( table_of_routes[line[2]])
            list_intersection[int(line[1])].income.append(table_of_routes[line[2]])



        #TODO initialize schedule

        for intersection in list_intersection:
            intersection.initialize_schedule(time_of_simulation/2)
            intersection.display()

        for priority, line in enumerate(lines[numbers_of_streets+1:]):
            list_of_cars.append(Car(line[1],priority, 'start', line[1:]))
        # print( list_of_cars)

        self.tableau_des_routes=table_of_routes
        self.tableau_des_intersections= list_intersection
        self.Temps_de_simulation=time_of_simulation
        self.tableau_des_cars=list_of_cars
        self.D=D
        self.Gain=int(first_line[-1])

    def __forwad_car__(self,Car_:Car, TIME):
        print('dddkdkd')
        print(self.tableau_des_routes[Car_.Route].intersection.which_road_is_green(TIME))
        is_green= self.tableau_des_routes[Car_.Route].intersection.which_road_is_green(TIME)[0]==Car_.Route
        Car_.time_spend_on_the_road+=1
        can_go_through= self.tableau_des_routes[Car_.Route].intersection.can_go_through==True
        if Car_.status=='start'   and is_green and  can_go_through:
            print("voiture en position")
            Car_.Route=Car_.path_queue.get(False)#the next one
            self.tableau_des_routes[Car_.Route].intersection.can_go_through=False
            Car_.status='onroute'
        elif Car_.status=="onroute":
            print('car on track')
            # print('erererere')
            # print(Car_.time_spend_on_the_road)
            # print(self.tableau_des_routes[Car_.Route].Longueur)
            if Car_.time_spend_on_the_road>=self.tableau_des_routes[Car_.Route].Longueur:
                if Car_.path_queue.empty():
                    Car_.status='termine'
                    Car_.Time_end=TIME
                else:
                    #TODO:end with queue empty and status onqueue
                    Car_.status='onqueue'

        elif Car_.status=='onqueue' and is_green and can_go_through:
            print('car waiting')
            try:
                 Car_.Route=Car_.path_queue.get(False)
                 self.tableau_des_routes[Car_.Route].intersection.can_go_through=False
                 Car_.status='onroute'
            except:
                print('car arrived finally ///////////////////')
                Car_.status='termine'
                Car_.Time_end=TIME
        else:
            print('nothing happen to this car')

    def __score_car__(self,Car):
        """
        Compute the gained score of a car
        """
        if Car.status=='termine':
            return  self.Gain +(self.D -Car.Time_end)
        else:
            return 0
        



    def initialisation():
     pass
    def simuler(self):
        """
        performance du reseau
        """
        list_of_cars=[]
        for priority, line in enumerate(self.lines[self.numbers_of_streets+1:]):
            list_of_cars.append(Car(line[1],priority, 'start', line[1:]))
        self.tableau_des_cars=list_of_cars
        for time in range(self.Temps_de_simulation-1):
            for inter in self.tableau_des_intersections:
                inter.can_go_through=True

            for car in self.tableau_des_cars:
                print("avancement de la voiture")
                # car.display()
                self.__forwad_car__(car, time)
        
        for car in self.tableau_des_cars:
            print('eeeee')
            print(list(car.path_queue.queue))
            car.display()
        for inter in self.tableau_des_intersections:
            print(inter.schedule)
        self.points= sum([self.__score_car__(car) for car in self.tableau_des_cars])
        print(f'the points of this simulation are {self.points}')



    def mutation(self , with_swaping=False):
        list_int_to_mod=random.choices(self.tableau_des_intersections,k=int(len(self.tableau_des_intersections)/2))
        print(f'mutation on {list_int_to_mod}')
        for inter in list_int_to_mod:
            inter.sum_time=0
            while inter.sum_time==0:
                inter.schedule= [(name, math.fabs(  int(time+random.uniform(-2,+2))))  for name,time in inter.schedule]
                inter.sum_time=sum(  [int(k[1]) for k in inter.schedule] )
                inter.index_time= list(accumulate([k[1] for k in inter.schedule]))
                if with_swaping and len(inter.schedule)>1:
                    permutations=list(itertools.permutations(range(len(inter.schedule)),2))
                    print('perm')
                    print(permutations)
                    random.shuffle(permutations)
                    permutations=random.choices(permutations,k=int(len(permutations)/2)  )
                    for a,b in permutations:
                        tmp=inter.schedule[a]
                        inter.schedule[a]=inter.schedule[b]
                        inter.schedule[b]=tmp
                    inter.index_time= list(accumulate([k[1] for k in inter.schedule]))
                    
        
            
    def reproduction(self, Reseau ):
     pass

if  __name__=='__main__':
    R=Reseau(open('a.txt', 'r'))

    nombre_de_generation=2
    nombre_de_population=4
    R.simuler()
    R.mutation(with_swaping=True)
    R.simuler()








