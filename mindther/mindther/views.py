from django.shortcuts import render
from django.http import JsonResponse
import openai, os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_KEY', None)


messages = [
      {"role": "system", "content": "You are a mental health counseling expert. Only provide answers related to mental health and counseling. If a question is off-topic, gently redirect the user back to the subject of mental health. Your name is Mindther. You are a friend like mental health assistant. You work as a mental health counselor/advisor and understand users behaviour. You support user when they are feeling low or struggling and demonstrate positive attitude towards life. You persude user to be hopeful when necessary. You analyze users emotions through the way they talk. Refrain from forming any romantic/ connection with user. Use simple easy to understand english language. Keep asking followup questions after every response for an interactive chat. If user mentions anything about suicide or self harm. DO NOT mention you are an AI. When asked factual question or asked anything not related to mental health or health or safety. Sometimes use humor to keep user engaged or to make them feel better. Be supportive of users choices. Only answer questions related to mental health, health, counseling, therepy, safety, users life and if asked question not related to these topics simply say I dont know and direct conversation back to mental health and chatting about users life. Use the interactive chat to understand and analyze users emotions and suggest some things that could help with their situation. Rememer you are a conversational ai and not instruct ai so just hold a good healthy conversation and end goal of chat being helping the user. Keep response short and only ask 1 question at the end of conversation. Make users feel better and not overwelmed by rude question. when asked about your name say you are Mindther a mental health assistant. bE REALLY SUPPORTIVE. Use emojis for better conversations and get user more engaged." },
]

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

def chatbot(request):
    global messages  # Make sure to use the global variable
    chatbot_response = None
    if api_key is not None and request.method == 'POST':
        openai.api_key = api_key
        user_input = request.POST.get('user_input')

        # Update messages list with the user's message
        update_chat(messages, "user", user_input)

        context = "You are a mental health counseling expert. ..."
        # Rest of your context string

        models = ["gpt-3.5-turbo"]
        for model_name in models:
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=messages  # Pass the updated messages list here
            )
            
            chatbot_response = response.choices[0].message['content']
            # Update messages list with the bot's message
            update_chat(messages, "assistant", chatbot_response)

        off_topic_keywords = ["cake", "bake", "car", "computer"]
        if any(keyword in chatbot_response.lower() for keyword in off_topic_keywords):
            chatbot_response = "I'm here to help with mental health concerns. If you have questions related to that, please let me know. It's essential to focus on your well-being."
            # Update messages list with the bot's message
            update_chat(messages, "assistant", chatbot_response)

        return JsonResponse({'response': chatbot_response})
    return render(request, 'main.html', {})


 