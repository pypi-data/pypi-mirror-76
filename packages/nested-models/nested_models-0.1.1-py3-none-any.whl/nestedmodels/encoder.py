import json

######################
# ENCODERS

# TODO: handling of lists

class JSONToDictEncoder(json.JSONEncoder):

    def default(self, obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        # Let the base class default method raise the TypeError
        return super().default(obj)

# TODO: YAML Encoder