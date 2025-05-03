Руководство по использованию конфигурационного файла
Описание
Конфигурационный файл SimpleCalculatorMVVM/config.json используется для настройки параметров оконного приложения SimpleCalculatorMVVM. Формат файла — JSON. Файл позволяет изменять внешний вид, размеры окна, шрифт, звук и стили интерфейса без перекомпиляции кода.
Структура файла
Файл содержит следующие параметры:

window:
width (int): Ширина окна (например, 500).
height (int): Высота окна (например, 750).


background_color (string): Цвет фона окна в формате HEX (например, "#f0f0f0").
font:
name (string): Название шрифта (например, "Helvetica").
size (int): Размер шрифта (например, 12).


sound_enabled (boolean): Включение/выключение звука (true или false).
animation:
width (int): Ширина анимации (например, 100).
height (int): Высота анимации (например, 50).


styles: Объект с различными стилями интерфейса:
default: Стандартный стиль.
high_contrast_light: Светлый режим для слабовидящих.
high_contrast_dark: Темный режим для слабовидящих.
male: Мужской стиль.
female: Женский стиль.
kids: Стиль для детей.
youth: Стиль для молодежи.
middle_age: Стиль для среднего возраста.
elderly: Стиль для пожилых.
Каждый стиль содержит:
background_color (string): Цвет фона.
button_color (string): Цвет кнопок цифр.
operator_color (string): Цвет кнопок операторов.
special_color (string): Цвет специальных кнопок ("C", "⌫", "CH").
text_color (string): Цвет текста.
font_size (int): Размер шрифта.




active_style (string): Имя активного стиля (например, "default").

Пример конфигурационного файла
{
  "window": {
    "width": 500,
    "height": 750
  },
  "background_color": "#f0f0f0",
  "font": {
    "name": "Helvetica",
    "size": 12
  },
  "sound_enabled": true,
  "animation": {
    "width": 100,
    "height": 50
  },
  "styles": {
    "default": {
      "background_color": "#f0f0f0",
      "button_color": "#d9d9d9",
      "operator_color": "#ff9500",
      "special_color": "#ff3b30",
      "text_color": "#000000",
      "font_size": 12
    },
    "high_contrast_dark": {
      "background_color": "#333333",
      "button_color": "#555555",
      "operator_color": "#ffaa00",
      "special_color": "#ff5555",
      "text_color": "#ffffff",
      "font_size": 14
    }
  },
  "active_style": "default"
}

Инструкции по изменению настроек

Откройте SimpleCalculatorMVVM/config.json в текстовом редакторе.
Измените параметры:
Для изменения размера окна: Измените window.width и window.height.
Для изменения фона: Измените background_color или styles.<style>.background_color.
Для смены стиля: Измените active_style на имя стиля (например, "high_contrast_dark").
Для отключения звука: Установите sound_enabled в false.
Для изменения анимации: Измените animation.width и animation.height.


Сохраните файл.
Перезапустите приложение:python3 SimpleCalculatorMVVM/view.py



Обработка ошибок

Если config.json не найден, приложение использует настройки по умолчанию и показывает предупреждение.
Если формат JSON неверный, выводится сообщение об ошибке, и используются настройки по умолчанию.
Если отсутствуют обязательные ключи, приложение переключается на конфигурацию по умолчанию.
Ошибки записываются в SimpleCalculatorMVVM/calculator.log.

Эффекты изменений

Размер окна: Изменение window.width/height меняет размер окна.
Цвет фона: Изменение background_color или styles.<style>.background_color меняет фон окна и элементов.
Шрифт: Изменение font.name/styles.<style>.font_size меняет шрифт кнопок и текста.
Звук: sound_enabled: false отключает звук для всех кнопок.
Стили: Переключение active_style меняет цвета и шрифт для соответствия стилю (например, "kids" — яркие цвета, крупный шрифт).
Анимация: Изменение animation.width/height меняет размер animation.gif.

Примеры использования

Для слабовидящих: Установите active_style: "high_contrast_dark" для темного режима с крупным шрифтом.
Для детей: Установите active_style: "kids" для ярких цветов и шрифта 16.
Для отключения звука: Установите sound_enabled: false.
Для изменения размера окна: Установите window.width: 600, window.height: 800.

Замечания

Убедитесь, что цвета указаны в формате HEX (#RRGGBB).
Шрифт (font.name) должен быть доступен в системе (например, "Helvetica", "Arial").
Файл config.json должен находиться в папке SimpleCalculatorMVVM.

