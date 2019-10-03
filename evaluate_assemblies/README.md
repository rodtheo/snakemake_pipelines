# Snakemake Pipeline to Evaluate _de novo_ Assemblies

## Quick Usage

First of all, make sure that you have [docker](https://docs.docker.com/install/) and [conda](https://docs.conda.io/en/latest/miniconda.html) (or miniconda) installed in your machine. These softwares will be essential to assist in the installation of the tools that are going to be executed in each pipeline.

For each pipeline we have a particular conda environment and a docker image that must be installed. To clarify, let's execute the pipeline that evaluates a genome assembly given a short read illumina paired-end file. After cloning the corresponding repo, we begin the installation of the pipeline's specific environment and docker image.

To do this, we enter the folder corresponding to the pipeline (`cd evaluate_assemblies`) and create a new conda environment corresponding to our pipeline with the following command:

```
conda env create -f envs/myenv.yaml
```

This will create a conda environment called `evaluate_assemblies`. We can check that the environement was created through `conda info --envs`.

After this, we go to the folder `build_docker_img` and type `docker build -t rodtheo/genomics:eval_assem_ale_reapr .`. This will create an image with the remainer tools required for the execution of pipeline that could not be installed by conda. Again, we can check if the image was created listing them with `docker images`.

Now, we enter our environment using `conda activate evaluate_assemblies` and them we execute the test dataset with `snakemake -s Snakefile_evaluate --cores <number of cores>` where `<number of cores>` must be replaced by a number informing the quantity of cores required by the user.
