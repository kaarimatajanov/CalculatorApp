Руководство по настройке config.json
Описание
Файл config.json в папке SimpleCalculatorMVVM/ используется для настройки параметров калькулятора, включая размер окна, цвета, шрифты, звук, анимацию и стили.
Структура config.json
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
    }
  },
  "active_style": "default"
}

Описание ключей

window: Размер окна (ширина, высота).
background_color: Цвет фона окна (hex).
font: Шрифт для текста (название, размер).
sound_enabled: Включение/выключение звука кнопок (true/false).
animation: Размер анимации (animation.gif).
styles: Набор стилей (фон, кнопки, операторы, текст).
active_style: Активный стиль (ключ из styles).

Настройка

Откройте SimpleCalculatorMVVM/config.json.
Измените значения, например:
Смените active_style на другой стиль.
Измените background_color на #e0e0e0.
Установите sound_enabled: false для отключения звука.


Сохраните файл и перезапустите калькулятор:python3 SimpleCalculatorMVVM/view.py



Обработка ошибок

Если config.json отсутствует или содержит ошибки, используется конфигурация по умолчанию.
Логи ошибок записываются в SimpleCalculatorMVVM/calculator.log.

Пример изменения стиля
Добавьте новый стиль в styles:
"dark": {
  "background_color": "#333333",
  "button_color": "#555555",
  "operator_color": "#ff9500",
  "special_color": "#ff3b30",
  "text_color": "#ffffff",
  "font_size": 12
}

Установите "active_style": "dark" и перезапустите калькулятор.
