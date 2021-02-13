patterns = [
    {
        "pattern": "[^A-Za-z0-9]",
        "description": "remove special characters"
    },
    {
        "pattern": "\\D",
        "description": "not digits"
    },
    {
        "pattern": "\\[.*?\\]",
        "description": "match square brackets and contents it encloses"
    }
]

function copyText(idToCopy) {
    var value = document.getElementById(idToCopy).innerHTML;

    // create temp input (can only select on 'input' elements)
    var tempInput = document.createElement("input");
    tempInput.value = value;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand("copy");
    document.body.removeChild(tempInput);

    showSnackBar(`copied to clipboard: ${value}`);
  }

function showSnackBar(message) {
    //  https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_snackbar
    var x = document.getElementById("snackbar");
    x.innerHTML = message;
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

document.addEventListener("DOMContentLoaded", function(event) {
    var table = document.getElementById('pattern-table').getElementsByTagName('tbody')[0];

    for (i = 1, len = patterns.length; i <= len; i++) {
        // insert row for #
        var row = table.insertRow();
        var cell = row.insertCell();
        cell.innerHTML = i;

        // 2nd and 3rd column: pattern and notes
        var patt = patterns[i-1];
        for (var key in patt) {
            cell = row.insertCell();
            cell.innerHTML = patt[key];
            // add id to cell if current item is pattern (for copying)
            if (key=="pattern") {
                cell.id=`pattern${i}`
            };
        }
        // insert copy button column
        cell = row.insertCell();
        cell.innerHTML += `<button class="btn btn-outline-secondary" alt="copy" onclick=copyText(\"pattern${i}\")><i class="bi bi-stickies"></i></button>`
    };
});
