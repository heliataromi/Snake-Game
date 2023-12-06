import random
import tkinter as tk


class Snake:
    """
    Class representing the snake in the game.

    Attributes
    ----------
    canvas : tk.Tk
        The game's main canvas.
    coordinates : list of tuple of int
        List of coordinates (x, y) representing the snake's body segments.
    canvas_ids : list
        List of canvas item ids for each of the snake's segments.
    color : str
        Color code of the snake.
    direction : str
        The current moving direction of the snake.

    Methods
    -------
    draw_snake_on_canvas()
        Updates the snake's position on the canvas by appending a new head segment
        and removing the tail segment.
    """

    def __init__(self, canvas):
        """Initialize the snake with a canvas, initial coordinates, color, and direction."""

        self.coordinates = [(0, 0), (20, 0)]  # Starting position of the snake
        self.canvas = canvas
        self.canvas_ids = []  # Stores IDs of the snake's body segments on the canvas
        self.color = '#62A150'  # Define the color of the snake
        self.direction = 'Right'  # Initial direction of the snake

        # Draw the snake on the canvas
        for x, y in self.coordinates:
            id = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill=self.color, tag='snake')
            # Store the rectangle ID
            self.canvas_ids.append(id)

    def draw_snake_on_canvas(self):
        """Update the snake's drawing on the canvas."""

        # Get the head coordinates of the snake
        head_x, head_y = self.coordinates[-1]

        # Determine new head position based on current direction
        if self.direction == 'Up':
            new_head = (head_x, head_y - 20)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + 20)
        elif self.direction == 'Left':
            new_head = (head_x - 20, head_y)
        elif self.direction == 'Right':
            new_head = (head_x + 20, head_y)

        # Add new head to the coordinates list
        self.coordinates.append(new_head)

        # Draw new head
        x, y = new_head
        id = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill=self.color, tag='snake')

        # Store the rectangle ID
        self.canvas_ids.append(id)


class Food:
    """
        Class representing the food in the game.

        Attributes
        ----------
        coordinates : tuple of int
            A tuple representing the x and y coordinates of the food.
        canvas : tk.Tk
            The game's main canvas.

        Methods
        -------
        draw_food_on_canvas()
            Draws food on the canvas at a random location.
        """

    def __init__(self, canvas):
        """Initialize the food with a canvas and place it randomly on the canvas."""

        self.coordinates = (random.randrange(0, 380, 20), random.randrange(0, 380, 20))
        self.canvas = canvas
        self.draw_food_on_canvas()

    def draw_food_on_canvas(self):
        """Place new food on the canvas at a random location."""

        # Remove the old food item
        self.canvas.delete('food')

        # Generate new food coordinates as a random tuple
        self.coordinates = (random.randrange(0, 380, 20), random.randrange(0, 380, 20))

        # Draw new food on the canvas
        x, y = self.coordinates
        self.canvas.create_oval(x, y, x + 20, y + 20, fill='#FF0000', outline='#FF0000', tag='food')


class Game:
    """
        Class representing the snake game.

        Attributes
        ----------
        snake : Snake
            The Snake object in the game.
        food : Food
            The Food object in the game.
        score : int
            The current score of the game.
        root : tk.Tk
            The Tkinter root window.

        Methods
        -------
        create_gui(root)
            Sets up the user interface for the game.
        change_dir(event)
            Changes the direction of the snake based on keyboard input.
        move()
            Conducts the movement of the snake, checks for collisions, updates the score, and redraws the game elements.
        check_collision()
            Checks if the snake has collided with the borders or itself.
        has_hit_food()
            Checks if the snake's head has reached the food.
        """

    def __init__(self, root):
        """Initialize the game with the Tkinter root."""

        self.snake = None
        self.food = None
        self.score: int = 0
        self.create_gui(root)  # Create the game interface

    def create_gui(self, root):
        """Creates the graphical user interface of the game."""

        self.root = root
        self.root.title('Snake Game')  # Set window title
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg='#FFFFFF')  # Create the game canvas
        self.canvas.pack()
        self.score_label = tk.Label(
            self.root,
            text=f'Score: {self.score}',
            font=('Courier', 20, 'bold'))  # Score display
        self.score_label.pack()

        # Bind arrow keys to change the direction of the snake
        self.root.bind('<Up>', self.change_dir)
        self.root.bind('<Down>', self.change_dir)
        self.root.bind('<Left>', self.change_dir)
        self.root.bind('<Right>', self.change_dir)

        # Initiate the movement of the snake
        self.root.after(300, self.move)

        # Create instances of Snake and Food
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)

    def change_dir(self, event):
        """Changes the snake's direction based on keyboard input."""

        # Get the key pressed by the user
        key = event.keysym

        # Update the direction if key is an arrow not opposite to current direction
        if key in ['Up', 'Down', 'Left', 'Right'] and not (
                (key == 'Up' and self.snake.direction == 'Down')
                or (key == 'Down' and self.snake.direction == 'Up')
                or (key == 'Left' and self.snake.direction == 'Right')
                or (key == 'Right' and self.snake.direction == 'Left')
        ):
            self.snake.direction = key

    def move(self):
        """Handles the logic of the snake's movement, updates the score, and checks for game over condition."""

        # End the game on collision
        if self.check_collision():
            # Clear the canvas and displaying game over message
            self.canvas.delete('all')
            self.canvas.create_text(
                200,
                200,
                text='Game over!',
                fill='#C70404',
                font=('Courier', 32, 'bold'),
            )
            return  # Ending the method

        # Check if the snake has eaten the food
        if self.has_hit_food():
            self.score += 1  # Increment score
            self.score_label.config(text=f'Score: {self.score}')  # Update score label
            self.food.draw_food_on_canvas()  # Place new food
        else:
            # Remove the tail segment if food is not eaten
            self.snake.coordinates.pop(0)
            tail_id = self.snake.canvas_ids.pop(0)
            self.canvas.delete(tail_id)

        # Add a new head segment
        self.snake.draw_snake_on_canvas()
        # Continue the game loop
        self.root.after(300, self.move)

    def check_collision(self):
        """Check for collision with the wall or the snake itself."""

        head_x, head_y = self.snake.coordinates[-1]  # Get head position

        # Check if collision occurs
        if (
                head_x < 0
                or head_x >= 380
                or head_y < 0
                or head_y >= 380
                or (head_x, head_y) in self.snake.coordinates[:-1]
        ):
            return True
        return False

    def has_hit_food(self):
        """Check if the snake head has collided with the food."""

        head_x, head_y = self.snake.coordinates[0]  # Get head position
        food_x, food_y = self.food.coordinates  # Get food position
        # Return True if positions match
        return (head_x, head_y) == (food_x, food_y)


if __name__ == '__main__':
    # Create a tkinter window
    root = tk.Tk()

    # Create an instance of the Game class
    board = Game(root)

    # Start the main loop of the window
    root.mainloop()
