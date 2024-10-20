import tkinter as tk
import random
from time import sleep

class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def attack(self, other, action):
        damage = random.randint(10, 30) 
        other.health -= damage
        return damage

    def is_alive(self):
        return self.health > 0

class FightingGame:
    def __init__(self, root, player1_name, player2_name):
        self.root = root
        self.character1 = Character(player1_name, 100)
        self.character2 = Character(player2_name, 100)

        self.root.title("Fighting Game")

        self.canvas = tk.Canvas(root, width=800, height=400, bg="lightgrey")
        self.canvas.pack()

        self.status_label = tk.Label(root, text=self.get_status(), font=("Arial", 14))
        self.status_label.pack()

        self.action_frame = tk.Frame(root)
        self.action_frame.pack()

        self.create_action_buttons()

        self.draw_characters()

    def create_action_buttons(self):
        actions = [
            "Kick",
            "Punch",
            "Head Butt",
            "Chokeslam",
            "Special Power Attack"
        ]
        
        for action in actions:
            button = tk.Button(self.action_frame, text=action, command=lambda a=action: self.perform_action(a))
            button.pack(side=tk.LEFT)

    def perform_action(self, action):
        if self.character1.is_alive() and self.character2.is_alive():
            damage = self.character1.attack(self.character2, action)
            self.animate_attack(self.character1, self.character2, action, damage)

            if not self.character2.is_alive():
                self.update_status(f"{self.character2.name} is defeated! {self.character1.name} wins!")
                return
            self.update_status(f"{self.character2.name} is thinking...")
            self.action_frame.after(2000, self.enemy_turn) 

    def enemy_turn(self):
        if self.character1.is_alive() and self.character2.is_alive():
            enemy_action = random.choice(["Kick", "Punch", "Head Butt", "Chokeslam", "Special Power Attack"])
            self.update_status(f"{self.character2.name} chose {enemy_action}!")
            
            damage = self.character2.attack(self.character1, enemy_action)
            self.animate_attack(self.character2, self.character1, enemy_action, damage)

            if not self.character1.is_alive():
                self.update_status(f"{self.character1.name} is defeated! {self.character2.name} wins!")

    def animate_attack(self, attacker, defender, action, damage):
        self.update_status(f"{attacker.name} uses {action}! {defender.name} takes {damage} damage.")
        self.update_health_display()

        attacker_original_x = 100 if attacker == self.character1 else 600 
        defender_x = 600 if attacker == self.character1 else 100           
        for i in range(11):
            self.canvas.delete("all")  

            attacker_x = attacker_original_x + i * ((defender_x - attacker_original_x) // 10)
            
            if i < 10:  
                self.draw_character(attacker_x, 250, attacker)
            else:  
                self.draw_character(defender_x, 250, attacker)
                self.draw_character(defender_x, 250, defender, hit=True)  
            
            if i < 10: 
                self.draw_character(defender_x, 250, defender)

            self.canvas.update()
            self.canvas.after(30)

        for i in range(11):
            self.canvas.delete("all")  

            attacker_x = defender_x - i * ((defender_x - attacker_original_x) // 10)
            
            self.draw_character(attacker_x, 250, attacker)
            
            self.draw_character(defender_x, 250, defender)

            self.canvas.update()
            self.canvas.after(30)
        self.draw_characters()


    def draw_characters(self):
        self.canvas.delete("all")  # Clear previous drawings
        self.draw_character(100, 250, self.character1)
        self.draw_character(600, 250, self.character2)

    def draw_character(self, x, y, character, hit=False):
        body_color = "red" if hit else "blue"
        self.canvas.create_oval(x, y - 50, x + 50, y, fill=body_color) 
        self.canvas.create_rectangle(x + 10, y, x + 40, y + 100, fill=body_color)  
        self.canvas.create_line(x + 10, y + 30, x, y + 60, fill=body_color, width=5) 
        self.canvas.create_line(x + 40, y + 30, x + 50, y + 60, fill=body_color, width=5)  
        self.canvas.create_line(x + 10, y + 100, x + 20, y + 150, fill=body_color, width=5)  
        self.canvas.create_line(x + 40, y + 100, x + 30, y + 150, fill=body_color, width=5)  
        self.canvas.create_text(x + 25, y - 70, text=character.name, fill="black", font=("Arial", 12))

    def get_status(self):
        return f"{self.character1.name} Health: {self.character1.health} | {self.character2.name} Health: {self.character2.health}"

    def update_health_display(self):
        self.status_label.config(text=self.get_status())

    def update_status(self, message):
        self.status_label.config(text=message)

def start_game():
    player1_name = player1_entry.get()
    player2_name = player2_entry.get()
    if player1_name and player2_name:
        root.destroy()
        new_root = tk.Tk()
        game = FightingGame(new_root, player1_name, player2_name)
        new_root.mainloop()

root = tk.Tk()
root.title("Fighting Game - Enter Player Names")

tk.Label(root, text="Enter Player 1 Name:").pack()
player1_entry = tk.Entry(root)
player1_entry.pack()

tk.Label(root, text="Enter Player 2 Name:").pack()
player2_entry = tk.Entry(root)
player2_entry.pack()

start_button = tk.Button(root, text="Start Fight", command=start_game)
start_button.pack()

root.mainloop()
