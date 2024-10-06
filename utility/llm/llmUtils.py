from langchain_ollama import OllamaLLM


if __name__ == "__main__":
    
    import llmTemplates
else:
    
    from utility.llm import llmTemplates

   
model = OllamaLLM(model = "gemma2:2b")


def classifyRBG(rgb):
    
    template = llmTemplates.rgbTemplate

    template = template.format(input = rgb)

    response = model.invoke(input = template, temperature = 0)
    """response = response.upper()

    response = response.replace("\n","")"""
    
    response = response.strip("\n")
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
        print(f"|{response}|")
        return "Error"

def chatReply(userInput):
    
    template = llmTemplates.chatTemplate.format(userText = userInput)

    response = model.invoke(input = template)


    
    return response


if __name__ == '__main__':
    while True:
        print(classifyRBG(f"Red: 150.39, Green: 115.79, Blue: 101.87"))