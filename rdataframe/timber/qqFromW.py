from TIMBER.Analyzer import analyzer
import ROOT

ROOT.gInterpreter.Declare('''
using Vec_t = const ROOT::RVec<float>&;
float ComputeInvariantMass(Vec_t pt, Vec_t eta, Vec_t phi, Vec_t mass) {
    const ROOT::Math::PtEtaPhiMVector p1(pt[0], eta[0], phi[0], mass[0]);
    const ROOT::Math::PtEtaPhiMVector p2(pt[1], eta[1], phi[1], mass[1]);
    return (p1 + p2).M();
}
''')

fpath = '/eos/user/a/adlintul/SWAN_projects/RDataFrame-test/NanoAOD.root'
a = analyzer(fpath)

#--------------------------------------------------------------
# Find all quarks with W parent

a.Define('q_bools', 'abs(GenPart_pdgId)<6') # [[True False False True ...]]
a.Define('q_idxMother', 'GenPart_genPartIdxMother[q_bools]') # [[GenPart indices GenPart indices GenPart indices ...]]
a.Define('q_mothers_pdgId', 'Take(GenPart_pdgId, q_idxMother)') # [[PDG IDs of mothers of particles from previous step ...]]
a.Define('qFromW_bools', 'abs(q_mothers_pdgId) == 24') # [[False True ...]]
#--------------------------------------------------------------

#--------------------------------------------------------------
# Get kinematics of quarks with W parent

a.Define('q_pt', 'GenPart_pt[q_bools]')
a.Define('qFromW_pt', 'q_pt[qFromW_bools]')

a.Define('q_eta', 'GenPart_eta[q_bools]')
a.Define('qFromW_eta', 'q_eta[qFromW_bools]')

a.Define('q_phi', 'GenPart_pt[q_bools]')
a.Define('qFromW_phi', 'q_phi[qFromW_bools]')

a.Define('q_mass', 'GenPart_mass[q_bools]')
a.Define('qFromW_mass', 'q_mass[qFromW_bools]')
#--------------------------------------------------------------

#--------------------------------------------------------------
# Cut events without two quarks origintaing from W

a.Cut('qqFromW', 'Sum(qFromW_bools) == 2') # Cut events
a.Cut('|eta| < 2.4', 'abs(qFromW_eta[0]) < 2.4 && abs(qFromW_eta[1]) < 2.4') # Cut events
#--------------------------------------------------------------

#--------------------------------------------------------------
# Compute invariant mass of quarks

a.Define('qqFromW_invmass', 'ComputeInvariantMass(qFromW_pt, qFromW_eta, qFromW_phi, qFromW_mass)')
#--------------------------------------------------------------


c0 = ROOT.TCanvas('c', '', 800, 700)
h = a.DataFrame.Histo1D('qqFromW_invmass')
h.Draw('histe')
c0.SaveAs("plots/qqFromW/qqFromW_invmass.png")

#raw_input('')

# Find W
# Check W daughters
# Find W that have at least two quark daughters
# Plot Generator_Q Generator x1 x2