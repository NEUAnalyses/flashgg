#include "TFile.h"
#include "TStyle.h"
#include "TH1.h"
#include "TH2.h"
#include "TTree.h" 
#include "TCanvas.h"
#include "TLegend.h"
#include "TColor.h"
#include "TLatex.h"
#include "TGraphAsymmErrors.h"
#include "TGraphErrors.h"
#include "TGaxis.h"
#include "TPaletteAxis.h"
#include "TProfile.h"
#include "TProfile2D.h"
#include "TKey.h"

//#include "FPCanvasStyle.C"
//#include "setStyle.C"
//#include "centerOfMassEnergy.h"
//#include "CMS_lumi.h"

#include<iostream>
#include<string>
#include<fstream>

using namespace std;

void draw_dZ_Plots() {
  
  gStyle->SetOptStat(0);

  //TFile* inFile = TFile::Open("/eos/cms/store/user/bmarzocc/H4G_Analysis/Dumpers_vtxProb/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8_dump.root");
  TFile* inFile = TFile::Open("../../outDir/SUSYGluGluToHToAA_AToGG_M-60_TuneCUETP8M1_13TeV_pythia8.root");
  TTree* tree = (TTree*)inFile->Get("h4gCandidateDumper_vtxProb/trees/SUSYGluGluToHToAA_AToGG_M_60_TuneCUETP8M1_13TeV_pythia8_13TeV_4photons");

  TH1F* h_dZ_zeroVtx = new TH1F("h_dZ_zeroVtx","",100,0.,20.);
  tree->Draw("fabs(dZ_zeroVtx) >> h_dZ_zeroVtx","BS_factor_0Vtx");

  TH1F* h_dZ_hggVtx = new TH1F("h_dZ_hggVtx","",100,0.,20.);
  tree->Draw("fabs(dZ_hggVtx) >> h_dZ_hggVtx","BS_factor_HggVtx");

  TH1F* h_dZ_bdtVtx = new TH1F("h_dZ_bdtVtx","",100,0.,20.);
  tree->Draw("fabs(dZ_bdtVtx) >> h_dZ_bdtVtx","BS_factor_BDTVtx");
 
  TGraphErrors* g_Eff_dZ_zeroVtx = new TGraphErrors();
  g_Eff_dZ_zeroVtx->SetMarkerColor(kGreen+2);
  g_Eff_dZ_zeroVtx->SetMarkerStyle(20);
  g_Eff_dZ_zeroVtx->SetMarkerSize(0.75);

  TGraphErrors* g_Eff_dZ_hggVtx = new TGraphErrors();
  g_Eff_dZ_hggVtx->SetMarkerColor(kRed+2);
  g_Eff_dZ_hggVtx->SetMarkerStyle(20);
  g_Eff_dZ_hggVtx->SetMarkerSize(0.75);

  TGraphErrors* g_Eff_dZ_bdtVtx = new TGraphErrors();
  g_Eff_dZ_bdtVtx->SetMarkerColor(kBlue+2);
  g_Eff_dZ_bdtVtx->SetMarkerStyle(20);
  g_Eff_dZ_bdtVtx->SetMarkerSize(0.75); 

  for(int bin=1; bin<=h_dZ_zeroVtx->GetNbinsX(); bin++)
  {
      double eff_zeroVtx=h_dZ_zeroVtx->Integral(1,bin)/h_dZ_zeroVtx->Integral();
      g_Eff_dZ_zeroVtx->SetPoint(bin-1,20./100.*bin,eff_zeroVtx); 
      g_Eff_dZ_zeroVtx->SetPointError(bin-1,0.,sqrt(eff_zeroVtx*(1-eff_zeroVtx)/h_dZ_zeroVtx->Integral()));
      
      double eff_hggVtx=h_dZ_hggVtx->Integral(1,bin)/h_dZ_hggVtx->Integral();
      g_Eff_dZ_hggVtx->SetPoint(bin-1,20./100.*bin,eff_hggVtx); 
      g_Eff_dZ_hggVtx->SetPointError(bin-1,0.,sqrt(eff_hggVtx*(1-eff_hggVtx)/h_dZ_hggVtx->Integral())); 

      double eff_bdtVtx=h_dZ_bdtVtx->Integral(1,bin)/h_dZ_bdtVtx->Integral();
      g_Eff_dZ_bdtVtx->SetPoint(bin-1,20./100.*bin,eff_bdtVtx); 
      g_Eff_dZ_bdtVtx->SetPointError(bin-1,0.,sqrt(eff_bdtVtx*(1-eff_bdtVtx)/h_dZ_bdtVtx->Integral()));

      if(20./100.*bin == 1.){
         std::cout << "eff_zeroVtx = " << eff_zeroVtx*100. << "+/-" << sqrt(eff_zeroVtx*(1-eff_zeroVtx)/h_dZ_zeroVtx->Integral())*100. << "%" << endl;
         std::cout << "eff_hggVtx  = " << eff_hggVtx*100. << "+/-" << sqrt(eff_hggVtx*(1-eff_hggVtx)/h_dZ_hggVtx->Integral())*100. << "%" << endl;
         std::cout << "eff_bdtVtx  = " << eff_bdtVtx*100. << "+/-" << sqrt(eff_bdtVtx*(1-eff_bdtVtx)/h_dZ_bdtVtx->Integral())*100. << "%" << endl;  
      } 
  }
   
  TCanvas* c = new TCanvas("c","c",1);
  g_Eff_dZ_zeroVtx->GetXaxis()->SetTitle("#DeltaZ (cm)");
  g_Eff_dZ_zeroVtx->GetYaxis()->SetTitle("efficiency");
  g_Eff_dZ_zeroVtx->Draw("AP");
  g_Eff_dZ_hggVtx->Draw("P,same");
  g_Eff_dZ_bdtVtx->Draw("P,same"); 
  c->SaveAs("h_Eff_dZ_H4G_M60.png","png");
  c->SaveAs("h_Eff_dZ_H4G_M60.pdf","pdf");
  
}
