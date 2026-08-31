const logout_btn = document.querySelector('#logout-button')
const delete_btn = document.querySelector('#delete-button')
const freeze_btn = document.querySelector('#freeze-button')

// в случае ошибки(а кнопки не могут быть одновременно не null)
// скрипт блокируется. Тогда нужно проверять на null:
if (logout_btn && logout_btn != 'null' && logout_btn != 'undefined') {
    logout_btn.addEventListener('click', (e) => {
        if (window.confirm('Вы точно хотите выйти из акаунта?')) {
            window.location.href = '/<true>';
        }
    })
}

// если админ, то любой профиль можно удалить/заблокировать/дать модерку
if (delete_btn && delete_btn != 'null' && delete_btn != 'undefined') {
    const freeze_btns = Array.from(document.querySelectorAll('.freeze-buttons'))
    const modal_block = document.querySelector('#modal-block')
    const close_btn = document.querySelector('#close-modal')

    // удаление
    delete_btn.addEventListener('click', (e) => {
        if (!window.confirm('Подтвердите удаление')) {
            e.preventDefault();
        }
    })

    // заблокировать аакаунт
    freeze_btn.addEventListener('click', (e) => {
        modal_block.classList.add('show')
    })
    close_btn.addEventListener('click', (e) => {
        modal_block.classList.remove('show')
    })
    // close_btn.addEventListener('click', (e) => {
    //     e.preventDefault()
    // })
}