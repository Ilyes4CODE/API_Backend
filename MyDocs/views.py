from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.
@api_view(['GET'])
def Plan(request):
    doc = {
        'Link_to_documentation' : '/Api/schema/Docs',
    }
    return Response(doc)