
var client_id = '863e4af9e14c4748be4d638fad066a68';
var redirect_uri = 'https://rajbirsingh.pythonanywhere.com/callback'
var fetchurl = 'https://rajbirsingh.pythonanywhere.com/get_recs?limit=5'
function test(event) {
    let button = document.getElementById("getRecsButton")
    alert("You pressed a button!")
}

var generateRandomString = function(length) {
  var text = '';
  var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

  for (var i = 0; i < length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
};

function getRecommendations() {
    fetch(fetchurl).then(function (response) {
        if (response.ok) {
            return response.json()
        }

        return Promise.reject("ASDFASDFASDFASDF");
    }).then(function(json) {
        htmlout = ""
        for (var i = 0; i < json.length; i++) {
            htmlout += "<li>" + json[i].name + "</li>";
        }
        document.getElementById("recommendationHolder").innerHTML = htmlout
    }).catch(function(error) {
        alert("An error occurred: ", error)
    })
}

function startLoginFlow() {

    var params = {
        scope: 'user-read-recently-played playlist-modify-public playlist-modify-private playlist-read-private user-read-private user-read-email',
        response_type: 'code',
        client_id: client_id,
        redirect_uri: redirect_uri,
        state: generateRandomString(16)
    }

    var queryString = Object.keys(params).map((key) => {
        return encodeURIComponent(key) + '=' + encodeURIComponent(params[key])
    }).join('&');
    var base = 'https://accounts.spotify.com/authorize?'
    window.location.replace(base + queryString);
}