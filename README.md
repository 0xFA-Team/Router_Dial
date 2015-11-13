# Router_Dial
For people who want to dial with router under the limit of NETKEEPER environment.

	>python net_dial.py -h
	    ____              __            ____        _ __
	   / __ \____  __  __/ /____  _____/ __ \____ _(_) /
	  / /_/ / __ \/ / / / __/ _ \/ ___/ / / / __ `/ / /
	 / _, _/ /_/ / /_/ / /_/  __/ /  / /_/ / /_/ / / /
	/_/ |_|\____/\__,_/\__/\___/_/  /_____/\__,_/_/_/  (alhpa-0.1)
	
	    Author: Purpleroc@0xfa.club
	  Modified: RickGray@0xfa.club     |
	      Date: 2015-10-22             |
	    Update: 2015-10-22             |
	___________________________________|
	
	usage: net_dial.py [-h] -u USERNAME -p PASSWORD [-a AUTH] [-m MODEL]
	
	optional arguments:
	  -h, --help   show this help message and exit
	
	account:
	  -u USERNAME  Network account username (e.g. 1621744@cqupt)
	  -p PASSWORD  Network account password
	
	router:
	  -a AUTH      Router auth username and password (e.g. admin:admin)
	  -m MODEL     Router models (Already exist Models are:TL_WR740N)
	


## Usage
* a. Clone this project or download `zip` file.  
```
git clone https://github.com/0xFA-Team/Router_Dial
```
* b. Type the follow command to dial.  
```
python net_dial.py -u username -p password -a admin:admin -m tl_wr740n 
```
* c. You can use your Router as a AP to surfer the Internet now.

## Notice
Now it only support TL_WR740N, We hope you can help us to make it more stronger. Add your router model in `net_router.py`. Thx.

## Enjoy it!
