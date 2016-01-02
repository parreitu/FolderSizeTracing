from django.core.management.base import BaseCommand, CommandError
from FolderSizeTracing.models import Folder, Historical
import subprocess
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        # TMP_CHECK_PATH = "/media/H-Fitxategiak/taldeak/TI"
        TMP_CHECK_PATH = "/home/parreitu/Mahaigaina"
        
        modifications_max_days = 30  # Ficheros modificados en el ultimo mes
        files_withouth_access_max_days = 180  # Ficheros no accedidos en los ultimos 6 meses
        
        all_folders = Folder.objects.all()
        now = datetime.datetime.now()
        for my_folder in all_folders:
            self.stdout.write(my_folder.name) 
            TMP_CHECK_PATH = my_folder.path

            p = subprocess.Popen(["du", "-s", TMP_CHECK_PATH], stdout=subprocess.PIPE)
            output, err = p.communicate()       

            for line in output.splitlines():
                pass

            my_folder_size_mb = int(line.split()[0]) / 1024

            self.stdout.write("Real Size:" + str(my_folder_size_mb))

            # HAU ALDATU BEHAR DA PRODUKZIOAN JARTZEKO. HIRU LERRO HAUEK DESKOMENTATU
            # p = subprocess.Popen(["find", TMP_CHECK_PATH, "-type", "f", "-mtime", "-" + str(modifications_max_days), "-exec", "du", "-c", "{}", "+"], stdout=subprocess.PIPE)
            # output, err = p.communicate()       
            # my_folder_files_changed = output
            # HAU ALDATU BEHAR DA PRODUKZIOAN JARTZEKO. LERRO HAU KENDU
            my_folder_files_changed = ""

            for line in output.splitlines():
                pass

            # self.stdout.write("That is the last line: " + line)
            my_size_mb = int(line.split()[0]) / 1024
            self.stdout.write("Size: " + str(my_size_mb))
            
            p = subprocess.Popen(["find", TMP_CHECK_PATH, "-type", "f", "-atime", "+" + str(files_withouth_access_max_days), "-exec", "du", "-c", "{}", "+"], stdout=subprocess.PIPE)
            output, err = p.communicate()       
            my_folder_files_not_accessed = output
            
            for line in output.splitlines():
                pass

            # self.stdout.write("That is the last line: " + line)
            not_accessed_mb = int(line.split()[0]) / 1024
            self.stdout.write("not_accessed_mb: " + str(not_accessed_mb))
            
            try:
                last_record = Historical.objects.filter(folder=my_folder).latest('id')
                self.stdout.write("Last record ID: " + str(last_record.id))
                previous_mb_count = last_record.size_mb
                self.stdout.write("Last record MB Count: " + str(previous_mb_count))
            except ObjectDoesNotExist:
                previous_mb_count = 0
                pass
            my_folder_delta_mb = my_folder_size_mb - previous_mb_count

            new_historical = Historical(folder=my_folder, size_mb=my_folder_size_mb, timestamp=timezone.now(),
                                        files_changed=my_folder_files_changed, delta_mb=my_folder_delta_mb,
                                        files_not_accessed=my_folder_files_not_accessed, not_accessed_mb=not_accessed_mb,
                                        big_files_changed="", big_files_delta_mb=0, big_files_size_mb=0
                                        )  
            new_historical.save()                                     
        
        # Fitxategi handiak: Zein fitxategi handi sortu diren azken egunean, eta nork sortu dituen.
        # print (output)
        
