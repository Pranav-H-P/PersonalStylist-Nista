from langchain_ollama import OllamaLLM
import markdown # for converting llm markdown output into html to directly insert into the dom
from bs4 import BeautifulSoup # for converting html into raw text for saving in llm memory

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

def summarize(newPoints, previousSummary):

    arrPoints = ""

    for session in newPoints: # session is [ humanMsg, AIMsg ]

        response = markdown.markdown(response).lstrip('<p>').rstrip('</p>') # converts the markdown stuff llms give by default into html
        response = response.replace("<script>"," ") # juuuust to make sure this isnt used for remote code execution by messing with the llm output

        soup = BeautifulSoup(session[1], "html.parser")
        rawResponse = soup.get_text() # gets raw text from the html formatting

        arrPoints += "User: " + session[0] + "\n" + "Stylist: " + rawResponse

    if len(previousSummary.strip()) != 0:
        previousSummary = "\nThe summary of the previous conversations is given below\n" + previousSummary

    template = llmTemplates.summaryTemplate.format(previousSummary = previousSummary, arrayPoints = arrPoints)

    response = model.invoke(input = template, temperature = 0)

    return response

def chatReply(userData):
    print(userData)
    freshChats = userData['freshChats']
    toSummarize = userData['toSummarize']
    summary = userData['summaryText']

    prevText = "" # will store previous conversation in gemma2 instruction tags

    if len(summary.strip()) != 0:
        summary = "\n" + "The summary of the previous conversations is given below\n"+summary

    for arr in toSummarize:
        prevText += "<start_of_turn>user\n" # enclosing user message
        prevText += arr[0] + "<end_of_turn>\n"
        
        prevText += "<start_of_turn>model\n" # enclosing AI message
        prevText += arr[1] + "<end_of_turn>\n"
    
    for arr in freshChats:
        prevText += "<start_of_turn>user\n" # enclosing user message
        prevText += arr[0] + "<end_of_turn>\n"
        
        prevText += "<start_of_turn>model\n" # enclosing AI message
        prevText += arr[1] + "<end_of_turn>\n"

    template = llmTemplates.chatTemplate.format(userText = userData['text'],
                                                name = userData['name'],
                                                age = userData['age'],
                                                gender = userData['gender'],
                                                ethnicity = userData['ethnicity'],
                                                skinTone = userData['skinTone'],
                                                height = userData['height'],
                                                bodyType = userData['bodyType'],
                                                preferences = userData['prefs'],
                                                previousConversation = prevText,
                                                summary = summary
                                                )

    response = model.invoke(input = template)

    mdResponse = response #markdown response for later llm reference

    response = markdown.markdown(response).lstrip('<p>').rstrip('</p>') # converts the markdown stuff llms give by default into html
    response = response.replace("<script>"," ") # juuuust to make sure this isnt used for remote code execution by messing with the llm output
    
    return {
        "htmlResponse": response, # displayed on screen
        "rawResponse": mdResponse # stored in history
        }


if __name__ == '__main__':
    while True:
        print(classifyBodyType(1.7, 0.19, 'Male'))