import click
import pandas as pd

from fractalai.engine.utils import get_config


@click.command()
@click.option("-c", "--config_path", required=True, help="Path to config file")
def check_csv(config_path: str):
    config = get_config(config_path)
    assert "csv" == config.train_loc.rsplit(".")[-1], "Not a csv file"
    data = pd.read_csv(config.train_loc)
    print(f"data shape: {data.shape}")
    print(data.head())
