import pandas as pd
import shlex
import subprocess
from pathlib import Path
from Bio import SeqIO
import re
from os import path
import jinja2
from collections import OrderedDict
import numpy as np


configfile: "config.yaml"

samples = pd.read_table(config["samples"]).set_index("sample", drop=False)

def get_genome(wildcards):
	return samples.loc[wildcards.sample, "assembly"]

def get_genome_prefix(wildcards):
	gen = samples.loc[wildcards.sample, "assembly"]
	return ''.join(gen.split('.')[:-1])

def get_all_genomes(wildcards):
  return ' '.join(samples["assembly"].values)

def get_all_names(wildcards):
  return ','.join(samples["sample"].values)

def parse_busco(out_short_summary):
    dict_busco = {}
    with open(out_short_summary, 'r') as infbusco:
        for idxline, line in enumerate(infbusco.readlines()):
            # line = line.strip("\n")
            if line.startswith("#"):
                match_db_obj = re.match(r'.+\(.+number of species\:\s(\d+),\snumber of BUSCOs\:\s(\d+)\)', line)
                if match_db_obj:
                    print(match_db_obj.group(1), match_db_obj.group(2))
            else:
                match_summary_obj = re.match(r'\s+C\:(\d+.\d+)\%\[S\:(\d+.\d)\%,D\:(\d+.\d+)\%\],F\:(\d+.\d+)\%,M:(\d+.\d+)%,n:\d+', line)
                if match_summary_obj:
                    dict_busco['pctcomplete'] = match_summary_obj.group(1)
                    dict_busco['pctsingle'] = match_summary_obj.group(2)
                    dict_busco['pctduplicated'] = match_summary_obj.group(3)
                    dict_busco['pctfragmented'] = match_summary_obj.group(4)
                    dict_busco['pctmissing'] = match_summary_obj.group(5)
                    print(idxline)
                elif idxline == 9:
                    match_n = re.match(r'\s+(\d+)\s+.+', line)
                    n = match_n.group(1)
                    dict_busco['ncomplete'] = n
                elif idxline == 10:
                    match_n = re.match(r'\s+(\d+)\s+.+', line)
                    n = match_n.group(1)
                    dict_busco['nsingle'] = n
                elif idxline == 11:
                    match_n = re.match(r'\s+(\d+)\s+.+', line)
                    n = match_n.group(1)
                    dict_busco['nduplicated'] = n
                elif idxline == 12:
                    match_n = re.match(r'\s+(\d+)\s+.+', line)
                    n = match_n.group(1)
                    dict_busco['nfragmented'] = n
                elif idxline == 13:
                    match_n = re.match(r'\s+(\d+)\s+.+', line)
                    n = match_n.group(1)
                    dict_busco['nmissing'] = n
    return(dict_busco)


rule all:
	input:
		expand('evaluate_assembly/{sample}/ALEScore_{sample}.finished', sample=samples['sample']),
		expand('evaluate_assembly/{sample}/REAPR_{sample}.finished', sample=samples['sample']),
		expand('evaluate_assembly/{sample}/busco/BUSCO_{sample}.finished', sample=samples['sample']),'evaluate_assembly/quast_results/QUAST.OK','evaluate_assembly/results.html'

rule check_header_fasta:
	input:
		genome=get_genome
	output:
		'evaluate_assembly/{sample}/FACHECK_ok.txt'
	run:
		bad_header = False
		print("HEADER")
		with open(input.genome, "r") as ingenome:
			for record in SeqIO.parse(ingenome, "fasta"):
				print(record.description)
				# if len(str(record.id).split(" ")) > 1:
				if re.search(r"\s", str(record.description)):
					print("BAD HEADER")
					bad_header = True
		if bad_header:
			print('\033[94m The header of assembly {} is not compatible with REAPR.\nPlease, execute reapr facheck and modify the file assemblies.tsv to point to assembly with corrected header! \033[0m \n\n\n To this y using command line: \033[96m reapr facheck <in.fa> [out_prefix] \033[0m'.format(input.genome))
			sequences = []
			with open(input.genome, "r") as ingenome:
				for record in SeqIO.parse(ingenome, "fasta"):
					header = str(record.description)
					record.id = "_".join(header.split(" "))
					record.description=""
					print(record.id)
					sequences.append(record)
			source = Path(input.genome)
			destination = Path(input.genome+".bkp")
			with destination.open(mode="xb") as fid:
				fid.write(source.read_bytes())
			with open(str(source), "w") as outgenome:
				SeqIO.write(sequences, outgenome, "fasta")
			shell('touch {output}')
		else:
			shell('touch {output}')


rule build_index_bowtie2:
	input:
		fasta=get_genome,
		fasta_ok='evaluate_assembly/{sample}/FACHECK_ok.txt'
	output:
		'evaluate_assembly/{sample}/{sample}.index_built'
	params:
		prefix=get_genome_prefix
	conda:
		"envs/myenv.yaml"
	shell:
		"bowtie2-build {input.fasta} {params.prefix} && touch {output}"

rule bowtie2:
	input:
		sample=[ config["fq1"], config["fq2"] ],
		index_bowtie2='evaluate_assembly/{sample}/{sample}.index_built'
	output:
		'evaluate_assembly/{sample}/{sample}.bam'
	log:
		'evaluate_assembly/logs/{sample}_bowtie2.log'
	params:
		index = get_genome_prefix,
		extra = "--end-to-end --very-sensitive"
	threads: config["threads"]
	conda:
		"envs/myenv.yaml"
	wrapper:
		"0.31.1/bio/bowtie2/align"

rule samtools_sort:
	input:
		'evaluate_assembly/{sample}/{sample}.bam'
	output:
		'evaluate_assembly/{sample}/{sample}.sorted.bam'
	params:
		"-m 4G"
	threads: config["threads"]
	conda:
		"envs/myenv.yaml"
	wrapper:
		"0.31.1/bio/samtools/sort"

rule samtools_index:
	input:
		'evaluate_assembly/{sample}/{sample}.sorted.bam'
	output:
		'evaluate_assembly/{sample}/{sample}.bam.bai'
	conda:
		"envs/myenv.yaml"
	wrapper:
		"0.31.1/bio/samtools/index"


rule evaluate_assembly_ALE:
        input:
                genome = get_genome, r = 'evaluate_assembly/{sample}/{sample}.sorted.bam'
        benchmark: "evaluate_assembly/benchmark/{sample}_ALE.log"
        output: "evaluate_assembly/{sample}/ALEScore_{sample}.finished"
        shell: "docker run -v `pwd`:/dir --rm rodtheo/genomics:eval_assem_ale_reapr ALE --nout --metagenome /dir/{input.r} /dir/{input.genome} /dir/evaluate_assembly/{wildcards.sample}/ALEoutput.txt && touch {output}"

rule evaluate_assembly_REAPR:
	input:
		genome = get_genome,
		r = 'evaluate_assembly/{sample}/{sample}.sorted.bam',
		bai = 'evaluate_assembly/{sample}/{sample}.bam.bai'
	benchmark:
		'evaluate_assembly/benchmark/{sample}_REAPR.log'
	output:
		'evaluate_assembly/{sample}/REAPR_{sample}.finished'
	params:
		prefix=get_genome_prefix
	shell:
		"docker run -v `pwd`:/dir --rm rodtheo/genomics:eval_assem_ale_reapr reapr pipeline /dir/{input.genome} /dir/{input.r} /dir/evaluate_assembly/{wildcards.sample}/reapr_results && touch {output}"
#		genome_fachecked = '{}_fachecked'.format(params.prefix)
#		facheck = subprocess.call(["reapr", "facheck", "{}".format(input.genome)],  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
#		print(facheck)
#		if facheck == 1:
#			genome_fachecked = '{}_fachecked'.format(params.prefix)
#			facheck = subprocess.check_output(["reapr", "facheck", "{}".format(input.genome), "{}".format(genome_fachecked)], shell=False,stderr=subprocess.STDOUT)
#			print("Repairing fasta header with facheck")
#			shell("reapr pipeline {genome_fachecked}.fa {input.r} evaluate_assembly/{wildcards.sample}/reapr_results && touch {output}")
#		else:
#			shell("reapr pipeline {input.genome} {input.r} evaluate_assembly/{wildcards.sample}/reapr_results && touch {output}")

		#'reapr pipeline {input.genome} {input.r} evaluate_assembly/{wildcards.sample}/reapr_results && touch {output}'

rule busco:
	input:
		genome = get_genome,
		lineage = config["lineage"]
	output:
		'evaluate_assembly/{sample}/busco/BUSCO_{sample}.finished'
	benchmark: "evaluate_assembly/benchmark/{sample}_BUSCO.log"
        params: species=config["species_augustus"]
        threads: config["threads"]
	conda: "envs/myenv.yaml"
        shell: 'run_BUSCO.py -i {input.genome} -o {wildcards.sample} -l {input.lineage} --cpu 10 --species {params.species} --mode genome && mv run_{wildcards.sample} evaluate_assembly/{wildcards.sample}/ && touch {output}'

rule quast:
	params:
		genomes = get_all_genomes,
		names = get_all_names
	threads: config['threads']
	benchmark: 'evaluate_assembly/benchmark/QUAST.log'
	output:
		'evaluate_assembly/quast_results/QUAST.OK'
	shell:
		'quast.py --labels "{params.names}" -e --threads {threads} -o evaluate_assembly/quast_results/ {params.genomes} && touch {output}'


rule generate_table_results:
	params:
		genomes_names = get_all_names
	input:
		ale_res=expand('evaluate_assembly/{sample}/ALEScore_{sample}.finished',sample=samples['sample']),
		reapr_res=expand('evaluate_assembly/{sample}/REAPR_{sample}.finished',sample=samples['sample']),
		busco_res=expand('evaluate_assembly/{sample}/busco/BUSCO_{sample}.finished', sample=samples['sample']),
		quast_res='evaluate_assembly/quast_results/QUAST.OK'
	output: "evaluate_assembly/results.html"
	run:
		items = []
		items_classes = []
		for pseudo_samp in (params.genomes_names).split(","):
			samp = pseudo_samp.split("/")[-1]
			dict_sample = OrderedDict()
			dict_classes = OrderedDict()
			dict_sample['name'] = samp
			print(pseudo_samp, samp)
			busco_summary_file = "evaluate_assembly/{}/run_{}/short_summary_{}.txt".format(pseudo_samp, samp, samp)
			if path.exists(busco_summary_file):
				dict_samp = OrderedDict(parse_busco(busco_summary_file))
			else:
				dict_samp['ncomplete'] = 'X'
				dict_samp['pctcomplete'] = 'X'
				dict_samp['nduplicated'] = 'X'
				dict_samp['pctduplicated'] = 'X'
				dict_samp['nfragmented'] = 'X'
				dict_samp['pctfragmented'] = 'X'
			genome_path = samples.loc[samp, "assembly"]
			genome_name  = genome_path.split('/')[-1]
			ale_file = "evaluate_assembly/{}/ALEoutput.txt".format(pseudo_samp, genome_name)
			print(ale_file)
			if path.exists(ale_file):
				with open(ale_file, 'r') as inale:
					nline = 0
					for line in inale.readlines():
						if nline == 0:
							line_list = line.split(" ")
							dict_sample['ale'] = line_list[-1].strip('\n')
			print(dict_sample)
			reapr_file = "evaluate_assembly/{}/reapr_results/05.summary.report.txt".format(pseudo_samp)
			if path.exists(reapr_file):
				with open(reapr_file, 'r') as inreapr:
					for line in inreapr.readlines():
						if line.endswith('errors:\n'):
							line_list = line.split(" ")
							dict_sample['reapr'] = line_list[0]
			# parsing quast results
			df_quast = pd.read_table('evaluate_assembly/quast_results/report.tsv', sep='\t')
			array_sample = df_quast[samp].values
			dict_sample['genomesize'] = '{:,}'.format(int(array_sample[6]))
			dict_sample['contigs']    = '{:,}'.format(int(array_sample[12]))
			dict_sample['n50']        = '{:,}'.format(int(array_sample[16]))
			dict_sample['largest']    = '{:,}'.format(int(array_sample[13]))
			# concatenating results
			# dict_sample['genomesize_class'] = "tg-lboi"
			dict_appended = {**dict_sample, **dict_samp}
			for k, v in dict_appended.items():
				key_class = '{}_class'.format(k)
				dict_classes[key_class] = "tg-lboi"
			items.append(dict_appended)
			items_classes.append(dict_classes)
		print(items)
		print("YES")
		myList = [list(col) for col in zip(*[d.values() for d in items])]
		myList_argmax = np.argmax(myList, axis=1)
		print("argmax",myList_argmax)

		for idx, arg in enumerate(myList_argmax):
			key_checked = list(dict_appended.keys())[idx]
			key_class = "{}_class".format(key_checked)
			items_classes[arg][key_class] = "mark"
			#print("K",items[arg][key_checked])
		res_items = []
		for t in list(zip(items, items_classes)):
			nd = {**t[0], **t[1]}
			res_items.append(nd)

		loader = jinja2.FileSystemLoader('template.html')
		env = jinja2.Environment(loader=loader)
		template = env.get_template('')
		output_jinja2 = template.render(items=res_items)
		print(output_jinja2)
		with open(output[0], 'w') as outfile:
			outfile.write(output_jinja2)
		# c = dict([(k,[a[k],b[k]]) for k in items])
		c = pd.DataFrame(items)
		c.to_excel("evaluate_assembly/results.xlsx")
