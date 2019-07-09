#ifndef flashgg_H4GCandidate
#define flashgg_H4GCandidate

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/EDMException.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "flashgg/DataFormats/interface/DiPhotonCandidate.h"
#include "flashgg/DataFormats/interface/SinglePhotonView.h"
#include "flashgg/DataFormats/interface/Photon.h"
#include "flashgg/DataFormats/interface/Jet.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "flashgg/DataFormats/interface/VertexCandidateMap.h"
#include "flashgg/DataFormats/interface/DiPhotonMVAResult.h"
#include "flashgg/DataFormats/interface/TagTruthBase.h"
#include "DataFormats/Common/interface/RefToPtr.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "flashgg/MicroAOD/interface/CutBasedDiPhotonObjectSelector.h"
#include "DataFormats/EgammaCandidates/interface/Conversion.h"

#include "TLorentzVector.h"
#include "DataFormats/Math/interface/LorentzVector.h"

#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"

#include "flashgg/Taggers/interface/FunctionHelpers.h"

#include "flashgg/DataFormats/interface/DiPhotonMVAResult.h"
#include "TMVA/Reader.h"

namespace flashgg {

  class H4GCandidate : public WeightedObject
  {
  public:
    //---ctors---
    H4GCandidate() ;
    H4GCandidate( std::vector<flashgg::Photon> phoVector, std::vector<edm::Ptr<reco::Vertex>> Vertices,std::vector<edm::Ptr<reco::Vertex>> slim_Vertices,edm::Ptr<reco::Vertex> vertex_diphoton, edm::Ptr<reco::Vertex> vertex_bdt, reco::GenParticle::Point genVertex, math::XYZPoint BSPoint, std::vector <edm::Ptr<flashgg::DiPhotonCandidate>> diPhoPtrs, std::vector<std::vector<float>> Vector, float MVA0, float MVA1, float MVA2, float dZ1, float dZ2, float dZtrue, int hgg_index, int trueVtx_index, int rndVtx_index, int bdtVtx_index, float tp_pt, float nVertices, float nConv, TMVA::Reader *VertexProbMva);

    //---dtor---
    ~H4GCandidate();

    //---utils---
    const std::vector<flashgg::Photon> phoVector() const { return phoVector_; };
    const std::vector< edm::Ptr<reco::Vertex> >Vertices() const { return Vertices_; };
    const std::vector< edm::Ptr<reco::Vertex> >slim_Vertices() const { return slim_Vertices_; };


    // const edm::Ptr<reco::Vertex> & vertex() const { return vertex_;  };
    const edm::Ptr<reco::Vertex> & Vertex_random() const { return Vertex_random_;  };
    const edm::Ptr<reco::Vertex> & vertex_diphoton() const { return vertex_diphoton_;  };
    const edm::Ptr<reco::Vertex> & vertex_bdt() const { return vertex_bdt_;  };
    const reco::GenParticle::Point & genVertex() const { return genVertex_;  };
    const math::XYZPoint &BSPoint() const { return BSPoint_; };
    const std::vector <edm::Ptr<flashgg::DiPhotonCandidate>> &diPhoPtrs() const { return diPhoPtrs_; };
    const float &logSumPt2_zero() const { return Vector_[0][0]; };
    const float &ptAsym_zero() const { return Vector_[1][0]; };
    const float &ptBal_zero() const { return Vector_[2][0]; };
    const float &pullConv_zero() const { return Vector_[3][0]; };
    const float &nConv_zero() const { return Vector_[4][0]; };
    const float &logSumPt2_hgg() const { return Vector_[0][hgg_index_]; };
    const float &ptAsym_hgg() const { return Vector_[1][hgg_index_]; };
    const float &ptBal_hgg() const { return Vector_[2][hgg_index_]; };
    const float &pullConv_hgg() const { return Vector_[3][hgg_index_]; };
    const float &nConv_hgg() const { return Vector_[4][hgg_index_]; };
    const float &logSumPt2_true() const { return Vector_[0][trueVtx_index_]; };
    const float &ptAsym_true() const { return Vector_[1][trueVtx_index_]; };
    const float &ptBal_true() const { return Vector_[2][trueVtx_index_]; };
    const float &pullConv_true() const { return Vector_[3][trueVtx_index_]; };
    const float &nConv_true() const { return Vector_[4][trueVtx_index_]; };
    const float &logSumPt2_rnd() const { return Vector_[0][rndVtx_index_]; };
    const float &ptAsym_rnd() const { return Vector_[1][rndVtx_index_]; };
    const float &ptBal_rnd() const { return Vector_[2][rndVtx_index_]; };
    const float &pullConv_rnd() const { return Vector_[3][rndVtx_index_]; };
    const float &nConv_rnd() const { return Vector_[4][rndVtx_index_]; };
    const float &logSumPt2() const { return Vector_[0][bdtVtx_index_]; };
    const float &ptAsym() const { return Vector_[1][bdtVtx_index_]; };
    const float &ptBal() const { return Vector_[2][bdtVtx_index_]; };
    const float &pullConv() const { return Vector_[3][bdtVtx_index_]; };
    const std::vector<std::vector<float>> &test() const { return Vector_; };
    const float &vtxProbMVA() const { return vtxProbMVA_; }; 
    const float &MVA0() const { return MVA0_; };
    const float &MVA1() const { return MVA1_; };
    const float &MVA2() const { return MVA2_; };
    const float &dZ1() const { return dZ1_; };
    const float &dZ2() const { return dZ2_; };
    const float &dZtrue() const { return dZtrue_; };
    const float &nConv() const { return Vector_[4][bdtVtx_index_]; };
    const int &hgg_index() const { return hgg_index_; };
    const int &trueVtx_index() const { return trueVtx_index_; };
    const int &rndVtx_index() const { return rndVtx_index_; };
    const int &bdtVtx_index() const { return bdtVtx_index_; };
    const float BS_factor_0Vtx() const { return BS_factor_0Vtx_; };
    const float BS_factor_HggVtx() const { return BS_factor_HggVtx_; };
    const float BS_factor_RandomVtx() const { return BS_factor_RandomVtx_; };
    const float BS_factor_BDTVtx() const { return BS_factor_BDTVtx_; };
    const std::vector<flashgg::Photon> phoP4Corrected() const { return phoP4Corrected_; };
    const flashgg::Photon phoP4Corrected1() const { return phoP4Corrected1_; };
    const flashgg::Photon phoP4Corrected2() const { return phoP4Corrected2_; };
    const flashgg::Photon phoP4Corrected3() const { return phoP4Corrected3_; };
    const flashgg::Photon phoP4Corrected4() const { return phoP4Corrected4_; };
    const float pho1_MVA() const { return pho1_MVA_; };
    const float pho2_MVA() const { return pho2_MVA_; };
    const float pho3_MVA() const { return pho3_MVA_; };
    const float pho4_MVA() const { return pho4_MVA_; };
    const reco::Candidate::LorentzVector& h4gDiPho1() const { return dp1_; };
    const reco::Candidate::LorentzVector& h4gDiPho2() const { return dp2_; };
    const reco::Candidate::LorentzVector& h4gDiPho1_Pho1() const { return dp1_pho1_; };
    const reco::Candidate::LorentzVector& h4gDiPho1_Pho2() const { return dp1_pho2_; };
    const reco::Candidate::LorentzVector& h4gDiPho2_Pho1() const { return dp2_pho1_; };
    const reco::Candidate::LorentzVector& h4gDiPho2_Pho2() const { return dp2_pho2_; };
    const int& h4gDiPho1_iPho1() const { return dp1_ipho1_; };
    const int& h4gDiPho1_iPho2() const { return dp1_ipho2_; };
    const int& h4gDiPho2_iPho1() const { return dp2_ipho1_; };
    const int& h4gDiPho2_iPho2() const { return dp2_ipho2_; };
    const reco::Candidate::LorentzVector& h4gPho12() const { return pho12_; };
    const reco::Candidate::LorentzVector& h4gPho13() const { return pho13_; };
    const reco::Candidate::LorentzVector& h4gPho14() const { return pho14_; };
    const reco::Candidate::LorentzVector& h4gPho23() const { return pho23_; };
    const reco::Candidate::LorentzVector& h4gPho24() const { return pho24_; };
    const reco::Candidate::LorentzVector& h4gPho34() const { return pho34_; };
    const reco::Candidate::LorentzVector& h4gFourVect() const { return tp_; };
    float getCosThetaStar_CS(float ebeam) const;
    std::vector<float> CosThetaAngles() const;
    float HelicityCosTheta( TLorentzVector Booster, TLorentzVector Boosted) const;


  private:

    std::vector<flashgg::Photon> phoVector_;
    std::vector<edm::Ptr<reco::Vertex>> Vertices_;
    std::vector<edm::Ptr<reco::Vertex>> slim_Vertices_;

    // edm::Ptr<reco::Vertex>               vertex_;
    edm::Ptr<reco::Vertex>               Vertex_random_;
    edm::Ptr<reco::Vertex>               vertex_diphoton_;
    edm::Ptr<reco::Vertex>               vertex_bdt_;
    reco::GenParticle::Point genVertex_;
    math::XYZPoint BSPoint_;
    std::vector <edm::Ptr<flashgg::DiPhotonCandidate>> diPhoPtrs_;
    std::vector<std::vector<float>> Vector_;
    float vtxProbMVA_;
    float MVA0_;
    float MVA1_;
    float MVA2_;
    float dZ1_;
    float dZ2_;
    float dZtrue_;
    int hgg_index_;
    int trueVtx_index_;
    int rndVtx_index_;
    int bdtVtx_index_;
    float BS_factor_0Vtx_;
    float BS_factor_HggVtx_;
    float BS_factor_RandomVtx_;
    float BS_factor_BDTVtx_;
    float tp_pt_;
    float nVertices_;
    float nConv_;
    TMVA::Reader *VertexProbMva_;
    std::vector<flashgg::Photon> phoP4Corrected_;
    flashgg::Photon phoP4Corrected1_;
    flashgg::Photon phoP4Corrected2_;
    flashgg::Photon phoP4Corrected3_;
    flashgg::Photon phoP4Corrected4_;
    float pho1_MVA_;
    float pho2_MVA_;
    float pho3_MVA_;
    float pho4_MVA_;
    reco::Candidate::LorentzVector dp1_;
    reco::Candidate::LorentzVector dp2_;
    reco::Candidate::LorentzVector dp1_pho1_;
    reco::Candidate::LorentzVector dp1_pho2_;
    reco::Candidate::LorentzVector dp2_pho1_;
    reco::Candidate::LorentzVector dp2_pho2_;
    int dp1_ipho1_;
    int dp1_ipho2_;
    int dp2_ipho1_;
    int dp2_ipho2_;
    reco::Candidate::LorentzVector pho12_;
    reco::Candidate::LorentzVector pho13_;
    reco::Candidate::LorentzVector pho14_;
    reco::Candidate::LorentzVector pho23_;
    reco::Candidate::LorentzVector pho24_;
    reco::Candidate::LorentzVector pho34_;
    reco::Candidate::LorentzVector tp_;

  };
  typedef std::vector<H4GCandidate> H4GCandidateCollection;


}

#endif
