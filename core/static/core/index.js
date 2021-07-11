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
        console.log("My Files", response)
        document.querySelector("#myfiles").innerHTML += template({"files":response["results"]})
    }

    // Send request
    request.send()

}
let blueHTML = `
            {{#each files}}
                <div class="media text-muted pt-3">
                <img src="/static/core/img/file.png" style="width:35px; height:35px;" alt="" class="mr-2 rounded">
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
                <img src="/static/core/img/file.png" style="width:35px; height:35px;" alt="" class="mr-2 rounded">                <div class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">
                <div class="d-flex justify-content-between align-items-center w-100">
                    <strong class="text-gray-dark">{{this.name}}</strong>
                    <a href="#">Share</a>
                </div>
                <span class="d-block">@{{this.username}}</span>
                </div>
                </div>
            {{/each}}`
// Start onload
document.addEventListener("DOMContentLoaded", ()=>{
    document.getElementById("morefiles").click();
    document.getElementById("moremyfiles").click();
 })