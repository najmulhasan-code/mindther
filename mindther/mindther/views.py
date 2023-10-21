#this is views
from django.shortcuts import render
import openai, os
from dotenv import load_dotenv
load_dotenv()

api_key=os.getenv('OPENAI_KEY', None)

def chatbot(request):
    chatbot_response= None
    if api_key is not None and request.method=='POST':
        openai.api_key=api_key
        user_input=request.POST.get('user_input')
        prompt=user_input
        
        response=openai.ChatCompletion.create(
            engine='gpt-3.5-turbo',
            prompt=prompt,
            max_tokens=256,
            stop="stop",
            temprature=0.5,
        )
        print(response)
    return render(request, 'base.html', {}
    )