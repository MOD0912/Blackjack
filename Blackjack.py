import os
import random
import re
try:
    import pyautogui
except:
    os.system("py -m pip install pyautogui")
  
try:
    import customtkinter as ctk
except:
    os.system("py -m pip install customtkinter")

try: 
    from PIL import Image, ImageTk
except:
    os.system("py -m pip install pillow")


class cards:
    def function(self):
        path ="cards"
        self.filelist = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file == "CardBack.png":
                    continue
                self.filelist.append(os.path.join(root, file))
        return self.filelist
        


class BlackjackGame(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width, self.height= pyautogui.size()
        print(self.width, self.height)
        self.delet()

    def delet(self):
        self.attributes("-fullscreen", True)
        self.bg = ImageTk.PhotoImage(Image.open("design\\design1.png").resize(size=(self.width, self.height)))
        self.canvas1 = ctk.CTkCanvas(self)
        self.canvas1.pack(fill = "both", expand = True)
        self.canvas1.create_image( 0, 0, image = self.bg, anchor = "nw")
        print(self.keys())
        self.second_card = None
        self.second_card_counter = 0
        self.player_cards_x = self.width/2
        self.player_cards_y = 730
        self.coupier_cards_x = self.width/2
        self.coupier_cards_y = 235
        self.x_change = 20
        self.y_change = 20
        self.value_player = 0
        self.value_coupier = 0
        self.lst = []
        self.filelist = cards().function()
        self.create_widgets()
        
    def create_widgets(self):
        self.coupier_text = self.canvas1.create_text(self.width/2, self.height/21.6, text=f"coupier value: {self.value_coupier}", font=('Times New Roman', 20, 'bold'), fill="white")
        self.player_text = self.canvas1.create_text(self.width/2, self.height/2, text=f"coupier value: {self.value_coupier}", font=('Times New Roman', 20, 'bold'), fill="white")
        self.create_cards("Coupier")
        self.create_cards("Player")
        self.create_cards("Coupier")
        self.create_cards("Player")

        self.Hit = ctk.CTkButton(self.canvas1, text="Hit", height=self.height/21.6, width=self.width/9.6, command=lambda:self.create_cards("Player"), fg_color="#202020", corner_radius=0)
        self.Hit.place(x=self.width/2-self.width/4.8, y=self.height-self.height/10.8)
        self.Stand = ctk.CTkButton(self.canvas1, text="Stand", height=self.height/21.6, width=self.width/9.6, command=self.stand, fg_color="#202020", corner_radius=0)
        self.Stand.place(x=self.width/2-100, y=self.height-self.height/10.8)
        self.leave = ctk.CTkButton(self.canvas1, text="Hit and run", height=self.height/21.6, width=self.width/9.6, command=exit, fg_color="#202020", corner_radius=0)
        self.leave.place(x=self.width/2+self.width/4.8-200, y=self.height-self.height/10.8)



    def create_cards(self, player):
        if len(self.filelist) == 0:
            self.filelist = cards().function()
        self.card = random.choice(self.filelist)
        self.filelist.remove(self.card)
        self.value = int(re.search(r'\d+', self.card).group())          # gets integer out of a string
        if player == "Player":
            self.player_cards_x += self.x_change
            self.player_cards_y += self.y_change
            self.x = self.player_cards_x - self.x_change
            self.y = self.player_cards_y - self.y_change
            self.value_player += self.value
            print(f"player value:{self.value_player}")
        else:
            self.second_card_counter += 1
            if self.second_card_counter == 2:
                self.card = "cards\CardBack.png"

            else:
                self.value_coupier += self.value
            self.coupier_cards_x += self.x_change
            self.coupier_cards_y += self.y_change
            self.x = self.coupier_cards_x - self.x_change
            self.y = self.coupier_cards_y - self.y_change
            print(f"coupier value:{self.value_coupier}")
        self.canvas1.itemconfig(self.coupier_text, text=f"coupier value: {self.value_coupier}")
        self.canvas1.itemconfig(self.player_text, text=f"player value: {self.value_player}")
        self.card = ImageTk.PhotoImage(Image.open(self.card).resize((int(self.width/9.6), int(self.height/3.6))))
        self.image = self.canvas1.create_image(self.x, self.y, image=self.card)
        if self.second_card_counter == 2 and player == "Coupier":
            self.hidden_card = self.image
        self.lst.append(self.card)                  #handels commen error
        if self.value_player > 21:
            winner="coupier"
            self.end(winner)
        elif self.value_coupier > 21:
            winner = "player"
            self.end(winner)
        if self.value_player == 21:
            self.stand()

    def stand(self):
        self.coupier_cards_x = self.coupier_cards_x - self.x_change
        self.coupier_cards_y = self.coupier_cards_y- self.y_change
        self.canvas1.delete(self.hidden_card)
        while self.value_coupier < 17:
            self.create_cards("Coupier")
        if self.value_coupier < self.value_player:
            winner = "player"
        if self.value_coupier > self.value_player:
            winner = "coupier"
        if self.value_coupier == self.value_player:
            winner = "draw"
        if self.value_coupier > 21 or self.value_player > 21:
            return
        self.end(winner)

    def end(self, winner):
        print(f"winner is {winner}")
        if winner == "draw":
            self.text = "draw"
            x = 625
        else:
            self.text = f"{winner} won!"
        if winner == "player":
            x = 200
        if winner == "coupier":
            x = 125
        self.Hit.configure(command=None)
        self.Stand.configure(command=None)
        self.frame_end = ctk.CTkFrame(self, width=500, height=500)
        self.frame_end.place(x=x, y=300)
        self.label_end = ctk.CTkLabel(self.frame_end, text=self.text, font=('Times New Roman', 300, 'bold'))
        self.label_end.pack()
        self.button_end_restart = ctk.CTkButton(self.frame_end, text="Again?", command=self.close, height=50)
        self.button_end_restart.pack(fill="x")
        self.button_end_end = ctk.CTkButton(self.frame_end, text="End the game", command=exit, height=50)
        self.button_end_end.pack(fill="x")

    def close(self):
        self.canvas1.destroy()
        self.delet()

 

game = BlackjackGame()
game.mainloop()
