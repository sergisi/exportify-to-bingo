import pandas as pd
import random
import typer
import functools as fun
import itertools as it
from jinja2 import Environment, FileSystemLoader, Template
import os
import dataclasses as dto


@dto.dataclass(frozen=True)
class Line:
    songs: list[str]

@dto.dataclass(frozen=True)
class BingoCard:
    lines: list[Line]


def process_template(bingos: list[BingoCard], filename: str, 
                     template: Template):
    with open(filename, 'w') as fh:
        fh.write(template.render(
            bingos = bingos,
        ))

@fun.lru_cache(maxsize=1)
def get_data():
    return pd.read_csv('playlist.csv')


def gen_bingo_card(rows: int, columns: int) -> frozenset[str]:
    """
        Creates a single bingo card
    """
    # NOTE: Creates a single bingo card
    data = get_data()
    bingo_card = (data
                  .sample(rows * columns)
                  .sort_index()
                  .itertuples())
    return frozenset(track._1 for track in bingo_card)


def transform(bingo_card: frozenset[str], columns: int) -> BingoCard:
    lines = []
    bingo_list = list(bingo_card)
    random.shuffle(bingo_list)
    for r in it.batched(bingo_list, n=columns):
        songs = []
        for track in r:
            songs.append(track)
        lines.append(Line(songs=songs))
    return BingoCard(lines=lines)


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
            break
    return [transform(bingo, columns) for bingo in bingos]

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

