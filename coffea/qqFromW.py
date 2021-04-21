import awkward as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from coffea import hist, processor
import uproot
import numpy as np
import matplotlib.pyplot  as plt

# register our candidate behaviors
from coffea.nanoevents.methods import candidate
ak.behavior.update(candidate.behavior)

#fpath = '/store/mc/RunIIAutumn18NanoAODv7/WprimeToWhToWhadhbb_narrow_M-600_13TeV-madgraph/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/110000/D18D997D-2339-D24B-B286-50967A503E20.root'
fpath = '/home/alintulu/cernbox/2021/phd/jupyter/NanoAOD.root'
events = NanoEventsFactory.from_root(fpath, schemaclass=NanoAODSchema).events()

# only events with at least one W
events_W = events[ak.any(abs(events.GenPart.pdgId) == 24, axis=1)]

# cuts
is_W = abs(events_W.GenPart.pdgId) == 24
two_children = ak.num(events_W.GenPart.children.pdgId, axis=-1) == 2
two_quark_children = (ak.sum((abs(events_W.GenPart.children.pdgId) <= 8), axis=-1) == 2)

# WToqq with to quark children
WToqq = events_W.GenPart[is_W & two_quark_children & two_children]

# quark children
qqFromW = ak.flatten(WToqq.children)
jets = events_W.Jet

def delta_R(q, j):
    return np.sqrt((q.eta-j.eta)**2 + (q.phi-j.phi)**2)

# Number of events
E = 100
  
inv_mass = []
    
for k in range(E):
    
    # Declaring rows
    N = len(qqFromW[k])

    # Declaring columns
    M = len(jets[k])

    delta_Rs = np.empty((N, M))
    
    for i in range(N):
        for j in range(M):
            delta_Rs[i][j] = delta_R(qqFromW[k][i], jets[k][j])
            
    j_quark0, j_quark1 = ak.Array(np.argmin(delta_Rs, axis=-1))    
    inv_mass.append((jets[k][j_quark0]+jets[k][j_quark1]).mass)

inv_ms = ak.Array(inv_mass)

bin_min = ak.min(inv_ms)
bin_max = ak.max(inv_ms)

h = hist.Hist(
            "Two AK4 jets",
            hist.Cat("sample", "Sample"),
            hist.Bin("data", "mass", 50, bin_min, bin_max),
        )
h.fill(
        sample="Two AK4 jets",
        data=ak.Array(inv_ms),
       )
hist.plot1d(h)
#plt.show()
plt.savefig('qqFromW_invmass.png')