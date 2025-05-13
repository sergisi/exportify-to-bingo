import pandas as pd
import typer
import functools as fun
import itertools as it
from jinja2 import Environment, FileSystemLoader, Template
import os
import dataclasses as dto


@dto.dataclass(frozen=True)
class Song:
    track: str
    artist: str

@dto.dataclass(frozen=True)
class Line:
    songs: tuple[Song]

@dto.dataclass(frozen=True)
class BingoCard:
    lines: tuple[Line]


def process_template(bingos: list[BingoCard], filename: str, 
                     template: Template):
    with open(filename, 'w') as fh:
        fh.write(template.render(
            bingos = bingos,
        ))

@fun.lru_cache(maxsize=1)
def get_data():
    return pd.read_csv('playlist.csv')


def gen_bingo_card(rows: int, columns: int) -> BingoCard:
    """
        Creates a single bingo card
    """
    # NOTE: Creates a single bingo card
    data = get_data()
    bingo_card = (data[['Track Name', 'Artist Name(s)']]
                  .sample(rows * columns)
                  .itertuples())
    lines = []
    for r in it.batched(bingo_card, n=columns):
        songs = []
        for track in r:
            songs.append(Song(track._1, track._2))
        lines.append(Line(songs=tuple(songs)))
    return BingoCard(lines=tuple(lines))


def create_bingos(cards: int, rows: int, columns: int) -> list[BingoCard]:
    """
    Does not guarantee the number of bingo cards generated, as
    they must be different. But, if the list of songs is large 
    enough, it's almost guanrateed.
    """
    bingos = set()
    for _ in range(cards * 2):
        bingos.add(gen_bingo_card(rows, columns))
        if len(bingos) >= cards:
            return list(bingos)
    return list(bingos)

def main(cards: int, 
         rows: int, 
         columns: int,
         template_name: str = 'bingo_template.tex'
         ):
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'templates')
    env = Environment( loader = FileSystemLoader(templates_dir) )
    template = env.get_template(template_name)
    filename = os.path.join(root, 'tex', 'bingo_template.tex')


    bingos = create_bingos(cards, rows, columns)
    process_template(bingos, filename, template)


if __name__ == '__main__':
    typer.run(main)
