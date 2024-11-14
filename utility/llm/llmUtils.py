from langchain_ollama import OllamaLLM
import markdown # for converting llm markdown output into html to directly insert into the dom
from bs4 import BeautifulSoup # for converting html into raw text for saving in llm memory
import time


if __name__ == "__main__":
    
    import llmTemplates
else:
    
    from utility.llm import llmTemplates

model = OllamaLLM(model = "gemma2:2B")


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

    return response.strip()

def chatReply(userData):
    
    freshChats = userData['freshChats']
    toSummarize = userData['toSummarize']
    summary = userData['summaryText']
    latestTrends = userData['latestTrends'].strip(" ")

    prevText = "" # will store previous conversation in gemma2 instruction tags

    if latestTrends != " ":
        latestTrends = ("Here is a curated list of recent trends in fashion\n" + latestTrends + "\n").strip()

    if len(summary.strip()) != 0:
        summary = "\n" + "The summary of the previous conversations is given below\n"+summary

    for arr in toSummarize:
        prevText += "<start_of_turn>user\n" # enclosing user message
        prevText += arr[0].strip() + "<end_of_turn>\n"
        
        prevText += "<start_of_turn>model\n" # enclosing AI message
        prevText += arr[1].strip() + "<end_of_turn>\n"
    
    for arr in freshChats:
        prevText += "<start_of_turn>user\n" # enclosing user message
        prevText += arr[0].strip() + "<end_of_turn>\n"
        
        prevText += "<start_of_turn>model\n" # enclosing AI message
        prevText += arr[1].strip() + "<end_of_turn>\n"



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
                                                summary = summary,
                                                latestTrends = latestTrends
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

    f = open(f"gemmaResponse.txt", "w")
    
    fin = ""

    classifyBodyType(1.7, 0.19, 'Male')
    classifyBodyType(1.7, 0.19, 'Male')
    avg = 0
    print("Classify body type")
    for i in range(5):
        call = time.time()
       
        classifyBodyType(1.7, 0.19, 'Male')
        rec = time.time()
        out =f"""\\hline
{i+1} & {call:.3f} & {rec:.3f} & {rec-call:.3f}\\\\"""
        avg += rec-call
        print(out)
        fin+=out+"\n"

    print(f"avg time: {(avg/5):.3f}")
    fin+=f"avg time: {(avg/5):.3f}\n"
    print("\nchat reply")

    data = {'name': 'ali', 'age': '26', 'gender': 'Male', 'ethnicity': 'indian', 'skinTone': 'Olive', 'height': '169', 'sHR': '1.5', 'hHR': '0.17', 'bodyType': 'athletic', 'prefs': 'Shirts', 'freshChats': [['Hello, I have a meeting tommorrow any tips', "Alright! Let's nail those meetings and leave a lasting impression 😉  Tell me:\n\n* **What kind of meeting is it?** (formal, casual) \n* **What industry are you in?**  (e.g., tech, finance, creative field) \n* **Is there a specific vibe or feel you want to give off?**  (professional, approachable, confident?)\n\n\nOnce I have that info, I can help curate the perfect outfit for your needs! 💯  Plus, some quick tips:\n\n* **Iron out those wrinkles:** A clean and crisp look always goes far.\n* **Confidence is key:** You've got this! \n \nLet's do this! 💪"], ['hello', "Hey there!  😊 What can I help you with today? Need some style inspiration, outfit advice, or just want to chat fashion? 😉 \n\n\nI'm ready for whatever you're feeling! 😎  Let me know. 👍 \n"], ['I have a meeting tomorrow, any suggestions?', "Okay, let's get this meeting-ready fashion game going!  Tell me: \n\n* **What kind of meeting is it?** (formal, casual, industry, etc.)\n* **Where will the meeting be?** (office, client's place, coffee shop, etc.) \n* **What are your usual style preferences?** (classic, edgy, sporty, preppy)\n\n\nOnce I have that info, I can give you some killer outfit suggestions.  Let's rock this! 🤩 😎 \n\n\n"], ['It is a formal meeting at my office', "Got it! A formal meeting at the office sounds like we need to step up our style game.  No worries, I got you covered. 😉 Let's aim for sophisticated and polished. Here are some ideas based on your preference for comfort:\n\n**Option 1: Classic & Polished:**\n\n* **Navy Blazer + Crisp Shirt + Chinos:** A classic combo, easy to adapt for any occasion.  For the shirt, consider a white or light blue Oxford style for a clean look.\n* **Tie optional but impactful:** If you're aiming for extra formality, try a lightweight patterned tie (thin stripes or subtle geometric)  for a touch of personality. \n\n**Option 2: Modern & Effortlessly Chic:**\n\n* **Light Grey Wool Suit + White/Striped Shirt:** This will give off a clean and professional vibe.  You can choose between a slim-fit suit for a modern feel, or a slightly more relaxed fit if you prefer.\n* **Experiment with pocket squares:** A subtle pattern adds a bit of visual interest and elevates the look! \n\n\n**Key Accessories to Enhance Your Look:**\n\n* **Dark belt:** This will complete your outfit in a professional but stylish way.\n* **Quality shoes:** Leather Oxford or Derbys for a polished look, keep them clean and shined!\n* **Timeless watch:** A simple, classy timepiece (analogue) adds sophistication to any outfit.\n\n\n**Tips for Success:**\n\n* **Confidence is key:** Own your look with a confident walk and posture! \n* **Grooming matters:** Make sure your hair, nails and skincare are on point for a polished finish.  \n* **Don't forget the scent:** A light, subtle cologne can add a touch of confidence to your overall look.\n\nWhat do you think of these ideas? We can dive into specific pieces or brands if you have something in mind! 💪 \n\n\n"], ['hello', "Hey there!  😊 How's it going? \n\nWhat can I help you with today? Need some style inspiration, outfit suggestions, or just a chat about fashion? 😉  \n\n\n\nI'm ready for whatever you're feeling! 😎  \n"]], 'toSummarize': [["I've just moved into a new city, people seem to be a lot more fashionable and I'm feeling a little lost. What can I do?", "Hey Ali!  Moving to a new place can definitely throw you for a loop with the fashion scene. But it's exciting, right? Let's get you looking sharp!\n\nFirst off, tell me about your style vibe. Do you lean towards classic pieces or are you into bold statements? We can work on building an outfit-building playbook that fits your taste and this cool new city vibe! 😉 \n"], ['I only feel comfortable with regular outfits', "Okay, let's keep it 💯  comfortable AND stylish. I'm thinking of clean lines, well-fitting silhouettes, and some subtle trends. Think classic denim jackets, a good quality white tee, chinos or linen pants... You get the picture!\n\nWant to take a look at some style inspo? We can do a quick search through some brands that know how to make regular outfits work their magic (think COS, Arket, Everlane),  and I'll suggest some go-to pieces for you. \n\n\nWhat do you say?  We can start there! 😉 \n"], ['Alright, tell me', "Okay, let's dive into some looks to get your style game going:\n\n**Casual & Everyday:**\n\n* **Classic Denim Jacket + White Tee + Chinos/Linen Pants:**  This combo is a staple for a reason! You can play with different washes and collar styles of the denim jacket.\n* **Striped Button-Down Shirt + Dark Jeans:** A classic striped shirt offers a little flair while looking effortlessly cool, paired with your favorite jeans. \n* **Turtleneck Sweater + Corduroy Pants:** This is a cozy yet stylish choice, especially if you're into earthy tones and textures.\n\n**Slightly Edgy (But Always Comfortable):**\n\n* **Oversized Graphic Tee + Slim Fit Jeans:**  Choose your favorite band tees or designs that speak to you. A slim fit creates a sleek silhouette while keeping things relaxed. \n* **Corduroy Jacket + T-Shirt + Straight Leg Jeans:** This is an elevated take on casual wear, giving off a more stylish vibe without being overdone.\n\n**Brands You Can Find in India:**\n\nFor these pieces, think about these brands:\n\n* **Whistler:**  Known for their clean lines and versatile pieces (think of them like a less expensive COS)\n* **Amante:**   Offers great basics at reasonable prices. \n* **United Colors of Benetton:**  Great color options and staples that can be mixed and matched.\n* **H&M:** For more trendy looks, H&M offers a wide variety of styles for every occasion (think of them as fast-fashion but with an edge)\n\n\n\nLet me know if you want to dive into any specific piece or style! We'll build your wardrobe together. 👍  \n"], ['I dont want to spend a lot of money, are there easier ways to improve my outfits', "You bet! You can totally level up your looks without breaking the bank. Here are some budget-friendly ways to inject some personality into your outfits:\n\n**Play with Accessories:**\n\n* **Scarf game:** A  bold scarf (think paisley, stripes, even a fun print) instantly elevates any basic outfit.\n* **Watch:** A nice watch elevates any look - check out second-hand shops or explore online options! \n* **Statement Earrings:** A bold pair of earrings can add instant personality to your style.\n* **Belt it out:**  A belt adds a touch of polish and definition (and makes those outfits more cohesive).\n\n**Texture & Fabric:**\n\n* **Layer Up:** A cardigan over a tee instantly creates a cooler look, while adding some warmth for colder days! Experiment with different fabrics - linen, cotton, or even knitwear can totally change the vibe.\n* **Try Out Textures:**  Corduroy pants, velvet jackets, and even denim textures add visual interest to your outfits. \n\n**Reimagine What You Have:**\n\n* **Style Up Your Basics:** Turn a plain white tee into something unique with a stylish knot, fold it in interesting ways or try layering it under a jacket for an unexpected twist! \n* **Play With the Fit:**  A slightly looser fit jeans can be just as chic as a slim fit.\n\n\nI'd love to brainstorm some ideas together. What kind of outfits are you drawn towards? 😊  \n"]], 'summaryText': '', 'text': 'Spontaneous suggestion please', 'latestTrends': ''}

    avg = 0
    for i in range(5):
        call = time.time()
        
        chatReply(data)
        rec = time.time()
        

        out = f"""\\hline
{i+1} & {call:.3f} & {rec:.3f} & {rec-call:.3f}\\\\"""
        avg += rec-call
        print(out)
        fin+=out+"\n"

    print(f"avg time: {(avg/5):.3f}")
    fin+=f"avg time: {(avg/5):.3f}\n"
    f.write(fin)
    f.close()