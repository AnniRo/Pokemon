class Pokemon:
  # A pokemon has a name, level, type,
  # maximum health points which are determined by its level,
  # current health points which are equal to the maximum at the beginning,
  # a knocked-out state which is False at the beginning,
  # experience points which are determined by its level, and
  # an evolution family list
  def __init__(self, name, level, type, fam):
    self.name = name
    self.level = level
    self.type = type
    self.hp = level * 3
    self.max_hp = level * 3
    self.knocked_out = False
    self.exp = (level-1) * 10**3
    self.fam = fam


  def __repr__(self):
    # When a pokemon is printed, its info and current state will be returned
    return '{name}! ({type} type, Lv.: {level}, HP: {hp}, Exp.Points: {exp})'.format(name=self.name, type=self.type, level=self.level, hp=self.hp, exp=self.exp)
            #'To Next Lv. {expleft}'.format())
            #isknockedout         


  def lose_health(self, damage):
    # Pokemon loses health points
    self.hp -= damage
    # if pokemon's damage is greater or equal to its health points, then the pokemon faints
    # pokemon's health points are set to zero
    if self.hp <= 0:
      self.hp = 0
      self.knocked_out = True
      print('{} fainted!'.format(self.name))
      print('--------------------------------')
    else:  
      print('{name} lost {amount} health point(s).'.format(name=self.name, amount=damage))
      print('--------------------------------')


  def gain_health(self, hp_gained):
    # if pokemon is fainted, it should be revived
    if self.knocked_out == True:
      print('{name} is knocked out. It should be revived first.\n'.format(name=self.name)) 
    # The sum of pokemon's health points and the gained amount cannot surpass its maximum health points
    elif (hp_gained + self.hp) > self.max_hp:
      print('{name}\'s health points are now {maxhp}.'.format(name=self.name, maxhp=self.max_hp))   
    # The pokemon's health points is increased by the gained amount of hp
    else:
      self.hp += hp_gained
      print('{pok}\'s health points are increased by {gain}.'.format(pok=self.name, gain=round(hp_gained)))


  def revive_pokemon(self):
    # Changes the pokemon's knocked-out status from True to False if a status healer is used
    if self.knocked_out == True:
      self.knocked_out = False
      print('{} recovered from fainting!'.format(self.name))
      print('--------------------------------')
    else:    
      print('{name} is not fainted! (HP = {hp})'.format(name=self.name, hp=self.hp))
      print('--------------------------------')  

     
  def attack(self, other_pokemon):
    # Checks if the pokemon is fainted
    if self.knocked_out == True:
      print(str(self.name) + ' is fainted! It cannot attack.')
      print('--------------------------------')
    elif other_pokemon.knocked_out == True:
      print('{pok} cannot attack a fainted pokemon!'.format(pok=self.name))  
      print('--------------------------------')
    # Depend on the pokemon's type, if it's advantageous over the opponent's type, 
    # the damage to the opponent is twice the level of the pokemon that attacked
    elif (self.type == 'fire' and other_pokemon.type == 'grass') or (self.type == 'water' and other_pokemon.type == 'fire') or (self.type == 'grass' and other_pokemon.type == 'water'):
      print('{pok} attacks {otherpok}!'.format(pok=self.name, otherpok=other_pokemon.name))
      damage = 2 * self.level
      print('Very effective!')
      print('--------------------------------')
      other_pokemon.lose_health(damage)
      self.exp_gain(other_pokemon)
    # Depend on the pokemon's type, if it's disadvantageous over the opponent's type, 
    # the damage to the opponent is half the level of the pokemon that attacked
    elif (self.type == 'fire' and other_pokemon.type == 'fire') or (self.type == 'grass' and other_pokemon.type == 'grass') or (self.type == 'water' and other_pokemon.type == 'water') or (self.type == 'fire' and other_pokemon.type == 'water') or (self.type == 'water' and other_pokemon.type == 'grass') or (self.type == 'grass' and other_pokemon.type == 'fire'):
      print('{pok} attacks {otherpok}!'.format(pok=self.name, otherpok=other_pokemon.name))
      damage = 0.5 * self.level
      print('Not very effective!')
      print('--------------------------------')
      other_pokemon.lose_health(round(damage))
      self.exp_gain(other_pokemon)          
           

  def exp_gain(self, other_pokemon):
    # Experience points required to level up, are determined by pokemon's level
    levelup_exp = self.level * 10**3
    # if the opponent has fainted, then the winning pokemon gains health 
    # and experience points based on the opponent's level 
    if other_pokemon.knocked_out == True:
        self.exp += 100 * other_pokemon.level
        # Pokemon levels up when it reaches the required experience points,
        # maximum health is increased, and
        if self.exp >= levelup_exp:
          self.level += 1
          self.max_hp += 50 
          print(self.name + ' grew to Lv. ' + str(self.level) + '!')
          self.gain_health(round(1.5 * other_pokemon.level))
          self.evolution() 
          print(str(self.name) + ': Exp. Points = ' + str(self.exp) + ', HP = ' + str(self.hp) + ', Max. HP = ' + str(self.max_hp))       
        else:
          print(self.name + ' won!')
          print(self.name + ' gained ' + str(self.exp) + ' Exp.Points!')
          print('--------------------------------')


  def evolution(self):
      # Pokemon evolves into the second pokemon in family list after it reaches a certain level
      if self.level >= 6:
        self.name = self.fam[1]
        print(self.fam[0] + ' evolves into ' + self.name + '!')
      # Pokemon evolves into the third pokemon in family list when it reaches level 20
      elif self.level >= 20:
        self.name = self.fam[2]
        print(self.fam[1] + ' evolves into ' + self.name + '!')


# Subclasses of class Pokemon are defined with their names, type and evolution family
class Charmander(Pokemon):
  def __init__(self, level):
    super().__init__('Charmander', level, 'fire', ['Charmander', 'Charmeleon', 'Charizard'])  


class Bulbasaur(Pokemon):
  def __init__(self, level):
    super().__init__('Bulbasaur', level, 'grass', ['Bulbasaur', 'Ivysaur', 'Venusaur'])


class Squirtle(Pokemon):
  def __init__(self, level):
    super().__init__('Squirtle', level, 'water', ['Squirtle', 'Wartortle', 'Blastoise'])    


class Trainer:
  # A Trainer has a name, a list of pokemons, 
  # a dictionary of different potions with each respective health points,
  # a list with status healers,
  # and an active pokemon which is the first pokemon of the list (represented with 0)
  def __init__(self, name, pokemons):
    self.name = name
    self.pokemons = pokemons
    self.potions = {'Potion': 20, 'Super Potion': 50, 'Hyper Potion': 200}
    self.status_healers = ['Revive', 'Max Revive']
    self.active_pok = 0

 
  def potion_use(self, potion):
    while True:
      # The user selects a pokemon to use the potion
      print('{} select a Pokemon to heal:'.format(self.name))
      pokemon_number = input(('Type 1 for ' + str(self.pokemons[0]) + '\n'
                              'Type 2 for ' + str(self.pokemons[1]) + '\n'
                              'Type 3 for ' + str(self.pokemons[2]) + '\n'))

      if pokemon_number == '1':
        chosen_pokemon = self.pokemons[0]  
      elif pokemon_number == '2':
        chosen_pokemon = self.pokemons[1]   
      elif pokemon_number == '3':
        chosen_pokemon = self.pokemons[2]

      # Checks if there are potions in the dictionary
      if bool(self.potions) == False:
        print(self.name + ', you don\'t have any potions\n')
        print('--------------------------------')
        break
      # Checks if there is a specific potion in the dictionary
      elif potion not in self.potions:
        print(self.name + ', you don\'t have ' + potion + ' at your disposal\n')
        print('--------------------------------')  
        continue
      # Uses the potion to restore the pokemon's health points,
      # removes the potion from the dictionary,
      # and prints which potions are left
      else:  
        print('{pokemon}\'s HP was restored by {num} point(s).'.format(pokemon=chosen_pokemon, num=self.potions[potion]))
        chosen_pokemon.gain_health(self.potions[potion])
        self.potions.pop(potion)
        print('Potions left: ' + str(self.potions))
        print('--------------------------------')
        break


  def healer_use(self, healer):
    while True:
      # The user selects a pokemon to use the healer
      print('{} select a Pokemon to recover:'.format(self.name))
      pokemon_number = input(('Type 1 for ' + str(self.pokemons[0]) + '\n'
                              'Type 2 for ' + str(self.pokemons[1]) + '\n'
                              'Type 3 for ' + str(self.pokemons[2]) + '\n'))

      if pokemon_number == '1':
        chosen_pokemon = self.pokemons[0]  
      elif pokemon_number == '2':
        chosen_pokemon = self.pokemons[1]   
      elif pokemon_number == '3':
        chosen_pokemon = self.pokemons[2]

      # Checks if there are any status healers left in the list
      if bool(self.status_healers) == False:
        print(self.name + ', you don\'t have any status healers left!')
        break
      # Checks if there is a specific healer in the list
      elif healer not in self.status_healers:
        print(self.name + ', you don\'t have ' + healer + ' at your disposal')
        continue
      # Revives pokemon and removes the healer from the list if pokemon is fainted
      elif chosen_pokemon.knocked_out == True:    
        print('{name} uses {healer}!'.format(name=self.name, healer=healer))
        print('--------------------------------')
        chosen_pokemon.revive_pokemon()
        if healer == self.status_healers[0]:
          chosen_pokemon.gain_health(chosen_pokemon.max_hp * 0.5)
        elif healer == self.status_healers[1]:
          chosen_pokemon.gain_health(chosen_pokemon.max_hp)
        self.status_healers.remove(healer)
        print('Remaining status healers: ' + str(self.status_healers))
        print('--------------------------------')
        break
      # If pokemon is not fainted, the pokemon cannot be revived  
      else:
        chosen_pokemon.revive_pokemon()
        continue     


  def attack_other_trainer(self, other_trainer):
    # The current trainer's active pokemon attacks the other trainer's active pokemon
    my_pokemon = self.pokemons[self.active_pok]
    other_pokemon = other_trainer.pokemons[other_trainer.active_pok]    
    my_pokemon.attack(other_pokemon)
    

  def switch_pokemon(self):
    while True:
      # Switches the current active pokemon to another one that is in the pokemon list
      # Asks the user for input
      print('{} select Pokemon:'.format(self.name))
      pokemon_number = input(('Type 1 for ' + str(self.pokemons[0]) + '\n'
                              'Type 2 for ' + str(self.pokemons[1]) + '\n'
                              'Type 3 for ' + str(self.pokemons[2]) + '\n'))

      if pokemon_number == '1':
        chosen_pokemon = self.pokemons[0]  
      elif pokemon_number == '2':
        chosen_pokemon = self.pokemons[1]   
      elif pokemon_number == '3':
        chosen_pokemon = self.pokemons[2]

      # Checks if the chosen pokemon is knocked out
      if chosen_pokemon.knocked_out == True:
        print(str(self.name) + ', the pokemon you want is fainted.\nSelect another pokemon.')
        print('--------------------------------')
        continue
      # Checks if the pokemon selected is already the active one 
      elif chosen_pokemon == self.pokemons[self.active_pok]:
        print(str(self.name) + ', your active pokemon is already ' + str(chosen_pokemon) + '\nSelect another pokemon.')
        print('--------------------------------')
        continue
      # The selected pokemon becomes the active one
      elif chosen_pokemon != self.pokemons[self.active_pok]:
        print(str(self.name) + ' withdraw ' + str(self.pokemons[self.active_pok]))
        print('Go! {pok}'.format(pok=chosen_pokemon))
        print('--------------------------------')
        # Find the index of the selected pokemon in order to change it with the current active pokemon
        chosen_pokemon_index = self.pokemons.index(chosen_pokemon)
        self.pokemons[self.active_pok], self.pokemons[chosen_pokemon_index] = self.pokemons[chosen_pokemon_index], self.pokemons[self.active_pok]
        break


  def battle(self, other_trainer):
    # Start a battle
    my_pokemon = self.pokemons[self.active_pok]
    other_pokemon = other_trainer.pokemons[other_trainer.active_pok]
    print(str(other_trainer.name) + ' is challenged by ' + str(self.name) + '!')
    print('--------------------------------')
    print('{name} sent out {pok}'.format(name=self.name, pok=my_pokemon))
    print('--------------------------------')
    print('{othername} sent out {otherpok}'.format(othername=other_trainer.name, otherpok=other_pokemon))
    print('--------------------------------')
    while True:
          # Ask the user to select an action
          print('{} select action:'.format(self.name))
          selection = input(('Type 1 to attack \n' 
                             'Type 2 to switch Pokemon \n' 
                             'Type 3 to use a Potion \n'  
                             'Type 4 to use a Status Healer \n'
                             'Type anything else to leave the battle\n'))
          # Attack other trainer
          if selection == '1':
              # The first trainer attacks
              self.attack_other_trainer(other_trainer)
              # Checks if pokemons have fainted to end the battle
              if all([pok.knocked_out==True for pok in other_trainer.pokemons]):
                print('{name} has won the battle!'.format(name=self.name))
                break
              elif all([pok.knocked_out==True for pok in self.pokemons]):
                print('{name} has won the battle!'.format(name=other_trainer.name))
                break
              # If the opponent's active pokemon has fainted, the trainer switches pokemon
              elif other_pokemon.knocked_out == True:
                other_trainer.switch_pokemon()  
                # The new pokemon is set as the current active
                other_pokemon = other_trainer.pokemons[other_trainer.active_pok]
              # The second trainer attacks
              elif other_pokemon.knocked_out == False:               
                other_trainer.attack_other_trainer(self)
                # If the active pokemon has fainted, the trainer switches pokemon
                if my_pokemon.knocked_out == True:
                  self.switch_pokemon()
                  # The new pokemon is set as the current active
                  my_pokemon = self.pokemons[self.active_pok]
                  # The other trainer attacks again
                  other_trainer.attack_other_trainer(self)
                  
              continue

          # Switch Pokemon
          elif selection == '2':
                self.switch_pokemon()
                my_pokemon = self.pokemons[self.active_pok]
                # After the first trainer switches pokemon, the other trainer attacks
                other_trainer.attack_other_trainer(self)
                continue

          # Ask the user for input to select a potion                  
          elif selection == '3':
              potion_number = input(('Select Potion: \n'
                                    'Type 1 for ' + list(self.potions.keys())[0] + '\n'
                                    'Type 2 for ' + list(self.potions.keys())[1] + '\n'
                                    'Type 3 for ' + list(self.potions.keys())[2] + '\n'))

              if potion_number == '1':
                chosen_potion = list(self.potions.keys())[0]               
                self.potion_use(chosen_potion)
                # After the first trainer heals a pokemon, the other trainer attacks
                other_trainer.attack_other_trainer(self)
                continue
              elif potion_number == '2':
                chosen_potion = list(self.potions.keys())[1]                    
                self.potion_use(chosen_potion)
                other_trainer.attack_other_trainer(self)
                continue
              elif potion_number == '3':
                chosen_potion = list(self.potions.keys())[2]                                          
                self.potion_use(chosen_potion)
                other_trainer.attack_other_trainer(self)
                continue

          # Ask the user for input to select a status healer 
          elif selection == '4':
              healer_number = input(('Select a Status Healer: \n'
                                    'Type 1 for ' + self.status_healers[0] + '\n'
                                    'Type 2 for ' + self.status_healers[1] + '\n'))
              
              if healer_number == '1':
                  chosen_healer = self.status_healers[0]                    
                  self.healer_use(chosen_healer)
                  # After the first trainer revives a pokemon, the other trainer attacks
                  other_trainer.attack_other_trainer(self)
                  continue
              elif healer_number == '2':
                  chosen_healer = self.status_healers[1]                    
                  self.healer_use(chosen_healer)
                  other_trainer.attack_other_trainer(self)
                  continue
          else:
            break      


#Pokemon instances
Charmander = Charmander(5)
Bulbasaur = Bulbasaur(5)
Squirtle = Squirtle(5)
Totodile = Pokemon('Totodile', 5, 'water', ['Totodile', 'Croconaw', 'Feraligatr'])
Cyndaquil = Pokemon('Cyndaquil', 5, 'fire', ['Cyndaquil', 'Quilava', 'Typhlosion'])
Chikorita = Pokemon('Chikorita', 5, 'grass', ['Chikorita', 'Bayleef', 'Meganium'])

#Trainer instances
Carol = Trainer('Carol', [Charmander, Bulbasaur, Squirtle])
Tim = Trainer('Tim', [Cyndaquil, Chikorita, Totodile])

# Test
Carol.battle(Tim)









