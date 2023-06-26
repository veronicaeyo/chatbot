import click

@click.command()
@click.option(
    '-a',
    type=int,
    default=1,
    help="First number"
)
@click.option(
    '-b',
    type=int,
    default=5,
    help="Second number"
)
def add(a, b):
    print(a + b)

if __name__ == '__main__':
    add()