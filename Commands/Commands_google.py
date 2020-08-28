# from googlesearch.googlesearch import GoogleSearch

@client.command(name='google', pass_context=True)
async def google(context,*, query=None):
    
    try: 
        from googlesearch import search 
    except ImportError:  
        await context.send("No module named 'google' found") 
    # to search 
    responseText=''
    for j in search(query, tld="com", num=10, stop=10, pause=2): 
        responseText += str(j) + "\n\n"
    embed = dc.Embed(title="Google", description=responseText, color=0xff0000)
    await context.send(embed=embed)
    # await context.send(responseText)

    '''
    print("Trigerred Google search:", query)
    # json_resp = MiscLibrary.StackOverflow_SearchQuery(query)
    response = GoogleSearch().search(query,num_results=5)
    responseText = ""
    for resp in response.results:
        responseText += str(resp.title) + "\n" + str(resp.url) + "\n\n"
        # responsetitle.append(resp.title)
        # responsecontent.append(resp.url)
    # response = MiscLibrary.GetAnswerURLs(json_resp)
 
    embed = dc.Embed(title="Google", description=responseText)
    await context.send(embed=embed)
    # MiscLibrary.OpenURLs(response)
    '''