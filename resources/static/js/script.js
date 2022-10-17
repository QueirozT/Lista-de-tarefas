// Conteúdo do DOM
const LISTA = document.querySelector('#todo')
const FAZER = document.querySelector('#doing')
const FEITO = document.querySelector('#done')



// Modelos
function InserirModelo(id, header, description, type, priority) {
    div = document.createElement('div')
    div.setAttribute('id', id);
    div.classList.add('terminal-card')
    if (priority) {
        div.classList.add('priority')
    }

    dataHeader = document.createElement('header')
    dataHeader.classList.add('name')
    dataHeader.innerText = header

    dataDescription = document.createElement('div')
    dataDescription.classList.add('description')
    dataDescription.innerText = description

    btns = document.createElement('div')
    btns.classList.add('buttons')
    
    btn01 = document.createElement('button')
        btn01.setAttribute('class', 'btn btn-primary btn-ghost')

        btn02 = document.createElement('button')
        btn02.setAttribute('class', 'btn btn-error btn-ghost')

    switch (type) {
        case 'lista':
            btn01.classList.add('btn-fazer')
            btn01.innerText = 'Fazer'

            btn02.classList.add('btn-cancelar')
            btn02.innerText = 'Cancelar'

            break;

        case 'fazer':
            btn01.classList.add('btn-feito')
            btn01.innerText = 'Pronto'

            btn02.classList.add('btn-voltar')
            btn02.innerText = 'Voltar'

            break;

        case 'feito':
            btn01.classList.add('btn-voltar')
            btn01.innerText = 'Refazer'

            btn02.classList.add('btn-cancelar')
            btn02.innerText = 'Remover'

            break;
    
        default:
            btn01.classList.add('btn-fazer')
            btn01.innerText = 'Fazer'

            btn02.classList.add('btn-cancelar')
            btn02.innerText = 'Cancelar'

            break;
    }

    btns.appendChild(btn01)
    btns.appendChild(btn02)

    div.appendChild(dataHeader)
    div.appendChild(dataDescription)
    div.appendChild(btns)

    switch (type) {
        case 'lista':
            if (LISTA.innerHTML.match(id=id)) {
                return console.error('Modelo já existe')
            }
            
            if (priority) {
                LISTA.insertAdjacentElement("afterbegin", div)
            }
            else {
                LISTA.appendChild(div)
            }
            break;
        case 'fazer':
            if (FAZER.innerHTML.match(id=id)) {
                return console.error('Modelo já existe')
            }
            if (priority) {
                FAZER.insertAdjacentElement("afterbegin", div)
            }
            else {
                FAZER.appendChild(div)
            }
            break;
        case 'feito':
            if (FEITO.innerHTML.match(id=id)) {
                return console.error('Modelo já existe')
            }
            if (priority) {
                FEITO.insertAdjacentElement("afterbegin", div)
            }
            else {
                FEITO.appendChild(div)
            }
            break;
        default:
            return console.error('Tipo não identificado!');
    }
}



// Funções
function ListarTarefas() {
    fetch(location.origin + "/collect", {method: "GET"})
        .then((response) => response.json())
        .then((data) => {
    
            for (obj in data) {
                InserirModelo(
                    data[obj].id,
                    data[obj].title,
                    data[obj].description,
                    data[obj].type,
                    data[obj].priority
                )
            }
        })
        .catch((error) => {
            console.error("Error:", error);
    });
}

function FazerTarefa(obj) {

    fetch(location.origin + "/update/" + obj.id, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({'type': 'fazer'}),
        })
        .then((response) => response.json())
        .then((data) => {

            InserirModelo(
                data.id, 
                data.title, 
                data.description, 
                data.type,
                data.priority
            )
            obj.remove()
        })
        .catch((error) => {
            console.error("Error:", error);
    });
}

function RefazerTarefa(obj) {

    fetch(location.origin + "/update/" + obj.id, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({'type': 'lista'}),
        })
        .then((response) => response.json())
        .then((data) => {

            InserirModelo(
                data.id, 
                data.title, 
                data.description, 
                data.type,
                data.priority
            )
            obj.remove()
        })
        .catch((error) => {
            console.error("Error:", error);
    });
}

function ConcluirTarefa(obj) {

    fetch(location.origin + "/update/" + obj.id, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({'type': 'feito'}),
        })
        .then((response) => response.json())
        .then((data) => {

            InserirModelo(
                data.id, 
                data.title, 
                data.description, 
                data.type,
                false
            )
            obj.remove()
        })
        .catch((error) => {
            console.error("Error:", error);
    });
}

function RemoverTarefa(obj) {

    fetch(location.origin + "/delete/" + obj.id, {method: "DELETE"})
        .then((response) => response.data)
        .then((data) => {

            obj.remove()
        })
        .catch((error) => {
            console.error("Error:", error);
    });
}


// Gatilhos
ListarTarefas()

document.querySelector('#submit').addEventListener('click', (e) => {
    // CRIAR A TAREFA COM O RESPONSE DO POST
    title = document.querySelector('#title')
    description = document.querySelector('#descricao')
    priority = document.querySelector('#priority')
    msg = "Este campo não pode ficar vazio"

    if (title.validity.valueMissing | description.validity.valueMissing) {
        if (title.validity.valueMissing & description.validity.valueMissing) {
            title.placeholder = msg
            description.placeholder = msg
        }
        else {
            if (title.validity.valueMissing) {
                title.placeholder = msg
            }
            else {
                description.placeholder = msg
            }
        }
        return
    }

    // #######################

    const data = { 
        'title': title.value, 
        'description': description.value,
        'type': 'lista',
        'priority': priority.checked
    };

    fetch(location.origin + "/create", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    })
    .then((response) => response.json())
    .then((data) => {
        
    InserirModelo(
        data.id,
        data.title,
        data.description,
        data.type,
        data.priority
    )

    title.value = ''
    title.placeholder = ''
    description.value = ''
    description.placeholder = ''
    priority.checked = false
    })
    .catch((error) => {
        console.error("Error:", error);
    });
})

document.querySelector('#todo').addEventListener('click', function(e) {
    obj = e.target.parentNode.parentNode

    if (e.target.classList.contains('btn-fazer')) {

        // ATUALIZAR O TYPE PARA "FAZER"
        FazerTarefa(obj)
    }
    if (e.target.classList.contains('btn-cancelar')) {

        // REMOVER O OBJETO DO BANCO DE DADOS
        RemoverTarefa(obj)
    }
});

document.querySelector('#doing').addEventListener('click', function(e) {
    obj = e.target.parentNode.parentNode

    if (e.target.classList.contains('btn-feito')) {

        // ATUALIZAR O TYPE PARA "FEITO"
        ConcluirTarefa(obj)
    }
    if (e.target.classList.contains('btn-voltar')) {

        // ATUALIZAR O TYPE PARA "LISTA"
        RefazerTarefa(obj)
    }
});

document.querySelector('#done').addEventListener('click', function(e) {
    obj = e.target.parentNode.parentNode

    if (e.target.classList.contains('btn-voltar')) {

        // ATUALIZAR O TYPE PARA "LISTA"
        FazerTarefa(obj)        
    }
    if (e.target.classList.contains('btn-cancelar')) {

        // REMOVER O OBJETO DO BANCO DE DADOS
        RemoverTarefa(obj)
    }
});
