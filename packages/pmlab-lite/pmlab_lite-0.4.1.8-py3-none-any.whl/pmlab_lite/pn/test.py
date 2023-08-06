from pn import PetriNet
from tn import TraceNet
from sp import SynchronousProduct


net = PetriNet()
for i in range(1,5):
    net.add_place(i)
net.add_transition("a")
net.add_transition("b")
net.add_transition("c")
net.add_edge(1,-1)
net.add_edge(-1,2)
net.add_edge(2,-2)
net.add_edge(-2,3)
net.add_edge(3,-3)
net.add_edge(-3,4)
b = net.get_index_initial_places()
print(net)
print(b)
trace = ['a', 'b', 'c', 'd']
tnet = PetriNet()
print(tnet)

tt_net = TraceNet(trace)
print("\n", tt_net)
print("\n", tt_net.incidence_matrix())

sp_net = SynchronousProduct(net, tt_net)
print(sp_net)