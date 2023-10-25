import pandas as pd
import numpy as np

def match(a, b):
    return [ b.index(x) if x in b else None for x in a ]

def retrieve_or_na(ilocable, indices):
    return [ilocable.iloc[i] if i is not None else None for i in indices]

def prepare_belonging_df(df):
    """
    Prepare the belonging dataframe by shuffling and 
    removing rows with duplicate concepts.

    Parameters:
    - df (pd.DataFrame): The belonging dataframe with 'parent' and 'concept' columns.

    Returns:
    - pd.DataFrame: The prepared dataframe.
    """
    # Shuffle dataframe
    df = df.sample(frac=1).reset_index(drop=True)
    
    # Drop duplicates based on 'concept' column, keeping the first occurrence
    df = df.drop_duplicates(subset='concept', keep='first')
    
    return df

def generate_ontology_tree(gene_df):
    # Create a unique list of concepts and add root nodes
    unique_concepts = pd.unique(gene_df[['parent', 'concept']].values.ravel('K'))
    root_nodes = pd.DataFrame({"parent": "", "concept": unique_concepts[~np.isin(unique_concepts, gene_df['concept'])]})
    gene_df = pd.concat([root_nodes, gene_df], ignore_index=True)

    # Initialize columns for prefix and encoding
    gene_df['prefix'] = np.nan
    gene_df['encoding'] = np.nan

    # Assign binary prefixes for each concept associated with a particular parent
    for ip in gene_df['parent'].unique():
        match_indices = gene_df[gene_df['parent'] == ip].index
        gene_df.loc[match_indices, 'prefix'] = [str(10**i) for i in range(len(match_indices))]

    # Assign encodings for root nodes
    gene_df.loc[gene_df['parent'] == "", 'encoding'] = gene_df['prefix']

    # Recursively assign encodings by appending prefix to the parent's encoding
    while gene_df['encoding'].isna().sum() > 0:
        indices = match(list(gene_df['parent']), list(gene_df['concept']))
        parent_encodings = retrieve_or_na(gene_df['encoding'], indices)
        sel = gene_df['encoding'].isna() & pd.Series(parent_encodings).notna()
        gene_df.loc[sel, 'encoding'] = gene_df.loc[sel, 'prefix'].astype(str) + pd.Series(parent_encodings).astype(str)[sel]

    return gene_df

if __name__ == "__main__":
    belongings = [
        {"parent": "Science", "concept": "Physics"},
        {"parent": "Physics", "concept": "Quantum Mechanics"},
        {"parent": "Physics", "concept": "Relativity"},
        {'parent': "Art", "concept": "Watercolor"}
        # ... you can add more belongings here
    ]
    
    # Convert belongings to DataFrame
    belongings_df = pd.DataFrame(belongings)
    
    belongings_df = prepare_belonging_df(belongings_df)
    result_df = generate_ontology_tree(belongings_df)
    print(result_df)
    
    # Example:
    df = pd.DataFrame({"parent": ["A", "A", "B", "B", "G", "G", "B", "A", "A", "B", "Q"], 
                    "concept": ["B", "C", "D", "E", "H", "J", "T", "Blah", "adsada", "C", "Z"]})
    df = prepare_belonging_df(df)

    result_df = generate_ontology_tree(df)
    print(result_df)

    # Check uniqueness
    print(len(result_df['encoding'].unique()) == len(result_df))