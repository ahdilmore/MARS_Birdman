#!/bin/bash
#SBATCH --chdir=/projects/u19/Wisconsin_MARS/birdman/apoe4/
#SBATCH --output=/projects/u19/Wisconsin_MARS/birdman/apoe4/slurm_out/zebra/%x.%a.out
#SBATCH --partition=short
#SBATCH --mail-user="adilmore@ucsd.edu"
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mem=64G
#SBATCH --nodes=1
#SBATCH --partition=short
#SBATCH --cpus-per-task=4
#SBATCH --time=6:00:00
#SBATCH --array=1-20

pwd; hostname; date

set -e

# REPLACE WITH YOUR ENVIRONMENT NAME
source ~/anaconda3/bin/activate birdman

echo Chunk $SLURM_ARRAY_TASK_ID / $SLURM_ARRAY_TASK_MAX

# REPLACE WITH YOUR FILEPATHS
TABLEID="zebra_ft_apoe4"
TABLE="/projects/u19/Wisconsin_MARS/data/feature_tables/"$TABLEID".biom"
SLURMS="/projects/u19/Wisconsin_MARS/birdman/apoe4/slurm_out/metab/"$TABLEID
OUTDIR="/projects/u19/Wisconsin_MARS/birdman/apoe4/inferences/"$TABLEID
LOGDIR="/projects/u19/Wisconsin_MARS/birdman/apoe4/logs/"$TABLEID
mkdir -p $SLURMS
mkdir -p $OUTDIR
mkdir -p $LOGDIR

echo Starting Python script...
# REPLACE WITH YOUR SCRIPT PATH 
time python /projects/u19/Wisconsin_MARS/birdman/src/apoe4_birdman_chunked.py \
    --table-path $TABLE \
    --inference-dir $OUTDIR \
    --num-chunks $SLURM_ARRAY_TASK_MAX \
    --chunk-num $SLURM_ARRAY_TASK_ID \
    --logfile "${LOGDIR}/chunk_${SLURM_ARRAY_TASK_ID}.log" && echo Finished Python script!

