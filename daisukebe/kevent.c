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
	/* カーネルキューを開く */
	if ((kq = kqueue()) < 0) {
		fprintf(stderr, "Could not open kernel queue.Error was %s.\n", strerror(errno));
	}
	/*
	  監視するファイル／ディレクトリのファイル記述子
	  を開く
	*/
	event_fd = open(path, O_EVTONLY);
	if (event_fd <=0) {
		fprintf(stderr, "The file %s could not be opened for monitoring.Error was %s.\n",
			path, strerror(errno));
		exit(-1);
	}
	/*
	  user_data内のアドレスをイベントのあるフィールドに
	  コピーする。複数ファイルを監視している場合、たとえば、
	  それぞれのファイルに異なるデータ構造体を渡すことになる。
       この例ではパスの文字列を使用している。
	*/
	user_data 	      = path;
	/* タイムアウトの通知を、0.5秒おきに設定する */
	timeout.tv_sec    = 0;      // 0秒
	timeout.tv_nsec   = 500000000;	// 500マイクロ秒
	/* 監視するイベントのリストを設定する */
	vnode_events 	      = NOTE_DELETE |  NOTE_WRITE | NOTE_EXTEND |
		NOTE_ATTRIB | NOTE_LINK | NOTE_RENAME | NOTE_REVOKE;
	EV_SET( &events_to_monitor[0], event_fd, EVFILT_VNODE, EV_ADD | EV_CLEAR,
		vnode_events, 0, user_data);
	/* イベントの処理 */
	int 	num_files     = 1;
	int continue_loop = 40; 	/* 20秒間監視する */
	while (--continue_loop) {
		int 	event_count   = kevent(kq, events_to_monitor, NUM_EVENT_SLOTS, event_data,
					       num_files, &timeout);
		if ((event_count < 0) || (event_data[0].flags == EV_ERROR)) {
			/* エラーが発生 */
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
		/* タイムアウトをリセットする。シグナル割り込みが発生すると
		   値が変わる */
		timeout.tv_sec 	= 0;    // 0秒
		timeout.tv_nsec = 500000000;	// 500マイクロ秒
	}
	close(event_fd);
	return 0;
}
/* 一連のフラグの文字列を返す簡単なルーチン */
char *flagstring(int flags)
{
	static char 	 ret[512];
	char 		*or 						      = "";
	ret[0]							      =	'\0';	// 文字列をクリア
	if (flags & NOTE_DELETE) {strcat(ret,or);strcat(ret,"NOTE_DELETE");or =	"|";}
	if (flags & NOTE_WRITE) {strcat(ret,or);strcat(ret,"NOTE_WRITE");or   =	"|";}
	if (flags & NOTE_EXTEND) {strcat(ret,or);strcat(ret,"NOTE_EXTEND");or =	"|";}
	if (flags & NOTE_ATTRIB) {strcat(ret,or);strcat(ret,"NOTE_ATTRIB");or =	"|";}
	if (flags & NOTE_LINK) {strcat(ret,or);strcat(ret,"NOTE_LINK");or     =	"|";}
	if (flags & NOTE_RENAME) {strcat(ret,or);strcat(ret,"NOTE_RENAME");or =	"|";}
	if (flags & NOTE_REVOKE) {strcat(ret,or);strcat(ret,"NOTE_REVOKE");or =	"|";}
	return ret;
}
