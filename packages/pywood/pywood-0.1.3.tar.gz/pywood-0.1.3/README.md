# PROJECT STATUS: DEVELOPMENT
## Что такое pytelegrambots?
pytelegrambots - *легковесный* фреймворк для создания ботов для телеграма.

## Содержание
  * [Установка](#installation)
  * [Общее описание](#description)
  * [Использование](#using)
  * [API](#api)
  * [Пример создания бота](#example)
  * [Получение помощи](#help)
  * [Помощь в разработке](#contributing)
  * [Лицензия](#license)
## Установка<a name="installation"></a>
```
pip install pytelegrambots
```
## Общее описание<a name="description"></a>

## Использование<a name="using"></a>
Для того, что бы создать бота, используя pytelegrambots вы должны:
## API<a name="api"></a>
### Класс FSM
### События
|   Состояние | Описание |
| ------------- | ------------- |
| `IncomingCommandEvent` | Update есть число |
| `IncomingStartCommandEvent` | Update есть команда /start |
| `IncomingHelpCommandEvent` | Update есть команда /help |
| `IncomingNumberEvent` | Update есть число |
| `IncomingStrictNumberEvent` | Update есть число |
| `IncomingTextEvent` | Update есть текст |
| `IncomingStrictTextEvent` | Update есть строгий текст |
| `IncomingSinglePhotoEvent` | Update есть единичное фото|
### Реализация собственных классов событий
Для того, что бы создать свой класс события, необходимо:
1. Создать класс, унаследованный от класса `eventlib.UpdateEvent`
2. Реализовать метод `happened()`. Метод должен принимать в качестве аргумента объект класса [Update](https://core.telegram.org/bots/api#update), и возвращать `True` или `False`, в зависимости от того определяет ли `update` данное событие или нет.
Пример:
cdferfre
## Пример создания бота<a name="example"></a>
  * [Формулировка задачи](#example-formulation)
  * [Предварительная подготовка](#example-preliminaries)
  * [Диаграмма состояний](#example-diagram)
  * [Создание пользовательского события](#example-user-event-creation)
### Формулировка задачи<a name="example-formulation"></a>
Создадим примитивного бота для доставки пиццы. 
Сформулируем, что бот должен делать.  

Сначала бот приветствует пользователя. 
После приветствия, бот просит написать какую пиццу же``лает клиент. (pizza_type: str)  
Потом бот просит указать количество пицц. (quantity: int)  
Потом посредством клавиатуры просит указать способ получения пиццы клиентом: самовывоз или доставка курьером. (delivery_type: str)    
Если самовывоз, бот присылает собеседнику сообщение "Пицца {pizza_type} в количестве {quantity} будет готова через 15 минут. Номер заказа {chat_id}}"  
Если клиент выбрал доставку курьером, "Пиццу {pizza_type} в количестве {quantity} курьер привезет через 45 минут." 
### Предварительная подготовка<a name="example-preliminaries></a>
Создайте бота при помощи @botfather и получите токен.
### Диаграмма состояний<a name="example-diagram"></a>
Дадим названия состояниям, в которым может находиться чат пользователя с ботом:
|   Состояние | Описание |
| ------------- | ------------- |
| AfterStart | Чат сразу после старта перед приветственным сообщением |
| AfterWelcomeMessage | Чат после приветственного сообщения |
| PromptedForPizzaType | Чат после отображения предложения пользователю написать тип пиццы, который он хочет заказать |
| PromptedForQuantity  | Чат после отображения предложения пользователю написать количества заказываемой пиццы |
| PromptedForDeliveryType  | Чат после отображения пользователя клавиатуры с выбором одного из двух способов доставки |
| DeliveryByCouurierMessagePosted | Чат после отображения клиенту сообщения о времени получении пицц |
| HimselfDeliveryPosted | Чат после отображения клиенту сообщения о времени получении пицц |
### Создание пользовательского события<a name="example-user-event-creation"></a>
## Получение помощи<a name="help"></a>
Рекомендуемый способ получения помощи- создание вопроса в данном репозитарии.
Можете также обратиться по эл. адресу maliuzhenetsdzmitry @ гугляком ()
## Помощь в разработке<a name="contributing"></a>
## Лицензия<a name="license"></a>
MIT License      Copyright (c) 2020 Dzmitry Maliuzhenets