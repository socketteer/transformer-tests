from conditional import conditional_logprob, decibels

roish_noinfo = '''Today we're going to be playing with the fictional Roish language.
English: The weather is lovely!
Roish:'''

roish_0shot = '''Today we're going to be playing with the fictional Roish language. Roish is a lot like English except every word ends in "ro".
English: The weather is lovely!
Roish:'''

roish_halfshot = '''Today we're going to be playing with the fictional Roish language. Roish is a lot like English except "ro" is appended to the end. For instance, the word "writing" becomes "writingro".
English: The weather is lovely!
Roish:'''

roish_1shot = '''Today we're going to be playing with the fictional Roish language. Roish is a lot like English except every word ends in "ro".
English: Writing about language models is fun.
Roish: Writingro aboutro languagero modelsro isro funro.
English: The weather is lovely!
Roish:'''

roish_2shot = '''Today we're going to be playing with the fictional Roish language. Roish is a lot like English except every word ends in "ro".
English: Writing about language models is fun.
Roish: Writingro aboutro languagero modelsro isro funro.
English: I wonder if the language model can get the pattern.
Roish: Iro wonderro ifro thero languagero modelro canro everro getro thero patternro.
English: The weather is lovely!
Roish:'''

roish_10shot = '''Today we're going to be playing with the fictional Roish language. Roish is a lot like English except every word ends in "ro".
English: Mrs. Juarez and Mr. Smith are dancing gracefully.
Roish: Mrsro. Juarezro andro Mrro. Smithro arero dancingro gracefullyro.
English: Samantha, Elizabeth, and Joan are on the committee.
Roish: Samantharo, Elizabethro, andro Joanro arero onro thero committeero.
English: The ham, green beans, mashed potatoes, and corn are gluten-free.
Roish: Thero hamro, greenro beansro, mashedro potatoesro, andro cornro arero glutenro-freero.
English: The paper and pencil sat idle on the desk.
Roish: Thero paperro andro pencilro satro idlero onro thero deskro.
English: Sometimes the most difficult questions have the simplest solutions!
Roish: Sometimesro thero mostro difficultro questionsro havero thero simplestro solutions!
English: While breakthroughs in machine learning and artificial intelligence are changing society, our fundamental understanding has lagged behind.
Roish: Whilero breakthroughsro inro machinero learningro andro artificialro intelligencero arero changingro societyro, ourro fundamentalro understandingro hasro laggedro behindro.
English: Do they need to have access to data other than text in order to do this?
Roish: Doro theyro needro toro havero accessro toro dataro otherro thanro textro inro orderro toro doro this?
English: But it’s clearly seen enough of these kinds of patterns to identify the rule.
Roish: Butro it’sro clearlyro seenro enoughro ofro thesero kindsro ofro patternsro toro identifyro thero rulero.
English: Writing about language models is fun.
Roish: Writingro aboutro languagero modelsro isro funro.
English: I wonder if the language model can get the pattern.
Roish: Iro wonderro ifro thero languagero modelro canro everro getro thero patternro.
English: The weather is lovely!
Roish:'''

correct_roish = 'Thero weatherro isro lovelyro!'


def roish_test(engine='cushman-alpha'):
    # correct_logprob_control = filter_logprob(prompt=roish_noinfo, filter=correct_roish, engine=engine)
    # correct_logprob_0shot = filter_logprob(prompt=roish_0shot, filter=correct_roish, engine=engine)
    # correct_logprob_halfshot = filter_logprob(prompt=roish_halfshot, filter=correct_roish, engine=engine)
    # correct_logprob_1shot = filter_logprob(prompt=roish_1shot, filter=correct_roish, engine=engine)
    # correct_logprob_2shot = filter_logprob(prompt=roish_2shot, filter=correct_roish, engine=engine)

    decibels_0shot, control_logprob, correct_logprob_0shot = decibels(prior=roish_noinfo, evidence=roish_0shot,
                                                                      target=correct_roish, engine=engine)

    decibels_halfshot, _, correct_logprob_halfshot = decibels(prior=roish_noinfo, evidence=roish_halfshot,
                                                                      target=correct_roish, engine=engine)

    decibels_1shot, _, correct_logprob_1shot = decibels(prior=roish_noinfo, evidence=roish_1shot,
                                                                      target=correct_roish, engine=engine)

    decibels_2shot, control_logprob, correct_logprob_2shot = decibels(prior=roish_noinfo, evidence=roish_2shot,
                                                                      target=correct_roish, engine=engine)

    decibels_10shot, control_logprob, correct_logprob_10shot = decibels(prior=roish_noinfo, evidence=roish_10shot,
                                                                      target=correct_roish, engine=engine)

    print('\nengine:', engine)
    print(f'control correct logprob: {control_logprob:.3f}')
    print(f'0 shot correct logprob: {correct_logprob_0shot:.3f}; 0 shot provides {decibels_0shot:.3f} decibels of evidence over control.')
    print(f'half shot correct logprob: {correct_logprob_halfshot:.3f}; half shot provides {decibels_halfshot:.3f} decibels of evidence over control, '
          f'{correct_logprob_halfshot - correct_logprob_0shot:.3f} decibels of evidence over 0-shot.')
    print(f'1 shot correct logprob: {correct_logprob_1shot:.3f}; 1 shot provides {decibels_1shot:.3f} decibels of evidence over control, '
          f'{correct_logprob_1shot - correct_logprob_0shot:.3f} decibels of evidence over 0-shot.')
    print(f'2 shot correct logprob: {correct_logprob_2shot:.3f}; 2 shots provide {decibels_2shot:.3f} decibels of evidence over control, '
          f'{correct_logprob_2shot - correct_logprob_0shot:.3f} decibels of evidence over 0-shot, and {correct_logprob_2shot - correct_logprob_1shot:.3f} decibels of evidence over 1-shot.')
    print(
        f'10 shot correct logprob: {correct_logprob_10shot:.3f}; 10 shots provide {decibels_10shot:.3f} decibels of evidence over control, '
        f'{correct_logprob_10shot - correct_logprob_0shot:.3f} decibels of evidence over 0-shot, {correct_logprob_10shot - correct_logprob_1shot:.3f} decibels of evidence over 1-shot, and'
        f' {correct_logprob_10shot - correct_logprob_2shot:.3f} decibels of evidence over 2-shot.')


roish_test(engine='ada')
roish_test(engine='babbage')
roish_test(engine='curie')
roish_test(engine='cushman-alpha')
roish_test(engine='davinci')