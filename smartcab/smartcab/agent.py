import random
import math
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """ An agent that learns to drive in the Smartcab world.
        This is the object you will be modifying. """

    def __init__(self, env, learning=False, epsilon=1.0, alpha=0.5, seed=42, decay_function=0, epsilon_step=0.05, use_input_right=True):
        super(LearningAgent, self).__init__(env)     # Set the agent in the evironment
        self.planner = RoutePlanner(self.env, self)  # Create a route planner
        self.valid_actions = self.env.valid_actions  # The set of valid actions

        # Set parameters of the learning agent
        self.learning = learning # Whether the agent is expected to learn
        self.Q = dict()          # Create a Q-table which will be a dictionary of tuples
        self.epsilon = epsilon   # Random exploration factor
        self.alpha = alpha       # Learning factor

        # Set any additional class parameters as needed
        random.seed(seed)
        self.t = 0
        self.decay_function = decay_function
        self.epsilon_step = epsilon_step
        self.use_input_right = use_input_right



    def reset(self, destination=None, testing=False):
        """ The reset function is called at the beginning of each trial.
            'testing' is set to True if testing trials are being used
            once training trials have completed. """

        # Select the destination as the new location to route to
        self.planner.route_to(destination)

        # Update additional class parameters as needed
        self.t += 1.0

        # Update epsilon using a decay function of your choice
        if self.decay_function == 0:
            # simple decay
            self.epsilon -= self.epsilon_step
        elif self.decay_function == 1:
            # custom decay 1:
            self.epsilon = math.pow(self.alpha, self.t)
        elif self.decay_function == 2:
            # custom decay 2:
            self.epsilon = 1.0 / math.pow(self.t, 2)
        elif self.decay_function == 3:
            # custom decay 3:
            self.epsilon = math.exp( self.alpha * self.t * (-1.0) )
        elif self.decay_function == 4:
            # custom decay 4:
            self.epsilon = math.cos( self.alpha * self.t)
        elif self.decay_function == 5:
            # custom decay 5:
            self.epsilon = math.exp( math.sqrt(self.t) * (-0.05))
        else:
            self.epsilon = 0

        # If 'testing' is True, set epsilon and alpha to 0
        if testing:
            self.epsilon = 0
            self.alpha = 0

        return None

    def build_state(self):
        """ The build_state function is called when the agent requests data from the
            environment. The next waypoint, the intersection inputs, and the deadline
            are all features available to the agent.

            Environment:
            'waypoint', which is the direction the Smartcab should drive leading to the destination, relative to the Smartcab's heading.
            'inputs', which is the sensor data from the Smartcab. It includes
                'light', the color of the light.
                'left', the intended direction of travel for a vehicle to the Smartcab's left. Returns None if no vehicle is present.
                'right', the intended direction of travel for a vehicle to the Smartcab's right. Returns None if no vehicle is present.
                'oncoming', the intended direction of travel for a vehicle across the intersection from the Smartcab. Returns None if no vehicle is present.
            'deadline', which is the number of actions remaining for the Smartcab to reach the destination before running out of time.
        """

        # Collect data about the environment
        waypoint = self.planner.next_waypoint() # The next waypoint
        inputs = self.env.sense(self)           # Visual input - intersection light and traffic
        deadline = self.env.get_deadline(self)  # Remaining deadline

        # NOTE : you are not allowed to engineer features outside of the inputs available.
        # Because the aim of this project is to teach Reinforcement Learning, we have placed
        # constraints in order for you to learn how to adjust epsilon and alpha, and thus learn about the balance between exploration and exploitation.
        # With the hand-engineered features, this learning process gets entirely negated.

        # Set 'state' as a tuple of relevant data for the agent
        state = (inputs['light'], waypoint, inputs['left'], inputs['oncoming'],)

        if self.use_input_right:
            # https://stackoverflow.com/questions/16730339/python-add-item-to-the-tuple
            state = state + (inputs['right'],)
        return state


    def get_maxQ(self, state):
        """ The get_max_Q function is called when the agent is asked to find the
            maximum Q-value of all actions based on the 'state' the smartcab is in. """

        # Calculate the maximum Q-value of all actions for a given state

        # getting max actions (https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary):
        max_actions = list(filter(lambda t: t[1] == max(self.Q[state].values()), self.Q[state].items()))
        maxQ = random.choice(max_actions)[0]
        print('maxQ_action taken: %s from %s' % (maxQ, max_actions))
        return maxQ


    def createQ(self, state):
        """ The createQ function is called when a state is generated by the agent. """

        # When learning, check if the 'state' is not in the Q-table
        # If it is not, create a new dictionary for that state
        #   Then, for each action available, set the initial Q-value to 0.0
        if self.learning and state not in self.Q:
            self.Q[state] = dict().fromkeys(self.valid_actions, 0.0)

        return


    def choose_action(self, state):
        """ The choose_action function is called when the agent is asked to choose
            which action to take, based on the 'state' the smartcab is in. """

        # Set the agent state and default action
        self.state = state
        self.next_waypoint = self.planner.next_waypoint()
        action = None

        # When not learning, choose a random action
        # When learning, choose a random action with 'epsilon' probability
        # Otherwise, choose an action with the highest Q-value for the current state
        # Be sure that when choosing an action with highest Q-value that you randomly select between actions that "tie".
        if not self.learning:
            action = random.choice(self.valid_actions)
        else:
            if random.uniform(0.0, 1.0) <= self.epsilon:
                action = random.choice(self.valid_actions)
            else:
                action = self.get_maxQ(self.state)
        return action


    def learn(self, state, action, reward):
        """ The learn function is called after the agent completes an action and
            receives a reward. This function does not consider future rewards
            when conducting learning. """

        if self.learning:
            # When learning, implement the value iteration update rule
            #   Use only the learning rate 'alpha' (do not use the discount factor 'gamma')
            before = self.Q[state][action]
            self.Q[state][action] = before * ( 1.0 - self.alpha ) + reward * self.alpha
            print ('learn before: %s, and after: %s' % (before, self.Q[state][action]))

        return


    def update(self):
        """ The update function is called when a time step is completed in the
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """

        state = self.build_state()          # Get current state
        self.createQ(state)                 # Create 'state' in Q-table
        action = self.choose_action(state)  # Choose an action
        reward = self.env.act(self, action) # Receive a reward
        self.learn(state, action, reward)   # Q-learn

        return


def run():
    """ Driving function for running the simulation.
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    # #################
    # hyper parameters:
    # #################
    epsilon = 1.0
    epsilon_step = 0.0
    alpha = 0.0075
    tolerance = 0.07
    use_input_right = False
    # decay function: 0 for simple, 1 - 5 for custom implementations
    decay_function = 4

    ##############
    # Create the environment
    # Flags:
    #   verbose     - set to True to display additional output from the simulation
    #   num_dummies - discrete number of dummy agents in the environment, default is 100
    #   grid_size   - discrete number of intersections (columns, rows), default is (8, 6)
    env = Environment()

    ##############
    # Create the driving agent
    # Flags:
    #   learning   - set to True to force the driving agent to use Q-learning
    #    * epsilon - continuous value for the exploration factor, default is 1
    #    * alpha   - continuous value for the learning rate, default is 0.5
    agent = env.create_agent(LearningAgent, learning=True, epsilon=epsilon, alpha=alpha, decay_function=decay_function, epsilon_step=epsilon_step, use_input_right=use_input_right)

    ##############
    # Follow the driving agent
    # Flags:
    #   enforce_deadline - set to True to enforce a deadline metric
    env.set_primary_agent(agent, enforce_deadline=True)

    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    #   log_metrics  - set to True to log trial and simulation results to /logs
    #   optimized    - set to True to change the default log file name
    sim = Simulator(env, update_delay=0.0, log_metrics=True, optimized=True, display=False)

    ##############
    # Run the simulator
    # Flags:
    #   tolerance  - epsilon tolerance before beginning testing, default is 0.05
    #   n_test     - discrete number of testing trials to perform, default is 0
    sim.run(n_test=10, tolerance=tolerance)


if __name__ == '__main__':
    run()
