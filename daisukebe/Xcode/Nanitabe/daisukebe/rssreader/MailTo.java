import java.io.UnsupportedEncodingException;
//import java.util.Properties;
//import java.util.Date;
//import java.util.Hashtable;
import java.util.*;
import javax.mail.Session;
import javax.mail.Message;
import javax.mail.Transport;
import javax.mail.internet.MimeMessage;
import javax.mail.internet.InternetAddress;


public class MailTo {

	// member variable
	String addr,smtp,from;
	// constructer
	MailTo(Map<String,String> mailInfoMap) {
		this.addr = mailInfoMap.get("Mail Address");
		this.smtp = mailInfoMap.get("Mail Smtp Host");
		this.from = mailInfoMap.get("From Name");
		
		//System.out.println(this.addr);
		//System.out.println(this.smtp);
		//System.out.println(this.from);
		
	}

	public int send(Date today, Map<Integer,String> url,
					Map<Integer,String> title, Map<Integer, String> value, int count) {

		// sending e-mail
		String info = new String();
		System.out.println("Sending mail to " + addr);

		for(int c = 0; c < count; c++) {
			//info += "<a href=\"" + (String)URL.get(c) + "\">"+ (String)TITLE.get(c) + "</a></br>";
			info += "<a href=\"" + url.get(c) + "\">"+ title.get(c) + "</a></br>" + value.get(c) + "</br>";
			//System.out.println((String)URL.get(c) + " " + (String)TITLE.get(c));
		}
		try {
			Properties props = System.getProperties();
			props.put("mail.smtp.host", this.smtp);
			Session session = Session.getDefaultInstance(props, null);
			MimeMessage mimeMessage = new MimeMessage(session);
			mimeMessage.setFrom(new InternetAddress(this.addr, this.from, "iso-2022-jp"));
			mimeMessage.setRecipients(Message.RecipientType.TO, this.addr);
			mimeMessage.setSubject("[new entry]" + today, "iso-2022-jp");
			mimeMessage.setText(info, "iso-2022-jp");
			mimeMessage.setHeader("Content-Type", "text/html");
			mimeMessage.setSentDate(new Date());
			Transport.send(mimeMessage);
		}catch (Exception e){
			e.printStackTrace();
			return 1;
		}
		return 0;
	}
}

