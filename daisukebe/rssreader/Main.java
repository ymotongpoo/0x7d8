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
