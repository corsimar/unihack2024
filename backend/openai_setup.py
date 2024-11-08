from openai import OpenAI
client = OpenAI()

def genLesson(topic):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful teacher assistant. Please note that I want any formulas and anything math related to be written in LaTeX format, also place that between dollar signs."}, 
            {
                "role": "user",
                "content": f"Write a lesson regarding this topic: ${topic}."
            }
        ]
    )
    return completion.choices[0].message.content
