import arcade


class App(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    # def setup(self):
    #     pass

    def on_key_press(self, key, modifiers):
        print(key)


if __name__ == "__main__":
    window = App(500, 500, 'keytest')
    # window.setup()
    arcade.run()
