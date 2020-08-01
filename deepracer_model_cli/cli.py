import typer
import termcolor

from deepracer_model_cli.models.model import DeepRacerModel
from pyfiglet import figlet_format
from typing import List, Optional

app = typer.Typer()


@app.command()
def validate():
    typer.echo(f"TODO: Test if a given tar.gz can be loaded by the car.")

@app.command()
def archive_car(folder: str = typer.Argument(..., help="Path to the folder which contains your locally trained model."), output_file: str = typer.Argument("model.tar.gz", help="Path to the tar file in which the output is stored."), export_last: Optional[bool] = typer.Option(None, "--export_last/--export_best")):
    model = DeepRacerModel(folder)

    if export_last:
        mode= "last"
    else:
        mode = "best"
    
    model.archive(output_file, mode="best")

def main():
    termcolor.cprint(figlet_format("AWS DeepRacer", font="speed"), 'white', attrs=['bold'])
    app()