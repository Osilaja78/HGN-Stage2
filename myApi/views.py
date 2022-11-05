import re
from urllib import response
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
import wolframalpha

# Create your views here.

@api_view(['POST'])
def arithmetics(request:Request):

    question = request.data["operation_type"]
    x = request.data["x"]
    y = request.data["y"]


    if question == "addition":
        answer = x + y
        response = {"slackUsername": "Hameed", "result": answer, "operation_type": question}
    elif question == "subtraction":
        answer = x - y
        response = {"slackUsername": "Hameed", "result": answer, "operation_type": question}
    elif question == "multiplication":
        answer = x * y
        response = {"slackUsername": "Hameed", "result": answer, "operation_type": question}
    else:
        # Wolfram Alpha App id obtained
        app_id = 'UYVJR4-HK3V8WARW8'

        # client class
        client = wolframalpha.Client(app_id)

        # Stores the response from 
        # wolf ram alpha
        res = client.query(question)
        
        # Includes only text from the response
        answer = next(res.results).text

        # REGEX patterns to check for operation performed
        pattern_one = re.search(r'add | plus | also | too | as well as | increase | adding | added | sum | total | tot | count | reckon | summate| enumereate | adds', question)
        pattern_two = re.search(r'subtract | minus | deduct | decrease | withhold | detract | diminish | remove | take | teke away | takeaway | take out | take off | take from | withdraw | discount | draw back | subtracting | subtracted | subtracts | lessen', question)
        pattern_three = re.search(r'multiply | multiplies | multiplied| produce | product | compound | procreate| aggregate | mount | manifold | spread', question)

        if pattern_one:
            operation = "addition"
        elif pattern_two:
            operation = "subtraction"
        elif pattern_three:
            operation = "multiplication"
        else:
            operation = "unknown"

        response = {"slackUsername": "Hameed", "result": answer, "operation_type": operation}
    return Response(data=response)