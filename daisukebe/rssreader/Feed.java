import java.util.*;
import java.net.URL;
import java.io.*;
import java.text.*;
import com.sun.syndication.feed.synd.SyndEntry;
import com.sun.syndication.feed.synd.SyndFeed;
import com.sun.syndication.feed.synd.SyndContent;
import com.sun.syndication.fetcher.FeedFetcher;
import com.sun.syndication.fetcher.impl.HttpURLFeedFetcher;


public class Feed {

	static String address = null;
	static MailTo mail;

	Feed (String mailInfoCSV) {

		Map<String,String> mailInfoMap = new HashMap<String,String>();
		
		try {
			
			File newMailInfoCSV  = new File(mailInfoCSV);
			BufferedReader br = new BufferedReader(new FileReader(newMailInfoCSV));
			
			while (br.ready()) {
				String line = br.readLine();
				String [] csvElement = line.split(",");
				mailInfoMap.put(csvElement[0],csvElement[1]);
			}
			
			br.close();
			
		} catch (FileNotFoundException e){
			e.printStackTrace();
		} catch (IOException e){
			e.printStackTrace();
		}
		// call constructer				
		mail = new MailTo(mailInfoMap);

	}

	public static void writeToCSV(Map<Integer,Date> datemap, String csvfilename){

		try {
			
			File csv = new File(csvfilename);			
		    System.out.println("Writing last update date file to .... " + csvfilename);		

			PrintWriter writer = new PrintWriter(new BufferedWriter(new FileWriter(csv)));

			for (int i = 0; i < datemap.size(); i++){
				//writer.println(entry.getKey() + "," + entry.getValue());
				writer.println(i + "," + datemap.get(i));
			}
			
			writer.close();			

		} catch (FileNotFoundException e) {				
			System.out.println("Failed to find last update date file...");
			e.printStackTrace();
		} catch (IOException e){
			System.out.println("Failed to write last update date file...");
			e.printStackTrace();
		}
				
	}
	
	public static void getFeedInfo2(SyndFeed feed[], int urlcount) {
		//
		int c;
		int fcount = 0;
		SyndFeed feedtmp = null;
		Date today = new Date();
		Date updated_day = null;
		Date last_day = null;
		String day;
		String csvfilename = "rssLastUpdateDate.csv";
		//URL = new Hashtable();
		//Hashtable TITLE = new Hashtable();
		Map<Integer,String> url = new HashMap<Integer,String>(); 
		Map<Integer,String> title = new HashMap<Integer,String>();
		Map<Integer,String> maintitle = new HashMap<Integer,String>();
		Map<Integer,String> value = new HashMap<Integer,String>();
		Map<Integer,Date> datemap = new HashMap<Integer,Date>();
		ArrayList<Date> csvdatelist  = new ArrayList<Date>();
		ArrayList<Date> newentrylist = new ArrayList<Date>();
		
		try {
			File newcsv = new File(csvfilename);
			BufferedReader br = new BufferedReader(new FileReader(newcsv));
			while (br.ready()) {
				String line = br.readLine();
				String [] update_date_value = line.split(",");
				//System.out.println(update_date_value[1]);
				SimpleDateFormat sdf = new SimpleDateFormat();
				sdf.setDateFormatSymbols(new DateFormatSymbols(Locale.US));
				sdf.applyPattern("EEE MMM dd HH:mm:ss ZZZ yyyy");
				try {
					last_day = sdf.parse(update_date_value[1]);
					csvdatelist.add(last_day);
				} catch (java.text.ParseException e){
					e.printStackTrace();
				}
			}
			br.close();		
		} catch (FileNotFoundException e){
		        System.out.println("Making " + csvfilename + "....");
		} catch (IOException e){
			e.printStackTrace();
		}
		
		for(int u = 0; u < urlcount; u++){
			
			c = 0;
			feedtmp = feed[u];

			for(SyndEntry entry : (List<SyndEntry>)feedtmp.getEntries()){
				updated_day = entry.getPublishedDate();
				//System.out.println(updated_day);
				try {
					if(csvdatelist.get(u).before(updated_day)){
						/* get all of the entry */
						for(SyndContent e : (List<SyndContent>) entry.getContents()){
							value.put(fcount, e.getValue());
						}
							
						System.out.println("We got new entry!");
						url.put(fcount, entry.getUri());
						title.put(fcount, entry.getTitle());
						newentrylist.add(updated_day);
						c++;
					}else{
					    if(c > 0){
							newentrylist.add(updated_day);
					    } else {
							//System.out.println("No new entry...");
							newentrylist.add(updated_day);
					    }
					    break;
					}
				} catch (Exception e) {
				    
				    // print when there is no rssLastUpdateDate.csv
				    System.out.println("We got new entry!");
				    newentrylist.add(updated_day);
				    break;

				}
				
				fcount++;
			}
			
			datemap.put(u,newentrylist.get(0));
			newentrylist.clear();

		}
				
		if(url.get(0) != null) {
			writeToCSV(datemap,csvfilename);
			mail.send(today, url, title, value, fcount);
		} else {
		    writeToCSV(datemap,csvfilename);
		}

	}
	
	public static void getFeed(String site[], int urlcount) {
		int c;
		FeedFetcher fetcher;
		SyndFeed[] feed = new SyndFeed[site.length];
		String[] FEED_URL = new String[site.length];

		System.setProperty("http.proxyHost", "148.87.19.20");
		System.setProperty("http.proxyPort", "80");
			

		//get feed of the site
		for(c = 0; c < urlcount; c++){
			if(site[c] == null){
				//System.out.println("not new entry...............");
				continue;
			}
			//System.out.println(c);
			FEED_URL[c] = site[c];
			fetcher = new HttpURLFeedFetcher();
			try {
				feed[c] = fetcher.retrieveFeed(new URL(FEED_URL[c]));
			}catch (Exception e){
				//System.out.println("hoge");
				e.printStackTrace();
			}
		}

		getFeedInfo2(feed, urlcount);

	}
}
