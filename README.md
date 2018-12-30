# gym-micropolis
An interface with micropolis for city-building agents, packaged as an OpenAI gym environment.

We can render a training agent in real time and interact with its gui. An experimental hack makes builds taken by the player during training appear to the agent as samples from its own action probability distribution, so that it backpropogates over its own weights as a result of our actions, allowing us to expose the agent to handpicked behaviours so that it might learn from them, or, as is more often the case, so that they may violently disrupt the course of its training. It would be nice to establish a baseline of performance without intervention, and compare to performance of agents trained alongside various strategies of human intervention.

![breathy](https://github.com/smearle/gym-micropolis/blob/master/gifs/breathy.gif)

# Installation

Clone this repository, then 
```
cd micropolis/MicropolisCore/src
make
sudo make install
```

# Basic Use

From this directory, run:
```
from gym_micropolis.envs.corecontrol import MicropolisControl
m = MicropolisControl(MAP_W=50, MAP_H=50)
m.layGrid(4, 4)
```
# Training w/ RL

To use micropolis as a gym environment, install [gym](https://github.com/openai/gym).

To train an agent using ACKTR:

```
python3 main.py --log-dir trained_models/acktr --save-dir trained_models/acktr --algo acktr --num-process 24 --map-width 20
```

To run inference using the agent we have just trained:

```
python3 enjoy.py --load-dir trained_models/acktr --map-width 20
```

The neural architecture consists of a 3x3 convolution applied repeatedly to a fixed-size feature map - enacting a kind of neural game-of-life on the feature map.

Reward corresponds to change in overall population, plus a bonus for each nonzero zone-specific population (or, alternatively, for even distribution of population between zones) - lest the bot exploit the game, since it is able to generate large residential populations without providing any employment.

Generally, agents quickly discover the power-plant + residential zone pairing that creates initial populations, then spend very long at a local minima consisting of a gameboard tiled by residential zones, surrounding a single power plant. On more successful runs, the agent will make the leap toward a smattering of lone road tiles place next to zones, at least one per zone to maximize population density. 

I'm interested in emergent transport networks, though it does not see that the simulation is complex enough for population-optimizing builds to require large-scale transport networks. 

We can, however, reward traffic density just enough for continuous/traffic-producing roads to be drawn between zones, but not so much that they billow out into swaths of traffic-exploiting asphalt badlands.

# Interacting w/ the Bot

During training and inference, a micropolis gui will be rendered by default. During training, it is the environment of rank 0 if multiple games are being run in parallel. The gui is controlled by the learning algorithm, and thus can be laggy, but is fully interactive, so that a player may build or delete zones during training and inference.

Any action that is successfully performed by the player on the subsection of the larger game-map which corresponds to the bot's play-area, is registered by the bot as an action of its own, sampled from its own action distribution, so that the player can influence the agent's training data in real time.

