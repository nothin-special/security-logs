![](./Images/20250629103447.png)

Started: 8/7/25

Creds: levi.james / KingofAkron2025!

NMAP Results

![](./Images/20250807081331.png)

Ran RPC Client enumdomusers

![](./Images/20250629103529.png)

Ran NetExec and SMB Map

![](./Images/20250629181135.png)

Interesting DEV share found

![](./Images/20250807081615.png)

Ran bloodhound-python command to pull AD data

![](./Images/20250807092847.png)

Uploaded all output from bloodhound-python command to Bloodhound CE

![](./Images/20250807093024.png)

Marked user as owned and starting point

![](./Images/20250807093201.png)

Attack path

![](./Images/20250807094049.png)

Added user to group where we can use the genericwrite to get developers user

![](./Images/20250807095023.png)

Confirmed levi.james was added to HR group

![](./Images/20250807095800.png)

Re-ran SMB map now that we may have access to DEV SMB share

![](./Images/20250807102310.png)

Getting keepass hash to crack with john

![](./Images/20250807182315.png)

John cracked the password

![](./Images/20250807185929.png)

This is the cracked password. Now we can open the keepass file and get some passwords to spray with.

![](./Images/20250807185955.png)

Creds available in KeePass file upon opening

![](./Images/20250807191840.png)

Now we can access the ant.edwards account

![](./Images/20250807192205.png)

Ran bloodhound-python again to get more info using ant.edwards creds

![](./Images/20250807194314.png)

Senior devs group has generic all for adam.silver

![](./Images/20250807194240.png)

We can change adam.silver's password

![](./Images/20250808025159.png)

The user is disabled so we must enable them too. Once enabled and we change the password, they are in the remote management users group so we can try to get user flag using winrm.

![](./Images/20250808030514.png)

Now we can enable adam.silver and change their password to that of our choosing.

![](./Images/20250808030745.png)

User flag obtained!
![](./Images/20250808031001.png)

Back to bloodhound, which did not yield any viable paths that I could find.

![](./Images/20250808031410.png)

However, snooping more in the C drive revealed a backups folder containing a zip file.

![](./Images/20250808033724.png)

After unzipping and printing out the hidden file. We have another password to use.

![](./Images/20250808034046.png)

PrivEsc using dpapi
- https://pentestlab.blog/tag/sharpdpapi/
- https://notes.benheater.com/books/active-directory/page/dumping-passwords-from-windows-credential-manager

Created an SMB share to transfer the two files.

![](./Images/20250808084420.png)

First I grabbed the credential file.

![](./Images/20250808084232.png)

Next the master key

![](./Images/20250808084408.png)

Using the master key, we can get the decrpyted key.

![](./Images/20250808084712.png)

steph.cooper_adm user password stolen from the decrypted credential file.

![](./Images/20250808084853.png)

Root flag obtained

![](./Images/20250808085116.png)

![](./Images/20250808085256.png)
