class ActionSerializerMixin:
    ACTION_SERIALIZERS = {}

    # Перезаписываем метод get_serializer_class
    # Возвращает указываемый serializer или дефолтный
    def get_serializer_class(self):
        return self.ACTION_SERIALIZERS.get(self.action, super().get_serializer_class())