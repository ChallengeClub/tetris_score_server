import subprocess
from django.http import HttpResponse

from .usecase import score_evaluation_usecase

def main(request):
    response = HttpResponse()
    usecase = score_evaluation_usecase.ScoreEvaluationUsecase()
    result = usecase.execute()
    if result is None:
        response.content = "No message in queue"
    else:
        response.content = result.to_json()
    return response