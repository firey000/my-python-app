-- phpMyAdmin SQL Dump
-- version 5.2.2deb1
-- https://www.phpmyadmin.net/
--
-- Хост: localhost:3306
-- Время создания: Ноя 19 2025 г., 17:24
-- Версия сервера: 11.8.3-MariaDB-0+deb13u1 from Debian
-- Версия PHP: 8.4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `phpmyadmin`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Employees`
--

CREATE TABLE `Employees` (
  `id` int(11) NOT NULL,
  `Fcs` varchar(30) NOT NULL COMMENT 'ФИО',
  `Post` varchar(20) NOT NULL COMMENT 'Должность',
  `Timezone` varchar(6) DEFAULT 'UTC+3' COMMENT 'Часовой пояс',
  `email` varchar(20) DEFAULT NULL COMMENT 'E-mail'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Employees`
--

INSERT INTO `Employees` (`id`, `Fcs`, `Post`, `Timezone`, `email`) VALUES
(1, 'Михайлов Данил Иванович', 'Директор', 'UTC+3', NULL),
(2, 'Морохин Артур Николаевич', 'Начальник директора', 'UTC+3', NULL),
(3, 'Гончарук Кирилл Вадимович', 'Старший программист', 'UTC+3', NULL),
(4, 'Иван Иванов Иванович', 'Тестировщик', 'UTC+1', NULL),
(5, 'Петр Петров Петрович', 'Фронтед разработчик', 'UTC+5', NULL),
(6, 'Елена Сергеевна Игоревна', 'Ведущий разработчик', 'UTC-1', NULL),
(7, 'Михаил Иванов Дмитриевич', 'Инженер-тестировщик', 'UTC+11', NULL),
(8, 'Иван Кузнецов Викторович', 'Менеджер по продукту', 'UTC+4', NULL),
(9, 'Олег  Петров  Александрович', 'Менеджер продукта', 'UTC-1', NULL),
(10, 'Анна  Морозова  Викторовна', 'Тех. поддержка', 'UTC-4', NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `Employee_Tasks`
--

CREATE TABLE `Employee_Tasks` (
  `employee_id` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  `project_id` int(11) DEFAULT NULL COMMENT 'Если задача привязана к конкретному проекту',
  `status_id` int(11) NOT NULL DEFAULT 1 COMMENT 'Текущий статус этой задачи у этого сотрудника'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `Productivity_Report`
--

CREATE TABLE `Productivity_Report` (
  `id` int(11) NOT NULL,
  `employee_id` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  `status` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Productivity_Report`
--

INSERT INTO `Productivity_Report` (`id`, `employee_id`, `task_id`, `status`) VALUES
(1, 1, 4, 2),
(2, 1, 3, 2),
(3, 2, 5, 4),
(4, 2, 6, 4),
(5, 3, 7, 4),
(6, 3, 8, 2);

-- --------------------------------------------------------

--
-- Структура таблицы `Project`
--

CREATE TABLE `Project` (
  `id` int(11) NOT NULL,
  `Name` varchar(60) NOT NULL COMMENT 'Название проекта',
  `Purpose` text NOT NULL COMMENT 'Цель проекта',
  `Deadline` date NOT NULL COMMENT 'Дедлайн'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Project`
--

INSERT INTO `Project` (`id`, `Name`, `Purpose`, `Deadline`) VALUES
(3, '«Умный дневник тренировок»', 'Программный помощник для любителей спорта и фитнеса, который ведет учет физических нагрузок, прогресса тренировок, рекомендаций по тренировочным планам и мотивации. Предоставляет полезную аналитику и советы по улучшению физической формы.', '2026-02-12'),
(4, '«Монитор цен»', 'Веб-сервис для отслеживания стоимости товаров в онлайн-магазинах. Позволяет подписываться на товары и получать уведомления о снижении цен. Пользователям предоставляется возможность сравнивать цену продукта в разных магазинах и находить лучшие предложения.\r\n\r\n', '2026-01-30'),
(5, '«Планировщик путешествий»', 'Удобный сайт или мобильное приложение для планирования поездок и туров. Помогает подобрать маршруты, достопримечательности, отели и транспорт. Предусматривает удобную навигацию, бронирование билетов и формирование маршрутов с минимальным временем ожидания и затратами.', '2026-04-01'),
(6, 'Оптимизация инфраструктуры	', 'Повышение производительности и отказоустойчивости серверов	', '2025-12-31'),
(7, 'Модификация API	', 'Расширение функционала API для интеграции с новыми системами	', '2026-06-15'),
(8, 'Автоматическое тестирование	', 'Внедрение автоматизированных тестов для повышения качества выпускаемого ПО	', '2026-03-20'),
(9, 'Поддержка пользователей	', 'Организация круглосуточной службы поддержки клиентов	', '2025-11-10'),
(10, 'Анализ рынка	', 'Исследование потребностей пользователей и разработка стратегии развития продукта	', '2026-04-30');

-- --------------------------------------------------------

--
-- Структура таблицы `Project_Employees`
--

CREATE TABLE `Project_Employees` (
  `project_id` int(11) NOT NULL,
  `employee_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `Tasks`
--

CREATE TABLE `Tasks` (
  `id` int(11) NOT NULL,
  `purpose` text NOT NULL COMMENT 'Цель задачи'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Tasks`
--

INSERT INTO `Tasks` (`id`, `purpose`) VALUES
(3, 'Генерация персонализированных писем'),
(4, 'Анализ посещаемости сайта компании'),
(5, 'Автоматизация выдачи справок сотрудникам'),
(6, 'Автоматизация рассылки поздравительных открыток'),
(7, 'Генератор еженедельных отчетов'),
(8, 'Автоматизированная инвентаризация оборудования');

-- --------------------------------------------------------

--
-- Структура таблицы `Task_status`
--

CREATE TABLE `Task_status` (
  `id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL COMMENT 'Название статуса'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Task_status`
--

INSERT INTO `Task_status` (`id`, `name`) VALUES
(1, 'В работе'),
(2, 'Готова'),
(3, 'На проверке'),
(4, 'Отменена');

-- --------------------------------------------------------

--
-- Структура таблицы `Working_Hours`
--

CREATE TABLE `Working_Hours` (
  `id` int(11) NOT NULL,
  `employee_id` int(11) NOT NULL,
  `time_start` time NOT NULL COMMENT 'Приход на работу',
  `time_end` time DEFAULT NULL COMMENT 'Уход с работы'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `Working_Hours`
--

INSERT INTO `Working_Hours` (`id`, `employee_id`, `time_start`, `time_end`) VALUES
(2, 2, '07:20:00', '17:00:00'),
(3, 1, '10:00:00', '15:00:00'),
(4, 3, '08:00:00', '16:25:00');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Employees`
--
ALTER TABLE `Employees`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Индексы таблицы `Employee_Tasks`
--
ALTER TABLE `Employee_Tasks`
  ADD PRIMARY KEY (`employee_id`,`task_id`),
  ADD KEY `task_id` (`task_id`),
  ADD KEY `project_id` (`project_id`),
  ADD KEY `status_id` (`status_id`);

--
-- Индексы таблицы `Productivity_Report`
--
ALTER TABLE `Productivity_Report`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_emp_task` (`employee_id`,`task_id`),
  ADD KEY `task_id` (`task_id`),
  ADD KEY `status` (`status`);

--
-- Индексы таблицы `Project`
--
ALTER TABLE `Project`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `Project_Employees`
--
ALTER TABLE `Project_Employees`
  ADD PRIMARY KEY (`project_id`,`employee_id`),
  ADD KEY `employee_id` (`employee_id`);

--
-- Индексы таблицы `Tasks`
--
ALTER TABLE `Tasks`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `Task_status`
--
ALTER TABLE `Task_status`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `Working_Hours`
--
ALTER TABLE `Working_Hours`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Employees`
--
ALTER TABLE `Employees`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `Productivity_Report`
--
ALTER TABLE `Productivity_Report`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `Project`
--
ALTER TABLE `Project`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `Tasks`
--
ALTER TABLE `Tasks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `Task_status`
--
ALTER TABLE `Task_status`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `Working_Hours`
--
ALTER TABLE `Working_Hours`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `Employee_Tasks`
--
ALTER TABLE `Employee_Tasks`
  ADD CONSTRAINT `Employee_Tasks_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `Employees` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `Employee_Tasks_ibfk_2` FOREIGN KEY (`task_id`) REFERENCES `Tasks` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `Employee_Tasks_ibfk_3` FOREIGN KEY (`project_id`) REFERENCES `Project` (`id`) ON DELETE SET NULL;

--
-- Ограничения внешнего ключа таблицы `Productivity_Report`
--
ALTER TABLE `Productivity_Report`
  ADD CONSTRAINT `Productivity_Report_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `Employees` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `Productivity_Report_ibfk_2` FOREIGN KEY (`task_id`) REFERENCES `Tasks` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `Productivity_Report_ibfk_3` FOREIGN KEY (`status`) REFERENCES `Task_status` (`id`);

--
-- Ограничения внешнего ключа таблицы `Project_Employees`
--
ALTER TABLE `Project_Employees`
  ADD CONSTRAINT `Project_Employees_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `Project` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `Project_Employees_ibfk_2` FOREIGN KEY (`employee_id`) REFERENCES `Employees` (`id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `Working_Hours`
--
ALTER TABLE `Working_Hours`
  ADD CONSTRAINT `Working_Hours_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `Employees` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
