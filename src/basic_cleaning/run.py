#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################

    logger.info("Downloading artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)
    
    # Drop outliers
    logger.info("Removing outliers")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    
    # Convert last_review to datetime    
    logger.info("Casting last_review column's type to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])
    
    # Saving results to csv file    
    logger.info("Saving results to local csv file")
    df.to_csv("clean_sample.csv", index=False)
    
    # Uploading local csv file to Weights & Biases
    logger.info("Uploading results to Weights & Biases")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")

    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="the input artifact",
        required=True,
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="the name for the output artifact",
        required=True,
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="the type for the output artifact",
        required=True,
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="a description for the output artifact",
        required=True,
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="the minimum price to consider",
        required=True,
    )
    parser.add_argument(
        "--max_price", 
        type=float,
        help="the maximum price to consider",
        required=True,
    )


    args = parser.parse_args()

    go(args)
