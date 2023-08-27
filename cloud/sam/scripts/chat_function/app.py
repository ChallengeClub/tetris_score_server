import json
from tools.utils import DynamoDBManager, OpenAIManager
from tools.response import HttpResponse
from role.role_tetris import TetrisAssistant
import logging

# ロギングの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ChatHandler:
    
    def __init__(self, event):
        self.event = event
        self.db_manager = DynamoDBManager()
        self.openai_manager = OpenAIManager()
        self.http_response = HttpResponse()
        self.tetris_assistant = TetrisAssistant()
    
    def get_message_from_event(self):
        body_content = self.event.get('body', None)
        if not body_content:
            raise ValueError("The 'body' field in the event is missing or empty.")
        try:
            return json.loads(body_content)['input_text']
        except KeyError:
            raise ValueError("Invalid input. 'input_text' key is required.")
    
    def handle_get_request(self):
        return self.http_response.success('hello world')
    
    def handle_delete_request(self):
        # RESTfulな設計では、DELETEはbodyを持たせるべきではないが、他に方法が分からなかった。
        try:
            data = json.loads(self.event["body"])
            user_id = data['identity_id']
            char_name = data['character_name']
            try:
                self.db_manager.delete_items_with_secondary_index(user_id, char_name)
                return self.http_response.success('delete success')

            except Exception as e:
                print(f"An error occurred: {e}")
                return self.http_response.server_error(f'Error during delete operation: {e}')
        except KeyError as e:
            print(f"An error occurred: {e}")
            return self.http_response.client_error(f'Error during delete operation: {e}')

    
    def gpt_function_call(self, response_data, messages, functions, user_id, char_name, max_order_id, input_text):
        print(f"function call defined\n")
        # gptが定義した関数を実行し、結果を取得する
        func_name, args, function_response, function_args = self.openai_manager.execute_function_call(response_data)

        # 2回目のAPI実行のための関数の引数を作成
        function_args = self.openai_manager.create_function_args(func_name, args)
        #print(f"function_args: {function_args}")
        messages.append({"role": "assistant", "content": None, "function_call": function_args})
        messages.append({"role": "function", "content": function_response, "name": func_name})

        response_2nd = self.openai_manager.get_chat_response_func(messages, functions)
        response_content = response_2nd.choices[0]["message"]["content"]

        # DynamoDBにトーク履歴を記録
        self.db_manager.store_conversation(user_id, char_name, max_order_id + 0, "user", input_text)
        self.db_manager.store_conversation(user_id, char_name, max_order_id + 1, "assistant", None, name=None, function_call=function_args)
        self.db_manager.store_conversation(user_id, char_name, max_order_id + 2, "function", function_response, name=func_name, function_call=None)
        self.db_manager.store_conversation(user_id, char_name, max_order_id + 3, "assistant", response_content)

        return response_content
    

    def gpt_simple_response(self, response_data, user_id, char_name, max_order_id, input_text):
        print(f"function call undefined\n")
        response_content = response_data["message"]["content"]
        self.db_manager.store_conversation(user_id, char_name, max_order_id + 0, "user", input_text)
        self.db_manager.store_conversation(user_id, char_name, max_order_id + 1, "assistant", response_content)
        return response_content
    

    def call_openai_api(self, messages, functions, user_id, char_name, input_text, max_order_id):
        response_1st = self.openai_manager.get_chat_response_func(messages, functions)
        response_data = response_1st["choices"][0]
        if response_data["finish_reason"] == "function_call":
            if response_data["message"]["function_call"]["name"]:
                return self.gpt_function_call(response_data, messages, functions, user_id, char_name, max_order_id, input_text)
        else:
            return self.gpt_simple_response(response_data, user_id, char_name, max_order_id, input_text)

    
    def handle_post_request(self):
        self.openai_manager.get_secret()

        # メッセージを取得
        try:
            data = json.loads(self.event["body"])
            logger.info('Event: %s', json.dumps(data))
            user_id = data['identity_id']
            char_name = data['character_name']
            input_text = data['input_text']
        except ValueError as e:
            return self.http_response.client_error(f'Error during post operation: {e}')
        
        # 過去の応答を取得
        try:
            messages = self.tetris_assistant.get_chat_messages()
            functions = self.tetris_assistant.get_chat_functions()
            max_order_id,items = self.db_manager.get_max_conversation_id(user_id, char_name)

            #今までの対話をmessagesに並べる
            messages.extend([
                {
                    "role": item["role"],
                    "content": item["content"],
                    **({"name": item["name"]} if "name" in item else {}),
                    **({"function_call": item["function_call"]} if "function_call" in item else {})
                } 
                for item in items
            ])
            messages.append({"role": "user", "content": data['input_text']})
            
            #openAIのAPIを叩く
            response_content = self.call_openai_api(messages, functions, user_id, char_name, input_text, max_order_id)
            return self.http_response.success(response_content)
            
        except Exception as e:
            return self.http_response.server_error(f'Error during post operation: {e}')

    def handle(self):
        http_method = self.event.get('httpMethod', '')
        if http_method == 'GET':
            return self.handle_get_request()
        elif http_method == 'DELETE':
            return self.handle_delete_request()
        elif http_method == 'POST':
            return self.handle_post_request()


def lambda_handler(event, context):
    handler = ChatHandler(event)
    return handler.handle()
