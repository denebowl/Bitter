import torch


class Model:
    layer_count = 10  # 여러 개의 데이터로 학습하자

    def __init__(self, input_size):
        l1 = input_size
        l2 = 50
        l3 = len(ai_base.action_set)

        self.model = torch.nn.Sequential(
            torch.nn.Linear(l1, l2),
            torch.nn.ReLU(),
            torch.nn.Linear(l2, l3),
            # torch.nn.ReLU(),
            # torch.nn.Linear(l3, l4),
            # torch.nn.ReLU(),
            # torch.nn.Linear(l4, l5),
            # torch.nn.ReLU(),
            # torch.nn.Linear(l5, l6),
        )
        self.loss_fn = torch.nn.MSELoss()
        self.learning_rate = 1e-3
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate)

        self.gamma = 0.9
        self.epsilon = 1.0
