import boto3

class Migrator:
    def __init__(self) -> None:
        self.dynamo = boto3.resource('dynamodb')
        self.table = self.dynamo.Table('tetris_score_results_table') 

    def exec(self):
        results = self.table.scan()["Items"]
        for _result in results:
            print(_result)
            _res = self.convert_csv_to_list(_result)
            print(_res)
            # if _res["ResponseMetadata"]["HTTPStatusCode"] != 200:
            #     break

    def convert_csv_to_list(self, _result: dict):
        if type(_result.get("RandomSeeds", [])) == list:
            return
        response = self.table.update_item(
            Key = {
                "Id": _result["Id"],
                "CreatedAt": _result["CreatedAt"]
            },
            UpdateExpression='set \
                #RandomSeeds = :random_seeds, \
                #Scores = :scores \
                ',
            ExpressionAttributeNames= {
                '#RandomSeeds' : 'RandomSeeds',
                '#Scores' : 'Scores',
		    },
            ExpressionAttributeValues={
                ':random_seeds' : list(map(int, _result.get("RandomSeeds", "").split(","))),
                ':scores' : list(map(int, _result.get("Scores", "").split(","))),
            },
        )
        return response

if __name__=='__main__':
    migrator = Migrator()
    migrator.exec()
