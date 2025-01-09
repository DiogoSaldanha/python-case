import requests
import pandas

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
        "ID de Usuário": userId,
        "Nome de Usuário": userName,
        "Quantidade de Posts": amountOfPosts,
        "Média de Caracteres por Post": averageOfCharacters
    })


print("\n", userData)

#Usando pandas para criar a planilha

#Criando o DataFrame
dataFrame = pandas.DataFrame(userData)
dataFrame.to_excel("user-data.xlsx", index=False)
print("\nDados transferidos para o arquivo 'user-data.xlsx' com sucesso.")

#Enviando para endpoint fictício
endpointURL = "https://jsonplaceholder.typicode.com/send-email"
postRequest = requests.post(endpointURL, json=userData)

print("\nStatus da requisição POST: ", postRequest.status_code)
print("Resposta: ", postRequest.text)
