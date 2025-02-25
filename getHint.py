from openai import OpenAI

def gpto3Hint(solutionString, problemDescription, correctAnswer, userAnswer):

    try:
        #I will give you the code separately
        client = OpenAI(api_key='X')
        
        response = client.chat.completions.create(
 
                model = 'o3-mini',
                
                messages= [
                    {
                    #Description of how to generate the hint
                    "role": "user",   
                    "content": f'Goal: Your task is to determine what error has been made by a student when solving a math problem and give the student a hint to try and correct their error. Your hint should be based on the problem description, a transcription of the handwritten solution made by the student and the incorrect answer submitted by the student. The hint should be based on a potential error that the student could have made which the student should pay extra attention to in order to understand where he went wrong. The hint should be very encouraging, simple and short. Some general guidelines for what errors to look for and base your hint on are. 1. Make sure every step of the solution is correct regarding the elements described in the problem description. This means that the mathematical expression written down by the student reflects the expression in the problem description at each step. If the students solution contains a step with specific elements or operations that do not match the problem description your hint should advice the student to have a closer look at these elements/operations and the problem description. If the problem description has been written down and interpreted correctly you should not mention that they should have a closer look at the problem description. 2. Make sure that each step of the students solution is mathematically correct. If the result from any of the steps in the students solution are incorrect your hint should advice the student to have a closer look at that specific step. Its crucial that you never give the correct answer away in your hint and that your hint is based on the error made by the student, and the reason why the students answer is incorrect. The hint should never be longer than 1 sentence and use simple mathematical terminology that could be understood by a child. Repeating one of the most important requirements, never reveal the correct answer to the hint. This implies that the correct answer: ${correctAnswer} should never be mentioned in your ouput. In your output only return the hint and nothing else.'
                    },
                    {
                    #Description of how to format the output
                    "role": "user",
                    "content": f'Output format: The hint should never be longer than 1 sentence and use simple mathematical terminology that could be understood by a child. Never reveal the correct answer in the hint. This implies that the correct answer: {correctAnswer} should never be mentioned in your output. In your output only return the hint and nothing else.'
                    },
                    {
                    #Description of variables in input: problem description, correct answer, students answer and transcription of students solution
                    "role": "user",
                    "content": f'The problem description is ${problemDescription}. The correct answer is ${correctAnswer}. The incorrect answer they submitted is ${userAnswer}. A transcription of the students solution is {solutionString}.'
                    },
                ],
                max_completion_tokens=6000,
                reasoning_effort='low'
            )

        hint = response.choices[0].message.content.strip()

    except:
        return -1

    return hint