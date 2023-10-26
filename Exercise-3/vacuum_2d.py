# ======= #
# IMPORTS #
# ======= #
import numpy as np
import random

# For final animation
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.path import Path
from matplotlib.animation import ArtistAnimation


# ============ #
# ROOMS METHOD #
# ============ #
def rooms(x: int, y: int):
    """
    ## `rooms` method

    ==================================

    #### Description

    Takes as input the two dimensions of the room and creates one accordingly with random status for every cell, chosen between "Clean", "Dirty" and "Obstacle". Every cell touching other two squares that are either Clean or Dirty at directions North, West, South, or East.

    ==================================

    #### Parameters

    #### - `x`: `int`

    Room's dimension on the `x` axis.

    #### - `y`: `int`

    Room's dimension on the `y` axis.

    #### - `strings`: `list[str]`

    The list of strings that will be used to randomly assign a value to every cell of the room.
    """
    strings = ["Clean", "Clean", "Clean", "Dirty", "Dirty", "Obstacle"]
    # Create matrix of fixed size with random values chosen between the three above:
    matrix = np.random.choice(strings, size=(x, y))

    # Creating two charging stations:
    # Charge 1:
    a = random.randint(0, x - 1)
    b = random.randint(0, y - 1)
    # Charge 2:
    c = random.randint(0, x - 1)
    d = random.randint(0, y - 1)

    # Loop through the matrix and replace "Clean" or "Dirty" elements that do not have two adjacent squares of the same type with a random value chosen between "Clean" and "Dirty";
    # this is made to avoid most of infinite loops where the agent gets stuck in between obstacles:
    for i in range(x):
        for j in range(y):
            if matrix[i][j] == "Clean":
                adjacent_one = False
                adjacent_two = False
                if i > 0 and matrix[i - 1][j] == "Clean":
                    if adjacent_one == False:
                        adjacent_one = True
                    elif adjacent_two == False:
                        adjacent_two = True
                elif i < x - 1 and matrix[i + 1][j] == "Clean":
                    if adjacent_one == False:
                        adjacent_one = True
                    elif adjacent_two == False:
                        adjacent_two = True
                elif j > 0 and matrix[i][j - 1] == "Clean":
                    if adjacent_one == False:
                        adjacent_one = True
                    elif adjacent_two == False:
                        adjacent_two = True
                elif j < y - 1 and matrix[i][j + 1] == "Clean":
                    if adjacent_one == False:
                        adjacent_one = True
                    elif adjacent_two == False:
                        adjacent_two = True
                if i > 0 and matrix[i - 1][j] == "Dirty":
                    if adjacent_one == False:
                        adjacent_one = True
                    elif adjacent_two == False:
                        adjacent_two = True
                elif i < x - 1 and matrix[i + 1][j] == "Dirty":
                    if adjacent_one == False:
                        adjacent_one = True
                    elif adjacent_two == False:
                        adjacent_two = True
                elif j > 0 and matrix[i][j - 1] == "Dirty":
                    if adjacent_one == False:
                        adjacent_one = True
                    elif adjacent_two == False:
                        adjacent_two = True
                elif j < y - 1 and matrix[i][j + 1] == "Dirty":
                    if adjacent_one == False:
                        adjacent_one = True
                    elif adjacent_two == False:
                        adjacent_two = True
                if not adjacent_one or not adjacent_two:
                    matrix[i][j] = np.random.choice(["Clean", "Dirty"])
            elif matrix[i][j] == "Dirty":
                adjacent_one = False
                adjacent_two = False
                if i > 0 and matrix[i - 1][j] == "Clean":
                    if adjacent_one == False:
                        adjacent_one = True
                    elif adjacent_two == False:
                        adjacent_two = True
                elif i < x - 1 and matrix[i + 1][j] == "Clean":
                    if adjacent_one == False:
                        adjacent_one = True
                    elif adjacent_two == False:
                        adjacent_two = True
                elif j > 0 and matrix[i][j - 1] == "Clean":
                    if adjacent_one == False:
                        adjacent_one = True
                    elif adjacent_two == False:
                        adjacent_two = True
                elif j < y - 1 and matrix[i][j + 1] == "Clean":
                    if adjacent_one == False:
                        adjacent_one = True
                    elif adjacent_two == False:
                        adjacent_two = True
                if i > 0 and matrix[i - 1][j] == "Dirty":
                    if adjacent_one == False:
                        adjacent_one = True
                    elif adjacent_two == False:
                        adjacent_two = True
                elif i < x - 1 and matrix[i + 1][j] == "Dirty":
                    if adjacent_one == False:
                        adjacent_one = True
                    elif adjacent_two == False:
                        adjacent_two = True
                elif j > 0 and matrix[i][j - 1] == "Dirty":
                    if adjacent_one == False:
                        adjacent_one = True
                    elif adjacent_two == False:
                        adjacent_two = True
                elif j < y - 1 and matrix[i][j + 1] == "Dirty":
                    if adjacent_one == False:
                        adjacent_one = True
                    elif adjacent_two == False:
                        adjacent_two = True
                if not adjacent_one or not adjacent_two:
                    matrix[i][j] = np.random.choice(["Clean", "Dirty"])

    # In the end, place the charging station:
    matrix[a][b] = "Charger"
    matrix[c][d] = "Charger"
    return matrix


# ================================ #
# BIDIMENSIONAL VACUUM AGENT CLASS #
# ================================ #
class BidimensionalVacuumAgent:
    """
    ## `BidimensionalVacuumAgent` class

    ===================================================

    #### Description

    This custom agent class creates a vacuum agent that tries to create an efficient movement
    pattern to clean the whole room, avoiding obstacles. After 100 moves, the internal battery
    of the vacuum runs out and the agent stops where it is.
    """

    # =========== #
    # INIT METHOD #
    # =========== #
    def __init__(self, env: np.ndarray):
        """
        ## `__init__` method

        ===================================================

        Initialization of some variables that the agent needs to know.
        """
        self.performance = 0
        self.x = env.shape[0]
        self.y = env.shape[1]
        self.env = env
        self.previous_action = ""

    # ================== #
    # VACUUM DROP METHOD #
    # ================== #
    def vacuum_drop(self):
        """
        ## `vacuum_drop` class

        ===================================================

        #### Description

        This function chooses a valid position at random where the agent can spawn and places the
        vacuum there.
        """
        # Create a 2D array with the specified dimensions and strings:
        print(f"The room is: \n {self.env}")

        valid_positions = []

        # Create a list of valid positions that are not obstacles:
        for i in range(self.x):
            for j in range(self.y):
                if self.env[i, j] != "Obstacle" and self.env[i, j] != "Charger":
                    valid_positions.append((i, j))

        # You'll get here only if you're really unlucky (or lucky?)
        if not valid_positions:
            print(
                f"""No valid starting positions (without obstacles) available. You hit the one in {(1 / (1/3)^(self.x * self.y))} chance to get a {self.x} by {self.y} self.env composed
                at random choosing among three values composed of only one of these three elements, I'd go play some scratch cards if I were you.
                """
            )
            return []

        # Choose a random starting position for the agent from valid positions:
        self.agent_pos = random.choice(valid_positions)

    # =============== #
    # MOVEMENT METHOD #
    # =============== #
    def movement(self, battery=100):
        """
        ## `movement` method

        ===================================================

        #### Description

        This class dictates the movement pattern of the vacuum. It checks for nearby dirty cells
        and goes there to clean them, avoids obstacles and avoids loops by limiting the battery
        duration of the agent.

        """
        # Initializing battery duration (default 100 moves):
        self.battery = battery

        # Creating lists useful for the final animation:
        room_history = [self.env.copy()]
        agent_history = [self.agent_pos]

        # Checking the battery status:
        default_battery = battery

        # Loop until all cells are either Clean or Obstacle:
        while True:
            # Get the value of the current cell:
            current_cell = self.env[self.agent_pos]
            print(
                f"Vacuum is in position {self.agent_pos}; the status of the cell is {current_cell}. "
            )

            # If the cell is Dirty, clean it:
            if current_cell == "Dirty":
                self.env[self.agent_pos] = "Clean"

                # Register position for final animation:
                room_history.append(self.env.copy())
                agent_history.append(self.agent_pos)

                print(f"Cleaned cell {self.agent_pos}")

                # Register performance value:
                self.performance += 25

            # If the cell is Clean, check adjacent cells for Dirty cells:
            elif current_cell == "Clean":
                possible_moves = []
                dirty_adjacent = False

                # Checking if there are dirty cells nearby:
                if (
                    self.agent_pos[0] > 0
                    and self.env[self.agent_pos[0] - 1, self.agent_pos[1]] == "Dirty"
                ):
                    dirty_adjacent = True
                    print(
                        f"There's a Dirty square near here! It's located in {[self.agent_pos[0] - 1, self.agent_pos[1]]}! "
                    )
                    possible_moves.append([self.agent_pos[0] - 1, self.agent_pos[1]])
                if (
                    self.agent_pos[0] < self.x - 1
                    and self.env[self.agent_pos[0] + 1, self.agent_pos[1]] == "Dirty"
                ):
                    dirty_adjacent = True
                    print(
                        f"There's a Dirty square near here! It's located in {[self.agent_pos[0] + 1, self.agent_pos[1]]}! "
                    )
                    possible_moves.append([self.agent_pos[0] + 1, self.agent_pos[1]])

                if (
                    self.agent_pos[1] > 0
                    and self.env[self.agent_pos[0], self.agent_pos[1] - 1] == "Dirty"
                ):
                    dirty_adjacent = True
                    print(
                        f"There's a Dirty square near here! It's located in {[self.agent_pos[0], self.agent_pos[1] - 1]}! "
                    )
                    possible_moves.append([self.agent_pos[0], self.agent_pos[1] - 1])
                if (
                    self.agent_pos[1] < self.y - 1
                    and self.env[self.agent_pos[0], self.agent_pos[1] + 1] == "Dirty"
                ):
                    dirty_adjacent = True
                    print(
                        f"There's a Dirty square near here! It's located in {[self.agent_pos[0], self.agent_pos[1] + 1]}! "
                    )
                    possible_moves.append([self.agent_pos[0], self.agent_pos[1] + 1])

                # If there is a Dirty cell adjacent, move to it. If there's more than one, choose one at random:
                if dirty_adjacent:
                    dirty_pos = tuple(
                        possible_moves[random.randint(0, len(possible_moves) - 1)]
                    )
                    self.agent_pos = dirty_pos
                    self.env[self.agent_pos] = "Clean"

                    # Register current status of the environment for final animation:
                    room_history.append(self.env.copy())
                    agent_history.append(self.agent_pos)
                    self.battery -= 1
                    print(f"Moved to cell {self.agent_pos}")

                    # Register performance:
                    self.performance -= 0.5

                else:
                    # Find a random cell that is not an Obstacle and move to it:
                    possible_moves = []
                    if (
                        self.agent_pos[0] > 0
                        and self.env[self.agent_pos[0] - 1, self.agent_pos[1]]
                        != "Obstacle"
                    ):
                        possible_moves.append("North")
                    if (
                        self.agent_pos[0] < self.x - 1
                        and self.env[self.agent_pos[0] + 1, self.agent_pos[1]]
                        != "Obstacle"
                    ):
                        possible_moves.append("South")
                    if (
                        self.agent_pos[1] > 0
                        and self.env[self.agent_pos[0], self.agent_pos[1] - 1]
                        != "Obstacle"
                    ):
                        possible_moves.append("West")
                    if (
                        self.agent_pos[1] < self.y - 1
                        and self.env[self.agent_pos[0], self.agent_pos[1] + 1]
                        != "Obstacle"
                    ):
                        possible_moves.append("East")

                    if len(possible_moves) > 0:
                        action = possible_moves[
                            random.randint(0, len(possible_moves) - 1)
                        ]

                        if action == "North":
                            if self.previous_action == "South":
                                while True:
                                    action = possible_moves[
                                        random.randint(0, len(possible_moves) - 1)
                                    ]
                                    if action != self.previous_action:
                                        break
                            else:
                                self.agent_pos = (
                                    self.agent_pos[0] - 1,
                                    self.agent_pos[1],
                                )
                        elif action == "South":
                            if self.previous_action == "North":
                                while True:
                                    action = possible_moves[
                                        random.randint(0, len(possible_moves) - 1)
                                    ]
                                    if action != self.previous_action:
                                        break
                            else:
                                self.agent_pos = (
                                    self.agent_pos[0] + 1,
                                    self.agent_pos[1],
                                )
                        elif action == "West":
                            if self.previous_action == "East":
                                while True:
                                    action = possible_moves[
                                        random.randint(0, len(possible_moves) - 1)
                                    ]
                                    if action != self.previous_action:
                                        break
                            else:
                                self.agent_pos = (
                                    self.agent_pos[0],
                                    self.agent_pos[1] - 1,
                                )
                        elif action == "East":
                            if self.previous_action == "West":
                                while True:
                                    action = possible_moves[
                                        random.randint(0, len(possible_moves) - 1)
                                    ]
                                    if action != self.previous_action:
                                        break
                            else:
                                self.agent_pos = (
                                    self.agent_pos[0],
                                    self.agent_pos[1] + 1,
                                )
                        print(f"Executing action {action}...")
                        print(f"Moved to cell {self.agent_pos}")
                        self.previous_action = action
                        self.battery -= 1

                        # Registering performance:
                        self.performance -= 0.5

            # If the vacuum reaches a Charging station, the battery gets recharged:
            elif current_cell == "Charger":
                if self.battery < default_battery / 2:
                    self.battery = default_battery
                    print("The battery has been recharged. ")
                    # The recharging station gets used:
                    current_cell = "Clean"
                else:
                    print(
                        f"The vacuum passed on a Charging station, but does not need to recharge: its battery still has {self.battery} charges of {default_battery}. "
                    )
                possible_moves = []
                dirty_adjacent = False
                # Checking if there are dirty cells nearby:
                if (
                    self.agent_pos[0] > 0
                    and self.env[self.agent_pos[0] - 1, self.agent_pos[1]] == "Dirty"
                ):
                    dirty_adjacent = True
                    print(
                        f"There's a Dirty square near here! It's located in {[self.agent_pos[0] - 1, self.agent_pos[1]]}! "
                    )
                    possible_moves.append([self.agent_pos[0] - 1, self.agent_pos[1]])
                if (
                    self.agent_pos[0] < self.x - 1
                    and self.env[self.agent_pos[0] + 1, self.agent_pos[1]] == "Dirty"
                ):
                    dirty_adjacent = True
                    print(
                        f"There's a Dirty square near here! It's located in {[self.agent_pos[0] + 1, self.agent_pos[1]]}! "
                    )
                    possible_moves.append([self.agent_pos[0] + 1, self.agent_pos[1]])

                if (
                    self.agent_pos[1] > 0
                    and self.env[self.agent_pos[0], self.agent_pos[1] - 1] == "Dirty"
                ):
                    dirty_adjacent = True
                    print(
                        f"There's a Dirty square near here! It's located in {[self.agent_pos[0], self.agent_pos[1] - 1]}! "
                    )
                    possible_moves.append([self.agent_pos[0], self.agent_pos[1] - 1])
                if (
                    self.agent_pos[1] < self.y - 1
                    and self.env[self.agent_pos[0], self.agent_pos[1] + 1] == "Dirty"
                ):
                    dirty_adjacent = True
                    print(
                        f"There's a Dirty square near here! It's located in {[self.agent_pos[0], self.agent_pos[1] + 1]}! "
                    )
                    possible_moves.append([self.agent_pos[0], self.agent_pos[1] + 1])

                # If there is a Dirty cell adjacent, move to it. If there's more than one, choose one at random:
                if dirty_adjacent:
                    dirty_pos = tuple(
                        possible_moves[random.randint(0, len(possible_moves) - 1)]
                    )
                    self.env[self.agent_pos] = "Clean"
                    self.agent_pos = dirty_pos

                    # Register current status of the environment for final animation:
                    room_history.append(self.env.copy())
                    agent_history.append(self.agent_pos)
                    self.battery -= 1
                    print(f"Moved to cell {self.agent_pos}")

                    # Register performance:
                    self.performance -= 0.5

                else:
                    # Find a random cell that is not an Obstacle and move to it:
                    possible_moves = []
                    if (
                        self.agent_pos[0] > 0
                        and self.env[self.agent_pos[0] - 1, self.agent_pos[1]]
                        != "Obstacle"
                    ):
                        possible_moves.append("North")
                    if (
                        self.agent_pos[0] < self.x - 1
                        and self.env[self.agent_pos[0] + 1, self.agent_pos[1]]
                        != "Obstacle"
                    ):
                        possible_moves.append("South")
                    if (
                        self.agent_pos[1] > 0
                        and self.env[self.agent_pos[0], self.agent_pos[1] - 1]
                        != "Obstacle"
                    ):
                        possible_moves.append("West")
                    if (
                        self.agent_pos[1] < self.y - 1
                        and self.env[self.agent_pos[0], self.agent_pos[1] + 1]
                        != "Obstacle"
                    ):
                        possible_moves.append("East")

                    if len(possible_moves) > 0:
                        action = possible_moves[
                            random.randint(0, len(possible_moves) - 1)
                        ]

                        if action == "North":
                            if self.previous_action == "South":
                                while True:
                                    action = possible_moves[
                                        random.randint(0, len(possible_moves) - 1)
                                    ]
                                    if action != self.previous_action:
                                        break
                            else:
                                self.agent_pos = (
                                    self.agent_pos[0] - 1,
                                    self.agent_pos[1],
                                )
                        elif action == "South":
                            if self.previous_action == "North":
                                while True:
                                    action = possible_moves[
                                        random.randint(0, len(possible_moves) - 1)
                                    ]
                                    if action != self.previous_action:
                                        break
                            else:
                                self.agent_pos = (
                                    self.agent_pos[0] + 1,
                                    self.agent_pos[1],
                                )
                        elif action == "West":
                            if self.previous_action == "East":
                                while True:
                                    action = possible_moves[
                                        random.randint(0, len(possible_moves) - 1)
                                    ]
                                    if action != self.previous_action:
                                        break
                            else:
                                self.agent_pos = (
                                    self.agent_pos[0],
                                    self.agent_pos[1] - 1,
                                )
                        elif action == "East":
                            if self.previous_action == "West":
                                while True:
                                    action = possible_moves[
                                        random.randint(0, len(possible_moves) - 1)
                                    ]
                                    if action != self.previous_action:
                                        break
                            else:
                                self.agent_pos = (
                                    self.agent_pos[0],
                                    self.agent_pos[1] + 1,
                                )
                        print(f"Executing action {action}...")
                        print(f"Moved to cell {self.agent_pos}")
                        self.previous_action = action
                        self.battery -= 1

                        # Registering performance:
                        self.performance -= 0.5

            # Registering positions:
            room_history.append(self.env.copy())
            agent_history.append(self.agent_pos)

            # Checking battery duration. If it ran out, the agent stops:
            if self.battery < 0:
                print("Vacuum's battery ran out. ")
                break

            # If all cells are Clean or Obstacle, break out of the loop; the agent completed its job:
            if np.all(np.isin(self.env, ["Clean", "Obstacle", "Charger"])):
                print("All cells are Clean, Charging stations or Obstacles. ")
                break

        return room_history, agent_history


# ========================== #
# VISUALIZE ANIMATION METHOD #
# ========================== #
def visualize_animation(room_history, agent_history):
    """
    ## `visualize_animation` method

    ===================================================

    #### Description

    The method creates a very basic grid of the room dimension
    and color-patterns the cells. It also keeps track of the agent
    movement.

    ===================================================

    #### Parameters

    #### - `room_history`: `list`
    List of all the states of the room, in chronological order.

    #### - `agent_history`: `list`
    List of all the movements that the agent does, in chronological
    order.
    """
    fig, ax = plt.subplots()
    ims = []

    # Define the custom ColoredMap:
    colors = [
        (1.0, 1.0, 1.0),  # White - Clean cells
        (0.6, 0.4, 0.2),  # Brown - Dirty cells
        (0.2, 0.2, 0.2),  # Dark Grey - Obstacles
        (0.7, 0.9, 0.7),  # Light Green - Charging stations
        (0.0, 0.0, 0.0),  # Black - Borders
    ]
    cmap = LinearSegmentedColormap.from_list("my_cmap", colors, N=256)

    # Define the animated agent:
    vertices = [
        (0, 0),
        (0, 1),
        (1, 1),
        (1, 0),
        (0, 0),
    ]
    codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
        Path.CLOSEPOLY,
    ]
    path = Path(vertices, codes)
    marker = path

    # Remove the initial empty frame, and start with the actual room state:
    room_history.pop(0)
    agent_history.pop(0)

    # Create the final animation:
    for room, agent_pos in zip(room_history, agent_history):
        # Convert the room data to numerical representation using the mapping:
        value_map = {
            "Clean": 0,
            "Dirty": 1,
            "Obstacle": 2,
            "Charger": 3,
            "CellBorder": 4,
        }
        room_numeric = np.vectorize(value_map.get)(room)

        # Create an image with the room state:
        room = np.zeros((room_numeric.shape[0] + 2, room_numeric.shape[1] + 2))
        room[1:-1, 1:-1] = room_numeric
        room[0, :] = value_map["CellBorder"]
        room[-1, :] = value_map["CellBorder"]
        room[:, 0] = value_map["CellBorder"]
        room[:, -1] = value_map["CellBorder"]
        im = ax.imshow(
            room,
            cmap=cmap,
            interpolation="none",
        )

        # Highlight the agent's position with its marker:
        dot = ax.plot([], [], marker=marker, markersize=20, color="red")[0]
        dot.set_data((agent_pos[1] + 1, agent_pos[0] + 1))

        ims.append([im, dot])

    # Final animation output creator:
    ani = ArtistAnimation(
        fig,
        ims,
        interval=150,
        blit=True,
    )
    # Add a title and labels to the subplot:
    ax.set_title(
        f"Model Based Vacuum Cleaner Agent working in a {room_numeric.shape[0]}x{room_numeric.shape[1]} room with obstacles."
    )
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    # Animation output:
    plt.show()


# =========== #
# MAIN METHOD #
# =========== #
if __name__ == "__main__":
    random_matrix = rooms(10, 10)

    vacuum = BidimensionalVacuumAgent(random_matrix)
    vacuum.vacuum_drop()
    room_history, agent_history = vacuum.movement(450)

    print(
        f"The vacuum has finished its job. Its performance score is {round(vacuum.performance, 3)}."
    )

    # Visualize the animation
    visualize_animation(room_history, agent_history)
