from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class PostDeleteMixin:
    permission_classes = [IsAuthenticated, ]
    obj_to_add_model = None
    serializer_class = None
    object_to_add_name = None

    def post(self, request, id):
        obj_to_add = get_object_or_404(
            self.obj_to_add_model, pk=id  # Product id
        )
        data = {
            self.object_to_add_name: obj_to_add.id,
            'user': request.user.id
        }
        serializer = self.serializer_class(
            data=data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        pass
