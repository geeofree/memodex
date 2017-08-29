from flask import jsonify

def json_response(status_code, status_message, **payload):
    """ Abstracts API JSON responses

    Args:
        status_code:int
            - HTTP response status code
        status_message:str
            - Describes the response's status
        payload:dict
            - A collection of keyword arguments to add into the JSON response data

    Return:
        json response using Flask's jsonify function
        with the created json data
    """

    if type(status_code) != int:
        raise ValueError("Invalid status_code value: Must be of type 'int'")

    if type(status_message) != str:
        raise ValueError("Invalid status_message value: Must be of type 'str'")

    json_data = {
        'status': int(status_code),
        'status_message': status_message
    }

    # Add payload/other data if it exists
    if payload:
        for key, items in payload.items():
            json_data[key] = items

    return jsonify(json_data)
