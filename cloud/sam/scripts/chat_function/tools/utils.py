import boto3
import openai
import json
from tools.config import DYNAMODB_TABLE_NAME, DYNAMODB_INDEX_NAME, OPENAI_MODEL_NAME
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from role.role_tetris import TetrisIndexSearch

# ドメイン駆動設計におけるリポジトリ部分
class DynamoDBManager:
    def __init__(self, table_name=DYNAMODB_TABLE_NAME, index_name=DYNAMODB_INDEX_NAME):
        self.table_name = table_name
        self.index_name = index_name
        self.client = boto3.client('dynamodb')
        self.resource = boto3.resource('dynamodb')
        self.table = self.resource.Table(self.table_name)

    def get_max_conversation_id(self, user_id, char_name):
        response = self.table.query(
            IndexName=self.index_name,
            KeyConditionExpression=Key('user_id').eq(user_id) & Key('char_name').eq(char_name),
            ScanIndexForward=False
        )
        items = response.get('Items', [])
        max_order_id = max(item['order_id'] for item in items) if items else -1
        return max_order_id, items

    def delete_items_with_secondary_index(self, user_id, char_name):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(self.table_name)
        
        response = table.query(
            IndexName=self.index_name,
            KeyConditionExpression='user_id = :uid and char_name = :cname',
            ExpressionAttributeValues={
                ':uid': user_id,
                ':cname': char_name,
            },
        )

        primary_keys = [{'user_id': item['user_id'], 'order_id': item['order_id']} for item in response['Items']]
        
        for key in primary_keys:
            print('delete_item:', key)
            table.delete_item(Key=key)

        print(f'Deleted {len(primary_keys)} item(s) from {self.table_name}.')

    def store_conversation(self, user_id, char_name, max_order_id, role, content, name=None, function_call=None):
        item = {
            'user_id': user_id,
            'order_id': (max_order_id + 1),
            'char_name': char_name,
            'role': role,
            'content': content
        }
        if name:
            item['name'] = name
        if function_call:
            item['function_call'] = function_call
        self.table.put_item(Item=item)

class OpenAIManager:
    def __init__(self, model_name=OPENAI_MODEL_NAME):
        self.model_name = model_name
        self.tetris_assistant = TetrisIndexSearch()

    @staticmethod
    def get_secret():
        secret_name = "openai-key"
        region_name = "ap-northeast-1"
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e

        secret = get_secret_value_response['SecretString']
        key_value = json.loads(secret)
        openai.api_key = key_value['openai-key']

    def get_chat_response(self, messages):
        return openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages
        )

    def get_chat_response_func(self, messages, functions):
        return openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            functions=functions,
            function_call="auto"
        )

    @staticmethod
    def create_function_args(func_name, args):
        function_call = {
            "name": func_name,
            "arguments": json.dumps(args)
        }
        return function_call
    
    def execute_function(self, func_name, **args):
        # 定義された関数を実行
        if func_name == "search_tetris_index":
            return self.tetris_assistant.search_tetris_index(**args)
        else:
            func = globals().get(func_name)
            if func:
                return func(**args)
            else:
                raise Exception(f"No function named {func_name} found.")


    def execute_function_call(self, response_data):
        # gptが定義した関数名や引数を取得する
        call_data = response_data["message"]["function_call"]
        func_name = call_data["name"]
        args = eval(call_data["arguments"])
        print(f"func_name: {func_name}, args: {args},\n")

        function_response = self.execute_function(func_name, **args)
        print(f"function_response: {function_response}")

        # 2回目のAPI実行のための関数の引数を作成
        function_args = self.create_function_args(func_name, args)
        #print(f"function_args: {function_args}")
        
        return func_name, args, function_response, function_args

