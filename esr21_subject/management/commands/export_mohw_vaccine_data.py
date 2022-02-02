import csv

from django.core.management.base import BaseCommand

from ...models import PersonalContactInfo, DemographicsData, InformedConsent, VaccinationDetails
from edc_base.utils import get_utcnow


class Command(BaseCommand):
    help = 'Export vaccine data'

    def handle(self, *args, **kwargs):
        vaccinations_tuple = ('received_dose_before', 'vaccination_site',
                              'vaccination_date', 'lot_number', 'expiry_date',
                              'provider_name')
        vaccinations = VaccinationDetails.objects.filter(received_dose='Yes').only(
            *vaccinations_tuple)
        count = 0
        toCSV = []
        for vaccination in vaccinations:
            obj_dict = vaccination.__dict__

            consent = InformedConsent.objects.filter(
                subject_identifier=vaccination.subject_visit.subject_identifier).last()
            first_name = consent.first_name
            last_name = consent.last_name
            dob = consent.dob
            gender = consent.gender
            age = consent.formatted_age_at_consent
            site = consent.site.name
            country = None
            employment_status = None
            employment_status_other = None
            subject_cell = None

            identity_number = consent.identity
            identity_type = consent.identity_type

            demographics = DemographicsData.objects.filter(
                subject_visit__subject_identifier=vaccination.subject_visit.subject_identifier).last()
            if demographics:
                country = demographics.country
                employment_status = demographics.employment_status
                employment_status_other = demographics.employment_status_other

            try:
                personal_contact = PersonalContactInfo.objects.get(
                    subject_identifier=vaccination.subject_visit.subject_identifier)
            except PersonalContactInfo.DoesNotExist:
                pass
            else:
                subject_cell = personal_contact.subject_cell
                physical_address = personal_contact.physical_address
            obj_dict.update(
                first_name=first_name,
                last_name=last_name,
                dob=dob,
                gender=gender,
                age=age,
                country=country,
                employment_status=employment_status,
                employment_status_other=employment_status_other,
                subject_cell=subject_cell,
                identity_number=identity_number,
                identity_type=identity_type,
                covidzone=site,
                physical_address=physical_address
                )
            obj_dict.pop('id')
            obj_dict.pop('_state')
#             obj_dict.pop('form_as_json')
            obj_dict.pop('subject_visit_id')
            toCSV.append(obj_dict)
            count += 1

        keys = toCSV[0].keys()
        timestamp = get_utcnow().strftime("%m%d%Y%H%M%S")
        with open('vacinations_' + timestamp + '.csv', 'w', newline='')  as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(toCSV)

        self.stdout.write(self.style.SUCCESS(f'Total exported: {count}.'))

