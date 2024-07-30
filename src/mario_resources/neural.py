import constants

from torch import nn
import copy

"""
Class for Crew Chief online and target neural nets
"""
class CCNet(nn.Module):

    def __init__(self, input_dim, output_dim):
        super().__init__()

        if input_dim != constants.SMALL_LAYER_SIZE:
            raise ValueError(f"Expecting input of dimension 64, got: {input_dim}")

        # Define the online NN, using the proper inputs and the ReLU function
        self.online = nn.Sequential(
            nn.Linear(input_dim, constants.BIG_LAYER_SIZE),
            nn.ReLU(),
            nn.Linear(constants.BIG_LAYER_SIZE, SMALL_LAYER_SIZE),
            nn.ReLU(),
            nn.Linear(SMALL_LAYER_SIZE, output_dim)
        )

        # Create the target network as a copy of the online network
        self.target = copy.deepcopy(self.online)

        for param in self.target.parameters():
            param.requires_grad = False

    # Separate forward for online and target networks
    def forward(self, input, model):
        if model == 'online':
            return self.online(input)
        elif model == 'target':
            return self.target(input)
