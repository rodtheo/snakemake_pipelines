# snakemake_pipelines

Collection of often used pipelines based on snakemake.

## Evaluating Assemblies

Overview of the REAPR algorithm

Two metrics to pinpoint errors:

- Small Local Errors: mapped bases differ from observed in assembled sequence.
- Structural Errors: when the insert/fragment size deviates from expected.

Flag as mis-assembly a region that has no fragment depth or has fragment distribution around a base that causes an FCD error. FCD error at each base of and assembly is defined as the area between the observed and ideal fragment coverage distributions normalized by mean insert size and fragment depth. So, if a base has zero coverage we cannot calculate this metric and the assumption is that this base is an assembly error. If a base is covered by at least 5 uniquely mapped reads and the FCD error <= FCD cutoff it receives a score of 1. In cases where the base fail in some tests it receives a score between 0 and 1 reling on how many tests this base fails. Note that 0 is the worst score.

Outputs:

|   | File                      | Description                                                                      |
|---|---------------------------|----------------------------------------------------------------------------------|
| * | 05.summary.stats.tsv      | Summary spreadsheet produced containing error counts and metrics for each contig |
| * | 05.summary.report.txt/tsv | Summary reporting N50's and error counts and types for whole assembly            |
|   | 04.break.broken_assembly  | REAPR generated new assembly after breaking in errors located in gaps            |
|   | 01.stats.FCDerror.*       | Per base "time series" for each metric (fragment_coverage, FCDerror, ...)        |
|   | 02.fcdrate.*              | File showing which fcd cutoff was selected                                       |
|   | 03.score.errors.*         | The scores for each base or for a region in GFF format                           |

- Fragment Coverage Distribution (FCD): plot of the fragment size (distance between the outermost ends of a proper read pair) depth.


In `evaluate_assembly` folder we put a pipeline that runs the evaluation assembly tools [REAPR](https://doi.org/10.1186/gb-2013-14-5-r47) (Recognition of Errors in Assemblies using Paired Reads) and [ALE](). To run please edit the following files in the pointed line:

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
