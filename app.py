from openai import OpenAI
import gradio as gr


client = OpenAI()

def predict(message,history,human,model,temperature,tokens):
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})
    history_openai_format.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model=model,
            messages=history_openai_format,
            temperature=temperature,
            max_tokens=int(tokens),
            stream=True,
        )
    except Exception as e:
        # Handle errors on API calls
        print(f"An error occurred during the API call: {e}")
        return "Sorry, an error has occurred."

    partial_message = ""
    try:
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                partial_message += chunk.choices[0].delta.content
            print(partial_message)
            yield partial_message
    except Exception as e:
        # Handle errors during response processing
        print(f"An error occurred during response processing: {e}")
        yield "Sorry, an error has occurred."


gr.ChatInterface(predict,
                 additional_inputs=[
                    gr.Text(value="You are the assistant", label="Role"),
                    gr.Dropdown(choices=["gpt-3.5-turbo", "gpt-3.5-turbo-1106","gpt-4-1106-preview"], value="gpt-3.5-turbo", label="Model"),
                    gr.Slider(minimum=0, maximum=1, step=0.1, value=0.7, label="Temperature"),
                    gr.Number(value=int(50),label="Maxtoken")   
                ]).queue().launch()