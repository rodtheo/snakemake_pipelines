import os
import subprocess
from pathlib import Path

#aug_path = os.system("which augustus")
aug_path = str(subprocess.Popen("which augustus", shell=True, stdout=subprocess.PIPE).stdout.read())
#aug_path = subprocess.check_output(["which", "augustus"])
#path_aug = Path(aug_path)
print(str(aug_path))
path_aug = Path('/'+'/'.join(aug_path.split("/")[1:-2]))

print("Setting augustus config path environment variable")
os.environ['AUGUSTUS_CONFIG_PATH'] = str(path_aug/"config/")

print("Setting busco config.ini script")

config_def = Path("config.ini.default")
config_p  = config_def.parent/"config.ini"

config_p.write_text(config_def.read_text())

with open(config_p, "+a") as conf_file:
    conf_file.write("[gff2gbSmallDNA.pl]\n")
    conf_file.write("path = {}/scripts/\n".format(str(path_aug)))

    conf_file.write("[new_species.pl]\n")
    conf_file.write("path = {}/scripts/\n".format(str(path_aug)))

    conf_file.write("[optimize_augustus.pl]\n")
    conf_file.write("path = {}/scripts/\n".format(str(path_aug)))





print(path_aug)
#export AUGUSTUS_CONFIG_PATH="/home/rodtheo/miniconda2/envs/evaluate_assemblies_env/config/"
