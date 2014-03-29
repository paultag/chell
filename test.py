from chell.ui import Background, List, Table
import curses


def main(stdscr):
    # buf = [list(x) for x in open('/home/tag/interface', 'r').readlines()]
    # b = Background(stdscr, background=buf)
    # b._draw()

    l = Table(
        int(curses.COLS - 2),
        int(curses.LINES * 0.8),
        ["job", "builder", "flavor"],
        data=[
            (1, "job 1", "none", "lintian"),
            (2, "job 2", "leliel.pault.ag", "lintian"),
            (3, "job 3", "metatron.pault.ag", "lintian"),
            (4, "job 4", "blade01.debile.debian.plumbing", "lintian"),
            (5, "job 5", "none", "build"),
            (6, "job 6", "none", "build"),
            (7, "job 7", "none", "build"),
            (8, "job 8", "none", "build"),
        ])

    l._draw()
    l.window.getch()

curses.wrapper(main)
