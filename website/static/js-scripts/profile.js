const logout_btn = document.querySelector('#logout-button')
const delete_btn = document.querySelector('#delete-button')

// в случае ошибки(а кнопки не могут быть одновременно не null)
// скрипт блокируется. Тогда нужно проверять на null:
if (logout_btn && logout_btn != 'null' && logout_btn != 'undefined') {
    logout_btn.addEventListener('click', (e) => {
        if (window.confirm('Вы точно хотите выйти из акаунта?')) {
            window.location.href = '/<true>';
        }
    })
}

if (delete_btn && delete_btn != 'null' && delete_btn != 'undefined') {
    delete_btn.addEventListener('click', (e) => {
        if (!window.confirm('Подтвердите удаление')) {
            e.preventDefault()
        }
    })
}