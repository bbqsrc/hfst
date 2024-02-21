target_include_directories(hfst PRIVATE "${CMAKE_SOURCE_DIR}/back-ends/foma")

target_sources(hfst PRIVATE
    SfstTransducer.cc
    TropicalWeightTransducer.cc
    LogWeightTransducer.cc
    FomaTransducer.cc
    # XfsmTransducer.cc
    # OtherSymbolTransducer.cc
    HfstOlTransducer.cc
    ConvertTransducerFormat.cc 
    HfstTropicalTransducerTransitionData.cc 
    HfstBasicTransition.cc HfstBasicTransducer.cc 
    ConvertSfstTransducer.cc ConvertTropicalWeightTransducer.cc 
    ConvertLogWeightTransducer.cc ConvertFomaTransducer.cc 
    ConvertOlTransducer.cc ConvertXfsmTransducer.cc 
            compose_intersect/ComposeIntersectRulePair.cc 
            compose_intersect/ComposeIntersectLexicon.cc 
            compose_intersect/ComposeIntersectRule.cc 
            compose_intersect/ComposeIntersectFst.cc 
            compose_intersect/ComposeIntersectUtilities.cc
    optimized-lookup/transducer.cc 
    optimized-lookup/convert.cc 
    optimized-lookup/ospell.cc optimized-lookup/pmatch.cc 
    optimized-lookup/pmatch_tokenize.cc 
    optimized-lookup/find_epsilon_loops.cc)