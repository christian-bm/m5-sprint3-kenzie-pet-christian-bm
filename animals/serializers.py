from characteristics.models import Characteristic
from characteristics.serializers import CharacteristicSerializer
from groups.models import Group
from groups.serializers import GroupSerializer
from rest_framework import serializers

from .models import Animal


class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.FloatField()
    weight = serializers.FloatField()
    sex = serializers.CharField(max_length=15)

    group = GroupSerializer()
    characteristics = CharacteristicSerializer(many=True)

    def create(self, validated_data: dict):
        group_data = validated_data.pop("group")
        characteristics_data = validated_data.pop("characteristics")

        try:
            group = Group.objects.get(name=group_data["name"])
        except Group.DoesNotExist:
            group = Group.objects.create(**group_data)

        characteristics = []
        for characteristic in characteristics_data:
            try:
                db_characteristic = Characteristic.objects.get(
                    name=characteristic["name"]
                )
                characteristics.append(db_characteristic)
            except Characteristic.DoesNotExist:
                db_characteristic = Characteristic.objects.create(**characteristic)
                characteristics.append(db_characteristic)

        animal = Animal.objects.create(**validated_data, group=group)
        animal.characteristics.set(characteristics)

        return animal

    def update(self, instance: Animal, validated_data: dict):
        no_editable_keys = ("sex", "group")

        for key, value in validated_data.items():
            if key in no_editable_keys:
                raise Exception(key)
            setattr(instance, key, value)

        instance.save()
        return instance
