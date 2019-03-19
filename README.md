# snakemake_pipelines

Collection of often used pipelines based on snakemake.

## Evaluate Assembly

In `evaluate_assembly` folder we put a pipeline that runs the evaluation assembly tools REAPR and ALE. To run please edit the following files in the pointed line:

- Snakefile_evaluate: set the path of your configuration file `config.yaml` in configfile variable. An example of configuration file have is show to keep clear the structure and variables in the file.

```{yaml}
workdir: "."
samples: samples.tsv
fq1: fastq/reads_shortinsert_1.fastq
fq2: fastq/reads_shortinsert_2.fastq
threads: 1
```

The most important variables are `samples`, `fq1` and `fq2`. The variable `samples` must store the path of your table of query assemblies. In the example, before running the pipeline we create an file called `samples.tsv` that have two columns separate by a tab. The two columns represent the assembly name (`sample` column) and path to assembly in fasta format (`assembly` column). In the next snippet we can see an example where we have two assemblies performed by tool 1 located in datasets/assembly.fa (path relative to workdir folder) and tool 2 located in datasets/assembly_2.fa. The goal is to evaluate which assembly is better without using reference assembly information.

```
sample	assembly
Assembly_tool_1	datasets/assembly.fa
Assembly_tool_2	datasets/assembly_2.fa
```

So you can declare how many assemblies you want in `samples.tsv` file. After wrote all modifications and edit the table of samples we can run the pipeline through the command:

```
snakemake -s Snakefile_evaluate
```

Sometimes when running this pipeline you woulds encounter and RuleException error.. meaning that you have to fix the fasta header of assembly_2.fa before using it as input to REAPR. The tool REAPR comes with an module to fix the header and save another fasta. So, before running the pipeline please fix the header file with `reapr facheck <in.fa> [out_prefix]`. 

The pipeline has some dependencies and 
