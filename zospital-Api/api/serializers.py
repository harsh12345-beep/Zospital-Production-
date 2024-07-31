from rest_framework import serializers
import json

class MedicationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500, required=False, allow_blank=True)
    dosage = serializers.CharField(max_length=500, required=False, allow_blank=True)
    instruction = serializers.CharField(max_length=500, required=False, allow_blank=True)


class PDFDataSerializer(serializers.Serializer):
    patient_id = serializers.CharField(max_length=100)
    date = serializers.DateField()
    name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=255)
    contact = serializers.CharField(max_length=15)
    age = serializers.IntegerField()
    sex = serializers.CharField(max_length=10)
    height = serializers.CharField(max_length=10,required=False, allow_blank=True)
    weight = serializers.CharField(max_length=10,required=False, allow_blank=True)
    bp = serializers.CharField(max_length=10,required=False, allow_blank=True)
    investigation = serializers.CharField(max_length=5000,required=False, allow_blank=True)
    advice = serializers.CharField(max_length=5000,required=False, allow_blank=True)
    chief_complaints = serializers.CharField(max_length=5000,required=False, allow_blank=True)
    examination_findings = serializers.CharField(max_length=5000, required=False, allow_blank=True)
    diagnosis = serializers.CharField(max_length=5000, required=False, allow_blank=True)
    treatment_plan = serializers.CharField(max_length=5000, required=False, allow_blank=True)
    medications = serializers.ListField(child=MedicationSerializer())
    next_date = serializers.DateField()
    footer_address = serializers.CharField(max_length=500)
