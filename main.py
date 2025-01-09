import requests
import pandas

class DataCase:
    def __init__(self, usersURL, nameOfExcelFile, postEndpoint):
        self.usersURL = usersURL
        self.nameOfExcelFile = nameOfExcelFile
        self.postEndpoint = postEndpoint
        self.userData = []

    def getUsersFromAPI(self):
        usersGetResponse = requests.get(self.usersURL)
        return usersGetResponse.json()
    
    def getPostsFromAPI(self, currentUserId):
        postsGetResponse = requests.get(f"{self.usersURL}/{currentUserId}/posts")
        return postsGetResponse.json()
    
    def calculateAverageOfCharacters(self, posts, amountOfPosts):
        bodyCharacterByUser = 0
        for post in posts:
            postBody = post['body']
            postBodyLength = len(postBody)
            bodyCharacterByUser += postBodyLength

        averageOfCharacters = bodyCharacterByUser / amountOfPosts
        return averageOfCharacters

    def processData(self):
        currentUserID = 1
        getResponse = self.getUsersFromAPI()
        
        for user in getResponse:
            userId = user['id']
            userName = user['name']

            print("--------------------------------------------------------------------------------------------------------------------------")
            print("ID do usuário: ", userId)
            print("Nome do usuário: ", userName)

            postsResponse = self.getPostsFromAPI(currentUserID)
            amountOfPosts = len(postsResponse)
            average = self.calculateAverageOfCharacters(postsResponse, amountOfPosts)
            currentUserID += 1

            for post in postsResponse:
                print(f"Título do post de ID {post['id']}: {post['title']}")
                print(f"Body do post de ID {post['id']}: {post['body']}")
                print(f"Quantidade de caracteres no body do post: {len(post['body'])}\n")

            print(f"Média de caracteres do user de ID {userId}: {average}")

            self.userData.append({
                "ID de Usuário": userId,
                "Nome de Usuário": userName,
                "Quantidade de Posts": amountOfPosts,
                "Média de Caracteres por Post": average
            })

        print("--------------------------------------------------------------------------------------------------------------------------")
        print("\n\n-------------------------------------------------------\nDados dos Usuários:\n-------------------------------------------------------\n", self.userData)
        print("-------------------------------------------------------\n")

    def createDataFrame(self):
        dataFrame = pandas.DataFrame(self.userData)
        dataFrame.to_excel(self.nameOfExcelFile, index=False)
        print(f"\n-------------------------------------------------------\nDados transferidos para o arquivo {self.nameOfExcelFile} com sucesso.\n-------------------------------------------------------")

    def postToEndpoint(self):
        endpointPostRequest = requests.post(self.postEndpoint, json=self.userData)
        print("\n-------------------------------------------------------\nStatus da requisição POST: ", endpointPostRequest.status_code)
        print("Resposta: ", endpointPostRequest.text)
        print("-------------------------------------------------------")

    def runCode(self):
        self.processData()
        self.createDataFrame()
        self.postToEndpoint()


usersURL = "https://jsonplaceholder.typicode.com/users"
excelFileName = "nome-teste.xlsx"
fakeEndpoint = "https://jsonplaceholder.typicode.com/send-email"

main = DataCase(usersURL, excelFileName, fakeEndpoint)
main.runCode()