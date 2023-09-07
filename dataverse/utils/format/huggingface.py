
import os
import datasets
from pathlib import Path


def huggingface2parquet(
        dataset: datasets.Dataset,
        save_path: str = None,
        verbose: bool = True,
        **kwargs
    ):
    """
    Convert a huggingface dataset to parquet format and save it to the path.
    
    Args:
        dataset (datasets.Dataset): a huggingface dataset
        save_path (str): the path to save the parquet file
        verbose (bool): whether to print the information of the dataset
    """
    # check the dataset which has train, test, validation or other splits
    # concatenate all the splits into one
    dataset_list = []

    # check the dataset has splits
    try:
        for split in dataset.keys():
            dataset_list.append(dataset[split])
    except:
        dataset_list.append(dataset)

    dataset = datasets.concatenate_datasets(dataset_list)

    # save the dataset to parquet
    # FIXME: this is a temporary solution to store the dataset in the package root path
    #        we will change it to a better solution in the future
    if save_path is None:
        # save the parquet at package root path
        save_path = Path(os.path.abspath(__file__)).parents[3]

    dataset_path = f"{save_path}/.cache/huggingface_{dataset._fingerprint}.parquet"

    # check the dataset exist
    if os.path.exists(dataset_path):
        if verbose:
            print(f"Dataset already exists at {dataset_path}")
        return dataset_path

    os.makedirs(f"{save_path}/.cache", exist_ok=True)
    dataset.to_parquet(dataset_path)

    return dataset_path

if __name__ == "__main__":
    # test the function
    dataset = datasets.load_dataset("glue", "mrpc")
    dataset_path = huggingface2parquet(dataset, verbose=True)

    print(f"Dataset saved at {dataset_path}")