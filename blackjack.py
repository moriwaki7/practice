from random import shuffle

class Card:
    marks = ['スペード', 'ハート', 'ダイヤ', 'クラブ']
    values = [None, 'Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    points = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    def __init__(self, card):
        """card is taple"""
        self.mark = self.marks[card[0]]
        self.value = self.values[card[1]]
        self.point = self.points[card[1]]

class Deck:
    def __init__(self):
        self.deck = []
        for i in range(4):
            for j in range(1, 14):
                self.deck.append((i, j))
        shuffle(self.deck)

    def draw(self):
        if len(self.deck) == 0:
            return
        return self.deck.pop()

class Player:
    def __init__(self):
        self.point = 0
        self.cards = []
        self.is_burst = False

class Game:
    def __init__(self):
        self.game_deck = Deck()
        self.player = Player()
        self.dealer = Player()
        self.p_cards = self.player.cards
        self.p_point = self.player.point
        self.p_is_burst = self.player.is_burst
        self.d_cards = self.dealer.cards
        self.d_point = self.dealer.point
        self.d_is_burst = self.dealer.is_burst

    def play_game(self):
        print("＋＋＋＋Let's start Black Jack!!＋＋＋＋")
        self.initial_draw()
        while not self.p_is_burst:
            print('あなたの得点は:{}'.format(self.p_point))
            response = input('もう一枚カードを引きますか? y or n:')
            if response == 'Y' or response == 'y':
                self.player_turn()
                if self.p_is_burst:
                    print('あなたはバーストしたので負けです')
                    break
            elif response == 'N' or response == 'n':
                self.dealer_turn()
                if self.d_is_burst:
                    print('ディーラーがバーストしたのであなたの勝ちです')
                    break
                self.check_winner()
                break
            else:
                print('y or n を入力してください')
    def initial_draw(self):
        for i in range(2):
            self.p_card = self.game_deck.draw()
            self.p_cards.append(self.p_card)
            self.card = Card(self.p_card)
            print('あなたの引いたカードは{}の{}'\
                  .format(self.card.mark, self.card.value))
            self.p_point += self.card.point
        for i in range(2):
            self.d_card = self.game_deck.draw()
            self.d_cards.append(self.d_card)
            self.card = Card(self.d_card)
            self.d_point += self.card.point
            if i == 0:
                print('ディーラーの引いたカードは{}の{}'\
                      .format(self.card.mark, self.card.value))
            else:
                print('ディーラーの２枚目はわかりません')

    def player_turn(self):
        self.p_card = self.game_deck.draw()
        self.p_cards.append(self.p_card)
        self.card = Card(self.p_card)
        print('あなたの引いたカードは{}の{}'.format(self.card.mark, self.card.value))
        self.p_point += self.card.point
        if self.p_point > 21:
            self.p_is_burst = True

    def dealer_turn(self):
        second_card = self.d_cards[1]
        self.second_card = Card(second_card)
        print('ディーラーの２枚目のカードは{}の{}' \
              .format(self.second_card.mark, self.second_card.value))
        print('デーラーのポイントは{}'.format(self.d_point))
        while self.d_point < 17:
            self.d_card = self.game_deck.draw()
            self.d_cards.append(self.d_card)
            self.card = Card(self.d_card)
            print('ディーラーの引いたカードは{}の{}'.format(self.card.mark, self.card.value))
            self.d_point += self.card.point
            print('デーラーのポイントは{}'.format(self.d_point))
            if self.d_point > 21:
                self.d_is_burst = True

    def check_winner(self):
        if self.p_point > self.d_point:
            print('おめでとう！！あなたの勝ちです！！！')
        elif self.p_point < self.d_point:
            print('残念！あなたの負けです。')
        else:
            print('引き分けです')

game = Game()
game.play_game()
