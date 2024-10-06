from langchain_ollama import OllamaLLM
import markdown

if __name__ == "__main__":
    
    import llmTemplates
else:
    
    from utility.llm import llmTemplates

   
model = OllamaLLM(model = "gemma2:2b")


def classifyRBG(rgb):
    
    template = llmTemplates.rgbTemplate

    template = template.format(input = rgb)

    response = model.invoke(input = template, temperature = 0)
    
    
    response = response.upper()
    response = response.strip("\n ")

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


def classifyBodyType(sHR, hHR, gender): # takes shoulder to hip ratio, height to hip ratio and gender

    template = llmTemplates.bodyTypeTemplate.format(SHR = sHR, HHR = hHR, gender = gender)

    response = model.invoke(input = template, temperature = 0)

    response = response.lower()
    response = response.strip("\n ")

    return response

def chatReply(userData):
    
    userInput = userData['text']

    template = llmTemplates.chatTemplate.format(userText = userInput)

    response = model.invoke(input = template)

    response = markdown.markdown(response).lstrip('<p>').rstrip('</p>') # converts the markdown stuff llms give by default into html
    response = response.replace("<script>"," ") # juuuust to make sure this isnt used for remote code execution by messing with the llm output
    
    
    return response


if __name__ == '__main__':
    while True:
        print(classifyBodyType(1.7, 0.19, 'Male'))