var select = document.getElementById('select-algorithm');
var upload = document.getElementById('input-file');

change_config_form(1);

select.addEventListener('change', () => {
    change_config_form(select.value);
});

function execute() {
    var request = new XMLHttpRequest();
    var result = document.getElementById('output-text-box');
    var command = document.getElementById('encrypt').checked ? 'encrypt' : 'decrypt';
    console.log("Command : " + command);
    var keys = document.getElementById('cipher-key').value != "" ? document.getElementById('cipher-key').value : "abcd";
    
    var extra = "";
    var type = select.value;

    if (type == 3) {
        extra = "&r=" + document.getElementById("r-key").value;
    }
    console.log(extra);

    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            result.value = this.responseText;
        }
    }

    request.open('POST', '/update', true);
    request.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    request.send("text=" + document.getElementById('input-text-box').value + "&command=" + command + "&keys=" + keys + "&type=" + type + extra);
}

function change_config_form(id) {
    var request = new XMLHttpRequest();
    var result = document.getElementById('app-setting-form-dynamic');

    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            result.innerHTML = this.responseText;

            if (id == 1 | id == 3) {
                var key_upload = document.getElementById('input-key');

                key_upload.addEventListener('change', () => {
                    var filename = key_upload.value.replaceAll("\\", " ").split(" ");
                    document.getElementById('key-label').innerHTML = filename[filename.length - 1];

                    var file = key_upload.files[0];

                    const reader = new FileReader();
                    reader.onload = (e) => {
                        console.log("e.target.result");
                        console.log(e.target.result);
                        document.getElementById('cipher-key').value = e.target.result;
                    }
                    reader.readAsText(file);
                });
            }
        }
    }

    request.open('POST', '/form', true);
    request.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    request.send("algorithm_id=" + id);
}

function change_action(src) {
    if (src.id == "encrypt") {
        state = "encrypt";
        document.getElementById("left-tab").innerHTML = "Plaintext";
        document.getElementById("right-tab").innerHTML = "Ciphertext";
    } else {
        state = "decrypt";
        document.getElementById("right-tab").innerHTML = "Plaintext";
        document.getElementById("left-tab").innerHTML = "Ciphertext";
    }
}

upload.addEventListener('change', () => {
    var filename = upload.value.replaceAll("\\", " ").split(" ");
    document.getElementById('file-label').innerHTML = filename[filename.length - 1];

    var file = upload.files[0];

    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('input-text-box').value = e.target.result;
    }
    reader.readAsText(file);
});

var input = document.getElementById('input-text-box');

input.addEventListener('input', () => {
    document.getElementById('file-label').innerHTML = "Choose Input File!";
});

function download(filename, textInput) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(textInput));
    element.setAttribute('download', filename);
    document.body.appendChild(element);
    element.click();
}

document.getElementById("download-button").addEventListener("click", () => {
    var text = document.getElementById("output-text-box").value;
    var filename = document.getElementById('file-label').innerHTML != "Choose Input File!" ? document.getElementById('file-label').innerHTML.split(".")[0] : "text";
    var fileextension = document.getElementById('file-label').innerHTML.split(".")[1] != undefined ? document.getElementById('file-label').innerHTML.split(".")[1] : "txt";
    var downloadname = new Date().toJSON().slice(0, 19).replaceAll("-", "").replaceAll(":", "").replaceAll("T", "_") + "_" + filename + (document.getElementById("right-tab").innerHTML == "Ciphertext" ? "_encrypted." : "_decrypted.") + fileextension;
    download(downloadname, text);
}, false);
