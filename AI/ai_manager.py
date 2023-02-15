from asyncio import Queue
from threading import Thread
from time import sleep
from typing import List

from AI.ai_dto import CandleDto
from AI import ai_state
from DTO import upbitReceiver


class AIManager:
    def __init__(self):
        # self.input_size = Model.layer_count * State.state_count
        # self.model = Model(self.input_size)
        self.losses = []
        # self.queueHomework = Queue()

        self.thread = Thread(target=self.TaskAI)
        self.thread.daemon = True

    def start(self):
        self.thread.start()

    '''def stop(self):
        self.stop_thread = True

    def pause(self):
        self.pause_thread = True

    def resume(self):
        self.pause_thread = False'''

    def TaskAI(self):
        candleList = []

        while True:
            result = upbitReceiver.downloadCandleDate(60, 'KRW-BTC', 100)
            for tmp in result:
                candle = CandleDto(**tmp)
                candleList.append(candle)
            self.learn(candleList)
            sleep(1)

    def learn(self, candles: List[CandleDto]):
        if len(candles) < 100:  # 캔들 갯수 부족
            return

        ai_state.getBeforeState(candles)

        '''# start learning
        state_current_raw = render_np(crypto.tradeData).reshape(1, self.input_size) \
                            + np.random.rand(1, self.input_size) / 10.0
        state_current = torch.from_numpy(state_current_raw).float()'''

    '''def learn(self, crypto: Crypto):
        if len(crypto.tradeData) < 10:  # d
            return

        self.parent_agent.rebirth()

        training_index = 0
        not_random_count = 0
        while training_index < len(crypto.tradeData) - 1:
            # get q value
            qValue = self.model.model(state_current)
            qValue_np = qValue.data.numpy()

            # get Action
            if random() < self.model.epsilon:
                action = np.random.randint(0, len(action_set))
            else:
                action = np.argmax(qValue_np)
                not_random_count += 1
            self.doAction(crypto, action)

            state_next_raw = render_np(self.parent_agent, ).reshape(1, self.input_size) + np.random.rand(1,
                                                                                                         self.input_size) / 10.0
            state_next = torch.from_numpy(state_next_raw).float()
            reward = getReward()

    def needRebirth(self):
        return self.parent_agent.walletCash <= 10000

    def learn(self, tradeDTOList: List[Trade]):
        if len(tradeDTOList) < 11:  # 11개를 받아서 10개로 학습하고 1개로 검증하자
            return

        dataToLearn = tradeDTOList[0:10]
        dataToTest = tradeDTOList[10]

        # 목표 지점 생성
        epochs = 5000
        losses = []
        for i in range(epochs):
            # restart same game
            self.parent_agent.rebirth()

            # get current state
            state_current_raw = render_np(dataToLearn).reshape(1, self.input_size) \
                                + np.random.rand(1, self.input_size) / 10.0
            state_current = torch.from_numpy(state_current_raw).float()

            # set etc values
            learning_end = False
            not_random_count = 0
            while learning_end is False:
                # get q value
                qValue = self.model.model(state_current)
                qValue_np = qValue.data.numpy()
                if random() < self.model.epsilon:
                    action_ = np.random.randint(0, len(action_set))
                else:
                    action_ = np.argmax(qValue_np)
                    not_random_count += 1

                action = action_set[action_]
                self.doAction(action)

                state_next_raw = render_np().reshape(1, self.input_size) + np.random.rand(1, self.input_size) / 10.0
                state_next = torch.from_numpy(state_next_raw).float()
                reward = getReward()
                with torch.no_grad():
                    newQ = self.model.model(state_next.reshape(1, self.input_size))
                maxQ = torch.max(newQ)
                if reward == -1:
                    y = reward + (self.model.gamma * maxQ)
                else:
                    y = reward

                y = torch.Tensor([y]).detach().squeeze()
                x = qValue.squeeze()[action_]
                loss = self.model.loss_fn(x, y)
                self.model.optimizer.zero_grad()
                loss.backward()
                losses.append(loss.item())
                self.model.optimizer.step()
                state_current = state_next

                if reward != -1:
                    learning_end = True

                move_count += 1
                if self.stop_thread:
                    return

            if self.model.epsilon > 0.1:
                self.model.epsilon -= (1 / epochs)

            # 학습상황 출력
            result_text = "Epoch: %7d, Moves: %7d, Epsilon: %6.2f, Command: %6.2f, Loss: %9.2f" \
                          % (i, move_count, round(self.model.epsilon, 2),
                             round(not_random_count / move_count * 100, 2), round(losses[-1], 2))
            print(result_text)
        # print('losses: ' + str(losses))

    def doAction(self, crypto: Crypto, action: int):
        # 0: 'nothing',
        # 1: 'sell_100', 2: 'sell_75', 3: 'sell_50', 4: 'sell_30', 5: 'sell_10',
        # 6: 'buy_100', 7: 'sell_75', 8: 'buy_50', 9: 'buy_30', 10: 'buy_10',
        if action == 0:
            return
        elif action == 1:
            self.parent_agent.sell(crypto, 100)
        elif action == 2:
            self.parent_agent.sell(crypto, 75)
        elif action == 3:
            self.parent_agent.sell(crypto, 50)
        elif action == 4:
            self.parent_agent.sell(crypto, 30)
        elif action == 5:
            self.parent_agent.sell(crypto, 10)
        elif action == 1:
            self.parent_agent.buy(crypto, 100)
        elif action == 2:
            self.parent_agent.buy(crypto, 75)
        elif action == 3:
            self.parent_agent.buy(crypto, 50)
        elif action == 4:
            self.parent_agent.buy(crypto, 30)
        elif action == 5:
            self.parent_agent.buy(crypto, 10)


def render_np(agent, tradeDTOList: List[Trade]):
    tmp = []

    for index, val in enumerate(tradeDTOList):
        state = State(agent, val)
        tmp.append(state.toList())

    # result = np.zeros((layer_count, state_count), dtype=np.uint8)
    arr = np.array(tmp)
    return arr


def getReward(self, state):
    if self.parent_agent.piece == self.parent_agent.target_piece:
        return 100
    # elif (self.parent_board.components['Player'].pos == self.parent_board.components['Goal'].pos):
    # return -10
    else:
        return -1'''
