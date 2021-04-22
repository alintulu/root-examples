from TIMBER.Analyzer import analyzer

fpath = '/store/mc/RunIIAutumn18NanoAODv7/WprimeToWhToWhadhbb_narrow_M-600_13TeV-madgraph/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/110000/D18D997D-2339-D24B-B286-50967A503E20.root'
a = analyzer(fpath)

a.Define("q_bools", "abs(GenPart_pdgId)<6") # [True False False True ...]
a.Define("q_idxMother", "GenPart_genPartIdxMother[q_bools]") # GenPart indices
a.Define("q_mothers_pdgId", "ROOT::VecOps::Take(GenPart_pdgId, q_idxMother)") # PDG IDs of mothers of particles from previous step
a.Define("qFromW", "abs(q_mothers_pdgId) == 24") # [False True ...]
a.Cut("qqFromW", "ROOT::VecOps::Sum(qFromW) == 2") # Count the above

h = a.DataFrame.Histo1D('GenPart_pt')
h.Draw('histe')
