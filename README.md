# Basic Telegram Bot
This is the source code of an app that I built for a client. The client had a website on which many jobs are posted reguraly and wanted an easier way to post these jobs on their telegram channel. The bot is a responsive Python Flask Web App and is deployed on Heroku. It listens to all messages sent to the bot id via telegram and responds accordingly. On sending /start command, the bot return the list of all the commands available. The Beautiful Soup library of python is used to extract data from website pages. On sending recent or page with number command, the bot returns the list of most recent jobs posted or the jobs listed on the page number respectively. The user can then send command to post some or all of these jobs on their channel in a format with individual job details. The bot also has a command to post all list of jobs listed under a category. The webhook is set to recieve all the messages as they are sent. And the telegram API is used to send messages for bot chat section or to post jobs in the channel.
<br>
Language:
<ul>
<li>Python</li>
	<ul>
		<li> Flask Web App (For routing)</li>
		<li> Beautiful Soup (For Web Scrapping)</li>
		<li> urlib.request (To get html from job website) </li>
		<li> Telegram Api (For Sending & Recieving messages)</li>
	</ul>
</ul>
<br>	In addition, Webhooks are used to invoke the app every time a message is sent from client side.
