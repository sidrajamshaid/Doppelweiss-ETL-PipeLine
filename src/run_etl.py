import pandas as pd
from bronze_layer import bronze_dfs # This should be populated by the bronze_layer.py script
from silver_layer import clean_and_merge_bronze_data # This should be defined in silver_layer.py
from gold_layer import prepare_gold_layer # This should be defined in gold_layer.py

def main():
    # Step 1: Extract (bronze)
    # bronze_dfs is already populated by bronze_layer.py

    # Step 2: Transform (silver)
    silver_df = clean_and_merge_bronze_data(bronze_dfs)
    silver_df.to_csv("silver_reporting.csv", index=False)
    print("Silver layer output saved to silver_reporting.csv")

    # Step 3: Load/Prepare (gold)
    gold_df = prepare_gold_layer(silver_df)
    gold_df.to_csv("gold_reporting.csv", index=False)
    print("Gold layer output saved to gold_reporting.csv")

if __name__ == "__main__":
    main()