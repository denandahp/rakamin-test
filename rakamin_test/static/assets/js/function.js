function dropdown(data) {
    var length_data = data.length
    var checkBox = document.getElementById(data[0]);
    for (let i=1;i<=length_data-1;i++){
      var text = document.getElementById(data[i]);
      text.style.display = (checkBox.checked == true) ? "block" : "none";
    }
  }
