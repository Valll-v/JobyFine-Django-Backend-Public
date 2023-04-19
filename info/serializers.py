from rest_framework import serializers

from info.models import Question, ProjectInfo


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'question', 'answer')


class InfoSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    def get_questions(self, obj):
        return QuestionSerializer(Question.objects.all(), many=True).data

    class Meta:
        model = ProjectInfo
        fields = ('questions', 'about', 'confidence', 'agreement')
