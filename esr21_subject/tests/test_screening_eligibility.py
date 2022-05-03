from django.test import TestCase, tag
from edc_constants.constants import NO, YES

from ..models.second_eligibility import SecondEligibility


@tag('screening_eligibility')
class TestScreeningEligibility(TestCase):
    """
    Participant age >= 40 and <= 60 is eligible else ineligible
    """

    @tag('test_eligibility')
    def test_eligibility(self):
        eligiblity = SecondEligibility(
            substance_hypersensitivity=NO,
            pregnancy_status=NO,
            thrombosis_or_thrombocytopenia=NO,
            guillain_barre_syndrome=NO,
            suspected_immuno_condition=NO,
            clinical_bleeding=NO,
            covid_symptoms=None,
            comorbidities=None,
            symptoms_other=None,
            comorbidities_other=None,
            childbearing_potential=NO,

            # adding the fields to test cases
            symptomatic_infections_experiences=None,
            symptomatic_infections=None,
            symptomatic_infections_other=None,

        )
        self.assertTrue(eligiblity.is_eligible)

    """
    Participant age >= 40 and <= 60 is eligible else ineligible
    """

    @tag('test_ineligible')
    def test_ineligible(self):
        eligiblity = SecondEligibility(
            substance_hypersensitivity=YES,
            pregnancy_status=YES,
            thrombosis_or_thrombocytopenia=YES,
            guillain_barre_syndrome=YES,
            suspected_immuno_condition=YES,
            clinical_bleeding=YES,
            childbearing_potential=YES,
            birth_control=NO,
            covid_symptoms=None,
            comorbidities=None,
            symptoms_other=None,
            comorbidities_other=None,
            # adding the fields to test cases
            symptomatic_infections_experiences=None,
            symptomatic_infections=None,
            symptomatic_infections_other=None,
        )
        self.assertFalse(eligiblity.is_eligible)

    """
    Participant age >= 40 and <= 60 is eligible else ineligible
    """

    @tag('substance_hypersensitivity_yes')
    def test_substance_hypersensitivity_yes(self):
        eligiblity = SecondEligibility(
            substance_hypersensitivity=YES,
            pregnancy_status=NO,
            thrombosis_or_thrombocytopenia=NO,
            guillain_barre_syndrome=NO,
            suspected_immuno_condition=NO,
            clinical_bleeding=NO,
            covid_symptoms=None,
            comorbidities=None,
            symptoms_other=None,
            comorbidities_other=None,
            # adding the fields to test cases
            symptomatic_infections_experiences=None,
            symptomatic_infections=None,
            symptomatic_infections_other=None,
        )
        self.assertFalse(eligiblity.is_eligible)

    """
    Participant age >= 40 and <= 60 is eligible else ineligible
    """

    @tag('substance_hypersensitivity_no')
    def test_substance_hypersensitivity_yes(self):
        eligiblity = SecondEligibility(
            substance_hypersensitivity=NO,
            pregnancy_status=YES,
            thrombosis_or_thrombocytopenia=YES,
            guillain_barre_syndrome=YES,
            suspected_immuno_condition=YES,
            clinical_bleeding=YES,
            covid_symptoms=None,
            comorbidities=None,
            symptoms_other=None,
            comorbidities_other=None,
            # adding the fields to test cases
            symptomatic_infections_experiences=None,
            symptomatic_infections=None,
            symptomatic_infections_other=None,
        )
        self.assertFalse(eligiblity.is_eligible)

    """Participant age < 40 are in eligible"""

    @tag('pregnancy_status')
    def test_pregnancy_status(self):
        eligiblity = SecondEligibility(
            substance_hypersensitivity=NO,
            pregnancy_status=YES,
            thrombosis_or_thrombocytopenia=NO,
            guillain_barre_syndrome=NO,
            suspected_immuno_condition=NO,
            clinical_bleeding=NO,
            covid_symptoms=None,
            comorbidities=None,
            symptoms_other=None,
            comorbidities_other=None,
            # adding the fields to test cases
            symptomatic_infections_experiences=None,
            symptomatic_infections=None,
            symptomatic_infections_other=None,
        )
        self.assertFalse(eligiblity.is_eligible)

    @tag('thrombosis_or_thrombocytopenia')
    def test_thrombosis_or_thrombocytopenia(self):
        eligiblity = SecondEligibility(
            substance_hypersensitivity=NO,
            pregnancy_status=NO,
            thrombosis_or_thrombocytopenia=YES,
            guillain_barre_syndrome=NO,
            suspected_immuno_condition=NO,
            clinical_bleeding=NO,
            covid_symptoms=None,
            comorbidities=None,
            symptoms_other=None,
            comorbidities_other=None,
            # adding the fields to test cases
            symptomatic_infections_experiences=None,
            symptomatic_infections=None,
            symptomatic_infections_other=None,
        )
        self.assertFalse(eligiblity.is_eligible)

    @tag('guillain_barre_syndrome')
    def test_guillain_barre_syndrome(self):
        eligiblity = SecondEligibility(
            substance_hypersensitivity=NO,
            pregnancy_status=NO,
            thrombosis_or_thrombocytopenia=NO,
            guillain_barre_syndrome=YES,
            suspected_immuno_condition=NO,
            clinical_bleeding=NO,
            covid_symptoms=None,
            comorbidities=None,
            symptoms_other=None,
            comorbidities_other=None,
            # adding the fields to test cases
            symptomatic_infections_experiences=None,
            symptomatic_infections=None,
            symptomatic_infections_other=None,
        )
        self.assertFalse(eligiblity.is_eligible)

    """Participant age > 60 are in eligible"""

    @tag('clinical_bleeding')
    def test_clinical_bleeding(self):
        eligiblity = SecondEligibility(
            substance_hypersensitivity=NO,
            pregnancy_status=NO,
            thrombosis_or_thrombocytopenia=NO,
            guillain_barre_syndrome=NO,
            suspected_immuno_condition=NO,
            clinical_bleeding=YES,
            covid_symptoms=None,
            comorbidities=None,
            symptoms_other=None,
            comorbidities_other=None,
            # adding the fields to test cases
            symptomatic_infections_experiences=None,
            symptomatic_infections=None,
            symptomatic_infections_other=None,
        )
        self.assertFalse(eligiblity.is_eligible)

    """Participant age > 60 are in eligible"""

    @tag('covid_symptoms')
    def test_thrombosis_or_thrombocytopenia(self):
        eligiblity = SecondEligibility(
            substance_hypersensitivity=NO,
            pregnancy_status=NO,
            thrombosis_or_thrombocytopenia=YES,
            guillain_barre_syndrome=NO,
            suspected_immuno_condition=NO,
            clinical_bleeding=NO,
            covid_symptoms=None,
            comorbidities=None,
            symptoms_other=None,
            comorbidities_other=None,
            # adding the fields to test cases
            symptomatic_infections_experiences=None,
            symptomatic_infections=None,
            symptomatic_infections_other=None,
        )
        self.assertFalse(eligiblity.is_eligible)

    """Participant age > 60 are in eligible"""

    @tag('symptoms_other')
    def test_symptoms_other(self):
        eligiblity = SecondEligibility(
            substance_hypersensitivity=NO,
            pregnancy_status=NO,
            thrombosis_or_thrombocytopenia=NO,
            guillain_barre_syndrome=NO,
            suspected_immuno_condition=NO,
            clinical_bleeding=NO,
            covid_symptoms=None,
            comorbidities=None,
            symptoms_other='Other',
            comorbidities_other=None,
            # adding the fields to test cases
            symptomatic_infections_experiences=None,
            symptomatic_infections=None,
            symptomatic_infections_other=None,
        )
        self.assertFalse(eligiblity.is_eligible)

    """Participant age > 60 are in eligible"""

    @tag('comorbidities')
    def test_comorbidities(self):
        eligiblity = SecondEligibility(
            substance_hypersensitivity=YES,
            pregnancy_status=YES,
            thrombosis_or_thrombocytopenia=YES,
            guillain_barre_syndrome=YES,
            suspected_immuno_condition=YES,
            clinical_bleeding=YES,
            covid_symptoms=None,
            comorbidities=None,
            symptoms_other=None,
            comorbidities_other=None,
            # adding the fields to test cases
            symptomatic_infections_experiences=None,
            symptomatic_infections=None,
            symptomatic_infections_other=None,
        )
        self.assertFalse(eligiblity.is_eligible)

    @tag('symptomatic_infections')
    def test_symptomatic_infections(self):
        eligiblity = SecondEligibility(
            substance_hypersensitivity=NO,
            pregnancy_status=NO,
            thrombosis_or_thrombocytopenia=NO,
            guillain_barre_syndrome=NO,
            suspected_immuno_condition=NO,
            clinical_bleeding=NO,
            covid_symptoms=None,
            comorbidities=None,
            symptoms_other=None,
            comorbidities_other=None,
            # adding the fields to test cases
            symptomatic_infections_experiences=YES,
            symptomatic_infections=None,
            symptomatic_infections_other=None,
        )
        print(eligiblity.error_message)
        self.assertTrue(eligiblity.is_eligible)

    @tag('childbearing_potential')
    def test_childbearing_potential(self):
        eligiblity = SecondEligibility(
            substance_hypersensitivity=NO,
            pregnancy_status=NO,
            thrombosis_or_thrombocytopenia=NO,
            guillain_barre_syndrome=NO,
            suspected_immuno_condition=NO,
            clinical_bleeding=NO,
            covid_symptoms=None,
            comorbidities=None,
            symptoms_other=None,
            comorbidities_other=None,
            childbearing_potential=YES,
            birth_control=NO,
            # adding the fields to test cases
            symptomatic_infections_experiences=None,
            symptomatic_infections=None,
            symptomatic_infections_other=None,

        )

        self.assertFalse(eligiblity.is_eligible)
