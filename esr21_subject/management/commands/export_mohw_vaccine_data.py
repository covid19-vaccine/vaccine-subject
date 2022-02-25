import csv
from operator import index

from django.core.management.base import BaseCommand
from edc_base.utils import get_utcnow
from edc_registration.models import RegisteredSubject

import pandas as pd

from ...models import PersonalContactInfo, DemographicsData, InformedConsent, VaccinationDetails


class Command(BaseCommand):

    help = 'Export vaccine data'

    def add_arguments(self, parser):
        parser.add_argument(
            'site_id', type=str, help='Site specific export')

    def district_check(self, location):
        location = location.lower()
        switcher = {
            'gaborone': 'South East',
            'maun': 'Ngamiland',
            'francistown': 'North East',
            'phikwe': 'Central',
            'serowe': 'Central',
        }
        return switcher.get(location, 'no location')

    def site_name_by_id(self, site_id=None):
        sites_mapping = {
            '40': 'gaborone',
            '41': 'maun',
            '42': 'serowe',
            '43': 'francistown',
            '44': 'phikwe'}
        return sites_mapping.get(site_id, site_id)

    def dosage_mapping(self, dose_type=None):
        dosage_mapping = {
            'first_dose': 'DOSE1',
            'second_dose': 'DOSE2'}
        return dosage_mapping.get(dose_type, '')

    def handle(self, *args, **kwargs):
        identifiers = []
        site_id = kwargs.get('site_id')

        if site_id == 'all':
            identifiers = RegisteredSubject.objects.values_list(
                'subject_identifier', flat=True)
        else:
            identifiers = RegisteredSubject.objects.filter(site_id=site_id).values_list(
                'subject_identifier', flat=True)

        vaccinations_tuple = ('received_dose_before', 'vaccination_site',
                              'vaccination_date', 'site',)

        count = 0
        toCSV = []
        for identifier in identifiers[:6]:
            obj_dict = {}

            consent = InformedConsent.objects.filter(subject_identifier=identifier).last()
            first_name = consent.first_name
            last_name = consent.last_name
            dob = consent.dob
            gender = consent.get_gender_display()
            age = consent.formatted_age_at_consent
            country = None
            employment_status = None
            employment_status_other = None
            subject_cell = None
            physical_address = None
            location = None
            district = None
            occupation = None

            identity_number = consent.identity

            demographics = DemographicsData.objects.filter(
                subject_visit__subject_identifier=identifier).last()
            if demographics:
                country = demographics.country
                employment_status = demographics.get_employment_status_display()
                employment_status_other = demographics.employment_status_other
                if employment_status_other:
                    occupation = employment_status_other
                else:
                    occupation = employment_status

            try:
                personal_contact = PersonalContactInfo.objects.get(
                    subject_identifier=identifier)
            except PersonalContactInfo.DoesNotExist:
                pass
            else:
                subject_cell = personal_contact.subject_cell
                physical_address = personal_contact.physical_address

            obj_dict.update(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                dob=dob,
                subject_cell=subject_cell,
                identity_number=identity_number,
                covidzone=f'Greater {location} Zone',
                physical_address=physical_address,
                occupation=occupation)

            vaccinations = VaccinationDetails.objects.filter(
                received_dose='Yes',
                subject_visit__subject_identifier=identifier).only(*vaccinations_tuple)

            vaccine_type = 'Astra-Zeneca'
            for vaccination in vaccinations:
                dose_type = self.dosage_mapping(dose_type=vaccination.received_dose_before)

                # Get vaccination disctrict from site name
                site = vaccination.site.name
                location = site[6:]
                district = self.district_check(location)

                obj_dict.update(
                    {f'{dose_type}_vaccinesite': vaccination.vaccination_site,
                     f'{dose_type}_vaccine_type': vaccine_type,
                     f'{dose_type}_district': district,
                     f'{dose_type}_date_vaccinated': vaccination.vaccination_date})

            toCSV.append(obj_dict)
            count += 1

        df = pd.DataFrame(toCSV)
        df_mask = df.copy()
        df_mask2 = df_mask.rename(
            columns={'first_name': 'Firstname',
                     'last_name': 'Surname',
                     'gender': 'Sex',
                     'dob': 'Date of Birth',
                     'subject_cell': 'Mobile Number',
                     'identity_number': 'Identity Number',
                     'covidzone': 'Covid Zone',
                     'district': 'District',
                     'physical_address': 'Address',
                     'occupation': 'Occupation', })

        timestamp = get_utcnow().strftime("%m%d%Y%H%M%S")
        site_name = self.site_name_by_id(site_id=site_id)
        df_mask2.to_csv(f'~/source/esr21/{site_name}_vaccinations_{timestamp}.csv', index=False)
        # with open('vacinations_' + timestamp + '.csv', 'w', newline='')  as output_file:
        #     dict_writer = csv.DictWriter(output_file)
        #     dict_writer.writeheader()
        #     dict_writer.writerows(df_mask2)

        self.stdout.write(self.style.SUCCESS(f'Total exported: {count}.'))
