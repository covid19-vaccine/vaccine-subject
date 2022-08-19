from edc_base.model_mixins import BaseUuidModel, ListModelMixin


class COVIDSymptoms(ListModelMixin, BaseUuidModel):
    pass


class Contraception(ListModelMixin, BaseUuidModel):
    pass


class MedicationIndication(ListModelMixin, BaseUuidModel):
    pass


class MaternalDiagnosesList(ListModelMixin, BaseUuidModel):
    pass


class ParticipantMedications(ListModelMixin, BaseUuidModel):
    pass


class PriorArv(ListModelMixin, BaseUuidModel):
    pass


class SAECriteria(ListModelMixin, BaseUuidModel):
    pass


class SubjectRace(ListModelMixin, BaseUuidModel):
    pass


class WcsDxAdult(ListModelMixin, BaseUuidModel):
    pass


class SymptomaticInfections(ListModelMixin, BaseUuidModel):
    pass


class Diseases(ListModelMixin, BaseUuidModel):
    pass


class Symptoms(ListModelMixin, BaseUuidModel):
    pass


class SubjectIdentifiers(ListModelMixin, BaseUuidModel):
    pass