import subprocess,shutil,os,glob

shutil.rmtree("tmp")
shutil.rmtree("punters_test")


FILE='EE40098 (CI)-Test submissions (optional for feedback)-426656.zip'
DOWNLOAD='/home/eespjl/Downloads/'+FILE
#DOWNLOAD='/Users/pjl/Downloads/'+FILE

try:
    os.makedirs('./tmp')
except OSError:
    pass

try:
    os.makedirs('./punters_test')
except OSError:
    pass

os.chdir('tmp')


ls_output = subprocess.check_output(['/usr/bin/unzip', DOWNLOAD])

ls_output = subprocess.check_output(['/bin/rm', DOWNLOAD])


files=glob.glob('*.zip')

os.chdir('../punters_test')

for file in files:
    ls_output = subprocess.check_output(['/usr/bin/unzip','-o','../tmp/'+file])
    


for f in glob.glob('*'):
    if os.path.isdir(f):
        subprocess.check_output(['/usr/bin/touch',f+'/__init__.py'])
        continue
    os.remove(f)

subprocess.check_output(['/usr/bin/touch','__init__.py'])
