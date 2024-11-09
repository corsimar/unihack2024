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

def responseAI(question):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful teacher that wants to help student to learn this by solving real problems. Please note that if you use any formulas and anything math related, I want them to be written in LaTeX format, also place that between dollar signs so they would be corectly displayed."}, 
            {
                "role": "user",
                "content": f"{question}"
            }
        ]
    )
    return completion.choices[0].message.content