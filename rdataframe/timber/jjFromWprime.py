from TIMBER.Analyzer import analyzer
import ROOT

fpath = '/eos/user/a/adlintul/SWAN_projects/RDataFrame-test/NanoAOD.root'
a = analyzer(fpath)

a.Cut('Two FatJets', 'nFatJet==2') # Cut events
a.Cut('|Eta| < 2.4','abs(FatJet_eta[0]) < 2.4 && abs(FatJet_eta[1]) < 2.4') # Cut events
a.Cut('Pt > 200','FatJet_pt[0] > 200 && FatJet_pt[1] > 200') # Cut events
a.Define("Dijet_mass", "InvariantMass(FatJet_pt, FatJet_eta, FatJet_phi, FatJet_mass)") # [Mass Mass Mass ...] 
a.Define('Dijet_deltaR', 'DeltaR(FatJet_eta[0], FatJet_eta[1], FatJet_phi[0], FatJet_phi[1])') # [deltaR, deltaR, deltaR ...]
a.Define('Dijet_deltaPhi', 'DeltaPhi(FatJet_phi[0], FatJet_phi[1])') # [deltaPhi, deltaPhi, deltaPhi ...]
a.Define('Dijet_deltaEta', 'DeltaPhi(FatJet_eta[0], FatJet_eta[1])') # [deltaEta, deltaEta, deltaEta ...]
a.Cut('deltaR < 3.7', 'Dijet_deltaR < 3.7') # Cut events
a.Cut('|deltaEta| < 2', 'abs(Dijet_deltaEta) < 2') # Cut events

c0 = ROOT.TCanvas("c", "", 800, 700)
h = a.DataFrame.Histo1D('Dijet_mass')
h.Draw('histe')
c0.SaveAs("plots/invmass/dijet_mass_cutEtaPtDeltaRDeltaEta.png")

# c1 = ROOT.TCanvas("c", "", 800, 700)
# g1 = a.DataFrame.Graph("Dijet_mass", "Dijet_deltaR")
# g1.SetMarkerSize(3)
# g1.SetMarkerStyle(7)
# g1.Draw("AP")
# c1.SaveAs("plots/2d/dijet_2D_massVsdeltaR_cut.png")

# c2 = ROOT.TCanvas("c", "", 800, 700)
# g2 = a.DataFrame.Graph("Dijet_mass", "Dijet_deltaPhi")
# g2.SetMarkerSize(3)
# g2.SetMarkerStyle(7)
# g2.Draw("AP")
# c2.SaveAs("plots/2d/dijet_2D_massVsdeltaPhi.png")

c3 = ROOT.TCanvas("c", "", 800, 700)
g3 = a.DataFrame.Graph("Dijet_mass", "Dijet_deltaEta")
g3.SetMarkerSize(3)
g3.SetMarkerStyle(7)
g3.Draw("AP")
c3.SaveAs("plots/2d/dijet_2D_massVsdeltaEta_cut.png")

#raw_input('')

# Two slim jets would be one W rather than one fat jet
# For each event look at the W or Higgs boson candidate, if it's not around the mass
# try if you can combine the mass of two small jets to the match the W'
# See if you find the critera to find the right combination
# delta eta, delta phi (absolute value), delta R is sqrt (delta eta^2 + delta phi^2)
# 2D-plot - delta R - invariant mass of the two jets, pattern?
# Make cut on the pt
# Make cut on (delta)phi and (delta)eta
# Plot inv mass vs delta phi and delta eta