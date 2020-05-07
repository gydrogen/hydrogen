const fetch = require("node-fetch");

async function getData() {
    // the url we fetch best repos from
    // this url fetches the best swift repos
    let url = 'https://api.github.com/search/repositories?q=language:swift+sort:stars'
    let response = await fetch(url,
                          {
                              headers: {
                                  authorization: "token 6666bbf3eafa1d6b8b76a8744fb6af7621d921a3"
                              }
                          });

    let jsonData = await response.json();

    // listOfRepos contains urls of repos
    var listOfRepos = [];
    var i;
    for (i = 0; i < jsonData.items.length; i++) {
        listOfRepos.push(jsonData.items[i].url);
    }

    // for each repo url in "listOfRepos", get specific commits
    for (i = 0; i < listOfRepos.length; i++) {
        console.log(listOfRepos[i] + '/commits' + ' ~~~~~~~~~~~~')
        await getCommits(listOfRepos[i])
        console.log("****************************************")
    }
}

async function getCommits(repoURL) {
    // fetch commits and jsonData is a json object of all commits
    let response = await fetch(repoURL + '/commits',
                              {
                                  headers: {
                                      authorization: "token 6666bbf3eafa1d6b8b76a8744fb6af7621d921a3"
                                  }
                              });

    let jsonData = await response.json();

    /**
    Now, iterate through the commits and find the ones that contain
    a fix to a bug
    **/

    // fixCommitsId is an array of commit sha that refer to fixed bugs/issues
    var fixCommitsId = [];
    var commitMessages = [];

    // these are the words we look for in commit messages
    var words = ["Fix", "fix"];

    // checking each commit message for the special words
    var i;
    var j;

    for (i = 0; i < jsonData.length; i++) {
        var message = jsonData[i].commit.message;
        for (j = 0; j < words.length; j++) {
            // console.log(j)
            if (message.indexOf(words[j]) != -1) {
                // if a special word like "Fix" is in the commit message
                // save the commit sha for analysis
                fixCommitsId.push(jsonData[i].sha);
                commitMessages.push(jsonData[i].commit.message);
                break;
            }
        }
    }

    // print out commit sha
    for (i = 0; i < fixCommitsId.length; i++) {
        console.log(commitMessages[i])
        console.log(fixCommitsId[i]);
        console.log("\n\n")

    }
}

getData()
