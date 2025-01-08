import requests

# Variáveis para as URL's
usersURL = "https://jsonplaceholder.typicode.com/users"

# Respostas GET dos endpoints para 'users'
usersGetResponse = requests.get(usersURL)
usersResponse = usersGetResponse.json()

#Printando informações
currentID = 1
listOfAverageBody = []
userData = []
for item in usersResponse:
    userId = item['id']
    userName = item['name']

    print("------------------------------------------------------------------------------------------")
    print("ID do usuário: ", userId)
    print("Nome do usuário: ", userName)

    # Resgatando e printando os dados para as requisições dos Posts
    print('\nPosts:')

    postsURL= f"https://jsonplaceholder.typicode.com/users/{currentID}/posts"
    postsGetResponse = requests.get(postsURL)
    postsResponse = postsGetResponse.json()
    bodyCharactersByUser = 0
    for id in postsResponse:
        postTitle = id['title']
        postBody = id['body']
        postBodyLength = len(postBody)

        print(f"Título do post de ID {id['id']}: ", postTitle)
        print(f"Body do post de ID {id['id']}: ", postBody)
        print("Quantidade de caracteres no body do post: ", postBodyLength)
        print()

        # Em uma variável antes de incrementar 'currentID', posso ir adicionando os valores para salvá-los em uma lista e depois fazer o cálculo
        bodyCharactersByUser += postBodyLength

    currentID += 1

    #Percebi que o len de "postsResponse" é igual ao número de posts feitos por user, o que me leva a fazer o cálculo de maneira mais fácil dentro da própria iteração
    amountOfPosts = len(postsResponse)
    averageOfCharacters = bodyCharactersByUser / amountOfPosts
    print(f"Média de caracteres do user de ID {userId}: {averageOfCharacters}")

    userData.append({
        "UserID": userId,
        "UserName": userName,
        "AmountOfPosts": amountOfPosts,
        "AveragePostCharacters": averageOfCharacters
    })


print(userData)