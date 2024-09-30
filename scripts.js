document.addEventListener('DOMContentLoaded', function () {
    // Получаем все кнопки показа/скрытия паролей
    const togglePasswordButtons = document.querySelectorAll('.show-password');

    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Найдем поле пароля рядом с кнопкой
            const passwordField = this.previousElementSibling;

            // Проверим тип поля и изменим его
            if (passwordField.type === 'password') {
                passwordField.type = 'text';  // Показываем пароль
            } else {
                passwordField.type = 'password';  // Скрываем пароль
            }
        });
    });
});
