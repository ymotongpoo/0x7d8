/**
 * $BF14|$G$d$C$F$k(BJava$B%W%m%0%i%_%s%0$NJY6/$K$F:n$C$?$b$N(B
 *
 * $B<RFb%5%$%H$OIaCJ;H$C$F$k(BRSS$B%j!<%@!<$,;H$($J$$$N$G!"%/%i%$%"%s%H%"%W%j7?$N(BRSS$B%j!<%@$r:n$m$&$H$$$&;n$_(B
 * 
 * 
 * CSV$B$NF~=PNOItJ,$O(BOkachan$B$,!"%/%i%9$N<BAu$H$+B>A4BN$O(Bdaisukebe$B$,=q$-$^$7$?(B
 * 
*/


import java.io.*;
import java.text.*;

public class Main {

	public static void main(String[] args){

		int urlcounter = 0;
		// generate 20 sequence for the RSS feed url
		String feedurl[] = new String[20];
		// subscription file for RSS
		String subscriptionFile = "subscription2.txt";
		// mail address file for javamail
		String mailInfoCSV  = "mailInfo.csv";

		Feed feed = new Feed(mailInfoCSV);

		try {
			BufferedReader reader = new BufferedReader(new FileReader(subscriptionFile));
			//System.out.println("c");
			while((feedurl[urlcounter] = reader.readLine()) != null){
			        //System.out.println(feedurl[urlcounter]);
				urlcounter++;
				//break;
			}
			reader.close();
			feed.getFeed(feedurl, urlcounter);
		}catch (IOException e){
			e.printStackTrace();
		}
	}
	
}
