import google.generativeai as genai

def geminiTrans(image, problemDescription, correctAnswer, userAnswer):

    #Description of how to transcribe the image
    prompt = f"""Your task is to transcribe the handwritten math solution in this image. Consider the description of the mathematical problem and answer submitted by the student for some context of what is written in the image. The solution is incorrect and therefore you should carefully look at each digit and operator in the image when transcribing, since the sequence of operation might be incorrect and not make sense from a mathematical point of view. Consider the fact that the math solution is written by a child and complex mathematical operations are most likely not included in the solution. If the image does not contain a transcribable math solution, return X as your transcription. In your output only return the transcription of the hand written solution and nothing else. The problem description is {problemDescription} to which the correct answer is {correctAnswer}. The students hand-written solution can be seen in the Image. The incorrect answer they submitted is {userAnswer}."""

    #I will give you the code separately
    genai.configure(api_key='X')

    model = genai.GenerativeModel('gemini-2.0-flash')

    response = model.generate_content([prompt, image])

    # Extract the classification from the response
    trans = response.candidates[0].content.parts[0].text

    return trans