import libhfst

def compare_alphabets(t1, t2):
    alpha1 = t1.get_alphabet()
    alpha2 = t2.get_alphabet()
    return alpha1 == alpha2
    


types = [libhfst.sfst_type(), libhfst.tropical_openfst_type(), libhfst.foma_type()]

for type in types:

    if not libhfst.HfstTransducer.is_implementation_type_available(type):
        continue


    print("Function compare")

    t1 = libhfst.HfstTransducer("foo", "bar", type)
    t2 = libhfst.HfstTransducer("foo", "@_EPSILON_SYMBOL_@", type)
    t3 = libhfst.HfstTransducer("@_EPSILON_SYMBOL_@", "bar", type)
    t2.concatenate(t3).minimize()
    # Alignments must be the same
    assert(not t1.compare(t2))

    t4 = libhfst.HfstTransducer("foo", "bar", type)
    t5 = libhfst.HfstTransducer("@_EPSILON_SYMBOL_@", type)
    t4.concatenate(t5)
    # One transducer is minimal, the other is not
    assert(t1.compare(t4))

    # Weights
    if type == libhfst.tropical_openfst_type():
        t6 = libhfst.HfstTransducer("foo", "bar", type)
        t6.set_final_weights(0.3)
        t7 = libhfst.HfstTransducer("foo", "bar", type)
        t7.set_final_weights(0.1)

        # Weights differ
        assert(not t6.compare(t7))

        t8 = libhfst.HfstTransducer("@_EPSILON_SYMBOL_@", type)
        t8.set_final_weights(0.2)
        t7.concatenate(t8)
        # Weights are the same on each path
        assert(t6.compare(t7))


    print("Function compose")

    t1 = libhfst.HfstTransducer("foo", "bar", type)
    t1.set_final_weights(2)
    t2 = libhfst.HfstTransducer("bar", "baz", type)
    t2.set_final_weights(3)
    t3 = libhfst.HfstTransducer("foo", "baz", type)
    t3.set_final_weights(5)
    t1.compose(t2)
    assert(t1.compare(t3))
    

    print("Function shuffle")

    tok = libhfst.HfstTokenizer()
    t1 = libhfst.HfstTransducer("abc", "abc", tok, type)
    t2 = libhfst.HfstTransducer("cde", "cde", tok, type)
    t1.shuffle(t2)
    
    t3 = libhfst.HfstTransducer("abc", "abC", tok, type)
    try:
        t3.shuffle(t2)
        assert(False)
    except libhfst.TransducersAreNotAutomataException:
        assert(True)


    print("Function convert")

    t1 = libhfst.HfstTransducer("foo", "bar", type)
    t2 = libhfst.HfstTransducer("foo", "bar", type)
    # Go through all implementation formats and get back to the original one
    for conv_type in types:
        t1.convert(conv_type)
        assert(compare_alphabets(t1, t2))
    t1.convert(type)
    assert(t1.compare(t2))
    assert(compare_alphabets(t1, t2))


    print("Function extract_paths(_fd)")

    # Create a transducer that contains animals
    tok = libhfst.HfstTokenizer()
    cat = libhfst.HfstTransducer("cat", "cats", tok, type)
    cat.set_final_weights(3)
    dog = libhfst.HfstTransducer("dog", "dogs", tok, type)
    dog.set_final_weights(2.5)
    mouse = libhfst.HfstTransducer("mouse", "mice",  tok, type)
    mouse.set_final_weights(1.7)
    animals = libhfst.HfstTransducer(type)
    animals.disjunct(cat)
    animals.disjunct(dog)
    animals.disjunct(mouse)
    animals.minimize()

    results = libhfst.extract_paths(animals, 3, 0)
    #print results

    # Add an animal with two possible plurals
    hippopotamus1 = libhfst.HfstTransducer("hippopotamus", "hippopotami", tok, type)
    hippopotamus1.set_final_weights(1.2)
    hippopotamus2 = libhfst.HfstTransducer("hippopotamus", "hippopotamuses", tok, type)
    hippopotamus2.set_final_weights(1.4)
    animals.disjunct(hippopotamus1)
    animals.disjunct(hippopotamus2)
    animals.minimize()

    results = libhfst.extract_paths(animals, 5, 0)
    #print results

    # Convert into optimized lookup format
    animals_ol = libhfst.HfstTransducer(animals)
    if type == libhfst.tropical_openfst_type():
        animals_ol.convert(libhfst.hfst_olw_type())
    else:
        animals_ol.convert(libhfst.hfst_ol_type())
    
    result = libhfst.detokenize_paths(animals_ol.lookup("hippopotamus"))
    #for res in result:
    #    print res[0]
    #    print res[1]
    
    if type == libhfst.tropical_openfst_type:
        best_animals = libhfst.HfstTransducer(animals)
        best_animals.n_best(3)
        assert(libhfst.detokenize_paths(best_animals.lookup("mouse"))[0].output == "mice")
        assert(libhfst.detokenize_paths(best_animals.lookup("hippopotamus"))[0].output == "hippopotami")
        assert(libhfst.detokenize_paths(best_animals.lookup("hippopotamus"))[1].ouput == "hippopotamuses")
    
    
    print("Function insert_freely")

    t1 = libhfst.HfstTransducer("a", "b", type)
    t1.insert_freely(("c", "d"))

    t2 = libhfst.HfstTransducer("a", "b", type)
    tr = libhfst.HfstTransducer("c", "d", type)
    t2.insert_freely(tr)
    assert(t1.compare(t2))

    cd_star = libhfst.HfstTransducer("c", "d", type)
    cd_star.repeat_star()
    ab = libhfst.HfstTransducer("a", "b", type)
    test = libhfst.HfstTransducer(type)
    test.assign(cd_star)
    test.concatenate(ab)
    test.concatenate(cd_star)

    assert(t1.compare(test))
    assert(t2.compare(test))

    unk2unk = libhfst.HfstTransducer("@_UNKNOWN_SYMBOL_@", "@_UNKNOWN_SYMBOL_@", type)
    unk2unk.insert_freely(("c", "d"))
    dc = libhfst.HfstTransducer("d", "c", type)

    empty = libhfst.HfstTransducer(type)
    assert(not unk2unk.intersect(dc).compare(empty))

    unk2unk_ = libhfst.HfstTransducer("@_UNKNOWN_SYMBOL_@", "@_UNKNOWN_SYMBOL_@", type)
    cd_ = libhfst.HfstTransducer("c", "d", type)
    unk2unk_.insert_freely(cd_)

    dc_ = libhfst.HfstTransducer("d", "c", type)
    empty_ = libhfst.HfstTransducer(type)
    assert(not unk2unk_.intersect(dc_).compare(empty))


    print("function is_cyclic")

    t1 = libhfst.HfstTransducer("a", "b", type)
    assert(not t1.is_cyclic())
    t1.repeat_star()
    assert(t1.is_cyclic())


    if (type == libhfst.tropical_openfst_type()):

        print("function push_weights")

        # Create an HFST basic transducer [a:b] with transition
        # weight 0.3 and final weight 0.5
        t = libhfst.HfstBasicTransducer()
        t.add_state(1)
        t.add_transition(0, libhfst.HfstBasicTransition(1, "a", "b", 0.3))
        t.set_final_weight(1, 0.5)

        # Convert to tropical OpenFst format and push weights
        # toward final and initial states
        T_final = libhfst.HfstTransducer(t, libhfst.tropical_openfst_type())
        T_final.push_weights(libhfst.to_final_state())
        T_initial = libhfst.HfstTransducer(t, libhfst.tropical_openfst_type())
        T_initial.push_weights(libhfst.to_initial_state())

        # Convert back to HFST basic transducer
        t_final = libhfst.HfstBasicTransducer(T_final)
        t_initial = libhfst.HfstBasicTransducer(T_initial)

        # Test the final weight
        try:
            # Rounding can affect the precision
            assert((0.79 < t_final.get_final_weight(1)) and (t_final.get_final_weight(1) < 0.81))
            # If the state does not exist or is not final
        except (libhfst.HfstException):
            assert(False)

        # Test the transition weight
        try:
            transitions = t_initial.transitions(0)
            assert(len(transitions) == 1)
            weight = transitions[0].get_weight()
            # Rounding can affect the precision
            assert((0.79 < weight) and (weight < 0.81))
            # If the state does not exist or is not final */
        except (libhfst.HfstException):
            assert(False)


        # Functions set_final_weights and transform_weights

        print("function set_final_weights")

        # Create an HFST basic transducer [a:b] with transition
        # weight 0.3 and final weight 0.5
        t = libhfst.HfstBasicTransducer()
        t.add_state(1)
        t.add_transition(0, libhfst.HfstBasicTransition(1, "a", "b", 0.3))
        t.set_final_weight(1, 0.5)

        # Modify weights
        T = libhfst.HfstTransducer(t, type)
        T.set_final_weights(0.2)
        # T.transform_weights(&modify_weights)
        T.push_weights(libhfst.to_final_state())

        # Convert back to HFST basic transducer and test the weight
        tc = libhfst.HfstBasicTransducer(T)
        try:
          assert((0.49 < tc.get_final_weight(1)) and (tc.get_final_weight(1) < 0.51))
        except (libhfst.HfstException):
            assert(False)


    # Functions substitute

    print("functions substitute")

    tok = libhfst.HfstTokenizer()
    tok.add_multichar_symbol("<eps>")
    t = libhfst.HfstTransducer("cat", "cats", tok, type)

    # String with String
    t1 = libhfst.HfstTransducer(t)
    t1.substitute("c", "C", True, False)
    t1.substitute("t", "T", False, True)
    t1.substitute("@_EPSILON_SYMBOL_@", "<eps>")
    t1.substitute("a", "A")
    t1.substitute("T", "T")       # special
    t1.substitute("foo", "bar")   # cases
    t1_ = libhfst.HfstTransducer("CAt<eps>", "cATs", tok, type)
    assert(t1.compare(t1_))

    # StringPair with StringPair
    t2 = libhfst.HfstTransducer(t)
    t2.substitute(("c","c"), ("C","c"))
    t2.substitute(("C","c"), ("H","h"))
    t2.substitute(("a","a"), ("a","a"))      # special
    t2.substitute(("foo","bar"), ("f","b"))  # cases
    t2_ = libhfst.HfstTransducer("Hat", "hats", tok, type)
    assert(t2.compare(t2_))

    # StringPair with StringPairSet
    t3 = libhfst.HfstTransducer(t)
    sps = (("c","c"), ("C","C"), ("h","h"), ("H","H"))
    t3.substitute(("c","c"), sps)
    t3_ = libhfst.HfstTransducer("cat", "cats", tok, type)
    t3_1 = libhfst.HfstTransducer("Cat", "Cats", tok, type)
    t3_2 = libhfst.HfstTransducer("hat", "hats", tok, type)
    t3_3 = libhfst.HfstTransducer("Hat", "Hats", tok, type)
    t3_.disjunct(t3_1)
    t3_.disjunct(t3_2)
    t3_.disjunct(t3_3)
    t3_.minimize()
    assert(t3.compare(t3_))

    # StringPair with HfstTransducer
    t4 = libhfst.HfstTransducer(t)
    subs = libhfst.HfstTransducer("ch", tok, type)
    t4.substitute(("c","c"), subs)
    t4_ = libhfst.HfstTransducer("chat", "chats", tok, type)
    assert(t4.compare(t4_))

    # Substitute with function
    # t5 = libhfst.HfstTransducer(t);
    # t5.substitute(&modify_transitions);
    # tok.add_multichar_symbol("<ID>");
    # HfstTransducer t5_("<ID><ID><ID>", "<ID><ID><ID>s", tok, types[i]);
    # assert(t5.compare(t5_));

    # Perform multiple string-to-string substitutions
    # t6 = libhfst.HfstTransducer(t)
    # HfstSymbolSubstitutions subs_symbol;
    # subs_symbol["c"] = "C";
    # subs_symbol["a"] = "A";
    # subs_symbol["t"] = "T";
    # subs_symbol["s"] = "S";
    # t6.substitute(subs_symbol);
    # HfstTransducer t6_("CAT", "CATS", tok, types[i]);
    # assert(t6.compare(t6_));

    # Perform multiple string pair-to-string pair substitutions
    # t7 = libhfst.HfstTransducer (t)
    # HfstSymbolPairSubstitutions subs_pair;
    # subs_pair[("a", "a")] = ("A", "a");
    # subs_pair[("s", "s")] = ("S", "S");
    # subs_pair[("t", "t")] = ("t", "T");
    # t7.substitute(subs_pair);
    # HfstTransducer t7_("cAt", "caTs", tok, types[i]);
    # assert(t7.compare(t7_));

    # print("alphabets")

    # HfstTransducer a2unk("a", "@_UNKNOWN_SYMBOL_@", types[i]);
    # assert(a2unk.get_alphabet().size() == 4);
    # a2unk.insert_to_alphabet("FOO");
    # assert(a2unk.get_alphabet().size() == 5);
    # a2unk.remove_from_alphabet("FOO");
    # assert(a2unk.get_alphabet().size() == 4);
    # StringSet alpha = a2unk.get_alphabet();
    # assert(alpha.find("FOO") == alpha.end());

