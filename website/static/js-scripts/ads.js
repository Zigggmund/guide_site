const color_dark_main = getComputedStyle(document.body).getPropertyValue('--dark-main')
const color_main = getComputedStyle(document.body).getPropertyValue('--title-main')
const color_dark_green = getComputedStyle(document.body).getPropertyValue('--guide-dark')
const color_bright_green = getComputedStyle(document.body).getPropertyValue('--guide-bright')
const color_header_footer = getComputedStyle(document.body).getPropertyValue('--header-footer')

const back_btn = document.querySelector('#back')
const open_comments = Array.from(document.querySelectorAll('.read-comms-button'))
const sort_buttons = Array.from(document.querySelectorAll('input[type=radio]'))
const write_ad_btn = document.querySelector('#write-ad-button');
const write_comm_buttons = Array.from(document.querySelectorAll('.write-comm-button'))
const delete_buttons = Array.from(document.querySelectorAll('.exit-btn, .exit-btn-ad'))

// переход на статью
back_btn.addEventListener('click', () => {
    window.location.href = window.location.href.substring(0, window.location.href.lastIndexOf('/'))
})

// Посмотреть комментарии
open_comments.forEach((el) => {
    // начальная настройка
    // transition не работает
    el.parentElement.parentElement.nextElementSibling.style.transition = '2s';
    let children = Array.from(el.parentElement.parentElement.nextElementSibling.children)
    children.forEach((el) => {
        el.style.display = 'none'
    })

    el.addEventListener('click', function(e) {
        let parent = e.target.parentElement.parentElement
        let children = Array.from(parent.nextElementSibling.children)

        if (children[0].style.display == 'block') {
            children.forEach((el) => {
                el.style.display = 'none'
            })
            e.target.style.background = color_main;
        } else {
            children.forEach((el) => {
                el.style.display = 'block'
            })
            e.target.style.background = color_dark_main;
        }
}) 
})

// сортировка
sort_buttons.forEach((el) => {
    el.addEventListener('click', function(e) {
        let location = window.location.href.substring(0, window.location.href.lastIndexOf('/')) + '/ads'
        window.location.href = location + '<'+e.target.value+'>'
    })
})

// КНОПКА НАПИСАТЬ ОБЪЯВЛЕНИЕ
if (write_ad_btn != null) {// проверка на гида
    write_ad_btn.addEventListener('click', (e) => {
        let parent = e.target.parentElement.parentElement
        e.target.firstChild.data = (e.target.firstChild.data == 'Отменить написание объявления') ? 'Оставить объявление': 'Отменить написание объявления';
        if (e.target.firstChild.data == 'Отменить написание объявления') {
            e.target.style.backgroundColor = color_dark_green
            let form = document.createElement('form')
            form.style.backgroundColor = color_bright_green
            form.method = 'POST'
            form.style.border = '2px solid ' + color_header_footer
            form.style.marginBottom = '60px'
    
            let fields = document.createElement('section')
            fields.innerHTML = `
                <input name='ad_text' type="text" class="form-control bg-custom-bright" placeholder="Введите текст обявления">
            `
            
            let submit_btn = document.createElement('section')
            submit_btn.innerHTML = `
                <button class='send_comment_btn' name='submit_button' value="guide" type='submit'>Отправить объявление</button>
            `
            submit_btn.style.marginTop = '20px'
    
    
            parent.after(form)
            form.appendChild(fields)
            form.appendChild(submit_btn)
        } else {
            e.target.style.backgroundColor = color_bright_green
            parent.nextElementSibling.remove()
        }
    })
}

// КНОПКИ НАПИСАТЬ КОММЕНТАРИЙ
write_comm_buttons.forEach((el) => {
    el.addEventListener('click', function(e) {
        let parent = e.target.parentElement.parentElement
        e.target.firstChild.data = (e.target.firstChild.data == 'Отменить написание комментария') ? 'Написать комментарий': 'Отменить написание комментария';
        console.log(parent.nextElementSibling)
        if (! parent.nextElementSibling) {
            e.target.style.backgroundColor = color_dark_main
            let form = document.createElement('form')
            form.style.backgroundColor = color_main
            // form.action = window.location.href
            form.method = 'POST'
            form.style.border = '2px solid ' + color_header_footer
            form.style.marginTop = '40px'

            let ad_id = parent.id.substring(3, parent.id.length)

            let fields = document.createElement('section')
            fields.innerHTML = `
                <input name='comment_rate`+ad_id+`' type="text" class="form-control bg-custom-bright" placeholder="Введите оценку от 1 до 10(ОБЯЗАТЕЛЬНО для заполнения)">
                <input name='comment_text`+ad_id+`' type="textarea" class="form-control bg-custom-bright" placeholder="Введите комментарий">
            `
            
            let submit_btn = document.createElement('section')
            submit_btn.innerHTML = `
                <button class='send_comment_btn' name='submit_button' value='write`+ad_id+`' type='submit'>Отправить комментарий</button>
            `
            submit_btn.style.marginTop = '20px'


            parent.after(form)
            form.appendChild(fields)
            form.appendChild(submit_btn)
        } else {
            e.target.style.backgroundColor = color_main
            parent.nextElementSibling.remove()
        }
    })
})

// кнопки удаления
delete_buttons.forEach((el) => {
    el.addEventListener('click', function(e) {
        if (! window.confirm('Подтвердите удаление')) {
            e.preventDefault()
        }
    })
})