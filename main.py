import ollama
import sys_msgs

assistant_convo = [sys_msgs.assistant_msg]

def stream_response():
    global assistant_convo
    response_stream = ollama.chat(model='llama3.1:8b', messages=assistant_convo, stream=True)
    complete_response = ''
    print('QT:')

    for chunk in response_stream:
        print(chunk['message']['content'], end='', flush=True)
        complete_response += chunk['message']['content']
        
    assistant_convo.append({'role': 'assistant', 'content': complete_response})
    print('\n\n')

def main():
    global assistant_convo
    
    while True:
        user_input = input('USER: \n')
        assistant_convo.append({'role': 'user', 'content': user_input})
        stream_response()
    
if __name__ == '__main__':
    main()
