import random
import numpy as np
import matplotlib.pyplot as plt
import math


def roll():
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return die2 + die1


# ставка
# рол
# подсчет
def bet(i):
    print("bet")


def round():
    point = roll()
    round = True
    # пас лайн
    if point in (7, 11):  # выигрыш
        # проверка ставки
        return -1
    if point in (2, 3):  # проигрыш
        # проверка ставки
        return 0  # паслайн не сыграл
    if point == 12:
        return
    # 5 - point
    # фри одс
    while round:  # пока не выыпадет 5 или 7
        # ставка
        roll_result = roll()
        if roll_result == point:
            # проверка ставки
            return 2
        if roll_result == 7:
            # проверка ставки
            return point  # не сыграл паслайн и фри одс


EV_UNIT = 0
average_winings = []
round_history = []
list_intervals_down = []
list_intervals_up = []
mat_ojidanie = 0

experiment = 1_000_000
win_chance = 0
game_outcomes = [0, 0, 0, 0, 0, 0, 0]


# game_outcomes = {"x2": 0, "x3": 0, "x2.5": 0, "x2.2": 0, "lose_all": 0, "lose_pass": 0}


def game():
    bet = 1
    win = 0

    capital = 1
    game_number = 0
    game_length = 0
    overall_length = 0

    winnings = 0  # Ожидаемый выигрыш/проигрыш если - то казино в плюсе на эти деньги
    for i in range(experiment):

        ####
        game_length += 1
        if capital <= 0:
            game_number += 1
            capital = 1
            overall_length += game_length
            game_length = 0
        lets_play = round()

        if lets_play == -1:  # пас лайн прошел сразу - мы проиграли
            game_outcomes[0] += 1
            round_history.append(-bet)
            winnings -= bet
            capital -= bet

        if lets_play == 2:  # выпал поинт а не 7
            game_outcomes[1] += 1
            round_history.append(-bet * 2)
            winnings -= bet * 2
            capital -= bet * 2

        if lets_play == 0:  # пас лайн не прошел сразу - мы выиграли
            game_outcomes[2] += 1
            round_history.append(bet)
            win += 1
            winnings += bet
            capital += bet

        if lets_play in (4, 10):  # сделали 4 10
            game_outcomes[3] += 1
            round_history.append(bet * 0.5 + bet)
            win += 1
            winnings += bet * 0.5 + bet  # выплатили 1/2  + за dont pass
            capital += bet * 0.5 + bet

        if lets_play in (5, 9):  # сделали 5 9
            game_outcomes[4] += 1
            round_history.append(bet * 0.66 + bet)
            win += 1
            winnings += bet * 0.66 + bet  # выплатили 2/3  + за dont pass
            capital += bet * 0.66 + bet

        if lets_play in (6, 8):  # сделали 6 8
            game_outcomes[5] += 1
            round_history.append(bet * 0.83 + bet)
            win += 1
            winnings += bet * 0.83 + bet  # выплатили 5/6 + за dont pass
            capital += bet * 0.83 + bet

        if lets_play is None:
            round_history.append(0)
            game_outcomes[6] += 1
        average_winings.append(winnings / (experiment * bet))

    # Построение дов. вероятности
    disp = np.var(round_history)
    for i in range(0, len(round_history) - 1):
        list_intervals_down.append(average_winings[i + 1] - (1.65 / math.sqrt(i + 1)) * disp)
        list_intervals_up.append(average_winings[i + 1] + (1.65 / math.sqrt(i + 1)) * disp)

    # Вывод результатов
    win_chance = win / experiment
    print("Chance to win " + str(win_chance))
    print("Expected Value " + str(winnings))  # Ожидаемый выигрыш/проигрыш если - то казино в плюсе на эти деньги

    EV_per_Unit = winnings / (experiment * bet)

    print("EV per Unit " + str(EV_per_Unit))  # Ожидаемый выигрыш/проигрыш на одну ставку
    House_Edge = EV_per_Unit * 100
    print("House Edge " + str(House_Edge))  # Преимущество /доход заведения (house advantage/house edge, H.A.)

    RTP = 1 + winnings / (experiment * bet)
    print("Return to Player " + str(RTP))  # Процент возврата (Return To Player, RTP)

    VAR = np.var(round_history)  # Дисперсия - возможно
    print("Возможно дисперсия " + str(VAR))

    print("Дисперсия 2 " + str(np.var(round_history)))

    Standart_Deviation = VAR ** 0.5
    print("Среднекватратичное отклонение " + str(Standart_Deviation))

    EV_Units = EV_per_Unit * experiment

    SD_Units = Standart_Deviation * (experiment ** 0.5)
    print("Средний суммарный выигрыш " + str(EV_Units) + "\n"
          + "Его СКО " + str(SD_Units))

    z = 1.65
    VI = z * Standart_Deviation

    confidence_interval_low = RTP - VI / math.sqrt(experiment)
    confidence_interval_up = RTP + VI / math.sqrt(experiment)

    print("дов интервал" + str(confidence_interval_low))
    print("дов интервал врх" + str(confidence_interval_up))
    print("Индекс волатильности игры " + str(VI))
    # print("Средняя продолжительность игры " + str(overall_length / game_number))


def build_graphic():
    # -------график доверительной вероятности----
    plt.title("График доверительной вероятности")
    plt.hlines(mat_ojidanie, 0, 10000)
    plt.plot(list_intervals_down)
    plt.plot(list_intervals_up)

    # -------график средних выигрышей--------
    # plt.plot(average_winings)
    # # медиана
    # plt.title("График средних выигрышей")
    # plt.hlines(np.median(average_winings), 0, experiment, colors='r', label='Медиана')
    # # график стремится к мат ожиданию
    # a = np.std(average_winings)
    # plt.hlines(a, 0, experiment, colors='b', label='Ско')
    # plt.hlines(-a, 0, experiment, colors='b', label='-Ско')
    #
    # # -------график распределения выигрышей---------
    # plt.title("График распределения выигрышей")
    # probabilities = (list(map(lambda x: x / experiment, game_outcomes)))
    # x_values = ["lose_pass", "lose_point", "win_dont_pass", "win4_10", "win5_9", "win6_8", "12"]
    # print(probabilities)
    # plt.xticks(rotation=-15)
    # plt.plot(x_values, probabilities)
    # plt.legend()
    plt.show()


if __name__ == '__main__':
    game()
    build_graphic()
