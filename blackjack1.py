# -*- coding: utf-8 -*-
u"""Black Jack"""

from random import shuffle


class Card:
    u"""カード
    カード情報を定義
    """

    def __init__(self, no):
        u"""カードの初期化

        :param taple no:記号と番号のタブル
        """
        marks = ['スペード', 'ハート', 'ダイヤ', 'クラブ']
        values = [None, 'Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  'Jack', 'Queen', 'King']
        points = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        self.mark = marks[no[0]]
        self.value = values[no[1]]
        self.point = points[no[1]]


class Deck:
    u"""デッキ情報"""

    def __init__(self):
        u"""デッキの作成"""
        self.deck = []
        for i in range(4):
            for j in range(1, 14):
                self.deck.append((i, j))
        shuffle(self.deck)

    def draw(self):
        u"""デッキからカードを引く

        :return: Card
        :rtype: dict
        """
        if len(self.deck) == 0:
            return
        card_no = self.deck.pop()
        card = Card(card_no)
        return card


class Player_base:
    u"""プレイヤー（共通）"""

    def __init__(self, name):
        self.name = name
        self.point_list = []
        self.hand_cards = []
        self.ace_count = 0
        self.is_burst = False
        self.player_point = 0
        self.has_up_point = False

    def draw_card(self, card, display=True):
        u"""プレイヤーがカードを引く

        :param dict card:
        :param bool display:
        """
        if display:
            print('{} の引いたカードは {} の {} です'
                  .format(self.name, card.mark, card.value))
        else:
            print('{}の引いたカードはわかりません'.format(self.name))
        if card.value == 'Ace':
            self.ace_count += 1
        self.hand_cards.append(card)
        self.point_list.append(card.point)
        if card.value == 'Ace':
            self.ace_count += 1
        if sum(self.point_list) > 21:
            self.is_burst = True
        if sum(self.point_list) <= 11 and self.ace_count > 0:
            self.has_up_point = True
        else:
            self.has_up_point = False

    def calc_point(self):
        u"""ポイントの計算

        :return: 現在のポイント
        :rtype: int
        """
        if not self.is_burst:
            if self.has_up_point:
                self.player_point = sum(self.point_list) + 10
            else:
                self.player_point = sum(self.point_list)
        return self.player_point

    def display_nth_card(self, n):
        u"""n番目に引いたカードを表示"""
        card = self.hand_cards[n-1]
        print('{} の {}枚目のカードは {} の {} です'
              .format(self.name, n, card.mark, card.value))

    def display_point(self, display=True):
        u"""プレイ途中のポイントを表示"""
        if display:
            if self.has_up_point:
                print('{}のポイントは {} もしくは {} です'
                      .format(self.name, sum(self.point_list), sum(self.point_list) + 10))
            else:
                print('{}のポイントは {} です'
                      .format(self.name, sum(self.point_list)))
        else:
            print('{}のポイントはわかりません'
                  .format(self.name))


class Player(Player_base):
    u"""プレイヤー"""
    def is_continue(self):
        u"""次のカードを引くか

        :return: プレイヤーが次のカードを引くか
        :rtype: bool
        """
        self.display_point()
        response = input('もう一枚カードを引きますか? y or n:')
        if response == 'Y' or response == 'y':
            return True
        else:
            return False


class dealer(Player_base):
    u"""ディーラー"""
    def is_continue(self):
        u"""次のカードを引くか

        :return: ディーラーが次のカードを引くか
        :rtype: bool
        """
        self.display_point()
        if self.calc_point() < 17:
            return True
        else:
            return False


class Game:
    u"""ゲームの定義"""

    def __init__(self):
        u"""ゲームの初期化"""

        self.deck = Deck()
        self.player = Player('player')
        self.dealer = dealer('dealer')

    def play_game(self):
        u"""ゲームの進行"""

        self.player.draw_card(self.deck.draw())
        self.player.draw_card(self.deck.draw())
        self.dealer.draw_card(self.deck.draw())
        self.dealer.draw_card(self.deck.draw(), display=False)

        while self.player.is_continue():
            self.player.draw_card(self.deck.draw())
            if self.player.is_burst:
                print('あなたはバーストしました')
                print('あなたの負けです')
                break
        if not self.player.is_burst:
            self.dealer.display_nth_card(2)
            while self.dealer.is_continue():
                self.dealer.draw_card(self.deck.draw())
                if self.dealer.is_burst:
                    print('ディーラーがバーストしました')
                    print('あなたの勝ちです')
                    break
        if not self.player.is_burst and not self.dealer.is_burst:
            if self.player.calc_point() > self.dealer.calc_point():
                print('あなたの勝ちです')
            elif self.player.calc_point() < self.dealer.calc_point():
                print('あなたの負けです')
            else:
                print('引き分けです')

game = Game()
game.play_game()
