# Pipeline for General Evaluation of Assemblies

This repo contains the snakemake pipeline to evaluate _de novo_ assemblies using short-reads. As input, the pipeline takes a one or more assemblies in `fasta` format and a paired-end short reads in `fastq` format and run 3 tools that estimate assembly metrics. The pipeline is useful when we wish to estimate which assembly is best among a set of genome assemblies produced by different assemblers tools. The executed tools are:

- [REAPR](https://www.sanger.ac.uk/science/tools/reapr)
- [ALE](https://github.com/sc932/ALE)
- [BUSCO](https://busco.ezlab.org/)

## Quick Usage

First of all, make sure that you have [docker](https://docs.docker.com/install/) and [conda](https://docs.conda.io/en/latest/miniconda.html) (or miniconda) installed on your machine. These softwares will be essential to assist in the installation of the tools that are going to be executed in each pipeline.

For each pipeline we have a particular conda environment and a docker image that must be installed. To clarify, let's execute the pipeline that evaluates a genome assembly given a short read illumina paired-end file. After cloning the corresponding repo, we begin the installation of the pipeline's specific environment and docker image.

To do this, we enter the folder corresponding to the pipeline (`cd evaluate_assemblies`) and create a new conda environment corresponding to our pipeline with the following command:

```
conda env create -f envs/myenv.yaml
```

This will create a conda environment called `evaluate_assemblies_env`. We can check that the environement was created through `conda info --envs`.

After this, we go to the folder `build_docker_img` and type `docker build -t rodtheo/genomics:eval_assem_ale_reapr .`. This will create an image with the remainer tools required for the execution of pipeline that could not be installed by conda. Again, we can check if the image was created listing them with `docker images`.

Now, we enter our environment using `conda activate evaluate_assemblies_env` and them we execute the test dataset with `snakemake -s Snakefile_evaluate --cores <number of cores>` where `<number of cores>` must be replaced by a number informing the quantity of cores required by the user.

## Output files

The output files are written in `evaluate_assembly` folder that have one folder for each sample, one `benchmark` and one `logs` folders. In the case of the test dataset, the pipeline create the following folders:

- `evaluate_assembly/Sample1`
- `evaluate_assembly/Sample2`
- `evaluate_assembly/benchmark`
- `evaluate_assembly/logs`

Where `Sample1` and `Sample2` have the same output files. For instance, the most important files in `Sample1` analysis are `ALEoutput.txt`, `reapr_results/05.summary.report.txt` and `run_Sample1/short_summary_Sample1.txt`.


## Running the Pipeline with your data

1. Specifying your data

- Edit **config.yaml**. An example of configuration file have is show to keep clear the structure and variables in the file.

```{yaml}
workdir: "."
samples: samples.tsv
fq1: fastq/reads_shortinsert_1.fastq
fq2: fastq/reads_shortinsert_2.fastq
threads: 8
lineage: dataset/example/
species_augustus: aspergillus_terreus
```

The most important variables are `samples`, `fq1`, `fq2`, `lineage` and `species_augustus`. The variable `samples` must store the path of your assemblies. In the test dataset, the file called `samples.tsv` have two columns separate by a tab. The two columns represent the assembly name (`sample` column) and path to assembly in fasta format (`assembly` column). In the next snippet we can see an example where we have two assemblies performed by tool 1 located in datasets/assembly.fa (path relative to workdir folder) and tool 2 located in datasets/assembly_2.fa. The goal is to evaluate which assembly is better without using reference assembly information.

```
sample	assembly
Assembly_tool_1	datasets/assembly.fa
Assembly_tool_2	datasets/assembly_2.fa
```

So you can declare how many assemblies you want in `samples.tsv` file.

The `lineage` variable stores the path to busco dataset. You must download a dataset ideal to your species being assembled searching in [busco site](https://busco.ezlab.org/) and specify the relative path in this variable. The last variable is `species_augustus` and, again, must be consistent with your data being assembled. You can check the available agusutus species in [this site](http://augustus.gobics.de/binaries/README.TXT).
