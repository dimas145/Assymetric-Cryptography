var select_key = document.getElementById("select-algorithm-keys")

change_config_key_form(1);

select_key.addEventListener('change', () => {
    console.log("TEST");
    change_config_key_form(select_key.value);
});

function change_config_key_form(id) {
    var request = new XMLHttpRequest();
    var result = document.getElementById('key-setting-form-dynamic');

    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            result.innerHTML = this.responseText;
        }
    }

    request.open('POST', '/key-form', true);
    request.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    request.send("algorithm_id=" + id);
}

function execute_key() {
    var request = new XMLHttpRequest();
    var p_val = document.getElementById("p-value").value;
    var q_val = document.getElementById("q-value").value;
    var keys = p_val + " " + q_val;

    var type = select_key.value;

    if (type == 1) {
        var e_val = document.getElementById("e-value").value;
        keys += " " + e_val
    }

    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var result = this.responseText;
            var result_list = result.split(" ");
            console.log(result);

            if (type == 1) {
                var filename = "rsa";
                var downloadname = new Date().toJSON().slice(0, 19).replaceAll("-", "").replaceAll(":", "").replaceAll("T", "_") + "_" + filename;
                var private_key = result_list[1] + " " + result_list[2];
                var public_key = result_list[0] + " " + result_list[2];
                download(downloadname + ".pri", private_key);
                download(downloadname + ".pub", public_key);
            }
        }
    }

    request.open('POST', '/generate-keys', true);
    request.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    request.send("keys=" + keys + "&type=" + type);
}
