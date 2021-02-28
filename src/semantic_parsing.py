from conditional import substring_probs, sort_logprobs

preprompt = '''This measure would prohibit government agencies from confiscating guns or other firearms from citizens without due process, or from requiring background checks on firearm recipients unless a uniform national standard is required. 
Should this measure be enacted into law?
Should this proposition be approved? 
Let's consider both supporting and opposing arguments. 
On one hand,'''

content = ''' this proposition would protect gun owners from having their weapons confiscated by governments. If the government cannot confiscate guns, then law-abiding citizens will be in a better position to defend themselves from criminals who do not follow the law. Furthermore, the right to self-defense is an important one. If government officials can take away a person's guns, then this right is compromised. On the other hand, the proposition could be considered a threat to public safety. If a person cannot be prevented from possessing a firearm, then he or she could use a gun to commit crimes. Furthermore, if a person uses a gun to commit a crime, then the government has an obligation to do something about it. If the government cannot remove a gun from a person's possession, then it could be more difficult to prevent future crimes from being committed.'''

target = '\nOn the other hand'

engine = 'ada'

substrings, logprobs = substring_probs(preprompt=preprompt, content=content, target=target, engine=engine, quiet=1)
sorted_logprobs = sort_logprobs(substrings, logprobs)

print(engine)

print('\nLOGPROBS')
print(logprobs)

print('\nTOP LOGPROBS')
for substring in sorted_logprobs[:8]:
    print(substring)

print('\nBOTTOM LOGPROBS')
for substring in sorted_logprobs[-5:]:
    print(substring)