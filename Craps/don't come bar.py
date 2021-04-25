import random
import numpy as np
import matplotlib.pyplot as plt
import math


def roll():
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return die2 + die1


come_point = 0
bet = False
plus = 0


# ставка
# рол
# подсчет
# def bet(i):
#     print("bet")


# 0  = деньги возвращаются
# 1  = победа для нас
# -1 = проигрыш для нас
# 2 = перенос ставки
def round():
    global come_point, bet, plus
    point = roll()
    if (point == come_point) and (bet):  # если выпал кампоинт и ставка то луз
        bet = False
        return -1
    if (point == 7) and (bet):  # выигрываем если 7 и ставка
        bet = False
        return 1
    if point in (2, 3, 12, 11, 7):
        return 2
#ставка
    if not bet:
        bet = True
        comeout_roll = roll()
        come_point = comeout_roll
        if comeout_roll in (7, 11):  # автолуз
            bet = False
            return -1
        if comeout_roll in (2, 3):  # автовин
            bet = False
            return 1
        if comeout_roll == 12:  # ушли в ноль
            bet = False
            return 0
        if comeout_roll == point:
            return 2

    while True:
        comeout_roll = roll()
        if comeout_roll == come_point: # победили иль нет по ставке
            bet = False
            return -1
        if comeout_roll == point: # победили иль нет по игре
            return 2
        if comeout_roll == 7:
            bet = False
            return 1


EV_UNIT = 0
average_winnings = []
round_history = []
list_intervals_down = []
list_intervals_up = []
mat_ojidanie = 0
game_outcomes = [0, 0, 0]
experiment = 1000000

win_chance = 0
nothing = 0


def game():
    global nothing
    bet = 1
    win = 0

    capital = 1
    game_number = 0
    game_length = 0
    overall_length = 0
    i = 1
    winnings = 0  # Ожидаемый выигрыш/проигрыш если - то казино в плюсе на эти деньги
    while i < experiment:
        ####
        if capital == 0:
            game_number += 1
            capital = 1
            overall_length += game_length
            game_length = 0
        lets_play = round()
        if lets_play == 2:#перенос ставки
            # round_history.append(0)
            nothing += 1
            continue
        game_length += 1
        if lets_play == 0:# деньги возвращаются
            round_history.append(0)
            i += 1
            average_winnings.append(winnings / (i * bet))
        if lets_play == 1:
            game_outcomes[0] += 1
            round_history.append(1)
            win += 1
            winnings += bet
            capital += bet
            i += 1
            average_winnings.append(winnings / (i * bet))
        if lets_play == -1:
            round_history.append(-1)
            winnings -= bet
            capital -= bet
            i += 1
            average_winnings.append(winnings / (i * bet))

    # Построение дов. вероятности
    disp = np.var(round_history)
    for i in range(0, len(round_history) - 1):
        list_intervals_down.append(average_winnings[i + 1] - (1.65 / math.sqrt(i + 1)) * disp)
        list_intervals_up.append(average_winnings[i + 1] + (1.65 / math.sqrt(i + 1)) * disp)

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

    EV_per_Unit_Squared = EV_per_Unit ** 2
    EV_per_Squared_Unit = (win / experiment) + ((experiment - win) / experiment)
    VAR = EV_per_Squared_Unit - EV_per_Unit_Squared  # Дисперсия - возможно
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
    print("Средняя продолжительность игры " + str(overall_length / game_number))


def build_graphic():
    # -------график доверительной вероятности----
    plt.title("График доверительной вероятности")
    plt.hlines(-0.01, 0, 100000)
    plt.plot(list_intervals_down)
    plt.plot(list_intervals_up)
    plt.ylim(-0.2, 0.2)
    plt.xlim(0, 100000)
    # -------график средних выигрышей--------
    # plt.plot(average_winnings)
    # plt.title("График средних выигрышей")
    # # медиана
    # plt.hlines(np.median(average_winnings), 0, experiment, colors='r', label='Медиана')
    # # график стремится к мат ожиданию
    # a = np.std(average_winnings)
    # plt.hlines(a, 0, experiment, colors='yellow', label='Ско')
    # plt.hlines(-a, 0, experiment, colors='yellow', label='-Ско')
    # plt.ylim(-0.2, 0.2)
    # plt.xlim(0, 10000)

    # -------график распределения выигрышей---------
    # plt.title("График распределения выигрышей")
    # plt.vlines(-1, 0, 0.51)
    # plt.vlines(1, 0, 0.49)

    # plt.hlines(0.5, win_chance, 1)
    # plt.hlines(0.6, 1 - win_chance, 1)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    game()
    build_graphic()
