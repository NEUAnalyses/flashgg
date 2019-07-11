import subprocess
import FWCore.ParameterSet.Config as cms
import os
import FWCore.ParameterSet.VarParsing as VarParsing

from flashgg.Taggers.flashggH4GCandidate_cfi import FlashggH4GCandidate
from flashgg.Taggers.flashggPreselectedDiPhotons_cfi import flashggPreselectedDiPhotons
from flashgg.Taggers.flashggPreselectedDiPhotons_LowMass_cfi import flashggPreselectedDiPhotonsLowMass
import flashgg.Taggers.dumperConfigTools as cfgTools

process = cms.Process("FLASHggH4GTest")


from flashgg.MetaData.JobConfig import customize

customize.options.register('stdDumper',
                 '',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "stdDumper")

customize.options.register('vtxBDTDumper',
                 '',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "vtxBDTDumper")

customize.options.register('vtxProbDumper',
                 '',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "vtxProbDumper")

customize.options.register('isCondor',
                 '',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "isCondor")


from flashgg.MetaData.JobConfig import customize
customize.parse()

###---H4G candidates production
process.FlashggH4GCandidate = FlashggH4GCandidate.clone()
process.FlashggH4GCandidate.idSelection = cms.PSet(
        rho = flashggPreselectedDiPhotonsLowMass.rho,
        cut = flashggPreselectedDiPhotonsLowMass.cut,
        variables = flashggPreselectedDiPhotonsLowMass.variables,
        categories = flashggPreselectedDiPhotonsLowMass.categories
        )

###--- get the variables
import flashgg.Taggers.H4GTagVariables as var
vtx_BDT_variables_sig = var.vtx_BDT_variables_sig
vtx_BDT_variables_bkg = var.vtx_BDT_variables_bkg
vtxProb_BDT_variables = var.vtx_variables + var.vtxProb_BDT_variables
all_variables = var.pho_variables + var.dipho_variables + var.vtx_variables + var.tp_variables

from flashgg.Taggers.h4gCandidateDumper_cfi import h4gCandidateDumper

process.h4gCandidateDumper_vtxBDT_sig = h4gCandidateDumper.clone()
process.h4gCandidateDumper_vtxBDT_sig.dumpTrees = True
process.h4gCandidateDumper_vtxBDT_sig.dumpWorkspace = False


cfgTools.addCategories(process.h4gCandidateDumper_vtxBDT_sig,
                        [
                            ("Reject", "", -1),
                            ("4photons_sig","phoVector.size() > 3"),
                            ("3photons_sig","phoVector.size() == 3", 0),
                            ("2photons_sig","phoVector.size() == 2", 0)
                        ],
                        variables = vtx_BDT_variables_sig,
                        histograms=[]
                        )


process.h4gCandidateDumper_vtxBDT_bkg = h4gCandidateDumper.clone()
process.h4gCandidateDumper_vtxBDT_bkg.dumpTrees = True
process.h4gCandidateDumper_vtxBDT_bkg.dumpWorkspace = False

cfgTools.addCategories(process.h4gCandidateDumper_vtxBDT_bkg,
                        [
                            ("Reject", "", -1),
                            ("4photons_bkg","phoVector.size() > 3"),
                            ("3photons_bkg","phoVector.size() == 3", 0),
                            ("2photons_bkg","phoVector.size() == 2", 0)
                        ],
                        variables = vtx_BDT_variables_bkg,
                        histograms=[]
                        )

process.h4gCandidateDumper_vtxProb = h4gCandidateDumper.clone()
process.h4gCandidateDumper_vtxProb.dumpTrees = True
process.h4gCandidateDumper_vtxProb.dumpWorkspace = False

cfgTools.addCategories(process.h4gCandidateDumper_vtxProb,
                        [
                            ("Reject", "", -1),
                            ("4photons","phoVector.size() > 3"),
                            ("3photons","phoVector.size() == 3", 0),
                            ("2photons","phoVector.size() == 2", 0)
                        ],
                        variables = vtxProb_BDT_variables,
                        histograms=[]
                        )

process.h4gCandidateDumper = h4gCandidateDumper.clone()
process.h4gCandidateDumper.dumpTrees = True
process.h4gCandidateDumper.dumpWorkspace = False

cfgTools.addCategories(process.h4gCandidateDumper,
                       [
                            ("Reject", "", -1),
                            ("4photons","phoVector.size() > 3 "),
                            # ("4photons","phoVector.size() > 3 && phoP4Corrected[0].pt() > 30 && phoP4Corrected[1].pt() > 20 && phoP4Corrected[2].pt() > 10 && phoP4Corrected[3].pt() > 10 && abs(phoP4Corrected[0].eta()) < 2.5 && abs(phoP4Corrected[1].eta()) < 2.5 && abs(phoP4Corrected[2].eta()) < 2.5 && abs(phoP4Corrected[3].eta()) < 2.5 && pho1_MVA > -0.9 && pho2_MVA > -0.9 && pho3_MVA > -0.9 && pho4_MVA > -0.9 && h4gFourVect.mass() > 100 && h4gFourVect.mass() < 180", 0),
                            ("3photons","phoVector.size() == 3", 0),
                            ("2photons","phoVector.size() == 2", 0)
                        ],
                        variables = all_variables,
                        histograms=[]
                        )
# from flashgg.MetaData.JobConfig import customize

# files = []
# secondary_files = []

# for d in customize.inputdataset:
#     print('>> Creating list of files from: \n'+d)
#     # for instance in ['global', 'phys03']:
#     for instance in ['phys03']:
#         print "-query='file dataset="+d+" instance=prod/"+instance+"'"
#         query = "-query='file dataset="+d+" instance=prod/"+instance+"'"
#         print query
#         print 'dasgoclient '+query+' -limit=0'
#         lsCmd = subprocess.Popen(['dasgoclient '+query+' -limit=0'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, close_fds=True)
#         print lsCmd
#         str_files, err = lsCmd.communicate()
#         print str_files
#         print err
#         for ifile in str_files.split("\n"):
#             print 'root://cms-xrd-global.cern.ch/'+ifile
#         files.extend(['root://cms-xrd-global.cern.ch/'+ifile for ifile in str_files.split("\n")])
#         files.pop()
#         print files
#         for file in files:
#             print "file = ", file
#             print file[len('root://cms-xrd-global.cern.ch/'):]
#             query = "-query='parent file="+file[len('root://cms-xrd-global.cern.ch/'):]+" instance=prod/"+instance+"'"
#             lsCmd = subprocess.Popen(['dasgoclient '+query+' -limit=0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#             str_files, err = lsCmd.communicate()
#             secondary_files.extend(['root://cms-xrd-global.cern.ch/'+ifile for ifile in str_files.split("\n")])
#             secondary_files.pop()

# for f in files:
#     print f
#     print " "
#
# for s in secondary_files:
#     print s
#     print " "
# process.source.secondaryFileNames = secFileList
process.source = cms.Source ("PoolSource",
                             # fileNames = cms.untracked.vstring(files),
                             # secondaryFileNames = cms.untracked.vstring(secondary_files)
                             fileNames = cms.untracked.vstring(
"root://eoscms.cern.ch//eos/cms/store/group/phys_higgs/HiggsExo/H4Gamma/MicroAOD/H4G_Jun7/v0/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8/Test_jun7-R2S16MAODv2-PUM17_GT/170607_180035/0000/myMicroAODOutputFile_9.root"),
                             secondaryFileNames = cms.untracked.vstring("root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/C85D3FF6-84C8-E611-B11D-D4AE526A0B29.root")
)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("test.root"),
                                   closeFileFast = cms.untracked.bool(True)
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

if customize.inputFiles:
    inputFile = customize.inputFiles

# Require low mass diphoton triggers
from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.hltHighLevel= hltHighLevel.clone(HLTPaths = cms.vstring(
                                                              # "HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v*",
                                                              # "HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90", ##--std Hgg diphoton trigger
                                                              "HLT_Diphoton30PV_18PV_R9Id_AND_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55_v*", ##--low mass trigger
                                                              "HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55_v*"   ##--low mass diphoton trigger
                                                               ))
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

#############   Geometry  ###############
process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi")
process.load("Geometry.CaloEventSetup.CaloGeometry_cfi")
process.load("Geometry.CaloEventSetup.CaloTopology_cfi")
process.load('RecoMET.METFilters.eeBadScFilter_cfi')
process.load("Configuration.Geometry.GeometryECALHCAL_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

process.eeBadScFilter.EERecHitSource = cms.InputTag("reducedEgamma","reducedEERecHits") # Saved MicroAOD Collection (data only)

process.dataRequirements = cms.Sequence()
# process.dataRequirements += process.hltHighLevel
if customize.processId == "Data":
   process.dataRequirements += process.hltHighLevel
   process.dataRequirements += process.eeBadScFilter

process.load("flashgg/Taggers/vtxH4GSequence")

if customize.stdDumper:
   #standard dumper sequence
   process.path = cms.Path(process.vtxH4GSequence*process.dataRequirements*process.FlashggH4GCandidate*process.h4gCandidateDumper)

if customize.vtxBDTDumper:
   #vtxBDT dumper sequence
   process.path = cms.Path(process.vtxH4GSequence*process.dataRequirements*process.FlashggH4GCandidate*process.h4gCandidateDumper_vtxBDT_sig*process.h4gCandidateDumper_vtxBDT_bkg)

if customize.vtxProbDumper:
   #vtxProb dumper sequence
   process.path = cms.Path(process.vtxH4GSequence*process.dataRequirements*process.FlashggH4GCandidate*process.h4gCandidateDumper_vtxProb)

if customize.isCondor:
   customize(process)
