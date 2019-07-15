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

//#include "TMVAGui.C"

#if not defined(__CINT__) || defined(__MAKECINT__)
#include "TMVA/Factory.h"
#include "TMVA/Tools.h"
#endif

void VertexMvaProb_H4G()
{
    TFile* inputFile = TFile::Open("/eos/cms/store/user/bmarzocc/H4G_Analysis/Dumpers_vtxProb/SUSYGluGluToHToAA_AToGG_Total_TuneCUETP8M1_13TeV_pythia8.root");
    TTree* inputTree = (TTree*) inputFile->Get("h4gCandidateDumper_vtxProb/trees/SUSYGluGluToHToAA_AToGG_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons");

    TString outfileName( "outputTMVA_BDTVtxProb.root" );
    TFile* outputFile = TFile::Open( outfileName, "RECREATE" );

    TMVA::Tools::Instance();

    TMVA::Factory *factory = new TMVA::Factory( "TMVAClassification", outputFile,
                                               "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification" );
    factory->AddVariable( "tp_pt"    , "tp_pt"   , 'F');
    factory->AddVariable( "n_vertices" , "n_vertices", 'F');
    factory->AddVariable( "MVA0"  , "MVA0" , 'F');
    factory->AddVariable( "MVA1"  , "MVA1" , 'F');
    factory->AddVariable( "dZ1"   , "dZ1"  , 'F');
    factory->AddVariable( "MVA2"  , "MVA2" , 'F');
    factory->AddVariable( "dZ2"   , "dZ2"  , 'F');
    factory->AddVariable( "nConv" , "nConv", 'F');

    TCut signalCut = "fabs(dZtrue) < 1 && fabs(tp_pt)<999. && fabs(n_vertices)<999. && fabs(MVA0)<999. && fabs(MVA1)<999. && fabs(MVA2)<999. && fabs(dZ1)<999. && fabs(dZ2)<999. && fabs(nConv)<999. && !std::isnan(tp_pt) && !std::isnan(n_vertices) && !std::isnan(MVA0) && !std::isnan(MVA1) && !std::isnan(MVA2) && !std::isnan(dZ1) && !std::isnan(dZ2) && !std::isnan(nConv)";
    TCut backgrCut = "fabs(dZtrue) > 1 && fabs(tp_pt)<999. && fabs(n_vertices)<999. && fabs(MVA0)<999. && fabs(MVA1)<999. && fabs(MVA2)<999. && fabs(dZ1)<999. && fabs(dZ2)<999. && fabs(nConv)<999. && !std::isnan(tp_pt) && !std::isnan(n_vertices) && !std::isnan(MVA0) && !std::isnan(MVA1) && !std::isnan(MVA2) && !std::isnan(dZ1) && !std::isnan(dZ2) && !std::isnan(nConv)";
    factory->SetInputTrees( inputTree, signalCut, backgrCut );

    outputFile->cd();

    TCut mycuts = "MVA2 > -1 && fabs(tp_pt)<999. && fabs(n_vertices)<999. && fabs(MVA0)<999. && fabs(MVA1)<999. && fabs(MVA2)<999. && fabs(dZ1)<999. && fabs(dZ2)<999. && fabs(nConv)<999. && !std::isnan(tp_pt) && !std::isnan(n_vertices) && !std::isnan(MVA0) && !std::isnan(MVA1) && !std::isnan(MVA2) && !std::isnan(dZ1) && !std::isnan(dZ2) && !std::isnan(nConv)";
    TCut mycutb = "MVA2 > -1 && fabs(tp_pt)<999. && fabs(n_vertices)<999. && fabs(MVA0)<999. && fabs(MVA1)<999. && fabs(MVA2)<999. && fabs(dZ1)<999. && fabs(dZ2)<999. && fabs(nConv)<999. && !std::isnan(tp_pt) && !std::isnan(n_vertices) && !std::isnan(MVA0) && !std::isnan(MVA1) && !std::isnan(MVA2) && !std::isnan(dZ1) && !std::isnan(dZ2) && !std::isnan(nConv)"; 

    factory->PrepareTrainingAndTestTree( mycuts, mycutb,
//                                    "nTrain_Signal=0:nTrain_Background=0:SplitMode=Alternate:NormMode=NumEvents:!V" );
                                    "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V" );


    TMVA::MethodCategory* mcat = 0;

    TString theCat1Vars = "tp_pt:n_vertices:MVA0:MVA1:dZ1:MVA2:dZ2";
    TString theCat2Vars = "tp_pt:n_vertices:MVA0:MVA1:dZ1:MVA2:dZ2";
 
    //TMVA::MethodBase* BDT_Cat = factory->BookMethod( TMVA::Types::kCategory, "BDT","" );
    //mcat = dynamic_cast<TMVA::MethodCategory*>(BDT_Cat);

    //mcat->AddMethod( "NConv<1", theCat1Vars, TMVA::Types::kBDT, "0_1_BDTGNewTrue","!H:!V:!CreateMVAPdfs:NTrees=1000:NNodesMax=5:BoostType=Grad:UseBaggedGrad:Shrinkage=0.30:GradBaggingFraction=0.6:SeparationType=GiniIndex:nCuts=20:NNodesMax=5");
    //mcat->AddMethod( "NConv>=1",  theCat2Vars, TMVA::Types::kBDT, "1_BDTGNewTrue","!H:!V:!CreateMVAPdfs:NTrees=1000:NNodesMax=5:BoostType=Grad:UseBaggedGrad:Shrinkage=0.30:GradBaggingFraction=0.6:SeparationType=GiniIndex:nCuts=20:NNodesMax=5" );

    TMVA::MethodBase* BDT_Cat = factory->BookMethod( TMVA::Types::kCategory, "BDTVtxProb","" );
    mcat = dynamic_cast<TMVA::MethodCategory*>(BDT_Cat);

    mcat->AddMethod( "nConv<1 ", theCat1Vars, TMVA::Types::kBDT, "BDTVtxProb_noconv","!H:!V:!CreateMVAPdfs:NTrees=1000:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.6:SeparationType=GiniIndex:nCuts=20:MaxDepth=3:MinNodeSize=2");
    mcat->AddMethod( "nConv>=1",  theCat2Vars, TMVA::Types::kBDT, "BDTVtxProb_conv","!H:!V:!CreateMVAPdfs:NTrees=1000:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.6:SeparationType=GiniIndex:nCuts=20:MaxDepth=3:MinNodeSize=2");

    factory->TrainAllMethods();

    factory->TestAllMethods();

    factory->EvaluateAllMethods();

   // --------------------------------------------------------------

    outputFile->Close();

    std::cout << "==> Wrote root file: " << outputFile->GetName() << std::endl;
    std::cout << "==> TMVAClassification is done!" << std::endl;

    delete factory;
}
