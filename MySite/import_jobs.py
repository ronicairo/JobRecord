import csv
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Référence le module settings correctement
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JobRecord.settings')

# Initialise Django
django.setup()

from jobsite.models import JobRecord, Contract

created = 0
seen_keys = set()

with open('salaries.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        job_title = row['job_title'].strip()
        year = int(row['work_year'])
        location = row['employee_residence'].strip()


        # Vérifie en base si le job existe déjà
        if JobRecord.objects.filter(
            job_title=job_title,
            work_year=year,
            employee_residence=location
        ).exists():
            continue

        # Contrat
        contract, _ = Contract.objects.get_or_create(
            type_code=row['employment_type'].strip(),
            defaults={'description': ''}
        )

        # Création du JobRecord
        JobRecord.objects.create(
            work_year=year,
            experience_level=row['experience_level'].strip(),
            employment_type=contract,
            job_title=job_title,
            salary=float(row['salary']),
            salary_currency=row['salary_currency'].strip(),
            salary_in_usd=float(row['salary_in_usd']),
            employee_residence=row['employee_residence'].strip(),
            remote_ratio=int(row['remote_ratio']),
            company_location=row['company_location'].strip(),
            company_size=row['company_size'].strip()
        )

        created += 1

print(f"✅ {created} JobRecord(s) importés.")
