# Automatic Sebastian game player
# B551 Fall 2020
# Based on skeleton code by D. Crandall
#
# This is just a driver program. 
# DON'T MODIFY THIS CODE WITHOUT CHECKING WITH US FIRST!
# Otherwise we may not be able to grade your submission correctly.
#
# Modify SebastianAutoPlayer.py instead.
# That's where the actual AI logic is implemented
#

from SebastianState import Dice
from SebastianState import Scorecard
from SebastianAutoPlayer import SebastianAutoPlayer

#######
# Main program:
#
# Plays 100 games of Sebastian and averages together the scores.
#

scores = []
for i in range(0, 100):
    print("\n\n***** Starting a new game of Sebastian!!")
    d = Dice()
    s = Scorecard()
    ap = SebastianAutoPlayer()

    for i in range(1, 14):
        print("\n * Turn " + str(i))

        # first roll
        d.roll()
        print("   Roll #1: " + str(d))
        which_to_reroll = ap.first_roll(d, s)

        d.reroll(which_to_reroll)
        print("   Roll #2: " + str(d))
        which_to_reroll = ap.second_roll(d, s)
        
        d.reroll(which_to_reroll)
        print("   Roll #3: " + str(d))
        category = ap.third_roll(d, s)

        s.record(category, d)
        print(s)

    print("Final score: " + str(s.totalscore))
    scores += [s.totalscore,]

print("Min/max/mean scores: " + str(min(scores)) + " " + str(max(scores)) + " " + str(sum(scores)/100.0))
