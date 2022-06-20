from rest_framework.views import APIView, Response, status

from .models import Animal
from .serializers import AnimalSerializer


class AnimalView(APIView):
    def get(self, request):
        animals = Animal.objects.all()

        serializer = AnimalSerializer(animals, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = AnimalSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class AnimalViewDetail(APIView):
    def get(self, request, animal_id):
        try:
            animal = Animal.objects.get(pk=animal_id)

            serializer = AnimalSerializer(animal)

            return Response(serializer.data)
        except Animal.DoesNotExist:
            return Response({"message": "Animal not found."})

    def patch(self, request, animal_id):
        try:
            animal = Animal.objects.get(pk=animal_id)
            serializer = AnimalSerializer(animal, request.data, partial=True)

            serializer.is_valid()

            try:
                serializer.save()
            except Exception as key:
                return Response(
                    {"message": f"You can not update {key.args[0]} property."},
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            return Response(serializer.data)
        except Animal.DoesNotExist:
            return Response({"message": "Animal not found."})

    def delete(self, request, animal_id):
        try:
            animal = Animal.objects.get(pk=animal_id)
            animal.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Animal.DoesNotExist:
            return Response({"message": "Animal not found."})
