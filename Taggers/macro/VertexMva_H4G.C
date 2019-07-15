#include <cstdlib>
#include <iostream>
#include <map>
#include <string>

#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"

#include "TMVA/Factory.h"
//#include "TMVA/DataLoader.h"
#include "TMVA/Tools.h"
#include "TMVA/TMVAGui.h"

/*#if not defined(__CINT__) || defined(__MAKECINT__)
#include "TMVA/Factory.h"
#include "TMVA/DataLoader.h"
#include "TMVA/Tools.h"
#include "TMVA/TMVAGui.h"
#endif*/

void VertexMva_H4G()
{
   
    TString outfileName( "outputTMVA_BDTVtxId.root" );
    TFile* outputFile = TFile::Open( outfileName, "RECREATE" );

    TFile* inputFile = TFile::Open("/eos/cms/store/user/bmarzocc/H4G_Analysis/Dumpers_vtxID/SUSYGluGluToHToAA_AToGG_Total_TuneCUETP8M1_13TeV_pythia8.root");

    TTree* signal_ggf  = (TTree*)inputFile->Get("h4gCandidateDumper_vtxBDT_sig/trees/SUSYGluGluToHToAA_AToGG_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons_sig");
    TTree* bkg_ggf     = (TTree*)inputFile->Get("h4gCandidateDumper_vtxBDT_bkg/trees/SUSYGluGluToHToAA_AToGG_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons_bkg");
    
    TMVA::Tools::Instance();

    TMVA::Factory *factory = new TMVA::Factory( "TMVAClassification", outputFile,
                                               "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification" );
    factory->AddVariable("ptAsym", "ptAsym", "", 'F'); 
    factory->AddVariable("ptBal", "ptBal", "", 'F');
    factory->AddVariable("logSumpt2", "logSumpt2", "", 'F'); 
    factory->AddVariable("pullConv", "pullConv", "", 'F');
    factory->AddVariable("nConv", "nConv", "", 'F');
   
    Double_t signalWeight = 1.0;
    Double_t backgroundWeight = 1.0;
  
    factory->AddSignalTree( signal_ggf, signalWeight );
    factory->AddBackgroundTree( bkg_ggf, backgroundWeight );

    //factory->SetWeightExpression( "genweight" );

    outputFile->cd();

    TCut mycuts = "fabs(ptAsym) < 999. && fabs(ptBal) < 999. && fabs(logSumpt2)<999. && fabs(pullConv)<999. && fabs(nConv)<999. && !std::isnan(ptAsym) && !std::isnan(ptBal) && !std::isnan(logSumpt2) && !std::isnan(pullConv) && !std::isnan(nConv)";
    TCut mycutb = "fabs(ptAsym) < 999. && fabs(ptBal) < 999. && fabs(logSumpt2)<999. && fabs(pullConv)<999. && fabs(nConv)<999. && !std::isnan(ptAsym) && !std::isnan(ptBal) && !std::isnan(logSumpt2) && !std::isnan(pullConv) && !std::isnan(nConv)";

    factory->PrepareTrainingAndTestTree( mycuts, mycutb,
                                    "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V" );

    TMVA::MethodCategory* mcat = 0;

    TString theCat1Vars = "ptAsym:ptBal:logSumpt2";
    TString theCat2Vars = "ptAsym:ptBal:logSumpt2:pullConv";
 
    //TMVA::MethodBase* BDT_Cat = factory->BookMethod( TMVA::Types::kCategory, "BDT","" );
    //mcat = dynamic_cast<TMVA::MethodCategory*>(BDT_Cat);

    //mcat->AddMethod( "NConv<1", theCat1Vars, TMVA::Types::kBDT, "0_1_BDTGNewTrue","!H:!V:!CreateMVAPdfs:NTrees=1000:NNodesMax=5:BoostType=Grad:UseBaggedGrad:Shrinkage=0.30:GradBaggingFraction=0.6:SeparationType=GiniIndex:nCuts=20:NNodesMax=5");
    //mcat->AddMethod( "NConv>=1",  theCat2Vars, TMVA::Types::kBDT, "1_BDTGNewTrue","!H:!V:!CreateMVAPdfs:NTrees=1000:NNodesMax=5:BoostType=Grad:UseBaggedGrad:Shrinkage=0.30:GradBaggingFraction=0.6:SeparationType=GiniIndex:nCuts=20:NNodesMax=5" );

    TMVA::MethodBase* BDT_Cat = factory->BookMethod( TMVA::Types::kCategory, "BDTVtxId","" );
    mcat = dynamic_cast<TMVA::MethodCategory*>(BDT_Cat);

    mcat->AddMethod( "nConv<1 && nConv>-999.", theCat1Vars, TMVA::Types::kBDT, "BDTVtxId_noconv","!H:!V:!CreateMVAPdfs:NTrees=1000:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.6:SeparationType=GiniIndex:nCuts=20:MaxDepth=3:MinNodeSize=2:NegWeightTreatment=ignorenegweightsintraining");
    mcat->AddMethod( "nConv>=1 && nConv<999.",  theCat2Vars, TMVA::Types::kBDT, "BDTVtxId_conv","!H:!V:!CreateMVAPdfs:NTrees=1000:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.6:SeparationType=GiniIndex:nCuts=20:MaxDepth=3:MinNodeSize=2:NegWeightTreatment=ignorenegweightsintraining");

    factory->TrainAllMethods();

    factory->TestAllMethods();

    factory->EvaluateAllMethods();

   // --------------------------------------------------------------

    outputFile->Close();

    std::cout << "==> Wrote root file: " << outputFile->GetName() << std::endl;
    std::cout << "==> TMVAClassification is done!" << std::endl;

    delete factory;
}

