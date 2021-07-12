function sharedwithme(event) {
    if (event.dataset.url == 'null') return

    // create request OBJ
    const request = new XMLHttpRequest();

    // make request
    request.open("GET", event.dataset.url)
    
    let template = Handlebars.compile(blueHTML);
    // Get reqult of request made
    request.onload = ()=>{
        let response = JSON.parse(request.responseText)
        event.dataset.url = response['next']
        console.log(response["results"])
        document.querySelector("#filesplace").innerHTML += template({"files":response["results"]})
    }

    // Send request
    request.send()


}

function myfiles(event) {
    if (event.dataset.url == 'null') return

    // create request OBJ
    const request = new XMLHttpRequest();

    // make request
    request.open("GET", event.dataset.url)
    
    let template = Handlebars.compile(myfilesHTML);
    // Get reqult of request made
    request.onload = ()=>{
        let response = JSON.parse(request.responseText)
        event.dataset.url = response['next']
        document.querySelector("#myfiles").innerHTML += template({"files":response["results"]})
    }

    // Send request
    request.send()

}

function shareWith(event) {
    // create request OBJ
    const request = new XMLHttpRequest();
    let id = document.getElementById("recipient-name").value
    let username = document.getElementById("recipient-user").value
    let perm = document.getElementById("recipient-perm").value
    let csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    if (!username || !id || !perm || !csrf) {
        window.location.reload()
        return
    }
    let btn = document.getElementById("sharebtn") 
    delete btn.dataset.dismiss;
    btn.innerHTML = "Share"

    let url = "/api/files/"+id+"/shareWith/"
    console.log(url)
    // make request
    request.open("POST", url)
    
    let template = Handlebars.compile(myfilesHTML);
    // Get reqult of request made
    request.onload = ()=>{
        let response = JSON.parse(request.responseText)
        
        if (request.status == 200) {
            btn.innerHTML = "File Shared"        
            btn.dataset.dismiss="modal"
            btn.onclick = ()=>{
                btn.onclick = event => {shareWith(event)}

            };
        }
        else {
            btn.innerHTML = "Try Again"        
            delete btn.dataset.dismiss;
            btn.onclick = event => {shareWith(event)}
        }
    }

    const data = new FormData();
    data.append("file", id);
    data.append("username", username);
    data.append("perm", Boolean(perm=="1"));
    data.append("csrfmiddlewaretoken", csrf);

    // Send request
    request.send(data)
};

function upload(event) {
    const request = new XMLHttpRequest();
    let name = document.getElementById("file-name").value
    let description = document.getElementById("file-desc").value
    let file = document.getElementById("file-file").files[0];
    let csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    if (!name || !description || !file || !csrf) {
        window.location.reload()
        return
    }
    
    // make request
    request.open("POST", "/api/files/")
    
    // Get reqult of request made
    request.onload = ()=>{
        let response = JSON.parse(request.responseText)
        console.log(request.status)
        if (request.status == 201) {
            window.location.reload()

        } else {
            console.log(response)
        }
    }

    const data = new FormData();
    data.append("file", file);
    data.append("desc", description);
    data.append("name", name);
    data.append("csrfmiddlewaretoken", csrf);

    // Send request
    request.send(data)
}

function editcommentbtn(id, action=false) {
    if (action) {
        document.querySelector("#cm_"+id).type = "hidden";
        document.querySelector("#cmc_"+id).type = "hidden";
        document.querySelector("#edit_"+id).onclick = ()=>{
            editcommentbtn(id)
        }
    }
    else {
        document.querySelector("#cm_"+id).type = "text";
        document.querySelector("#cmc_"+id).type = "button";
        document.querySelector("#edit_"+id).onclick = ()=>{
            commentmanager(`${id}`)
        }
    }
    
    
}

function commentmanager(cmid=false, method="PUT", message=false) {
    if (!cmid)  return
    
    const request = new XMLHttpRequest();
    let csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    // make request
    request.open(method, "/api/comments/"+cmid+"/")
    request.setRequestHeader("X-CSRFToken", csrf)
    // Get reqult of request made
    request.onload = ()=>{
        let response = JSON.parse(request.responseText)
        console.log(response)
        if (request.status == 200) {
            window.location.reload()
        } else {
            editcommentbtn(cmid, "cancel")
        }
    }

    const data = new FormData();
    if (method == "PUT") {
        message=document.querySelector("#cm_"+cmid).value;
        data.append("text", message)
    }
    // Send request
    request.send(data)

}
let blueHTML = `
            {{#each files}}
                <div class="media text-muted pt-3">
                <a href="/detail/{{this.id}}"> <img src="/static/core/img/file.png" style="width:35px; height:35px;" alt="" class="mr-2 rounded"> </a>
                    <p class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">
                    <strong class="d-block text-gray-dark">{{this.name}}</strong>
                    @{{this.username}}
                    <br/><br/>
                    {{this.desc}}
                    </p>
                </div>
            {{/each}}    
            `
let myfilesHTML = `
            {{#each files}}
                <div class="media text-muted pt-3">
                <a href="/detail/{{this.id}}"> <img src="/static/core/img/file.png" style="width:35px; height:35px;" alt="" class="mr-2 rounded"> </a>
                <div class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">
                <div class="d-flex justify-content-between align-items-center w-100">
                    <strong class="text-gray-dark">{{this.name}}</strong>

                    <div>
                        <a href="javascript:;" > <img src="/static/core/img/shared.png" style="width:35px; height:35px;" alt="" class="mr-2 rounded"> </a>
                        <a href="javascript:;" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal" data-whatever="{{this.id}}">Share</a>
                        </div>
                </div>
                <span class="d-block">@{{this.username}}</span>
                </div>
                </div>
            {{/each}}`
// Start onload
document.addEventListener("DOMContentLoaded", ()=>{

    try {
        document.getElementById("morefiles").click();
        document.getElementById("moremyfiles").click();
    } catch (error) {
        
    }

 })

