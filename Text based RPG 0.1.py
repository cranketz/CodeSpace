import os
#                               1.Blok; Menü ve ardından inputlar 
#                             (cinsiyet sistemi buraya eklenecek.)
menu = """
      [1]Attack
      [2]Defence
      [3]Rest
      [4]Focus
      [Q]Exit
      Every player have two moves.
      Please select your move!
      """

class Player():
      name = ''
      hp = 100
      atk = 25
      defence = 20

player1 = Player()
player2 = Player()
#                       Oyuncu isimlerini sınıflarına tanımlama işlemi
name1 = input("Name of the player 1 :")
name2 = input("Name of the player 2 :")
player1.name = name1
player2.name = name2

#                             2.Blok; Fonksiyonların tanımlanması 
#                  (Gerekli fonksiyonlara kritik şans sistemi eklenecek)

def attack(attacker,defender):
      print("--------------------------------------------------------------------")
      print("{} decided to attack to {}!".format(attacker.name,defender.name))
      print("{}' health is {} and his defence is {}".format(defender.name,defender.hp,defender.defence))
      print()
      if defender.defence >= attacker.atk:
            print("{} attacked {} but he defended!".format(attacker.name,defender.name))
      else:
            defender.hp = defender.hp - (attacker.atk - defender.defence)
            print("The {} hit {} damage to {}!".format(attacker.name,attacker.atk,defender.name))
      print("{}'s health is now {}".format(defender.name,defender.hp))
      print("--------------------------------------------------------------------")

def defence(player):
      print("--------------------------------------------------------------------")
      print("{} decided to defence!".format(player.name))
      print("{}'s defence is {}".format(player.name,player.defence))
      print()
      addedDefence = player.defence * 10 / 100
      player.defence = player.defence + addedDefence
      print("{} is improved his defence! now he have {} defence".format(player.name,player.defence))
      print("--------------------------------------------------------------------")
def rest(player):
      print("--------------------------------------------------------------------")
      print("{} decided to rest!".format(player.name))
      print("{}'s health is {}".format(player.name,player.hp))
      print()
      heal = player.hp * 15 / 100
      player.hp = player.hp + heal
      print("The {} healed himself! Now he have {} hp".format(player.name,player.hp))
      print("--------------------------------------------------------------------")

def focus(player):
      print("--------------------------------------------------------------------")
      print("{} decided to focus for increasing his attack!".format(player.name))
      print("{}'s Attack power is {}!".format(player.name,player.atk))
      print()
      addedAtk = player.atk * 20 /100
      player.atk = player.atk + addedAtk
      print("{}'s Attack is now {}!".format(player.name,player.atk))
      print("--------------------------------------------------------------------")

#                                         3.Blok Döngüler

while True:
      turn = 2
      while turn >= 1:
            if turn < 1:
                  break
            else:
                  os.system('cls')
                  print("{}'s turn!".format(player1.name))
                  print(menu)
                  print("Which move you will do?")
                  choice = input()
                  if choice == "1":
                        attack(player1,player2)
                        turn = turn - 1
                        print("Press enter to continue")
                        input()
                  elif choice == "2":
                        defence(player1)
                        turn = turn - 1
                        print("Press enter to continue")
                        input()
                  elif choice == "3":
                        rest(player1)
                        turn = turn - 1
                        print("Press enter to continue")
                        input()
                  elif choice == "4":
                        focus(player1)
                        turn = turn - 1
                        print("Press enter to continue")
                        input()
                  elif choice == "Q" or choice == "q":
                        print("Leaving the game...")
                        exit()
                  else:
                        print("Invalid choice! Please enter a valid number.")
                        input()
      turn = 2
      while turn >= 1:
            if turn < 1:
                  break
            else:
                  os.system('cls')
                  print("{}'s turn!".format(player2.name))
                  print(menu)
                  print("Which move you will do?")
                  choice = input()
                  if choice == "1":
                        attack(player2,player1)
                        turn = turn - 1
                        print("Press enter to continue")
                        input()
                  elif choice == "2":
                        defence(player2)
                        turn = turn - 1
                        print("Press enter to continue")
                        input()
                  elif choice == "3":
                        rest(player2)
                        turn = turn - 1
                        print("Press enter to continue")
                        input()
                  elif choice == "4":
                        focus(player2)
                        turn = turn - 1  
                        print("Press enter to continue")
                        input()
                  elif choice == "Q" or choice == "q":
                        print("Leaving the game...")
                        exit()
                  else:
                        print("Invalid choice! Please enter a valid number.")
                        print("Press enter to continue")
                        input()
                        break