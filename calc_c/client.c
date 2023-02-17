#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<sys/wait.h>
#include<errno.h>
#include<netinet/in.h>

#define MYPORT 3000
#define MAX 50

int main(){
	int sockfd, connfd;
	struct sockaddr_in servaddr;
	struct sockaddr_in cli;
	char server_ip[40];
	char buff[MAX];
	printf("server IP : ");
	gets_s(server_ip, sizeof(server_ip));
	
	
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	
	if(sockfd == -1){
		perror("socketerr");
		exit(1);
	}else{
		printf("Socket successfully created..\n");
	}
	
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = inet_addr(server_ip);
	servaddr.sin_port = htons(MYPORT);
	memset(&servaddr, 0, sizeof(servaddr));
	
	if(connect(sockfd, (struct sockaddr *)servaddr, sizeof(servaddr)) == -1){
		perror("connecterr");
		exit(1);
	}
	
	while(1){
		get_s(buff, MAX);
		send(sockfd, buff, sizeof(buff), 0);
		if(strcmp(msg, "exit") == 0){
			break;
		}
		recv(sockfd, buff, sizeof(buff), 0);
		printf("receive : %s\n", buff);
	}
	closesocket(sockfd);
}
