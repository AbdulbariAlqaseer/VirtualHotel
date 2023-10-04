
function compare_address()
{
    var address_input = document.getElementById('staff address input');
    var address = address_input.value;

    console.log(address);
    const data = {
        new_address:address,
        id:id
    };

    fetch('',{method: 'POST', body: JSON.stringify(data) , redirect: 'follow'}).then(response =>{
        console.log(response.status)
    });

    var massage = document.createTextNode('Staff Updated Succesfully');
    var p = document.createElement('p');
    p.appendChild(massage);
    p.style.color = 'green';

    body = document.getElementsByTagName('body');
    body[0].appendChild(p);


    //window.location.assign("")
    /*var staff_id = document.createElement('input');
    var staff_form = document.getElementById('staff form');
    staff_id.setAttribute('type','text');
    staff_id.setAttribute('name','update id');
    staff_id.setAttribute('value',id)
    staff_form.appendChild(staff_id);*/
}