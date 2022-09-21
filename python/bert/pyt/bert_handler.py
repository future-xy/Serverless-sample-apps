from ts.torch_handler.base_handler import BaseHandler
import torch
import json


class BertHandler(BaseHandler):
    """
    BertHandler class for bert model handler
    """

    def __init__(self):
        super(BertHandler, self).__init__()
        self.device = None

    def preprocess(self, data):
        """
        Preprocess function for bert model
        """
        # assume batch size = 1
        # convert data to json
        data = json.loads(data[0]['body'].decode('utf-8'))['instances']
        data = data[0]

        # convert to tensor
        input_ids = torch.tensor(data['input_ids'], dtype=torch.long).to(self.device)
        token_type_ids = torch.tensor(data['token_type_ids'], dtype=torch.long).to(self.device)
        attention_mask = torch.tensor(data['attention_mask'], dtype=torch.long).to(self.device)

        print("input_ids: ", input_ids)
        print("token_type_ids: ", token_type_ids)
        print("attention_mask: ", attention_mask)

        return input_ids, token_type_ids, attention_mask

    def inference(self, data):
        """
        Inference function for bert model
        """
        input_ids, token_type_ids, attention_mask = data
        # inference
        with torch.no_grad():
            output = self.model(input_ids, token_type_ids, attention_mask)

        return output

    def postprocess(self, data):
        """
        Postprocess function for bert model
        """
        print("postprocess data: ", data)
        result = data[0].tolist()
        return result
