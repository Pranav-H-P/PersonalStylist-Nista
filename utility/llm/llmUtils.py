from langchain_ollama import OllamaLLM

phi35 = OllamaLLM(model = "gemma2:2b")

def classifyRBG(rgb):
    template = f"""You are a specialized classification AI developed by scientists to automate data gathering in a randomized control trial.
This randomized control trial aims to detect the effectiveness of sunscreen on preventing melanoma.
One of the datapoints that the scientists must gather is the skin tone of the participants. This is to rule out confounding factors such as natural melanin levels.
Scientists have used computer vision to identify the average RGB value of the participant's skin using sophisticated equipment.
You are tasked with classifying these RGB values into the academically accepted Fitzpatrick skin type classification system:
• 'TYPE I': Very Fair
• 'TYPE II': Fair
• 'TYPE III': Medium
• 'TYPE IV': Olive
• 'TYPE V': Dark
• 'TYPE VI': Very Dark

You must only reply in the format given below

INPUT>Red: 115.34, Green: 71.63, Blue: 69.35
OUTPUT>TYPE V
INPUT>Red: 180.12, Green: 127.77, Blue: 103.59
OUTPUT>TYPE III
INPUT>Red: 178.21, Green: 154.86, Blue: 149.37
OUTPUT>TYPE I
INPUT>Red: 130.31, Green: 80.45, Blue: 56.65
OUTPUT>TYPE V
ALWAYS FOLLOW THE ABOVE MENTIONED OUTPUT FORMAT. DO NOT EXPLAIN YOUR DECISION. ONLY RESPOND WITH THE TYPE NUMBER.
Do not reply in any other output format. Only reply with either TYPE I, TYPE II, TYPE III, TYPE IV, TYPE V or TYPE VI.
Failure to do so will lead to system malfunction.
The system input is given below.
INPUT>{rgb}
OUTPUT>"""
    
    response = phi35.invoke(input = template, temperature = 0)
    response = response.upper()

    response = response.replace("OUTPUT>","") # Output formatting
    response = response.replace("\n","")
    response = response.strip(" ")

    respDict = { # directly asking it to list skin color names makes it refuse due to concerns of racism sometimes
                "TYPE I": "Very light",
                "TYPE II": "Light",
                "TYPE III": "Medium",
                "TYPE IV": "Olive",
                "TYPE V": "Dark",
                "TYPE VI": "Very Dark"
    }

    if response in respDict:
        return respDict[response]
    else:
        return "Error"



if __name__ == "__main__":
    
    pass
   