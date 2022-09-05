import time

from .usecase.score_evaluation_usecase import ScoreEvaluationUsecase


def main():
    usecase = ScoreEvaluationUsecase()
    while True:
        eval = usecase.execute()
        print(eval.to_json())
        if eval.repository_url == "":
            time.sleep(60)

if __name__=="__main__":
    main()
