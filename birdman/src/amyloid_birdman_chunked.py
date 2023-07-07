import os
from tempfile import TemporaryDirectory
import time

import arviz as az
import biom
from birdman import ModelIterator
import cmdstanpy
import click
import numpy as np
import pandas as pd
from logger import setup_loggers
from model_amyloid_single import AmyloidModelSingle

@click.command()
@click.option("--table-path", required=True)
@click.option("--inference-dir", required=True)
@click.option("--num-chunks", required=True, type=int)
@click.option("--chunk-num", required=True, type=int)
@click.option("--chains", default=4)
@click.option("--num-iter", default=500)
@click.option("--num-warmup", default=500)
@click.option("--beta-prior", default=5)
@click.option("--inv-disp-sd", default=5)
@click.option("--logfile", required=True)
def run_birdman(
    table_path,
    inference_dir,
    num_chunks,
    chunk_num,
    chains,
    num_iter,
    num_warmup,
    beta_prior,
    inv_disp_sd,
    logfile,
):

    TABLE = biom.load_table(table_path)
    FIDS = TABLE.ids(axis="observation")
    birdman_logger = setup_loggers(logfile)

    model_iter = ModelIterator(
        TABLE,
        AmyloidModelSingle,
        num_chunks=num_chunks,
        beta_prior=beta_prior,
        inv_disp_sd=inv_disp_sd,
        chains=chains,
        num_iter=num_iter,
        num_warmup=num_warmup,
    )
    chunk = model_iter[chunk_num - 1]

    for feature_id, model in chunk:
        feature_num = np.where(FIDS == feature_id)[0].item()
        feature_num_str = str(feature_num).zfill(4)
        birdman_logger.info(f"Feature num: {feature_num_str}")
        birdman_logger.info(f"Feature ID: {feature_id}")

        tmpdir = f"{inference_dir}/tmp/F{feature_num_str}_{feature_id}"
        outfile = f"{inference_dir}/F{feature_num_str}_{feature_id}.nc"

        os.makedirs(tmpdir, exist_ok=True)

        with TemporaryDirectory(dir=tmpdir) as t:
            model.compile_model()
            model.fit_model(sampler_args={"output_dir": t})

            inf = model.to_inference()
            birdman_logger.info(inf.posterior)

            loo = az.loo(inf, pointwise=True)
            rhat = az.rhat(inf)
            birdman_logger.info("LOO:")
            birdman_logger.info(loo)
            birdman_logger.info("Rhat:")
            birdman_logger.info(rhat)
            if (rhat > 1.05).to_array().any().item():
                birdman_logger.warning(
                    f"{feature_id} has Rhat values > 1.05"
                )
            if any(map(np.isnan, loo.values[:3])):
                birdman_logger.warning(
                    f"{feature_id} has NaN elpd"
                )

            inf.to_netcdf(outfile)
            birdman_logger.info(f"Saved to {outfile}")
            time.sleep(10)

if __name__ == "__main__":
    run_birdman()
