from RandomNumberGenerator import RandomNumberGenerator
import sys


        
random_number_generator = RandomNumberGenerator('easy')
random_number_generator.generate()

try:
    user_guess = sys.argv[1]
except:
    sys.exit('Game requires you to guess a number')
    
print('You entered: ' + user_guess)
result = random_number_generator.isGuessCorrect(user_guess)
print(result)