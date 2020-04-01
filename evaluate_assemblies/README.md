# Pipeline for General Evaluation of Assemblies

This repo contains the snakemake pipeline to evaluate _de novo_ assemblies using short-reads. As input, the pipeline takes a one or more assemblies in `fasta` format and a paired-end short reads in `fastq` format and run 3 tools that estimate assembly metrics. The pipeline is useful when we wish to estimate which assembly is best among a set of genome assemblies produced by different assembler tools. The executed tools are:

- [REAPR](https://www.sanger.ac.uk/science/tools/reapr)
- [ALE](https://github.com/sc932/ALE)
- [BUSCO](https://busco.ezlab.org/)

## Quick Usage

First of all, make sure that you have [docker](https://docs.docker.com/install/) and [conda](https://docs.conda.io/en/latest/miniconda.html) (or miniconda) installed on your machine. These softwares will be essential to assist in the installation of the tools that are going to be executed in each pipeline.

For each pipeline we have a particular conda environment and a docker image that must be installed. To clarify, let's execute the pipeline that evaluates a genome assembly given a short read illumina paired-end file. After cloning the corresponding repo, we begin the installation of the pipeline's specific environment and docker image.

To do this, we enter the folder corresponding to the pipeline (`cd evaluate_assemblies`) and create a new conda environment corresponding to our pipeline with the following command:

```
conda env create -f envs/evaluate_env.yaml.yaml
```

This will create a conda environment called `evaluate_assemblies_env`. We can check that the conda environment was created through `conda info --envs`.

After this, we go to the folder `build_docker_img` and type `docker build -t rodtheo/genomics:eval_assem_ale_reapr .`. This will create an image with the remainer tools required for the execution of pipeline that could not be installed by conda. Again, we can check if the image was created listing all images with `docker images` command.

Now, we activate the environment using `conda activate evaluate_assemblies_env` and execute the test dataset with `snakemake -s Snakefile_evaluate --cores <number of cores>` where `<number of cores>` must be replaced by a number informing the quantity of cores required by the user.

## Very Quick Usage

```
# installing the required tools and environment
conda env create -f envs/evaluate_env.yaml.yaml
cd build_docker_img && docker build -t rodtheo/genomics:eval_assem_ale_reapr .
# entering the installed environment
conda activate evaluate_assemblies_env
# executing the pipeline with the test dataset
snakemake -s Snakefile_evaluate --configfile config.yaml
```

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
threads: 4
lineage: dataset/busco_fungi_datasets/fungi_odb9
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

## Evaluating the performance of the pipeline using Real Data

Using a computer with 4 cores 
36m25s

# Output

<table class="tg">
    <thead>
  <tr>
    <th class="tg-lboi" rowspan="2">Assembly</th>
    <th class="tg-lboi" rowspan="2">Length</th>
    <th class="tg-lboi" rowspan="2">Number of contigs</th>
    <th class="tg-lboi" rowspan="2">Largest contig (bp)</th>
    <th class="tg-lboi" rowspan="2">Contig N50</th>
    <th class="tg-lboi" colspan="2">Complete genes</th>
    <th class="tg-lboi" colspan="2">Duplicated genes</th>
    <th class="tg-0pky" colspan="2">Fragmented genes</th>
    <th class="tg-0pky" colspan="2">Missing genes</th>
    <th class="tg-0pky" rowspan="2">ALE score (log)</th>
    <th class="tg-0pky" rowspan="2">REAPR errors</th>
  </tr>
  <tr>
    <th class="tg-lboi">Number</th>
    <th class="tg-lboi">Pct</th>
    <th class="tg-lboi">Number</th>
    <th class="tg-0pky">Pct</th>
    <th class="tg-0pky">Number</th>
    <th class="tg-0pky">Pct</th>
    <th class="tg-0pky">Number</th>
    <th class="tg-0pky">Pct</th>
  </tr>
  </thead>
  
  <tr>
    <td class="tg-lboi">flye</td>
    <td class="tg-lboi">5136373</td>
    <td class="tg-lboi">35</td>
    <td class="tg-lboi">611735</td>
    <td class="tg-lboi">230412</td>
    <td class="tg-lboi">27</td>
    <td class="tg-lboi">18.3%</td>
    <td class="tg-lboi">1</td>
    <td class="tg-lboi">0.7%</td>
    <td class="tg-lboi">46</td>
    <td class="tg-lboi">31.1%</td>
    <td class="tg-lboi">75</td>
    <td class="tg-lboi">50.6%</td>
    <td class="tg-lboi">-53188249.653201</td>
    <td class="">5625</td>
  </tr>
  
  <tr>
    <td class="tg-lboi">flye_polished</td>
    <td class="tg-lboi">5109442</td>
    <td class="tg-lboi">35</td>
    <td class="tg-lboi">601312</td>
    <td class="tg-lboi">229584</td>
    <td class="tg-lboi">143</td>
    <td class="tg-lboi">96.6%</td>
    <td class="tg-lboi">0</td>
    <td class="tg-lboi">0.0%</td>
    <td class="tg-lboi">2</td>
    <td class="tg-lboi">1.4%</td>
    <td class="tg-lboi">3</td>
    <td class="tg-lboi">2.0%</td>
    <td class="tg-lboi">-36497168.441962</td>
    <td class="">5266</td>
  </tr>
  
  <tr>
    <td class="tg-lboi">spades_hybrid</td>
    <td class="tg-lboi">5721015</td>
    <td class="tg-lboi">84</td>
    <td class="tg-lboi">622000</td>
    <td class="tg-lboi">342546</td>
    <td class="tg-lboi">146</td>
    <td class="tg-lboi">98.6%</td>
    <td class="tg-lboi">0</td>
    <td class="tg-lboi">0.0%</td>
    <td class="tg-lboi">0</td>
    <td class="tg-lboi">0.0%</td>
    <td class="tg-lboi">2</td>
    <td class="tg-lboi">1.4%</td>
    <td class="tg-lboi">-14769025.222694</td>
    <td class="">6523</td>
  </tr>
  
  <tr>
    <td class="tg-lboi">unicycler_illumina_only</td>
    <td class="tg-lboi">5637716</td>
    <td class="tg-lboi">113</td>
    <td class="tg-lboi">323469</td>
    <td class="tg-lboi">150995</td>
    <td class="tg-lboi">146</td>
    <td class="tg-lboi">98.6%</td>
    <td class="tg-lboi">0</td>
    <td class="tg-lboi">0.0%</td>
    <td class="tg-lboi">0</td>
    <td class="tg-lboi">0.0%</td>
    <td class="tg-lboi">2</td>
    <td class="tg-lboi">1.4%</td>
    <td class="tg-lboi">-15743347.597692</td>
    <td class="">6296</td>
  </tr>
  
  <tr>
    <td class="tg-lboi">canu</td>
    <td class="tg-lboi">4639709</td>
    <td class="tg-lboi">65</td>
    <td class="tg-lboi">451020</td>
    <td class="tg-lboi">103098</td>
    <td class="tg-lboi">26</td>
    <td class="tg-lboi">17.6%</td>
    <td class="tg-lboi">0</td>
    <td class="tg-lboi">0.0%</td>
    <td class="tg-lboi">49</td>
    <td class="tg-lboi">33.1%</td>
    <td class="tg-lboi">73</td>
    <td class="tg-lboi">49.3%</td>
    <td class="tg-lboi">-55660817.201297</td>
    <td class="">4991</td>
  </tr>
  
  <tr>
    <td class="tg-lboi">unicycler_hybrid</td>
    <td class="tg-lboi">5695678</td>
    <td class="tg-lboi">72</td>
    <td class="tg-lboi">654987</td>
    <td class="tg-lboi">364058</td>
    <td class="tg-lboi">146</td>
    <td class="tg-lboi">98.6%</td>
    <td class="tg-lboi">0</td>
    <td class="tg-lboi">0.0%</td>
    <td class="tg-lboi">0</td>
    <td class="tg-lboi">0.0%</td>
    <td class="tg-lboi">2</td>
    <td class="tg-lboi">1.4%</td>
    <td class="tg-lboi">-15411554.523661</td>
    <td class="">6469</td>
  </tr>
  
  <tr>
    <td class="tg-lboi">unicycler_long_only</td>
    <td class="tg-lboi">1648245</td>
    <td class="tg-lboi">38</td>
    <td class="tg-lboi">91409</td>
    <td class="tg-lboi">49495</td>
    <td class="tg-lboi">23</td>
    <td class="tg-lboi">15.5%</td>
    <td class="tg-lboi">0</td>
    <td class="tg-lboi">0.0%</td>
    <td class="tg-lboi">16</td>
    <td class="tg-lboi">10.8%</td>
    <td class="tg-lboi">109</td>
    <td class="tg-lboi">73.7%</td>
    <td class="tg-lboi">-85829499.260974</td>
    <td class="">1704</td>
  </tr>
  
  <tr>
    <td class="tg-lboi">canu_polish</td>
    <td class="tg-lboi">4640833</td>
    <td class="tg-lboi">65</td>
    <td class="tg-lboi">452765</td>
    <td class="tg-lboi">102018</td>
    <td class="tg-lboi">128</td>
    <td class="tg-lboi">86.5%</td>
    <td class="tg-lboi">0</td>
    <td class="tg-lboi">0.0%</td>
    <td class="tg-lboi">0</td>
    <td class="tg-lboi">0.0%</td>
    <td class="tg-lboi">20</td>
    <td class="tg-lboi">13.5%</td>
    <td class="tg-lboi">-42542598.210604</td>
    <td class="">4723</td>
  </tr>
  
  <tr>
    <td class="tg-lboi">spades_illumina_only</td>
    <td class="tg-lboi">5688198</td>
    <td class="tg-lboi">121</td>
    <td class="tg-lboi">312426</td>
    <td class="tg-lboi">164348</td>
    <td class="tg-lboi">146</td>
    <td class="tg-lboi">98.6%</td>
    <td class="tg-lboi">0</td>
    <td class="tg-lboi">0.0%</td>
    <td class="tg-lboi">0</td>
    <td class="tg-lboi">0.0%</td>
    <td class="tg-lboi">2</td>
    <td class="tg-lboi">1.4%</td>
    <td class="tg-lboi">-15236766.76177</td>
    <td class="">6386</td>
  </tr>
  
  <tr>
    <td class="tg-lboi">unicycler_polish</td>
    <td class="tg-lboi">1641339</td>
    <td class="tg-lboi">38</td>
    <td class="tg-lboi">91567</td>
    <td class="tg-lboi">49548</td>
    <td class="tg-lboi">62</td>
    <td class="tg-lboi">41.9%</td>
    <td class="tg-lboi">0</td>
    <td class="tg-lboi">0.0%</td>
    <td class="tg-lboi">4</td>
    <td class="tg-lboi">2.7%</td>
    <td class="tg-lboi">82</td>
    <td class="tg-lboi">55.4%</td>
    <td class="tg-lboi">-81251206.905238</td>
    <td class="">1631</td>
  </tr>
  
</table>
