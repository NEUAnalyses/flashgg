import subprocess
import FWCore.ParameterSet.Config as cms
import os
# from FWCore.ParameterSet.VarParsing import VarParsing
import FWCore.ParameterSet.VarParsing as VarParsing

from flashgg.Taggers.flashggH4GCandidate_cfi import FlashggH4GCandidate
from flashgg.Taggers.flashggPreselectedDiPhotons_cfi import flashggPreselectedDiPhotons
from flashgg.Taggers.flashggPreselectedDiPhotons_LowMass_cfi import flashggPreselectedDiPhotonsLowMass
import flashgg.Taggers.dumperConfigTools as cfgTools

# from secFiles import secFileList

# print secFileList

process = cms.Process("FLASHggH4GTest")


from flashgg.MetaData.JobConfig import customize
# customize.options.register('inputdataset',
#                 '',
#                 VarParsing.VarParsing.multiplicity.list,
#                 VarParsing.VarParsing.varType.string,
#                 "Input dataset(s)")

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

customize.options.register('PURW',
		          1,
		          VarParsing.VarParsing.multiplicity.singleton,
		          VarParsing.VarParsing.varType.bool,
		          "Do PU reweighting")

from flashgg.MetaData.JobConfig import customize

customize.setDefault("maxEvents",-1)
customize.setDefault("targetLumi",1e+3)
customize.setDefault("puTarget",'2.39e+05,8.38e+05,2.31e+06,3.12e+06,4.48e+06,6e+06,7e+06,1.29e+07,3.53e+07,7.87e+07,1.77e+08,3.6e+08,6.03e+08,8.77e+08,1.17e+09,1.49e+09,1.76e+09,1.94e+09,2.05e+09,2.1e+09,2.13e+09,2.15e+09,2.13e+09,2.06e+09,1.96e+09,1.84e+09,1.7e+09,1.55e+09,1.4e+09,1.24e+09,1.09e+09,9.37e+08,7.92e+08,6.57e+08,5.34e+08,4.27e+08,3.35e+08,2.58e+08,1.94e+08,1.42e+08,1.01e+08,6.9e+07,4.55e+07,2.88e+07,1.75e+07,1.02e+07,5.64e+06,2.99e+06,1.51e+06,7.32e+05,3.4e+05,1.53e+05,6.74e+04,3.05e+04,1.52e+04,8.98e+03,6.5e+03,5.43e+03,4.89e+03,4.52e+03,4.21e+03,3.91e+03,3.61e+03,3.32e+03,3.03e+03,2.75e+03,2.47e+03,2.21e+03,1.97e+03,1.74e+03,1.52e+03,1.32e+03,1.14e+03,983,839')
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

process.h4gCandidateDumper.puReWeight=cms.bool(bool(customize.PURW))
if customize.PURW == False:
    process.h4gCandidateDumper.puTarget = cms.vdouble()

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
from flashgg.MetaData.JobConfig import customize

# files = []
# secondary_files = []
# files = ['/store/group/phys_higgs/HiggsExo/H4Gamma/MicroAOD/H4G_Jun7/v0/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8/Test_jun7-R2S16MAODv2-PUM17_GT/170607_180035/0000/myMicroAODOutputFile_9.root','/store/group/phys_higgs/HiggsExo/H4Gamma/MicroAOD/H4G_Jun7/v0/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8/Test_jun7-R2S16MAODv2-PUM17_GT/170607_180035/0000/myMicroAODOutputFile_8.root']
# secondary_files = ['/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/4EB38CC4-8DC8-E611-8B4E-F832E4CC4E51.root','/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/56121268-20C9-E611-9FC8-00266CFB9534.root','/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/6C3EB31D-0CC7-E611-BC45-02163E012E44.root','/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/6CFF7ADF-83C8-E611-8A14-008CFA0A5740.root','/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/9A344F39-25C8-E611-9A75-0CC47A706DC0.root','/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/A60237A4-1FC9-E611-9195-848F69FD29B2.root','/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/A8CBC588-3CC8-E611-8BE1-FA163E61F211.root','/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/C85D3FF6-84C8-E611-B11D-D4AE526A0B29.root','/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/56D830B2-83C8-E611-A696-FA163EB2D67F.root','/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/F28A073D-9CC8-E611-9302-0025905C975C.root','/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/56D830B2-83C8-E611-A696-FA163EB2D67F.root','/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/56121268-20C9-E611-9FC8-00266CFB9534.root','/store/mc/RunIISummer16MiniAODv2/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/4EB38CC4-8DC8-E611-8B4E-F832E4CC4E51.root']

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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

##--import flashgg customization
# from flashgg.MetaData.JobConfig import customize
# import FWCore.ParameterSet.VarParsing as VarParsing

##--set default options
# customize.setDefault("maxEvents",-1)
# customize.setDefault("targetLumi",1e+3)
# customize.register('PURW',
# 				1,
# 				VarParsing.VarParsing.multiplicity.singleton,
# 				VarParsing.VarParsing.varType.bool,
# 				"Do PU reweighting? Doesn't work on 76X")

##--call the customization
# customize(process)
# process.h4gCandidateDumper.puReWeight=cms.bool(bool(customize.PURW))
# if customize.PURW == False:
	# process.h4gCandidateDumper.puTarget = cms.vdouble()
#customize.setDefault("puTarget",'2.39e+05,8.38e+05,2.31e+06,3.12e+06,4.48e+06,6e+06,7e+06,1.29e+07,3.53e+07,7.87e+07,1.77e+08,3.6e+08,6.03e+08,8.77e+08,1.17e+09,1.49e+09,1.76e+09,1.94e+09,2.05e+09,2.1e+09,2.13e+09,2.15e+09,2.13e+09,2.06e+09,1.96e+09,1.84e+09,1.7e+09,1.55e+09,1.4e+09,1.24e+09,1.09e+09,9.37e+08,7.92e+08,6.57e+08,5.34e+08,4.27e+08,3.35e+08,2.58e+08,1.94e+08,1.42e+08,1.01e+08,6.9e+07,4.55e+07,2.88e+07,1.75e+07,1.02e+07,5.64e+06,2.99e+06,1.51e+06,7.32e+05,3.4e+05,1.53e+05,6.74e+04,3.05e+04,1.52e+04,8.98e+03,6.5e+03,5.43e+03,4.89e+03,4.52e+03,4.21e+03,3.91e+03,3.61e+03,3.32e+03,3.03e+03,2.75e+03,2.47e+03,2.21e+03,1.97e+03,1.74e+03,1.52e+03,1.32e+03,1.14e+03,983,839')

# customize(process)
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

customize(process)
