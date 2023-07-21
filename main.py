import random
import tkinter as tk


class Snake:
    def __init__(self, canvas):
        self.coordinates = [(0, 0), (20, 0)]
        self.canvas = canvas
        self.canvas_ids = []
        self.color = '#62A150'
        self.direction = 'Right'

        # Drawing the snake on the canvas using rectangles with tag 'snake'
        for x, y in self.coordinates:
            id = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill=self.color, tag='snake')
            # Appending the id to the canvas ids list
            self.canvas_ids.append(id)

    def draw_snake_on_canvas(self):
        # Getting the head coordinates of the snake
        head_x, head_y = self.coordinates[-1]
        # Moving the head of the snake based on the direction
        if self.direction == 'Up':
            new_head = (head_x, head_y - 20)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + 20)
        elif self.direction == 'Left':
            new_head = (head_x - 20, head_y)
        elif self.direction == 'Right':
            new_head = (head_x + 20, head_y)
        # Adding the new head to the snake coordinates list
        self.coordinates.append(new_head)
        # Creating a new rectangle for the snake head on the canvas with tag 'snake'
        x, y = new_head
        id = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill=self.color, tag='snake')
        # Appending the id to the canvas ids list
        self.canvas_ids.append(id)


class Food:
    def __init__(self, canvas):
        self.coordinates = (random.randrange(0, 380, 20), random.randrange(0, 380, 20))
        self.canvas = canvas
        self.draw_food_on_canvas()

    def draw_food_on_canvas(self):
        # Deleting the old food from the canvas
        self.canvas.delete('food')
        # Generating new food coordinates as a random tuple
        self.coordinates = (random.randrange(0, 380, 20), random.randrange(0, 380, 20))
        # Drawing the new food on the canvas using an oval with tag 'food'
        x, y = self.coordinates
        self.canvas.create_oval(x, y, x + 20, y + 20, fill='#FF0000', outline='#FF0000', tag='food')


class Game:
    def __init__(self, root):
        self.snake = None
        self.food = None
        self.score: int = 0
        self.create_gui(root)

    def create_gui(self, root):
        self.root = root
        # Setting the window title
        self.root.title('Snake Game')
        # Creating the canvas
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg='#FFFFFF')
        self.canvas.pack()
        # Creating the score label
        self.score_label = tk.Label(
            self.root,
            text=f'Score: {self.score}',
            font=('Courier', 20, 'bold'))
        self.score_label.pack()
        # Binding the arrow keys to the change_direction method
        self.root.bind('<Up>', self.change_dir)
        self.root.bind('<Down>', self.change_dir)
        self.root.bind('<Left>', self.change_dir)
        self.root.bind('<Right>', self.change_dir)

        # Calling the move method after 300 milliseconds
        self.root.after(300, self.move)

        # Creating snake and food
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)

    def change_dir(self, event):
        # Getting the key pressed by the user
        key = event.keysym
        # Checking if the key is valid and not opposite to the current direction
        if key in ['Up', 'Down', 'Left', 'Right'] and not (
                (key == 'Up' and self.snake.direction == 'Down')
                or (key == 'Down' and self.snake.direction == 'Up')
                or (key == 'Left' and self.snake.direction == 'Right')
                or (key == 'Right' and self.snake.direction == 'Left')
        ):
            # Updating the direction attribute of the snake
            self.snake.direction = key

    def move(self):
        # Checking if the snake has hit the wall or itself
        if self.check_collision():
            # Clearing the canvas and displaying game over message
            self.canvas.delete('all')
            self.canvas.create_text(
                200,
                200,
                text='Game over!',
                fill='#C70404',
                font=('Courier', 32, 'bold'),
            )
            return  # Ending the method

        # Checking if the snake has eaten the food
        if self.has_hit_food():
            # Increasing the score by one and updating the label text
            self.score += 1
            self.score_label.config(text=f'Score: {self.score}')
            # Drawing a new food on the canvas using the food method
            self.food.draw_food_on_canvas()
        else:
            # Removing the tail of the snake from the canvas and the coordinates list
            self.snake.coordinates.pop(0)
            tail_id = self.snake.canvas_ids.pop(0)
            self.canvas.delete(tail_id)

        # Drawing a new snake on the canvas using the snake method
        self.snake.draw_snake_on_canvas()
        # Calling the move method again after 300 milliseconds
        self.root.after(300, self.move)

    def check_collision(self):
        # Getting the head coordinates of the snake
        head_x, head_y = self.snake.coordinates[-1]
        # Checking if the snake has hit the wall or itself
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
        # Getting the head coordinates of the snake and the food coordinates
        head_x, head_y = self.snake.coordinates[0]
        food_x, food_y = self.food.coordinates
        # Returning True if they are equal, False otherwise
        return (head_x, head_y) == (food_x, food_y)


if __name__ == '__main__':
    # Creating a tkinter window
    root = tk.Tk()

    # Creating an instance of the Game class
    board = Game(root)

    # Starting the main loop of the window
    root.mainloop()
