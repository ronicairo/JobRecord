import os
import sys
import django
from pathlib import Path
from django.db.models import Avg, Count

# Récupère le chemin absolu du dossier contenant manage.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ajoute ce chemin au sys.path pour que jobsite soit importable
sys.path.append(BASE_DIR)

# Spécifie le fichier de configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JobRecord.settings')

# Initialise Django
django.setup()

from jobsite.models import JobRecord

output = []

# 1. Top 5 des jobs les mieux payés
top_jobs = (
    JobRecord.objects
    .values('job_title')
    .annotate(avg_salary=Avg('salary_in_usd'))
    .order_by('-avg_salary')[:5]
)
output.append("Top 5 Job Titles les mieux payés :")
for job in top_jobs:
    output.append(f"{job['job_title']}: {job['avg_salary']:.2f} USD")

# 2. Salaire moyen par niveau d'expérience
salaire_par_experience = (
    JobRecord.objects
    .values('experience_level')
    .annotate(avg_salary=Avg('salary_in_usd'))
)
output.append("\nSalaire moyen par niveau d'expérience :")
for row in salaire_par_experience:
    output.append(f"{row['experience_level']}: {row['avg_salary']:.2f} USD")

# 3. Nombre de jobs par lieu d'entreprise
jobs_par_location = (
    JobRecord.objects
    .values('company_location')
    .annotate(nb_jobs=Count('id'))
    .order_by('-nb_jobs')
)
output.append("\nNombre de jobs par lieu d'entreprise :")
for loc in jobs_par_location:
    output.append(f"{loc['company_location']}: {loc['nb_jobs']}")

# 4. Ratio de jobs 100 % remote
nb_total = JobRecord.objects.count()
nb_remote = JobRecord.objects.filter(remote_ratio=100).count()
ratio_remote = (nb_remote / nb_total) * 100 if nb_total else 0
output.append(f"\nRatio de jobs 100 % remote : {ratio_remote:.2f}%")

# 5. Écriture dans un fichier
results_path = Path("analyse_resultats.txt")
results_path.write_text("\n".join(output), encoding="utf-8")

print("\n--- Résultats enregistrés dans 'analyse_resultats.txt' ---\n")
print("\n".join(output))
