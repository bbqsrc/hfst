# file(GLOB_RECURSE SOURCES "*.cc")
target_include_directories(hfst PRIVATE 
    ${CMAKE_CURRENT_SOURCE_DIR})

target_sources(hfst PRIVATE
    xre_utils.cc XreCompiler.cc xre_parse.cc xre_lex.cc
    pmatch_utils.cc PmatchCompiler.cc pmatch_parse.cc pmatch_lex.cc
    lexc-utils.cc LexcCompiler.cc lexc-parser.cc lexc-lexer.cc
    SfstCompiler.cc SfstUtf8.cc SfstBasic.cc SfstAlphabet.cc sfst-compiler.cc sfst-scanner.cc
    xfst-utils.cc XfstCompiler.cc xfst_help_message.cc xfst-parser.cc xfst-lexer.cc

    TwolcCompiler.cc 
    commandline_src/CommandLine.cc 
    alphabet_src/Alphabet.cc 
    io_src/InputReader.cc 
    rule_src/ConflictResolvingLeftArrowRule.cc 
    rule_src/ConflictResolvingRightArrowRule.cc 
    rule_src/LeftArrowRule.cc 
    rule_src/LeftArrowRuleContainer.cc 
    rule_src/LeftRestrictionArrowRule.cc 
    rule_src/OtherSymbolTransducer.cc 
    rule_src/RightArrowRule.cc 
    rule_src/RightArrowRuleContainer.cc 
    rule_src/Rule.cc 
    rule_src/RuleContainer.cc 
    rule_src/TwolCGrammar.cc 
    string_src/string_manipulation.cc 
    variable_src/RuleSymbolVector.cc 
    variable_src/RuleVariables.cc 
    variable_src/RuleVariablesConstIterator.cc 
    variable_src/VariableValues.cc
    htwolcpre1-parser.cc htwolcpre1-lexer.cc htwolcpre2-parser.cc htwolcpre2-lexer.cc htwolcpre3-parser.cc htwolcpre3-lexer.cc
)