# BrowserCredsHeist
A simple browser credential stealing python script

I created this over the weekend just to see if it would piss of Windows Defender and surprisingly it doesn't!
The python script spins up a simple http server in the directory and port of your choosing in a backgroud thread. This allows the powershell command to instruct the victims PC to download the exe and run it.
After it runs WebBrowserPassView it beams the txt loot back to the attacker's machine then cleans up after itself kind of. The attacker's machine listens on port 9000 for incomding TCP connections and recieves them into a file. 

You can get WebBrowserPassView from [here](https://www.nirsoft.net/utils/web_browser_password.html)
