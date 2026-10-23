from sys import argv, exit
from pathlib import Path
from Draw import Draw


if __name__ == '__main__':
    if len(argv) != 2:
        exit('Usage: uv run python3 filename')
    if not Path(argv[1]).exists():
        exit('[ERROR]: File does not exists')
    if not argv[1].endswith('.txt'):
        exit('[ERROR]: File is not a TEXT(.txt) file')
    draw = Draw(argv[1])
    for i in draw.turns:
        print(i.strip())
    draw.draw()
