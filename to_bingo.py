import pandas as pd
import functools as fun
import itertools as it
from jinja2 import Environment, FileSystemLoader
import os
import dataclasses as dto

root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
env = Environment( loader = FileSystemLoader(templates_dir) )
template = env.get_template('bingo_template.tex')
filename = os.path.join(root, 'tex', 'bingo_template.tex')


@dto.dataclass
class Line:
    tracks: list[str]
    artists: list[str]

@dto.dataclass
class BingoCard:
    lines: list[Line]


def process_template(bingos: list[BingoCard]):
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
        tracks = []
        artists = []
        for track in r:
            tracks.append(track._1)
            artists.append(track._2)
        lines.append(Line(tracks=tracks, artists=artists))
    return BingoCard(lines=lines)
        

def main(cards: int, rows: int, columns: int):
    bingos = [gen_bingo_card(rows, columns) for _ in range(cards)]
    process_template(bingos)


if __name__ == '__main__':
    main(3, 3, 3)
