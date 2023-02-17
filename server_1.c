#include<winsock2.h>
#include<windows.h>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sys/types.h>
#include<errno.h>

#pragma comment(lib, "ws2_32.lib")

#define MYPORT 3000 //my port num
#define BACKLOG 10 //how many pending connections queue willl hold
#define MAX 50

void getClient(int connfd){
	char buff[MAX];
	int n;
	
	while(recv(connfd, buff, sizeof(buff), 0) > 0){
		printf("recv: %s\n", buff);
		send(connfd, buff, sizeof(buff), 0);
	}
	
	closesocket(connfd);
}

int main(){
	//set TCP server
	int sockfd, connfd;
	struct sockaddr_in servaddr;
	struct sockaddr_in cli;
	int sin_size;
	
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if(sockfd == -1){
		perror("socketerr");
		exit(1);
	}else{
		printf("Socket successfully created..\n");
	}
	
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = INADDR_ANY;
	servaddr.sin_port = htons(MYPORT);
	memset(&servaddr, 0, sizeof(servaddr));
	
	if(bind(sockfd, (struct sockaddr*)&servaddr, sizeof(struct sockaddr)) == -1){
		perror("binderr");
		exit(1);
	}else{
		printf("success bind..\n");
	}
	
	if(listen(sockfd, BACKLOG) == -1){
		perror("listenerr");
		exit(1);
	}else{
		printf("success listen..\n");
	}
	//TCP server set complete
	
	while(1){
		sin_size = sizeof(struct sockaddr_in);
		if((connfd = accept(sockfd, (struct sockaddr*)&cli, &sin_size)) == -1){
			perror("accepterr");
			break;
		}
		printf("server : got connection from %s..\n", inet_ntoa(cli.sin_addr));
		
		getClient(connfd);
	}
}

