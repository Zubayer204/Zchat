function changeTab(evt, cityName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    // get all the input fields
    let j_name = document.getElementById("j_name")
    let j_room = document.getElementById("j_room")
    let j_password = document.getElementById("j_password")
    let c_name = document.getElementById("c_name")
    let c_room = document.getElementById("c_room")
    let c_password = document.getElementById("c_password")

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
    inp_hidden = document.getElementById('action');
    if (inp_hidden.value == 'Join'){
        inp_hidden.value = 'Create'
        c_name.required = true
        c_room.required = true
        c_password.required = true
        j_name.required = false
        j_room.required = false
        j_password.required = false
    } else {
        inp_hidden.value = 'Join'
        c_name.required = false
        c_room.required = false
        c_password.required = false
        j_name.required = true
        j_room.required = true
        j_password.required = true
    }
}

document.getElementById("default").click();

let form = document.getElementById("form")

String.prototype.toCamelCase = function() {
    return this.replace(/\b(\w)/g, function(match, capture) {
        return capture.toUpperCase();
    })
}

let handleSubmit = async (e) => {
    e.preventDefault()
    let j_room = document.getElementById('j_room').value.toUpperCase()
    let j_name = document.getElementById('j_name').value.toCamelCase()
    let j_password = document.getElementById('j_password').value
    let c_room = document.getElementById('c_room').value.toUpperCase()
    let c_name = document.getElementById('c_name').value.toCamelCase()
    let c_password = document.getElementById('c_password').value
    let action = e.target.action.value

    let real_room = (j_room == "") ? c_room : j_room
    let real_name = (j_name == "") ? c_name : j_name

    let response = await fetch(`/get_token/?channel=${real_room}`)
    let data = await response.json()

    if (action == "Join"){
        let res = await fetch('enter_room/', {
            method: 'POST',
            headers: {
                'content-Type': 'application/json'
            },
            body:JSON.stringify({'room_name': j_room, 'name': j_name, 'password': j_password, 'UID': data.uid})
        })
        let d = await res.json()
        if(d.error){
            let error_span = document.getElementById("error_j")
            error_span.style.display = 'block'
            error_span.innerText = d.message
            return
        }
    } else if(action == "Create"){
        let res = await fetch('create_room/', {
            method: 'POST',
            headers: {
                'content-Type': 'application/json'
            },
            body:JSON.stringify({'room_name': c_room, 'password': c_password, 'UID': data.uid, 'name': c_name})
        }) 
        let d = await res.json()
        if(d.error){
            let error_span = document.getElementById("error_c")
            error_span.style.display = 'block'
            error_span.innerText = d.message
            return
        }
    }

    let UID = data.uid
    let token = data.token

    sessionStorage.setItem('UID', UID)
    sessionStorage.setItem('token', token)
    sessionStorage.setItem('room', real_room)
    sessionStorage.setItem('name', real_name)

    window.open("/room/", '_self')
}

form.addEventListener('submit', handleSubmit)