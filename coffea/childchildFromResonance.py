import awkward as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from coffea import hist, processor
import uproot
from coffea.nanoevents import NanoEventsFactory, BaseSchema
import matplotlib.pyplot as plt
import numpy as np
from coffea.nanoevents.methods import candidate
ak.behavior.update(candidate.behavior)

#fpath = '/store/mc/RunIIAutumn18NanoAODv7/WprimeToWhToWhadhbb_narrow_M-600_13TeV-madgraph/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/110000/D18D997D-2339-D24B-B286-50967A503E20.root'
fpath = '/home/alintulu/cernbox/2021/phd/jupyter/NanoAOD.root'
events = NanoEventsFactory.from_root(fpath, schemaclass=NanoAODSchema).events()

events_geq1res = events[ak.any(abs(events.GenPart.pdgId) == 9000002, axis=1)]
last_res = events_geq1res.GenPart[abs(events_geq1res.GenPart.pdgId) == 9000002][:,-1]
last_res_child_comb = last_res.children[:,0] + last_res.children[:,1]

data = last_res.eta
child_data = last_res_child_comb.eta

var = "eta"

bin_min = ak.min(child_data)
bin_max = ak.max(child_data)

h = hist.Hist(
            "Last 9000002 in decay chain",
            hist.Cat("sample", "Sample"),
            hist.Bin("res", "{0}".format(var), 50, bin_min, bin_max),
        )
h.fill(
        sample="9000002",
        res=data,
        )
h.fill(
        sample="9000002 child1 + child2",
        res=child_data,
        )
hist.plot1d(h)
#plt.show()
plt.savefig('9000002_{0}.png'.format(var))
