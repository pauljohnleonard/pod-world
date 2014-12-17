import subprocess,shutil,os,glob

DEST="punters_unseen"

shutil.rmtree("tmp")

PWD=os.getcwd()
FILE='CHALLENGE.zip'
DOWNLOAD=PWD+'/submissions/'+FILE

try:
    os.makedirs('./tmp')
except OSError:
    pass

os.chdir('tmp')


ls_output = subprocess.check_output(['/usr/bin/unzip', DOWNLOAD])

# ls_output = subprocess.check_output(['/bin/rm', DOWNLOAD])


files=glob.glob('*.zip')

os.chdir(PWD+"/"+DEST)

for file in files:
    ls_output = subprocess.check_output(['/usr/bin/unzip','-o','../tmp/'+file])
    


for f in glob.glob('*'):
    if os.path.isdir(f):
        subprocess.check_output(['/usr/bin/touch',f+'/__init__.py'])
        continue
    os.remove(f)

subprocess.check_output(['/usr/bin/touch','__init__.py'])
