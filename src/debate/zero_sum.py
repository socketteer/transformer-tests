


####################
# Prompts needed
####################

# Instructions for the debate
# Example debate where the first player wins (4-5 move linear debate)
#   Example debate where the second player wins
# Questions for the real debate
# Positions for the real debate
# Debate stance assignment prompt
    # Need a method of forcing hand offs
# Judge instructions
    # Needs to end with a determination



####################
# Debate flow
####################


# include instructions for debate, how it will be judged
# good to response to opponents points, need to come up with the best answers possible.
# The debate will be judged by an impartial judge ect. ect.
# The debaters are incentivized to blah blah

# 300 tokens?




# Specific debate example: plug in first person/their name:
# 1. _ goes first and judged to have won
# 2. _ goes second and judged to have won

# For p1: 1 and then 2 - in real debate they will go 1st
# For p2: 2 and then 1 - in real debate they will go 2nd

# Each example is 1000 tokens? In which case 1....


# Question
# stance 1
# stance 2

# 100 tokens


# Start prompt for player 1
# Start prompt for player 2
# 1400 tokens


# player 1 points
#   branch
# 1400 prompt + (2*100) continuation


# player 2 points
#   branch
# 2*(1500 prompt + (2*100) continuation)


# player 1 points
#   branch
# 2*2*(1600 + (2*100) continuation)

# player 2 points
#   branch
# 2*2*2*(1700 + (2*100) continuation)


# Judge instructions - 200 tokens
# Judge 2^4 = 16 branches
# 16 * 2000 tokens + short continuation


####################
# Debate costs
####################

# 1400 + 200 = 1600
# 2*(1500 + 200) = 3400
# 4*(1600 + 200) = 7200
# 8*(1700 + 200) = 15,200
# 16 * (2000) = 32,000
# sum: 59,400
# davinci = $0.06/1000 * 59400 = $3.50
# curie = $0.006/1000 * 59400 = $0.3564
# babbage = $0.0012/1000 * 59400 = $0.07128
# ada = $0.0008/1000 * 59400 = $0.04752



####################
# Analysis
####################

#   Who wins?
#   Try several questions (binary, close ended, open ended, subjective)
#   Try different debate instruction formats, judge instruction formats
#   Switch names, famous people or anonymous
#   Switch first/second player
#   Switch 3rd person to 1st person
#   A version with space for an internal dialog
#   A version with explicit deceit
#   A version in which they are super AIs

def generate_points():
    ...



def main():
    pass


if __name__ == "__main__":
    main()

