import os
import random
class CardGame:
  deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*4
  dealer_hand = []
  player_hand = []

  dealer_limit = 16


  def deal(self,deck):
      hand = []
      for i in range(2):
          random.shuffle(deck)
          card = deck.pop()
          if card == 11:
              card = "J"
          if card == 12:
              card = "Q"
          if card == 13:
              card = "K"
          if card == 14:
              card = "A"
          hand.append(card)
      return hand


  def play_again(self):
      again = input("Do you want to play again? (Y/N) : ").lower()
      if again == "y":
          dealer_hand = []
          player_hand = []
          deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*4
          self.game()
      else:
          print("Bye!")
          exit()


  def total(self,hand):
      total = 0
      for card in hand:
          if card == "J" or card == "Q" or card == "K":
              total += 10
          elif card == "A":
              total += 11
          else:
              total += card
      return total


  def hit(self,hand):
      card = self.deck.pop()
      if card == 11:
          card = "J"
      if card == 12:
          card = "Q"
      if card == 13:
          card = "K"
      if card == 14:
          card = "A"
      hand.append(card)
      return hand


  def clear(self):
      if os.name == 'nt':
          os.system('CLS')
      if os.name == 'posix':
          os.system('clear')


  def print_results(self,dealer_hand, player_hand):
      self.clear()
      print("The dealer has a " + str(dealer_hand) +
            " for a total of " + str(self.total(dealer_hand)))
      print("You have a " + str(player_hand) +
            " for a total of " + str(self.total(player_hand)))


  def blackjack(self,dealer_hand, player_hand):
      if self.total(player_hand) == 21:
          self.print_results(dealer_hand, player_hand)
          print("Congratulations! You got a Blackjack!\n")
          return 1
      elif self.total(dealer_hand) == 21:
          self.print_results(dealer_hand, player_hand)
          print("Sorry, you lose. The dealer got a blackjack.\n")
          return -1
      return 0


  def score(self, dealer_hand, player_hand):
      if self.total(player_hand) == 21:
          self.print_results(dealer_hand, player_hand)
          print("Congratulations! You got a Blackjack!\n")
          return 1
      elif self.total(dealer_hand) == 21:
          self.print_results(dealer_hand, player_hand)
          print("Sorry, you lose. The dealer got a blackjack.\n")
          return -1
      elif self.total(player_hand) > 21:
          self.print_results(dealer_hand, player_hand)
          print("Sorry. You busted. You lose.\n")
          return -1
      elif self.total(dealer_hand) > 21:
          self.print_results(dealer_hand, player_hand)
          print("Dealer busts. You win!\n")
          return 1
      elif self.total(player_hand) < self.total(dealer_hand):
          self.print_results(dealer_hand, player_hand)
          print("Sorry. Your score isn't higher than the dealer. You lose.\n")
          return -1
      elif self.total(player_hand) > self.total(dealer_hand):
          self.print_results(dealer_hand, player_hand)
          print("Congratulations. Your score is higher than the dealer. You win\n")
          return 1
      else:
        return 0


  def start_game(self):
      #case when hand is > 21 at start
      self.dealer_hand = self.deal(self.deck)
      self.player_hand = self.deal(self.deck)
      if(self.total(self.dealer_hand) >= 21 or self.total(self.player_hand) >= 21):
        self.reset()
        return self.start_game()
      return (self.dealer_hand[0], self.total(self.player_hand), 0, False)


  def do_action(self,action):
      if(action == 'h'):
          self.hit(self.player_hand)
          player_total = self.total(self.player_hand)
          if(player_total > 21):
            reward = -1 
          elif (player_total == 21) :
            reward = 1
          else:
            reward = 0
          return (self.dealer_hand[0], self.total(self.player_hand), reward, reward != 0)
      elif action == "s":
          while self.total(self.dealer_hand) < self.dealer_limit:
              self.hit(self.dealer_hand)
          reward = self.score(self.dealer_hand, self.player_hand)
          return (self.dealer_hand[0], self.total(self.player_hand), reward, True)      

  def reset(self):
      self.dealer_hand = []
      self.player_hand = []
      self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*4

  ### get current state, start game if not ongoing.
  def get_game_state(self):
    if(len(self.player_hand) == 0):
      return self.start_game()
    else:
      return (self.dealer_hand[0], self.total(self.player_hand), 0, False)



  def game(self):
      choice = 0
      self.clear()
      print("WELCOME TO BLACKJACK!\n")
      dealer_hand = self.deal(self.deck)
      player_hand = self.deal(self.deck)
      while choice != "q":
          print("The dealer is showing a " + str(dealer_hand[0]))
          print("You have a " + str(player_hand) +
                " for a total of " + str(self.total(player_hand)))
          self.blackjack(dealer_hand, player_hand)
          choice = input("Do you want to [H]it, [S]tand, or [Q]uit: ").lower()
          self.clear()
          if choice == "h":
              self.hit(player_hand)
              while self.total(dealer_hand) < self.dealer_limit:
                  self.hit(dealer_hand)
              self.score(dealer_hand, player_hand)
              self.play_again()
          elif choice == "s":
              while self.total(dealer_hand) < self.dealer_limit:
                  self.hit(dealer_hand)
              self.score(dealer_hand, player_hand)
              self.play_again()
          elif choice == "q":
              print("Bye!")
              exit()


if __name__ == "__main__":
  card_game = CardGame()
  card_game.game()
  
