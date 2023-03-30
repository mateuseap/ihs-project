#include <stdio.h>	/* printf */
#include <stdlib.h>	/* malloc, atoi, rand... */
#include <string.h>	/* memcpy, strlen... */
#include <stdint.h>	/* uints types */
#include <sys/types.h>	/* size_t ,ssize_t, off_t... */
#include <unistd.h>	/* close() read() write() */
#include <fcntl.h>	/* open() */
#include <sys/ioctl.h>	/* ioctl() */
#include <errno.h>	/* error codes */

#include "display.h"

int main(int argc, char** argv)
{
	int fd, len, retval;
	char buf[255];
	char cmd;

	if (argc < 2) {
		printf("Syntax: %s <device file path>\n", argv[0]);
		return -EINVAL;
	}

	if ((fd = open(argv[1], O_RDWR)) < 0) {
		fprintf(stderr, "Error opening file %s\n", argv[1]);
		return -EBUSY;
	}
	printf("file: %s opened!\n", argv[1]);

	while (1) {
		printf("Read or Write? [r,w]\nClose file [c]\n");
		scanf("%c%*c", &cmd);
		printf("CMD: %c\n", cmd);

		switch (cmd) {
		case 'r':
			printf("how many bytes you want to read?\n");
			scanf("%d%*c", &len);
			retval = read(fd, buf, len);
			buf[retval] = '\0';
			printf("red: %s. with %d bytes\n", buf, retval);
			buf[0] = '\0';
			break;
		case 'w':
			printf("type in what you want to write:\n");
			scanf("%[^\n]%*c", buf);
			retval = write(fd, buf, strlen(buf));
			printf("wrote %d bytes\n", retval);
			break;
		case 'c':
			close(fd);
			printf("file closed, exiting...\n");
			return EXIT_SUCCESS;
			break;
		default:
			printf("invalid input. try again\n");
			break;
		}
	}
}
