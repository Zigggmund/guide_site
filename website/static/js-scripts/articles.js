const color_main = getComputedStyle(document.body).getPropertyValue('--title-main')
const color_header_footer = getComputedStyle(document.body).getPropertyValue('--header-footer')
const color_main_dark = getComputedStyle(document.body).getPropertyValue('--dark-main')

const back_btn = document.querySelector('#back-btn')
const write_comm_btn = document.querySelector('#write-comm-button')
const delete_buttons = Array.from(document.querySelectorAll('.exit-btn'))

back_btn.addEventListener('click', (e) => {
    // через onclick строку не передать
    window.location.href = window.location.href + '/ads<date>'
})

write_comm_btn.addEventListener('click', (e) => {
    let parent = e.target.parentElement.parentElement
    e.target.firstChild.data = (e.target.firstChild.data == 'Отменить написание комментария') ? 'Написать комментарий': 'Отменить написание комментария';

    if (! parent.nextElementSibling) {
        e.target.style.backgroundColor = color_main_dark
        let form = document.createElement('form')
        form.style.backgroundColor = color_main
        // form.action = window.location.href
        form.method = 'POST'
        form.style.border = '2px solid ' + color_header_footer
        form.style.marginTop = '40px'

        let fields = document.createElement('section')
        fields.innerHTML = `
            <input name='comment_rate' type="text" class="form-control bg-custom-bright" placeholder="Введите оценку от 1 до 10(или оставьте это поле пустым)">
            <input name='comment_text' type="textarea" class="form-control bg-custom-bright" placeholder="Введите комментарий">
        `
        
        let submit_btn = document.createElement('section')
        submit_btn.innerHTML = `
            <button class='send_comment_btn' type='submit' name='submit_button' value='write-comm'>Отправить комментарий</button>
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

// кнопки удаления
delete_buttons.forEach((el) => {
    el.addEventListener('click', function(e) {
        if (! window.confirm('Подтвердите удаление')) {
            e.preventDefault()
        }
    })
})