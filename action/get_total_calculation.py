import pandas as pd
import streamlit as st
from io import StringIO

def try_parse_dataframe(value):
    if isinstance(value, pd.DataFrame):
        return value
    if isinstance(value, str):
        # Try to detect the format from the string structure
        try:
            # If the string is already a formatted table, parse it
            if "\n" in value and (value.count("\t") > 0 or value.count("  ") > 0):
                df = pd.read_csv(StringIO(value), sep=None, engine='python')
                return df
            else:
                # Try as JSON or other formats
                return pd.read_json(StringIO(value))
        except Exception:
            pass
    return None

def collect_tables(processed_array):
    tables = {
        "clicks_of_words": [],
        "top15": [],
        "GSC_top_KW": []
    }
    
    for item in processed_array:
        if isinstance(item, dict):
            for key in tables.keys():
                if key in item and item[key] is not None:
                    df = try_parse_dataframe(item[key])
                    if df is not None and not df.empty:
                        tables[key].append(df)
    
    return tables

def combine_and_aggregate_tables(tables):
    combined_tables = {}
    
    # Process clicks_of_words tables
    if tables["clicks_of_words"]:
        dfs_with_columns = []
        for df in tables["clicks_of_words"]:
            if len(df.columns) >= 2:  # Ensure there are at least 2 columns
                # Check column names and create a standardized DataFrame
                if "word" in df.columns and "clicks" in df.columns:
                    dfs_with_columns.append(df[["word", "clicks"]])
                else:
                    # Create new DataFrame with standard column names
                    dfs_with_columns.append(pd.DataFrame({
                        "word": df.iloc[:, 0] if df.shape[1] > 0 else [],
                        "clicks": df.iloc[:, 1] if df.shape[1] > 1 else []
                    }))
        
        if dfs_with_columns:
            combined_df = pd.concat(dfs_with_columns, ignore_index=True)
            # Convert to ensure proper grouping (in case of mixed types)
            combined_df["word"] = combined_df["word"].astype(str)
            aggregated_df = combined_df.groupby("word", as_index=False)["clicks"].sum()
            combined_tables["clicks_of_words"] = aggregated_df.sort_values("clicks", ascending=False)
    
    # Process top15 tables
    if tables["top15"]:
        dfs_with_columns = []
        for df in tables["top15"]:
            if df.shape[1] >= 2:  # Ensure DataFrame has at least 2 columns
                # Check if column names exist or are numeric
                if 0 in df.columns and 1 in df.columns:
                    # Create new DataFrame with standard column names
                    dfs_with_columns.append(pd.DataFrame({
                        "word": df[0],
                        "freq": df[1]
                    }))
                elif "word" in df.columns and "freq" in df.columns:
                    dfs_with_columns.append(df[["word", "freq"]])
                else:
                    # Use the first two columns whatever they're called
                    dfs_with_columns.append(pd.DataFrame({
                        "word": df.iloc[:, 0],
                        "freq": df.iloc[:, 1]
                    }))
        
        if dfs_with_columns:
            combined_df = pd.concat(dfs_with_columns, ignore_index=True)
            # Convert to ensure proper grouping
            combined_df["word"] = combined_df["word"].astype(str)
            aggregated_df = combined_df.groupby("word", as_index=False)["freq"].sum()
            combined_tables["top15"] = aggregated_df.sort_values("freq", ascending=False)
    
    # Process GSC_top_KW tables
    if tables["GSC_top_KW"]:
        dfs_with_columns = []
        for df in tables["GSC_top_KW"]:
            if df.shape[1] >= 2:  # Ensure DataFrame has at least 2 columns
                if "keyword" in df.columns and "clicks" in df.columns:
                    dfs_with_columns.append(df[["keyword", "clicks"]])
                else:
                    # Create new DataFrame with standard column names
                    dfs_with_columns.append(pd.DataFrame({
                        "keyword": df.iloc[:, 0],
                        "clicks": df.iloc[:, 1]
                    }))
        
        if dfs_with_columns:
            combined_df = pd.concat(dfs_with_columns, ignore_index=True)
            # Convert to ensure proper grouping
            combined_df["keyword"] = combined_df["keyword"].astype(str)
            aggregated_df = combined_df.groupby("keyword", as_index=False)["clicks"].sum()
            combined_tables["GSC_top_KW"] = aggregated_df.sort_values("clicks", ascending=False)
    
    return combined_tables

def get_total_calculation(processed_array):
    # Collect all tables by type
    tables = collect_tables(processed_array)
    
    # Combine and aggregate tables
    combined_tables = combine_and_aggregate_tables(tables)
    
    # Display combined tables
    for table_name, df in combined_tables.items():
        st.write(f"## Combined {table_name} Table")
        st.write(df)
    
    return combined_tables
