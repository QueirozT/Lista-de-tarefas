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

/* COMANDOS USADOS PARA GERAR OS 3 TIPOS DE LISTA:

InserirModelo(1, 'Modelo Lista', 'Lorem ipsum dolor sit amet consectetur adipisicing elit.', 'lista')

InserirModelo(1, 'Modelo Fazer', 'Lorem ipsum dolor sit amet consectetur adipisicing elit.', 'fazer')

InserirModelo(1, 'Modelo Feito', 'Lorem ipsum dolor sit amet consectetur adipisicing elit.', 'feito')
*/

// Funções
var cont = 5
function CriarTarefa() {
    InserirModelo(
        cont,
        document.querySelector('#title').value,
        document.querySelector('#descricao').value,
        'lista',
        document.querySelector('#priority').checked
    )
    cont++
}

function FazerTarefa(obj) {
    id = obj.id
    title = obj.children[0].innerText
    description = obj.children[1].innerText
    priority = obj.classList.contains('priority')

    InserirModelo(id, title, description, 'fazer', priority)
    obj.remove()
}

function RefazerTarefa(obj) {
    id = obj.id
    title = obj.children[0].innerText
    description = obj.children[1].innerText
    priority = obj.classList.contains('priority')

    InserirModelo(id, title, description, 'lista')
    obj.remove()
}

function ConcluirTarefa(obj) {
    id = obj.id
    title = obj.children[0].innerText
    description = obj.children[1].innerText
    InserirModelo(id, title, description, 'feito')
    obj.remove()
}


// Gatilhos
document.querySelector('#submit').addEventListener('click', (e) => {
    CriarTarefa()
})

document.querySelector('#todo').addEventListener('click', function(e) {
    id = e.target.parentNode.parentNode.getAttribute('id')
    obj = e.target.parentNode.parentNode

    console.log('ID = ', id)
    console.log('OBJ = ', obj)

    if (e.target.classList.contains('btn-fazer')) {
        console.log('botão Fazer')

        FazerTarefa(obj)
    }
    if (e.target.classList.contains('btn-cancelar')) {
        console.log('botão Cancelar')
        obj.remove()
    }
});

document.querySelector('#doing').addEventListener('click', function(e) {
    id = e.target.parentNode.parentNode.getAttribute('id')
    obj = e.target.parentNode.parentNode

    console.log('ID = ', id)
    console.log('OBJ = ', obj)

    if (e.target.classList.contains('btn-feito')) {
        console.log('botão Pronto')

        ConcluirTarefa(obj)
    }
    if (e.target.classList.contains('btn-voltar')) {
        console.log('botão Voltar')

        RefazerTarefa(obj)
    }
});

document.querySelector('#done').addEventListener('click', function(e) {
    id = e.target.parentNode.parentNode.getAttribute('id')
    obj = e.target.parentNode.parentNode

    console.log('ID = ', id)
    console.log('OBJ = ', obj)

    if (e.target.classList.contains('btn-voltar')) {
        console.log('botão Refazer')

        FazerTarefa(obj)        
    }
    if (e.target.classList.contains('btn-cancelar')) {
        console.log('botão Remover')

        obj.remove()
    }
});
