import curses
import curses.panel


class Window(object):
    data = None

    def __init__(self, width, height):
        self.window = curses.newwin(height, width, 1, 1)
        self.pane = curses.panel.new_panel(self.window)
        self.pane.top()
        self.pane.show()

    def move(self, x, y):
        self.pane.move(y, x)

    def draw(self):
        raise NotImplementedError("Not implemented.")

    def _draw(self):
        if self.data is None:
            return
        r = self.draw()
        self.window.refresh()
        return r


class Background(Window):
    def __init__(self, window, background=None):
        self.window = window
        self.pane = curses.panel.new_panel(window)
        self.pane.bottom()
        self.pane.show()
        self.data = background
        self._bg_width = max((len(x) for x in self.data))
        self._bg_height = len(self.data)

    def draw(self):
        height, width = self.window.getmaxyx()
        width = (width - self._bg_width) - 1
        height = (height - self._bg_height) - 1

        for li, line in enumerate(self.data):
            for ci, ch in enumerate(line):
                self.window.addch((width + ci), (height + li), ch)


class List(Window):
    def __init__(self, width, height, data=None):
        super(List, self).__init__(width, height)
        self.data = data
        self.selected = 2
        self.window.border(
            curses.ACS_VLINE,
            curses.ACS_VLINE,
            curses.ACS_HLINE,
            curses.ACS_HLINE,
            curses.ACS_ULCORNER,
            curses.ACS_URCORNER,
            curses.ACS_LLCORNER,
            curses.ACS_LRCORNER,
        )
        self.window.refresh()

    def draw(self):
        height, width = self.window.getmaxyx()
        for line, pairs in enumerate(self.data[:height]):
            attrib = curses.A_DIM

            if self.selected == line:
                attrib = curses.A_STANDOUT

            self.window.addnstr(1 + line, 2, pairs[0], width, attrib)


class Table(List):
    def __init__(self, width, height, layout, data=None):
        super(Table, self).__init__(width, height, data=data)
        self.layout = layout

    def draw(self):
        height, width = self.window.getmaxyx()
        height = (height - 2)
        increments = (int(width / len(self.layout)) - 1)

        self.window.addnstr(
            1,
            2,
            "".join([x.ljust(increments) for x in self.layout]),
            width,
            curses.A_BOLD
        )

        for line, pairs in enumerate(self.data[:(height - 2)]):
            attrib = curses.A_DIM

            if self.selected == line:
                attrib = curses.A_STANDOUT

            self.window.addnstr(
                3 + line,
                2,
                "".join([x.ljust(increments)[:increments] for x in pairs[1:]]),
                width,
                attrib
            )
