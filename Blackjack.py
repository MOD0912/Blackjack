import os
import random
import re

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
                self.filelist.append(os.path.join(root, file))
        return self.filelist
        


class BlackjackGame(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.second_card = None
        self.second_card_counter = 0
        self.player_cards_x = 0
        self.player_cards_y = 0
        self.coupier_cards_x = 0
        self.coupier_cards_y = 0
        self.x_change = 20
        self.y_change = 20
        self.value_player = 0
        self.value_coupier = 0
        self.x = 0
        self.y = 0
        self.lst = []
        self.filelist = cards().function()
        self.configure(fg_color='green')
        self.attributes('-fullscreen',True)
        self.create_widgets()

    def delet(self):
        self.second_card = None
        self.second_card_counter = 0
        self.player_cards_x = 0
        self.player_cards_y = 0
        self.coupier_cards_x = 0
        self.coupier_cards_y = 0
        self.x_change = 20
        self.y_change = 20
        self.value_player = 0
        self.value_coupier = 0
        self.lst = []
        self.filelist = cards().function()
        self.configure(fg_color='green')
        self.attributes('-fullscreen',True)
        self.create_widgets()

    def create_widgets(self):
        self.coupier_label = ctk.CTkLabel(self, text=f"Coupier value: {self.value_coupier}", font=('Times New Roman', 20, 'bold'))
        self.coupier_label.pack(side="top", anchor="s", pady=25)
        self.player_label = ctk.CTkLabel(self, text=f"Player value: {self.value_player}", font=('Times New Roman', 20, 'bold'))

        self.frame_coupier_cards = ctk.CTkFrame(self, height=350, width=260, fg_color="green")
        self.frame_coupier_cards.pack()
        self.frame_buttons = ctk.CTkFrame(self, height=50, width=600)
        self.frame_buttons.pack(side="bottom", pady=50)
        self.frame_player_cards = ctk.CTkFrame(self, height=350, width=260, fg_color="green")
        self.player_label.pack(pady=25, anchor="n")
        self.frame_player_cards.pack(anchor="center")

        self.create_cards("Coupier")
        self.create_cards("Player")
        self.create_cards("Coupier")
        self.create_cards("Player")

        self.Hit = ctk.CTkButton(self.frame_buttons, text="Hit", bg_color="green", height=50, width=200, command=lambda:self.create_cards("Player"))
        self.Hit.place(x=0, y=0)
        self.Stand = ctk.CTkButton(self.frame_buttons, text="Stand", bg_color="green", height=50, width=200, command=self.stand)
        self.Stand.place(x=200, y=0)
        self.leave = ctk.CTkButton(self.frame_buttons, text="Hit and run", bg_color="green", height=50, width=200, command=exit)
        self.leave.place(x=400, y=0)

    def create_cards(self, player):
        if len(self.filelist) == 0:
            self.filelist = cards().function()
        card = random.choice(self.filelist)
        self.filelist.remove(card)
        self.value = int(re.search(r'\d+', card).group())
        if player == "Player":
            self.frame = self.frame_player_cards
            self.player_cards_x += self.x_change
            self.player_cards_y += self.y_change
            self.x = self.player_cards_x - self.x_change
            self.y = self.player_cards_y - self.y_change
            self.value_player += self.value
            print(f"player value:{self.value_player}")
        else:
            self.second_card_counter += 1
            self.frame = self.frame_coupier_cards
            if self.second_card_counter == 2:
                card = "cards\CardBack.png"

            else:
                self.value_coupier += self.value
            self.coupier_cards_x += self.x_change
            self.coupier_cards_y += self.y_change
            self.x = self.coupier_cards_x - self.x_change
            self.y = self.coupier_cards_y - self.y_change
            print(f"coupier value:{self.value_coupier}")

        self.card = ImageTk.PhotoImage(Image.open(card).resize((200, 290)))
        self.cards = ctk.CTkLabel(self.frame, image=self.card, bg_color="green", text="")
        if self.second_card_counter == 2 and player == "Coupier":
            self.hidden_card = self.cards
        else:   
            self.lst.append(self.cards)
        self.cards.place(x=self.x, y=self.y)
        self.player_label.configure(text=f"Player value: {self.value_player}")
        self.coupier_label.configure(text=f"Coupier value: {self.value_coupier}")

        if self.value_player > 21:
            winner="coupier"
            self.end(winner)
        elif self.value_coupier > 21:
            winner = "player"
            self.end(winner)

    def stand(self):
        self.coupier_cards_x = self.coupier_cards_x - self.x_change
        self.coupier_cards_y = self.coupier_cards_y- self.y_change
        self.hidden_card.destroy()
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
            x = 350
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
        self.button_end_restart = ctk.CTkButton(self.frame_end, text="Again?", bg_color="green", command=self.close, height=50)
        self.button_end_restart.pack(fill="x")
        self.button_end_end = ctk.CTkButton(self.frame_end, text="End the game", bg_color="green", command=exit, height=50)
        self.button_end_end.pack(fill="x")

    def close(self):
        for i in self.lst:
            i.destroy()
        lst1 = [self.frame_coupier_cards, self.frame_player_cards, self.frame_buttons, self.frame_end, self.player_label, self.coupier_label]
        for i in lst1:
            i.destroy()
        self.delet()



game = BlackjackGame()
game.mainloop()
