#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/event.h>
#include <sys/time.h>
#include <errno.h>
#include <string.h>
#include <inttypes.h>
#define NUM_EVENT_SLOTS 1
#define NUM_EVENT_FDS 	1
char 	*flagstring(int flags);

int main(int argc, char *argv[])
{
	char 		*path = argv[1];
	int 		 kq;
	int 		 event_fd;
	struct kevent 	 events_to_monitor[NUM_EVENT_FDS];
	struct kevent 	 event_data[NUM_EVENT_SLOTS];
	void 		*user_data;
	struct timespec  timeout;
	unsigned int 	 vnode_events;
	if (argc != 2) {
		fprintf(stderr, "Usage:monitor <file_path>\n");
		exit(-1);
	}
	/* $B%+!<%M%k%-%e!<$r3+$/(B */
	if ((kq = kqueue()) < 0) {
		fprintf(stderr, "Could not open kernel queue.Error was %s.\n", strerror(errno));
	}
	/*
	  $B4F;k$9$k%U%!%$%k!?%G%#%l%/%H%j$N%U%!%$%k5-=R;R(B
	  $B$r3+$/(B
	*/
	event_fd = open(path, O_EVTONLY);
	if (event_fd <=0) {
		fprintf(stderr, "The file %s could not be opened for monitoring.Error was %s.\n",
			path, strerror(errno));
		exit(-1);
	}
	/*
	  user_data$BFb$N%"%I%l%9$r%$%Y%s%H$N$"$k%U%#!<%k%I$K(B
	  $B%3%T!<$9$k!#J#?t%U%!%$%k$r4F;k$7$F$$$k>l9g!"$?$H$($P!"(B
	  $B$=$l$>$l$N%U%!%$%k$K0[$J$k%G!<%?9=B$BN$rEO$9$3$H$K$J$k!#(B
       $B$3$NNc$G$O%Q%9$NJ8;zNs$r;HMQ$7$F$$$k!#(B
	*/
	user_data 	      = path;
	/* $B%?%$%`%"%&%H$NDLCN$r!"(B0.5$BIC$*$-$K@_Dj$9$k(B */
	timeout.tv_sec    = 0;      // 0$BIC(B
	timeout.tv_nsec   = 500000000;	// 500$B%^%$%/%mIC(B
	/* $B4F;k$9$k%$%Y%s%H$N%j%9%H$r@_Dj$9$k(B */
	vnode_events 	      = NOTE_DELETE |  NOTE_WRITE | NOTE_EXTEND |
		NOTE_ATTRIB | NOTE_LINK | NOTE_RENAME | NOTE_REVOKE;
	EV_SET( &events_to_monitor[0], event_fd, EVFILT_VNODE, EV_ADD | EV_CLEAR,
		vnode_events, 0, user_data);
	/* $B%$%Y%s%H$N=hM}(B */
	int 	num_files     = 1;
	int continue_loop = 40; 	/* 20$BIC4V4F;k$9$k(B */
	while (--continue_loop) {
		int 	event_count   = kevent(kq, events_to_monitor, NUM_EVENT_SLOTS, event_data,
					       num_files, &timeout);
		if ((event_count < 0) || (event_data[0].flags == EV_ERROR)) {
			/* $B%(%i!<$,H/@8(B */
			fprintf(stderr, "An error occurred (event count %d).The error was %s.\n",
				event_count, strerror(errno));
			break;
		}
		if (event_count) {
			printf("Event %" PRIdPTR " occurred.Filter %d, flags %d, filter flags %s,
filter data %" PRIdPTR ", path %s\n",
			       event_data[0].ident,
			       event_data[0].filter,
			       event_data[0].flags,
			       flagstring(event_data[0].fflags),
			       event_data[0].data,
			       (char *)event_data[0].udata);
		} else {
			printf("No event.\n");
		}
		/* $B%?%$%`%"%&%H$r%j%;%C%H$9$k!#%7%0%J%k3d$j9~$_$,H/@8$9$k$H(B
		   $BCM$,JQ$o$k(B */
		timeout.tv_sec 	= 0;    // 0$BIC(B
		timeout.tv_nsec = 500000000;	// 500$B%^%$%/%mIC(B
	}
	close(event_fd);
	return 0;
}
/* $B0lO"$N%U%i%0$NJ8;zNs$rJV$94JC1$J%k!<%A%s(B */
char *flagstring(int flags)
{
	static char 	 ret[512];
	char 		*or 						      = "";
	ret[0]							      =	'\0';	// $BJ8;zNs$r%/%j%"(B
	if (flags & NOTE_DELETE) {strcat(ret,or);strcat(ret,"NOTE_DELETE");or =	"|";}
	if (flags & NOTE_WRITE) {strcat(ret,or);strcat(ret,"NOTE_WRITE");or   =	"|";}
	if (flags & NOTE_EXTEND) {strcat(ret,or);strcat(ret,"NOTE_EXTEND");or =	"|";}
	if (flags & NOTE_ATTRIB) {strcat(ret,or);strcat(ret,"NOTE_ATTRIB");or =	"|";}
	if (flags & NOTE_LINK) {strcat(ret,or);strcat(ret,"NOTE_LINK");or     =	"|";}
	if (flags & NOTE_RENAME) {strcat(ret,or);strcat(ret,"NOTE_RENAME");or =	"|";}
	if (flags & NOTE_REVOKE) {strcat(ret,or);strcat(ret,"NOTE_REVOKE");or =	"|";}
	return ret;
}
