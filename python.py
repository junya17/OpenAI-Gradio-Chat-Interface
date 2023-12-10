from openai import OpenAI
import openai
import gradio as gr

client = OpenAI()

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    def predict(message, history):
        history_openai_format = []
        for human, assistant in history:
            history_openai_format.append({"role": "user", "content": human })
            history_openai_format.append({"role": "assistant", "content":assistant})
        history_openai_format.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages= history_openai_format,
            temperature=1.0,
            max_tokens=100,
            stream=True
        )

        partial_message = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                partial_message = partial_message + chunk.choices[0].delta.content 
                print(partial_message)
                return partial_message, response.choices[0].message.conetnt

    msg.submit(predict, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch()

# gr.ChatInterface(predict).queue().launch()