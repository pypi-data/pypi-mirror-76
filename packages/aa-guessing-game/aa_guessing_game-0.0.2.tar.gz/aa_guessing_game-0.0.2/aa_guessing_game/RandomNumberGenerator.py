import random

class RandomNumberGenerator:
    def __init__(self, difficulty):
        self.number_to_guess = 0;
        self.difficulty = difficulty
    
    def generate(self):
        if (self.difficulty == 'easy'):
            self.number_to_guess = random.randint(1,5)
            print('The number is between 1 and 5')
        elif (self.difficulty == 'hard'):
            self.number_to_guess = random.randint(1,10)
            print('The number is between 1 and 10')
                  
    def isGuessCorrect(self, guess):
        if (int(guess) == self.number_to_guess):
            return 'You win! The number was ' + str(self.number_to_guess);
        else:
            return 'You lose! The number was ' + str(self.number_to_guess);
                  
                 

                  
        
    