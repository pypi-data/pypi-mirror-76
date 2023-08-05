from sidermit.optimization import InfrastructureCost, UsersCost, OperatorsCost
from sidermit.publictransportsystem import Passenger

from sidermit.city import Graph, Demand
from sidermit.publictransportsystem import TransportNetwork
from sidermit.optimization.preoptimization import Assignment, Hyperpath, ExtendedGraph
from sidermit.optimization import Constrains

from collections import defaultdict


class Optimizer:
    def __init__(self, graph_obj: Graph, demand_obj: Demand, passenger_obj: Passenger, network_obj: TransportNetwork,
                 f=None):

        # definimos ciudad
        self.graph_obj = graph_obj
        _, _, _, self.p, _, _, _, _, _ = self.graph_obj.get_parameters()
        # definimos demanda
        self.demand_obj = demand_obj
        # definimos pasajeros
        self.passenger_obj = passenger_obj
        self.vp = self.passenger_obj.va
        self.spa = self.passenger_obj.spa
        self.spv = self.passenger_obj.spv
        self.sPTP = self.passenger_obj.spt

        # definimos red de transporte
        self.network_obj = network_obj

        # definimos frecuencia
        if f is None:
            self.f, self.f_opt, self.lines_position = self.f0()
        else:
            self.f, self.f_opt, self.lines_position = self.fini(f)

        self.extended_graph_obj = ExtendedGraph(self.graph_obj, self.network_obj.get_routes(), self.sPTP, self.f)
        self.hyperpath_obj = Hyperpath(self.extended_graph_obj, self.passenger_obj)

        self.hyperpaths, self.labels, self.successors, self.frequency, self.Vij = self.hyperpath_obj.get_all_hyperpaths(
            self.demand_obj.get_matrix())

        self.assignment = Assignment.get_assignment(self.hyperpaths, self.labels, self.p, self.vp, self.spa, self.spv)

    def f0(self):
        fini = defaultdict(float)
        fopt = []
        lines_position = defaultdict(None)
        n = 0
        for route in self.network_obj.get_routes():
            fini[route.id] = route.mode.fini
            fopt.append(route.mode.fini)
            lines_position[n] = route.id
            n += 1

        return fini, fopt, lines_position

    def fini(self, f):
        fini = defaultdict(float)
        fopt = []
        lines_position = defaultdict(None)
        n = 0
        for route in self.network_obj.get_routes():
            fini[route.id] = f[route.id]
            fopt.append(route.mode.fini)
            lines_position[n] = route.id
            n += 1

        return fini, fopt, lines_position

    def fopt_to_f(self, fopt):
        f = defaultdict(float)
        n = 0
        for fr in fopt:
            f[self.lines_position[n]] = fr
            n += 1
        return f

    @staticmethod
    def get_k(routes, z, v):
        most_loaded_section = Assignment.most_loaded_section(routes, z, v)
        k = defaultdict(float)
        for route_id in most_loaded_section:
            k[route_id] = most_loaded_section[route_id]
        return k

    def operators_cost(self, z, v, f, k):
        operators_cost_obj = OperatorsCost()

        edge_distance = self.graph_obj.get_edges_distance()
        routes = self.network_obj.get_routes()
        line_travel_time = operators_cost_obj.lines_travel_time(routes, edge_distance)

        cycle_time = operators_cost_obj.get_cycle_time(z, v, routes, line_travel_time)
        cost = operators_cost_obj.get_operators_cost(routes, cycle_time, f, k)
        return cost

    def infrastructure_cost(self, f):
        infrastructure_cost_obj = InfrastructureCost()
        cost = infrastructure_cost_obj.get_infrastruture_cost(self.graph_obj, self.network_obj, f)
        return cost

    def user_cost(self, hyperpaths, Vij, assignment, successors, extended_graph: ExtendedGraph, f):
        user_cost_obj = UsersCost()
        cost = user_cost_obj.get_users_cost(hyperpaths, Vij, assignment, successors, extended_graph, f,
                                            self.passenger_obj)
        return cost

    def constrains(self, z, v, f):

        most_loaded_section = Assignment.most_loaded_section(self.network_obj.get_routes(), z, v)

        constrains_obj = Constrains()

        ineq_k = constrains_obj.most_loaded_section_constrains(self.network_obj.get_routes(), most_loaded_section)
        ineq_f = constrains_obj.fmax_constrains(self.graph_obj, self.network_obj.get_routes(),
                                                self.network_obj.get_modes(), f)

        return ineq_k, ineq_f

    def VRC(self, fopt):

        f = self.fopt_to_f(fopt)

        z, v = Assignment.get_alighting_and_boarding(self.Vij, self.hyperpaths, self.successors, self.assignment, f)
        k = self.get_k(self.network_obj.get_routes(), z, v)

        CO = self.operators_cost(z, v, f, k)
        CI = self.infrastructure_cost(f)
        CU = self.user_cost(self.hyperpaths, self.Vij, self.assignment, self.successors, self.extended_graph_obj, f)

        return CO + CI + CU

    def get_constrains(self, fopt):

        f = self.fopt_to_f(fopt)

        z, v = Assignment.get_alighting_and_boarding(self.Vij, self.hyperpaths, self.successors, self.assignment, f)

        most_loaded_section = Assignment.most_loaded_section(self.network_obj.get_routes(), z, v)
        constrain_obj = Constrains()
        ineq_k = constrain_obj.most_loaded_section_constrains(self.network_obj.get_routes(), most_loaded_section)
        ineq_f = constrain_obj.fmax_constrains(self.graph_obj, self.network_obj.get_routes(),
                                               self.network_obj.get_modes(), f)

        return ineq_k, ineq_f
