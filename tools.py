import os
from config import DATA_FOLDER
from langchain.tools import tool
import pandas as pd
from pydantic import BaseModel

@tool
def get_all_jobs_ids() -> str:
    """Get all folder names in the data folder which are Job IDs"""
    folders = [f for f in os.listdir(DATA_FOLDER) if os.path.isdir(os.path.join(DATA_FOLDER, f))]
    # return str(folders)
    return "The following job IDs are available:\n" + "\n".join(folders)

@tool
def get_latest_job_id() -> str:
    """Get the latest job ID based on creation time"""
    folders = [f for f in os.listdir(DATA_FOLDER) if os.path.isdir(os.path.join(DATA_FOLDER, f))]
    latest = max(folders, key=lambda f: os.path.getctime(os.path.join(DATA_FOLDER, f)))
    return latest

class JobIDInput(BaseModel):
    job_id: str

@tool
def get_source_file_name_for_duplicates(job_id: str) -> str:
    """Get the source file name for duplicates.
    Source file name for duplicates starts with s1_duplicates and ends with the <job_id>.csv
    Args:
        job_id (str): The job ID to check for duplicates.
    Returns: 
        str: The file name of the source file for duplicates.
    """
    # Construct the file name based on the job ID
    file_name = next((f for f in os.listdir(os.path.join(DATA_FOLDER, job_id)) 
                      if f.startswith("s1_duplicates_") and f.endswith(f"_{job_id}.csv")), None)
    if not file_name:
        raise FileNotFoundError(f"No file matching the pattern 's1_duplicates_*_{job_id}.csv' was found.")
    return file_name


@tool
def get_target_file_name_for_duplicates(job_id: str) -> str:
    """Get the target file name for duplicates.
    Target file name for duplicates starts with s2_duplicates and ends with the <job_id>.csv
    Args:
        job_id (str): The job ID to check for duplicates.
    Returns: 
        str: The file name of the target file for duplicates.
    """
    # Construct the file name based on the job ID
    file_name = next((f for f in os.listdir(os.path.join(DATA_FOLDER, job_id)) 
                      if f.startswith("s2_duplicates_") and f.endswith(f"_{job_id}.csv")), None)
    if not file_name:
        raise FileNotFoundError(f"No file matching the pattern 's2_duplicates_*_{job_id}.csv' was found.")
    return file_name
   

class SourceCountInput(BaseModel):
    job_id: str
    source_duplicate_file_name: str

@tool
def get_source_records_count_for_duplicates(job_id: str) -> int:
    """Get the number of records in the source file for duplicates.
    Args:
        job_id (str): The job ID to check for duplicates.
    Returns: 
        int: The number of records in the source file for duplicates.
    """
    source_duplicate_file_name=get_source_file_name_for_duplicates(job_id)
    # Read the CSV file into a DataFrame
    df = pd.read_csv(os.path.join(DATA_FOLDER, job_id, source_duplicate_file_name))
    # Return the number of records
    return len(df)


class TargetCountInput(BaseModel):
    job_id: str
    target_duplicate_file_name: str

@tool
def get_target_records_count_for_duplicates(job_id: str) -> int:
    """Get the number of records in the target file for duplicates.
    Args:
        job_id (str): The job ID to check for duplicates. 
    Returns: 
        int: The number of records in the target file for duplicates.
    """
    target_duplicate_file_name=get_target_file_name_for_duplicates(job_id)
    # Read the CSV file into a DataFrame
    df = pd.read_csv(os.path.join(DATA_FOLDER, job_id, target_duplicate_file_name))
    # Return the number of records
    return len(df)


@tool
def get_source_file_name_for_unique_records(job_id: str) -> str:
    """Get the source file name for unique records
    Source file name for unique records starts with s1_not_in_s2 and ends with the <job_id>.csv
    Args:
        job_id (str): The job ID to check for unique records.  
    Returns:
        str: The file name of the source file for unique records.
    """
    # Construct the file name based on the job ID
    file_name = next((f for f in os.listdir(os.path.join(DATA_FOLDER, job_id)) 
                      if f.startswith("s1_not_in_s2_") and f.endswith(f"_{job_id}.csv")), None)
    if not file_name:
        raise FileNotFoundError(f"No file matching the pattern 's1_not_in_s2_*_{job_id}.csv' was found.")
    return file_name

@tool
def get_target_file_name_for_unique_records(job_id: str) -> str:
    """Get the target file name for unique records.
    Target file name for unique records starts with s2_not_in_s1 and ends with the <job_id>.csv
    Args:
        job_id (str): The job ID to check for unique records.
    Returns:
        str: The file name of the target file for unique records.
    """
    # Construct the file name based on the job ID
    file_name = next((f for f in os.listdir(os.path.join(DATA_FOLDER, job_id)) 
                      if f.startswith("s2_not_in_s1_") and f.endswith(f"_{job_id}.csv")), None)
    if not file_name:
        raise FileNotFoundError(f"No file matching the pattern 's2_not_in_s1_*_{job_id}.csv' was found.")
    return file_name



@tool
def get_source_records_count_for_unique_records(job_id: str) -> int:
    """Get the number of unique records in the source file that doesnot exist in the target file.
    Args:
        job_id (str): The job ID to check for duplicates.
    Returns:
        int: The number of unique records in the source file that doesnot exist in the target file.
    """
    source_unique_file_name=get_source_file_name_for_unique_records(job_id)
    # Read the CSV file into a DataFrame
    df = pd.read_csv(os.path.join(DATA_FOLDER, job_id, source_unique_file_name))
    # Return the number of records
    return len(df)


@tool
def get_target_records_count_for_unique_records(job_id: str) -> int:
    """Get the number of unique records in the target file that doesnot exist in the source file.
    Args:
        job_id (str): The job ID to check for duplicates.
    Returns:
        int: The number of unique records in the target file that doesnot exist in the source file.
    """
    target_unique_file_name=get_target_file_name_for_unique_records(job_id)
    # Read the CSV file into a DataFrame
    df = pd.read_csv(os.path.join(DATA_FOLDER, job_id, target_unique_file_name))
    # Return the number of records
    return len(df)

@tool
def get_file_name_for_mismatched_records(job_id: str) -> str:
    """Get the file name for mismatched records.
    Mismatch file name starts with mismatch_ and ends with the <job_id>.csv
    Args:
        job_id (str): The job ID to check for mismatched records.
    Returns:
        str: The file name of the mismatch file.
    """
    # Construct the file name based on the job ID
    file_name = next((f for f in os.listdir(os.path.join(DATA_FOLDER, job_id)) 
                      if f.startswith("mismatch_") and f.endswith(f"_{job_id}.csv")), None)
    if not file_name:
        raise FileNotFoundError(f"No file matching the pattern 'mismatch_*_{job_id}.csv' was found.")
    return file_name

# @tool
# def read_mismatched_records(job_id: str) -> pd.DataFrame:
#     """Read the mismatched records from the mismatch files.
#     mismatch file name starts with mismatch_ and ends with the <job_id>.csv
#     Args:
#         job_id (str): The job ID to check for mismatched records.
#     Returns:
#         pd.DataFrame: A DataFrame containing the mismatched records.
#     """
#     mismatch_file_name=get_file_name_for_mismatched_records(job_id)
#     # Read the CSV file into a DataFrame
#     df = pd.read_csv(os.path.join(DATA_FOLDER, job_id, mismatch_file_name))
#     # Return the DataFrame
#     return df


@tool
def get_mismatch_record_reason(job_id: str) -> dict:
    """Get the mismatch record reason by comparing corresponding source and target columns.
    It will compare the source and target columns in the mismatch file to provide the reason for the mismatch.
    The  actual column name starts after _ and before _ is source or target name.

    Mismatch file name starts with mismatch_ and ends with the <job_id>.csv
    Args:
        job_id (str): The job ID to check for mismatched records.
    Returns:
        Dictionary containing mismatched column pairs and their details.
    """
    mismatch_file_name=get_file_name_for_mismatched_records(job_id)
    # Read the CSV file into a DataFrame
    df = pd.read_csv(os.path.join(DATA_FOLDER, job_id, mismatch_file_name))
    # Call the function to find mismatches
    mismatch_dict = find_all_mismatches(df)
    return mismatch_dict

def find_all_mismatches(df):
    """
    Identifies mismatches across all source-target column pairs in a DataFrame.
    Returns an LLM-friendly JSON-like dictionary with mismatched row indices.

    :param df: DataFrame where source and target columns are paired consecutively
    :return: Dictionary containing mismatched column pairs and their details.
    """
    if df.shape[1] % 2 != 0:
        raise ValueError("The DataFrame must have an even number of columns for proper pairing.")

    df_copy = df.astype(str)  # Convert all columns to string for uniform comparison
    mismatch_dict = {}

    # Iterate through column pairs
    for i in range(0, df_copy.shape[1], 2):  
        col_source, col_target = df_copy.columns[i], df_copy.columns[i + 1]

        # Find mismatches using .ne() (not equal)
        mismatch_mask = df_copy[col_source].ne(df_copy[col_target])

        if mismatch_mask.any():
            mismatch_dict[f"{col_source}_vs_{col_target}"] = [
                {"row": idx, "source": df_copy.at[idx, col_source], "target": df_copy.at[idx, col_target]}
                for idx in mismatch_mask[mismatch_mask].index
            ]

    return mismatch_dict