from edc_constants.constants import OTHER, NOT_APPLICABLE, UNKNOWN, POS, NEG, \
    IND
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT
from edc_visit_tracking.constants import MISSED_VISIT, COMPLETED_PROTOCOL_VISIT

ACTION_TAKEN = (
    ('dose_not_changed', 'Dose not changed'),
    ('drug_withdrawal', 'Drug withdrawal'),
    (NOT_APPLICABLE, NOT_APPLICABLE),
    (UNKNOWN, UNKNOWN),
)

AE_GRADE = (
    ('mild', 'Mild (Grade 1)'),
    ('moderate', 'Moderate (Grade 2)'),
    ('severe', 'Severe (Grade 3)'),
    ('life_threatening', 'Life-threatening (Grade 4)'),
    ('fatal', 'Fatal (Grade 5)'),
)

AESI_CATEGORY = (
    ('generalized_convulsion', 'Generalized convulsion'),
    ('guillain_barre_syndrome', 'Guillain-Barre syndrome'),
    ('acute_disseminated', 'Acute disseminated encephalomyelitis'),
    ('other_neuro_events', 'Other neurologic events'),
    ('thrombotic', 'Thrombotic or thromboembolic or neurovascular events'),
    ('Thrombocytopenia', 'Thrombocytopenia'),
    ('vasculitides', 'Vasculitides'),
    ('anaphylaxis', 'Anaphylaxis'),
    ('vaccine_assoc_resp_disease',
     'Vaccine-associated enhanced respiratory disease'),
    ('immune_mediated_cond', 'Potential immune-mediated conditions'),
)

AGREE = (
    ('strongly_disagree', 'Strongly disagree'),
    ('undecided', 'Undecided'),
    ('strongly_agree', 'Strongly agree'),)

HOSPITALIZATION_OUTCOME = (
    ('expired', 'Expired'),
    ('hospice_care', 'Home: Hospice Care'),
    ('self_care', 'Home: Self Care'),
    ('hospice_medical_facility', 'Hospice Medical Facility'),
    ('inpatient_rehabilitation', 'Inpatient Rehabilitation'),
    ('intermediate_care_facility', 'Intermediate Care Facility'),
    ('medical_advice', 'Left Against Medical Advice'),
    ('long_term_care_hospital', 'Long Term Care Hospital'),
    ('nursing_facility', 'Nursing Facility'),
    ('unit_ward_change', 'Unit/Ward Change'),
)

HOSPITALIZATION_REASON = (
    ('covid19_related_symptoms', 'COVID-19 related symptoms'),
    (OTHER, 'Other'),
)

HOSPITALIZATION_STATUS = (
    ('er', 'ER'),
    ('regular_ward', 'Regular Ward'),
    ('icu_hdu', 'ICU/HDU'),
)
INFECTION_STATUS = (
    ('seronegative', 'Seronegative'),
    ('seropositive', 'Seropositive'),)

IDENTITY_TYPE = (
    ('country_id', 'Country ID number'),
    ('country_id_rcpt', 'Country ID receipt'),
    ('passport', 'Passport'),
    (OTHER, 'Other'),
)

LANGUAGE = (
    ('setswana', 'Setswana'),
    ('setswana', 'English'),
)

OUTCOME = (
    ('not_resolved', 'Not recovered/ not resolved'),
    ('resolved', 'Recovered / resolved'),
    ('resolved_with_sequelae', 'Recovered / resolved with sequelae'),
    ('resolving', 'Recovering / resolving'),
    ('fatal', 'Fatal'),
    (UNKNOWN, UNKNOWN),
)

POS_NEG_IND = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    (IND, 'Indeterminate')
)
REASON = (
    ('not_collected', 'Not collected'),
    ('not_required', 'Not required at this visit'),
    ('measurement_skipped', 'Measurement skipped at this visit'),
    ('subject_refused', 'Subject refused'),
    ('equipment_malfunction', 'Equipment malfunction'),
    ('staff_unavailable', 'Staff unavailable'),
    ('no_information', 'No further information'),
    (NOT_APPLICABLE, 'Not applicable'),
)

ROUTE = (
    ('intramuscular', 'Intramuscular'),
    ('oral', 'Oral'),
)

STATUS = (
    ('resolved', 'Resolved'),
    ('ongoing', 'Ongoing'),)

TREATMENT_RELATIONSHIP = (
    ('related', 'Related'),
    ('not_related', 'Not Related'),
)

TEST_TYPE = (
    ('pcr_test', 'PCR Test'),
    ('nasal_Swab', 'Nasal Swab'),
    (OTHER, 'Other, specify'),
)

VACCINATION_LOCATION = (
    ('left_deltoid', 'Left deltoid'),
    ('right_deltoid', 'Right deltoid'),
    (OTHER, 'Other, specify'),
)

VISIT_INFO_SOURCE = (
    ('clinic_visit_w_subject', 'Clinic visit with participant'),
    ('other_contact_w_subject',
     'Other contact with participant (i.e telephone call)'),
    ('contact_w_health_worker', 'Contact with health care worker'),
    ('Contact_w_family_design',
     'Contact with family or designated person who can provide information'),
    (OTHER, 'Other,specify'),
)

VISIT_REASON = (
    (SCHEDULED, 'Scheduled visit/contact'),
    (MISSED_VISIT, 'Missed Scheduled visit'),
    (UNSCHEDULED, 'Unscheduled visit/contact'),
    (LOST_VISIT, 'Lost to follow-up (use only when taking subject off study)'),
    (COMPLETED_PROTOCOL_VISIT, 'Subject has completed the study'),
)
